# Эмулятор GPS-трекера (gRPC)

Этот проект реализует эмулятор GPS-трекера, который подключается к серверу через gRPC и передаёт симулированные данные телеметрии (широта и долгота). Сервис поддерживает несколько команд и позволяет в реальном времени переключать алгоритмы движения.

## Возможности

- **`get_one`**: Возвращает текущие координаты трекера.
- **`start`**: Запускает симуляцию движения на заданное время с выбранным алгоритмом.
- **Переключение алгоритмов в реальном времени**: Вы можете переключаться между различными алгоритмами движения (`linear` или `random`) во время работы симуляции.

## Алгоритмы движения

1. **Линейное движение**: Трекер движется по прямой линии, увеличивая широту и долготу на небольшое фиксированное значение.
2. **Случайное движение**: Трекер движется в случайном направлении, слегка изменяя широту и долготу на случайную величину.

## Требования

Убедитесь, что у вас установлены:
- Python 3.x
- Библиотеки `grpcio` и `grpcio-tools`

Вы можете установить необходимые библиотеки с помощью команды:

```bash
pip install -r requirements.txt
```

## Как запустить
### Шаг 1: Генерация gRPC-файлов
После создания файла phone.proto, сгенерируйте необходимые Python-классы для работы с gRPC:
```bash
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. phone.proto
 ```

### Шаг 2: Запуск сервера
Запустите сервер, который будет обрабатывать gRPC-запросы:
```bash
python grpcServer.py
```

### Шаг 3: Запуск клиента
Запустите клиента, чтобы взаимодействовать с сервером:
```bash
python grpcClient.py
```

