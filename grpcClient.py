import random
import threading
import time

import grpc

import phone_pb2
import phone_pb2_grpc

# Variables for current coordinates and algorithm
current_latitude = 10.000
current_longitude = -10.000
current_algorithm = "linear"


# Functions for movement algorithms
def linear_movement(lat, lon):
    return lat + 0.0001, lon + 0.0001


def random_movement(lat, lon):
    return lat + random.uniform(-0.0001, 0.0001), lon + random.uniform(-0.0001, 0.0001)


# Function to read the configuration file
def read_config():
    global current_algorithm
    try:
        with open("config.txt", "r") as file:
            for line in file:
                if line.startswith("mode="):
                    mode = line.split("=")[1].strip()
                    if mode in ["linear", "random"]:
                        current_algorithm = mode
    except FileNotFoundError:
        print("Config file not found, using default mode.")


# Function that periodically checks the configuration file
def start_config_watcher():
    while True:
        read_config()
        time.sleep(5)  # Check the configuration every 5 seconds


# Main function for movement simulation
def start_simulation(duration):
    start_time = time.time()
    global current_latitude, current_longitude
    while time.time() - start_time < duration:
        # Select the algorithm based on the current mode
        if current_algorithm == "linear":
            current_latitude, current_longitude = linear_movement(current_latitude, current_longitude)
        elif current_algorithm == "random":
            current_latitude, current_longitude = random_movement(current_latitude, current_longitude)

        print(
            f"Current coordinates: Latitude: {current_latitude}, Longitude: {current_longitude}, Algorithm: {current_algorithm}")
        time.sleep(1)


# Generator for telemetry data to send to the server
def telemetry_stream_generator():
    """
    Generator for telemetry data to send to the server.
    """
    user_id = "user123"
    while True:
        # Example data with the current time and current coordinates
        timestamp = phone_pb2.Timestamp(seconds=int(time.time()), nanos=0)
        location = phone_pb2.Telemetry.Location(
            timestamp=timestamp,
            latitude=current_latitude,
            longitude=current_longitude
        )
        yield phone_pb2.Telemetry(user_id=user_id, location=location)

        # Simulate sending every 2 seconds
        time.sleep(2)


# Main function to run the client
def run():
    # Start a thread to monitor configuration changes
    config_thread = threading.Thread(target=start_config_watcher)
    config_thread.daemon = True
    config_thread.start()

    # Establish a connection to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = phone_pb2_grpc.TelemetryServiceStub(channel)

        # Create a bidirectional stream
        responses = stub.SetTelemetryStream(telemetry_stream_generator())

        # Handle commands from the server
        for command in responses:
            if command.HasField('get_one'):
                print("Received command: GetOne")
            elif command.HasField('start'):
                duration = command.start.duration
                print(f"Received command: Start with duration {duration}")
                # Start the movement simulation for the specified duration
                start_simulation(duration)
            elif command.HasField('ack'):
                print("Received command: Ack")
            else:
                print("Unknown command received")


if __name__ == '__main__':
    run()
