import grpc
import time
import random
from concurrent import futures
import threading

import phone_pb2
import phone_pb2_grpc


class TelemetryService(phone_pb2_grpc.TelemetryServiceServicer):
    def __init__(self):
        # Начальные координаты трекера
        self.current_latitude = 10.000
        self.current_longitude = -10.000
        self.lock = threading.Lock()

    def SetTelemetryStream(self, request_iterator, context):
        """
        Обрабатывает поток данных Telemetry и отправляет команды в ответ.
        """
        for telemetry_data in request_iterator:
            # Получаем данные телеметрии
            user_id = telemetry_data.user_id
            location = telemetry_data.location

            print(f"Received telemetry from {user_id}: "
                  f"Latitude: {location.latitude}, Longitude: {location.longitude}")

            # В зависимости от полученных данных, отправляем команды
            if random.random() < 0.5:
                # Пример отправки команды GetOne
                yield phone_pb2.TelemetryStreamCommand(
                    get_one=phone_pb2.TelemetryStreamCommand.GetOne()
                )
            else:
                # Пример отправки команды Start с произвольной продолжительностью
                yield phone_pb2.TelemetryStreamCommand(
                    start=phone_pb2.TelemetryStreamCommand.Start(duration=random.uniform(5, 10))
                )

            # Имитация задержки для демонстрации двусторонней потоковой связи
            time.sleep(1)


def serve():
    # Настройка gRPC-сервера
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    phone_pb2_grpc.add_TelemetryServiceServicer_to_server(TelemetryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
