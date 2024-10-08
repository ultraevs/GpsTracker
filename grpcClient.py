import grpc
import phone_pb2
import phone_pb2_grpc


# Get the current coordinates
def run_get_one(stub):
    response = stub.get_one(phone_pb2.Empty())
    print(f"Current coordinates: Latitude: {response.latitude}, Longitude: {response.longitude}")


# Start the movement simulation
def run_start_simulation(stub, algorithm, duration):
    response = stub.start(phone_pb2.MovementRequest(algorithm=algorithm, duration=duration))
    print(response.message)


# Switch the movement algorithm
def run_switch_algorithm(stub, new_algorithm):
    response = stub.switch_algorithm(phone_pb2.AlgorithmRequest(algorithm=new_algorithm))
    print(response.message)


# Run the client with command selection
def client():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = phone_pb2_grpc.TrackerServiceStub(channel)

        while True:
            print("\nCommands:")
            print("1: Get one coordinate")
            print("2: Start simulation (enter duration and algorithm)")
            print("3: Switch algorithm")
            print("4: Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                run_get_one(stub)

            elif choice == "2":
                duration = int(input("Enter duration in seconds: "))
                algorithm = input("Enter algorithm (linear/random): ")
                run_start_simulation(stub, algorithm, duration)

            elif choice == "3":
                algorithm = input("Enter new algorithm (linear/random): ")
                run_switch_algorithm(stub, algorithm)

            elif choice == "4":
                print("Exiting...")
                break

            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    client()
