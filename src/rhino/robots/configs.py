from typing import Final
from rhino.utils._typing import RCInputConfig, RobotConfig


RHINO: Final[RobotConfig] = RobotConfig(
    name="rhino",
    throttle=RCInputConfig(
        channel=3,
        min_pwm=1100,
        max_pwm=1900,
    ),
    steering=RCInputConfig(
        channel=1,
        min_pwm=1100,
        max_pwm=1900,
    ),
)


HOUND: Final[RobotConfig] = RobotConfig(
    name="hound",
    throttle=RCInputConfig(
        channel=3,
        min_pwm=1500,
        max_pwm=1900,
    ),
    steering=RCInputConfig(
        channel=1,
        min_pwm=1100,
        max_pwm=1900,
    ),
)
