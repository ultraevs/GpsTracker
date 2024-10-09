import unittest
from unittest.mock import MagicMock

import phone_pb2
from grpcServer import TelemetryService


class TestTelemetryService(unittest.TestCase):
    def test_set_telemetry_stream(self):

        # Create the service and mock context
        service = TelemetryService()
        context = MagicMock()

        # Create a stream of telemetry data
        telemetry_data = phone_pb2.Telemetry(
            user_id="test_user",
            location=phone_pb2.Telemetry.Location(
                timestamp=phone_pb2.Timestamp(seconds=123456789, nanos=0),
                latitude=10.0,
                longitude=20.0
            )
        )

        # Test the SetTelemetryStream method
        response_iterator = service.SetTelemetryStream(iter([telemetry_data]), context)
        responses = list(response_iterator)

        # Check that commands were sent
        self.assertTrue(any(isinstance(response, phone_pb2.TelemetryStreamCommand) for response in responses))


if __name__ == '__main__':
    unittest.main()
