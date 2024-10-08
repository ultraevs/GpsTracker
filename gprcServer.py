import random
import threading
import time
from concurrent import futures

import grpc

import phone_pb2
import phone_pb2_grpc


# Movement algorithms: Linear and random
def linear_movement(lat, lon):
    # Simulates linear movement by increasing both latitude and longitude slightly
    return lat + 0.0001, lon + 0.0001


def random_movement(lat, lon):
    # Simulates random movement by adding a small random value to latitude and longitude
    return lat + random.uniform(-0.0001, 0.0001), lon + random.uniform(-0.0001, 0.0001)


class TrackerService(phone_pb2_grpc.TrackerServiceServicer):
    # gRPC service for simulating GPS tracker behavior
    def __init__(self):
        # Initializes the tracker with default values and state
        self.current_latitude = 10.000
        self.current_longitude = -10.000
        self.current_algorithm = "linear"
        self.simulating = False
        self.lock = threading.Lock()

    def get_one(self, request, context):
        # Returns the current coordinates
        with self.lock:
            return phone_pb2.TelemetryData(
                latitude=self.current_latitude,
                longitude=self.current_longitude,
                timestamp=int(time.time())
            )

    def start_simulation(self, duration):
        # Starts the simulation for a given duration
        start_time = time.time()
        self.simulating = True
        step = 0

        while time.time() - start_time < duration:
            with self.lock:
                if self.current_algorithm == "linear":
                    self.current_latitude, self.current_longitude = linear_movement(self.current_latitude,
                                                                                    self.current_longitude)
                elif self.current_algorithm == "random":
                    self.current_latitude, self.current_longitude = random_movement(self.current_latitude,
                                                                                    self.current_longitude)
                else:
                    print(f"Invalid algorithm: {self.current_algorithm}")
                    self.simulating = False
                    return

            print(f"Sending: Latitude: {self.current_latitude}, Longitude: {self.current_longitude}, Algorithm: {self.current_algorithm}")
            time.sleep(1)
            step += 1

        self.simulating = False
        print("Simulation completed.")

    def start(self, request, context):
        # Starts the movement simulation in a separate thread
        duration = request.duration
        if not self.simulating:
            sim_thread = threading.Thread(target=self.start_simulation, args=(duration,))
            sim_thread.start()
            return phone_pb2.TelemetryResponse(message="Simulation started")
        else:
            return phone_pb2.TelemetryResponse(message="Simulation already running")

    def switch_algorithm(self, request, context):
        # Switches the movement algorithm (linear/random)
        new_algorithm = request.algorithm
        with self.lock:
            if new_algorithm in ["linear", "random"]:
                self.current_algorithm = new_algorithm
                print(f"Algorithm switched to {new_algorithm}")
                return phone_pb2.TelemetryResponse(message=f"Algorithm switched to {new_algorithm}")
            else:
                return phone_pb2.TelemetryResponse(message="Invalid algorithm")

    def SetTelemetryStream(self, request_iterator, context):
        # Handles incoming telemetry data stream from the client
        for telemetry_data in request_iterator:
            print(f"Received: Latitude: {telemetry_data.latitude}, Longitude: {telemetry_data.longitude}, Timestamp: {telemetry_data.timestamp}")
        return phone_pb2.TelemetryResponse(message="Telemetry data received")


def serve():
    # Starts the gRPC server on port 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    phone_pb2_grpc.add_TrackerServiceServicer_to_server(TrackerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
