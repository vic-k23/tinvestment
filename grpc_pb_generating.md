Генерация файлов-классов python для поддержки gRPC
==================================================

1. Качаем файлы .proto с репозитория Тинькофф: [https://github.com/Tinkoff/investAPI/tree/main/src/docs/contracts](https://github.com/Tinkoff/investAPI/tree/main/src/docs/contracts)
2. Качаем компилятор protoc с репы Google: [https://github.com/protocolbuffers/protobuf/releases/tag/v21.5](https://github.com/Tinkoff/investAPI/tree/main/src/docs/contracts). Файл называется **_protoc-$VERSION-$PLATFORM.zip_**
3. Оттуда же качаем Protobuf Runtime Installation архив для python, который называется, соответственно, **_protobuf-python-$VERSION.zip_**
4. Распаковываем компилятор (обе папки) в папку на диске, в пути которой желательно исключить пробелы, а ещё лучше на буржуйском.
5. Прописываем путь в папку _bin_ в переменную PATH. Перезагружаемся (или перезаходим, если в окружение пользователя прописали) и проверяем, что компилятор доступен, введя **_protoc --version_** в командной строке.
6. Распаковываем среду выполнения и заходим внутри в папку _python_, в которой открываем командную консоль.
7. Строим и устанавливаем среду выполнения Protobuf для python, для чего выполняем последовательно команды:
    * **python .\setup.py build**
    * **python .\setup.py test** (тут у меня ругнулось на отсутствие описания таймзоны для Японии, не понятно, нафиг оно мне, но я забил)
    * **python setup.py install**

8. Компилируем классы командой: **protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/*.proto**
9. Готово!

### НО! Это всё фигня! Надо вот так:

1. Создаём и активируем виртуальную среду.
2. Ставим пакеты **_pip install grpcio_** и **_pip install grpcio-tools_**
3. Запускаем команду: **_python -m grpc_tools.protoc -I../../contracts --python_out=./tinvestment/grpc_pb2 --grpc_python_out=./tinvestment/grpc_pb2 ../../contracts/*.proto_**
