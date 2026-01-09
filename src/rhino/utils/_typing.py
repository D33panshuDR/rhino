from dataclasses import dataclass
from typing import TypedDict


class RobotFeedback(TypedDict):
    """
    Feedback from the robot on receiving velocity commands
    """

    success: bool
    """Whether the command was successfully executed"""

    throttle_pwm: int | None
    """PWM sent to the throttle channel"""

    steering_pwm: int | None
    """PWM sent to the steering channel"""


@dataclass
class RCInputConfig:
    """
    Configuration for an RC Input.
    """

    channel: int
    """The channel this input is bound to"""
    min_pwm: int
    """The minimum PWM value of the RC input"""
    max_pwm: int
    """The maximum PWM value of the RC input"""


@dataclass
class RobotConfig:
    """
    Configuration for a vehicle with RC Inputs.
    """

    name: str
    """The name for the robot"""

    throttle: RCInputConfig
    """The configuration for the throttle RC input"""

    steering: RCInputConfig
    """The configuration for the steering RC input"""

    brake: RCInputConfig | None = None
    """The configuration for the braking RC input"""
