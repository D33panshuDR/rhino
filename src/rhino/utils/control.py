import time

from pymavlink import mavutil


class Controller:
    def __init__(self, connection_string: str):
        """

        Args:
            connection_string (str): The pymavlink connection string.

        Raises:
            IOError: If the connection cannot be established.
        """
        try:
            self.master = mavutil.mavlink_connection(connection_string, baud=115200)
        except Exception as e:
            raise IOError(f"Failed to connect to vehicle on {connection_string}: {e}")

    def wait_for_heartbeat(self):
        """
        Waits for the first heartbeat message to confirm a good connection.

        Raises:
            IOError: If no heartbeat is received after a timeout.
        """
        print("Waiting for vehicle heartbeat...")
        try:
            self.master.wait_heartbeat()  # type: ignore
        except Exception as e:
            raise IOError(
                f"No heartbeat received from vehicle. Check connection. Details: {e}"
            )

    def _map_throttle(self, throttle: float, min_pwm: int, max_pwm: int) -> int:
        """
        Maps a normalized throttle from [0, 1] to a PWM signal range.

        Args:
            throttle (float): Normalized throttle value [0, 1].
            min_pwm (int): The minimum possible PWM value (e.g., 1000).
            max_pwm (int): The maximum possible PWM value (e.g., 2000).

        Returns:
            int: The calculated PWM value.
        """
        throttle = max(0.0, min(1.0, throttle))  # Clamp input
        return int(min_pwm + (max_pwm - min_pwm) * throttle)

    def _map_steering(self, steering: float, min_pwm: int, max_pwm: int) -> int:
        """
        Maps a normalized steering from [-1, 1] to a PWM signal range.

        Args:
            steering (float): Normalized steering value [-1, 1].
            min_pwm (int): The minimum possible PWM value (e.g., 1000).
            max_pwm (int): The maximum possible PWM value (e.g., 2000).

        Returns:
            int: The calculated PWM value.
        """
        steering = max(-1.0, min(1.0, steering))  # Clamp input
        neutral_pwm = (min_pwm + max_pwm) / 2
        pwm_range = (max_pwm - min_pwm) / 2
        return int(neutral_pwm + pwm_range * steering)

    def send_rc_override(
        self,
        throttle_pwm: int,
        steering_pwm: int,
        throttle_channel: int,
        steering_channel: int,
    ):
        """
        Sends an RC_CHANNELS_OVERRIDE message.

        Overrides only the specified channels, leaving others untouched (set to 0).
        ArduPilot interprets a PWM value of 0 as "no change".

        Args:
            throttle_pwm (int): The PWM value for the throttle.
            steering_pwm (int): The PWM value for the steering.
            throttle_channel (int): The channel number for throttle (1-8).
            steering_channel (int): The channel number for steering (1-8).
        """
        rc_channels = [65535] * 8  # Initialize all 8 channels to 0 (no change)
        rc_channels[throttle_channel - 1] = throttle_pwm
        rc_channels[steering_channel - 1] = steering_pwm

        self.master.mav.rc_channels_override_send(  # type: ignore
            self.master.target_system,  # type: ignore
            self.master.target_component,  # type: ignore
            *rc_channels,
        )

    def get_servo_outputs(self, timeout: int = 2):
        """
        Requests and retrieves the SERVO_OUTPUT_RAW message.

        Args:
            timeout (int): Time to wait for the message in seconds.

        Returns:
            The SERVO_OUTPUT_RAW message object, or None if not received.
        """
        self.master.mav.srcSystem = 255  # type: ignore
        # Request the message stream
        self.master.mav.request_data_stream_send(  # type: ignore
            self.master.target_system,  # type: ignore
            self.master.target_component,  # type: ignore
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            10,  # Request at 10 Hz
            1,  # Start streaming
        )

        start_time = time.time()
        while time.time() - start_time < timeout:
            msg = self.master.recv_match(type="SERVO_OUTPUT_RAW", blocking=False)
            if msg:
                # Stop the stream once we have the message to avoid flooding
                self.master.mav.request_data_stream_send(  # type: ignore
                    self.master.target_system,  # type: ignore
                    self.master.target_component,  # type: ignore
                    mavutil.mavlink.MAV_DATA_STREAM_ALL,
                    0,  # Rate 0 Hz
                    0,  # Stop streaming
                )
                return msg
        return None

    def release_rc_override(self, throttle_channel: int, steering_channel: int):
        """
        Releases control by sending a command to reset the overrides.
        Sending a value of 0 for a channel tells ArduPilot to stop overriding it.
        """
        rc_channels = [0] * 8
        rc_channels[throttle_channel - 1] = 0
        rc_channels[steering_channel - 1] = 0
        self.master.mav.rc_channels_override_send(  # type: ignore
            self.master.target_system,  # type: ignore
            self.master.target_component,  # type: ignore
            *rc_channels,
        )

    # type: ignore
    def close(self):
        """Closes the MAVLink connection."""
        if self.master:
            self.master.close()  # type: ignore
