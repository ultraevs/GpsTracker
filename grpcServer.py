import grpc
import time
import random
from concurrent import futures
import threading

import phone_pb2
import phone_pb2_grpc


class TelemetryService(phone_pb2_grpc.TelemetryServiceServicer):
    def __init__(self):
        # Initial tracker coordinates
        self.current_latitude = 10.000
        self.current_longitude = -10.000
        self.lock = threading.Lock()

    def SetTelemetryStream(self, request_iterator, context):
        for telemetry_data in request_iterator:
            # Receive telemetry data
            user_id = telemetry_data.user_id
            location = telemetry_data.location

            print(f"Received telemetry from {user_id}: "
                  f"Latitude: {location.latitude}, Longitude: {location.longitude}")

            # Depending on the received data, send commands
            if random.random() < 0.5:
                # Example of sending the GetOne command
                yield phone_pb2.TelemetryStreamCommand(
                    get_one=phone_pb2.TelemetryStreamCommand.GetOne()
                )
            else:
                # Example of sending the Start command with a random duration
                yield phone_pb2.TelemetryStreamCommand(
                    start=phone_pb2.TelemetryStreamCommand.Start(duration=random.uniform(5, 10))
                )

            # Simulate a delay to demonstrate bidirectional streaming
            time.sleep(1)


def serve():
    # Setup gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    phone_pb2_grpc.add_TelemetryServiceServicer_to_server(TelemetryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
