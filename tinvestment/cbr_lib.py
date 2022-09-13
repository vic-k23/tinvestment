from decimal import Decimal
import aioredis
import aiohttp
from re import match
from xml.etree.ElementTree import fromstring

from exception_logger import log_exception


class CBRExchangeRate:
    """
    Класс для подключения к сайту ЦБР для получения курса валют
    """

    def __init__(self):
        self.__base_url = "http://www.cbr.ru"
        self.__exchange_script = "/scripts/XML_daily.asp"
        self.__currencies_descriptions = "/scripts/XML_valFull.asp"
        self.__redis_url = "redis://localhost"

        self.__session = aiohttp.ClientSession(self.__base_url)
        self.__redis = aioredis.from_url("redis://localhost", username="bot", password="CzsqvJwjY3U5!9SD")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.close()
        return True

    async def __fetch_currencies(self, **kwargs) -> str:
        """
        Отправляет запрос на сайт ЦБ на получение списка доступных валют
        :return: текст ответа сайта ЦБ
        :rtype: str
        """

        async with self.__session.get(self.__currencies_descriptions) as cbr_response:
            assert cbr_response.status == 200
            return await cbr_response.text()

    async def __fetch_exchange_rates(self, **kwargs) -> str:
        """
        Отправляет запрос на сайт ЦБ на получение списка доступных валют
        :return: текст ответа сайта ЦБ
        :rtype: str
        """

        async with self.__session.get(self.__exchange_script) as cbr_response:
            assert cbr_response.status == 200
            return await cbr_response.text()

    async def get_currencies(self) -> list:
        """
        Создаёт список словарей с описанием валют
        :return: список словарей, описывающих валюту
        :rtype:
        """

        currencies = []
        currencies_xml = fromstring(await self.__fetch_currencies())

        if currencies_xml:
            for currency in currencies_xml:
                currencies.append({
                    "name": currency.find('Name').text,
                    "eng_name": currency.find('EngName').text,
                    "nominal": int(currency.find('Nominal').text),
                    "code": currency.find('ISO_Char_Code').text
                    })

        return currencies

    async def get_currency_names(self) -> list:
        """
        Создаёт список названий валют согласно ISO стандарту
        :return: список названий валют
        """
        currencies = []
        currencies_xml = fromstring(await self.__fetch_currencies())
        if currencies_xml:
            for currency in currencies_xml:
                currencies.append(currency.find('ISO_Char_Code').text)

        return currencies

    async def __store_exchange_rate(self, currency: str, key_date: str, value_rate: str) -> int:
        """
        Stores given exchange rates of given currency to redis
        :param currency: the name of currency (from the list, returned by get_currencies)
        :type currency: str
        :param key_date: the exchange rate date of currency in format 'dd/mm/yyyy'
        :type key_date: str
        :param value_rate: the exchange rate value of currency for nominal in format nominal=value
        :type value_rate: str
        :return: the number of fields that were added
        :rtype: int
        """

        try:
            if match(r'\d\d/\d\d/\d\d\d\d', key_date):
                return await self.__redis.hset(name=currency, key=key_date, value=value_rate)
            else:
                log_exception("Неверный формат даты! Должен быть dd/mm/yyyy")

        except Exception as ex:
            log_exception("Не удалось сохранить курс:\n", ex)

    async def __get_exchange_rate(self, currency: str, key_date: str) -> str:
        """
        Request exchahge rates from redis
        :param currency: the currency wich rate you need
        :type currency: str
        :param key_date: the key, which is a date for exchage rate in format "dd/mm/yyyy"
        :type key_date: str
        :return: the exchange rate of currency for given date in format nominal=cost
        :rtype: str
        """

        try:
            return (await self.__redis.hget(name=currency, key=key_date)).decode()

        except Exception as ex:
            log_exception(f"Не удалось получить курс валюты на дату {key_date}:\n", ex)

    async def get_exchange_currency(self, currency_code: str, exchange_date: str) -> dict:
        """
        Создаёт словарь вида {name, nominal, cost}, отражающий курс валюты на указанную дату
        :param currency_code: трёхсимвольный код из словаря, возвращаемого в списке функцией get_currencies
        :param exchange_date: дата, на которую нужно узнать курс валюты по отношению к рублю в формате dd/mm/yyyy
        :return: dict{name, nominal, cost}
        """

        exchange_currency = {}

        try:
            if match(r'\d\d/\d\d/\d\d\d\d', exchange_date):

                exchange_rate = await self.__get_exchange_rate(currency_code, exchange_date)
                if exchange_rate:
                    nominal, cost = exchange_rate.split('=', 1)
                    exchange_currency['code'] = currency_code.upper()
                    exchange_currency['nominal'] = int(nominal)
                    exchange_currency['cost_decimal'] = Decimal(cost.replace(',', '.'))
                    exchange_currency['cost_str'] = f"\u20BD {cost}"

                else:
                    exchange_currencies_xml = fromstring(await self.__fetch_exchange_rates(date_req=exchange_date))
                    for currency in exchange_currencies_xml:
                        if currency.find('CharCode').text == currency_code.upper():
                            exchange_currency['code'] = currency.find('CharCode').text
                            exchange_currency['nominal'] = int(currency.find('Nominal').text)
                            exchange_currency['cost_decimal'] = Decimal(currency.find('Value').text.replace(',', '.'))
                            exchange_currency['cost_str'] = f"\u20BD {currency.find('Value').text}"

                            # Save the exchange rate to redis
                            await self.__store_exchange_rate(
                                    currency_code.upper(),
                                    exchange_date,
                                    f"{exchange_currency['nominal']}={currency.find('Value').text}")
                            break

            else:
                log_exception("Неверный формат даты! Должен быть dd/mm/yyyy")

            return exchange_currency

        except Exception as ex:
            log_exception(f"Не удалось получить курс валюты {currency_code}:", ex)


if __name__ == '__main__':
    from pprint import pprint
    from asyncio import run


    async def try_lib():
        try:
            async with CBRExchangeRate() as cbr:
                pprint(await cbr.get_currencies())
                print(20 * '=')
                print()
                pprint(await cbr.get_exchange_currency('USD', '19/11/2021'))
        except Exception as ex:
            log_exception("", ex)


    run(try_lib())
