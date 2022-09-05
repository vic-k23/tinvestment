import decimal

from requests import get
from re import match
from xml.etree.ElementTree import fromstring
from pprint import pprint


def get_currencies() -> list:
    """
    Создаёт список словарей с описанием валют
    :return: список словарей, описывающих валюту
    """

    currencies = []
    currencies_xml = fromstring(get('http://www.cbr.ru/scripts/XML_valFull.asp').text)

    if currencies_xml:
        for currency in currencies_xml:
            currencies.append({
                "name": currency.find('Name').text,
                "eng_name": currency.find('EngName').text,
                "nominal": int(currency.find('Nominal').text),
                "code": currency.find('ISO_Char_Code').text
            })

    return currencies


def get_currency_names() -> list:
    """
    Создаёт список названий валют согласно ISO стандарту
    :return: список названий валют
    """
    currencies = []
    currencies_xml = fromstring(get('http://www.cbr.ru/scripts/XML_valFull.asp').text)
    if currencies_xml:
        for currency in currencies_xml:
            currencies.append(currency.find('ISO_Char_Code').text)

    return currencies


def get_exchange_currency(currency_code: str, exchange_date: str) -> dict:
    """
    Создаёт словарь вида {name, nominal, cost}, отражающий курс валюты на указанную дату
    :param currency_code: трёхсимвольный код из словаря, возвращаемого в списке функцией get_currencies
    :param exchange_date: дата, на которую нужно узнать курс валюты по отношению к рублю в формате dd/mm/yyyy
    :return: dict{name, nominal, cost}
    """

    exchange_currency = {}

    if match(r'\d\d/\d\d/\d\d\d\d', exchange_date):
        exchange_currencies_xml = fromstring(get(f'https://cbr.ru/scripts/XML_daily.asp?date_req={exchange_date}').text)
        for currency in exchange_currencies_xml:
            if currency.find('CharCode').text == currency_code.upper():
                exchange_currency['name'] = currency.find('Name').text
                exchange_currency['nominal'] = int(currency.find('Nominal').text)
                exchange_currency['cost_decimal'] = decimal.Decimal(currency.find('Value').text.replace(',', '.'))
                exchange_currency['cost_str'] = f"\u20BD {currency.find('Value').text}"
                break

    else:
        print("Неверный формат даты! Должен быть dd/mm/yyyy")

    return exchange_currency


if __name__ == '__main__':
    pprint(get_currencies())
    print(20*'=')
    print()
    pprint(get_exchange_currency('USD', '19/11/2021'))
