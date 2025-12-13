import sys
import time

from rhino.utils.control import Controller
from rhino.utils.log import Logger
from rhino.utils._typing import RobotConfig


class Robot:
    def __init__(
        self,
        connection_string: str,
        config: RobotConfig,
        log_dir: str = "logs",
    ):
        """
        Initializes the robot controller.

        Args:
            connection_string (str): The MAVLink connection string.
                                     (e.g., 'udp:127.0.0.1:14550' for SITL).
            log_dir (str): Directory to store log files.
            file_name_prefix (str): Prefix for the log file name.
            throttle_channel (int): The RC channel for throttle (default is 3).
            steering_channel (int): The RC channel for steering (default is 1).
        """
        print(f"INFO: Connecting to vehicle on: {connection_string}")
        self.controller = Controller(connection_string)

        # Configuration
        self._config = config

        # Define channel mapping
        self.THROTTLE_CHANNEL = config.throttle.channel
        self.STEERING_CHANNEL = config.steering.channel

        print("INFO: Initializing logger...")
        self.logger = Logger(log_dir, f"{config.name}_log")
        # Write header to the log file
        header = [
            "timestamp",
            "throttle_cmd",
            "steering_cmd",
            "servo1_raw",
            "servo2_raw",
            "servo3_raw",
            "servo4_raw",
            "servo5_raw",
            "servo6_raw",
            "servo7_raw",
            "servo8_raw",
        ]
        self.logger.log(header, is_header=True)
        print(f"INFO: Logging to: {self.logger.log_file_path}")

        print("INFO: Waiting for heartbeat...")
        self.controller.wait_for_heartbeat()
        print("INFO: Heartbeat received. Rhino controller is ready.")

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def config(self) -> RobotConfig:
        return self._config

    def apply_brake(self) -> None:
        if self.config.brake is not None:
            # TODO Implement braking mechanism @D33panshuDR
            pass
        else:
            # NOTE Verbosity intentional
            self.send_velocity_cmd(throttle=0.0, steering=0.0)

    def send_velocity_cmd(self, throttle: float = 0.0, steering: float = 0.0):
        """
        Sends a velocity command to the rover and logs the data.

        Args:
            throttle (float): Throttle command, normalized from 0.0 to 1.0.
            steering (float): Steering command, normalized from -1.0 (left) to 1.0 (right).

        Returns:
            bool: True if the command was sent and logged successfully, False otherwise.
        """
        try:
            # Map normalized inputs to PWM values
            throttle_pwm = self.controller._map_throttle(
                throttle,
                min_pwm=self._config.throttle.min_pwm,
                max_pwm=self._config.throttle.max_pwm,
            )
            steering_pwm = self.controller._map_steering(
                steering,
                min_pwm=self._config.steering.min_pwm,
                max_pwm=self._config.steering.max_pwm,
            )

            # Send RC override command
            self.controller.send_rc_override(
                throttle_pwm=throttle_pwm,
                steering_pwm=steering_pwm,
                throttle_channel=self._config.throttle.channel,
                steering_channel=self._config.steering.channel,
            )
            self.logger.log(
                [
                    time.strftime("%Y-%m-%d_%H%M%S", time.localtime()),
                    throttle,
                    steering,
                    throttle_pwm,
                    steering_pwm,
                ]
            )
            # Get servo outputs for logging
            servo_outputs = self.controller.get_servo_outputs()

            if servo_outputs:
                log_data = [
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    throttle,
                    steering,
                    servo_outputs.servo1_raw,
                    servo_outputs.servo2_raw,
                    servo_outputs.servo3_raw,
                    servo_outputs.servo4_raw,
                    servo_outputs.servo5_raw,
                    servo_outputs.servo6_raw,
                    servo_outputs.servo7_raw,
                    servo_outputs.servo8_raw,
                ]
                self.logger.log(log_data)
                return True
            else:
                print("WARN: Could not retrieve servo outputs. Skipping log entry.")
                return False

        except Exception as e:
            print(f"ERROR: Failed to send velocity command: {e}", file=sys.stderr)
            return False

    def close(self):
        """
        Cleans up resources by releasing RC control and closing connections.
        This method MUST be called to ensure safe shutdown.
        """
        print("INFO: Releasing RC override control...")
        self.controller.release_rc_override(
            self._config.throttle.channel, self._config.steering.channel
        )
        print("INFO: Closing MAVLink connection...")
        self.controller.close()
        print("INFO: Closing logger...")
        self.logger.close()
        print("INFO: Rhino controller shut down successfully.")
