import grpc
import time
import threading
import random
import phone_pb2
import phone_pb2_grpc


def telemetry_stream_generator():
    """
    Генератор данных телеметрии для отправки на сервер.
    """
    user_id = "user123"
    while True:
        # Пример данных с текущим временем и случайными координатами
        timestamp = phone_pb2.Timestamp(seconds=int(time.time()), nanos=0)
        location = phone_pb2.Telemetry.Location(
            timestamp=timestamp,
            latitude=10.000 + random.uniform(-0.01, 0.01),
            longitude=-10.000 + random.uniform(-0.01, 0.01)
        )
        yield phone_pb2.Telemetry(user_id=user_id, location=location)

        # Имитация отправки каждые 2 секунды
        time.sleep(2)


def run():
    # Устанавливаем соединение с сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = phone_pb2_grpc.TelemetryServiceStub(channel)

        # Создаём двусторонний поток
        responses = stub.SetTelemetryStream(telemetry_stream_generator())

        # Обрабатываем команды от сервера
        for command in responses:
            if command.HasField('get_one'):
                print("Received command: GetOne")
            elif command.HasField('start'):
                print(f"Received command: Start with duration {command.start.duration}")
            elif command.HasField('ack'):
                print("Received command: Ack")
            else:
                print("Unknown command received")


if __name__ == '__main__':
    run()
