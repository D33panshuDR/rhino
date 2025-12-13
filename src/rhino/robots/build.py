from functools import partial

from rhino.robots.configs import HOUND as HOUND
from rhino.robots.configs import RHINO as RHINO
from rhino.robots.robot import Robot as Robot
from rhino.utils._typing import RobotConfig as RobotConfig


def _init_robot(
    config: RobotConfig, connection_str: str, log_dir: str = "logs"
) -> Robot:
    return Robot(connection_string=connection_str, config=config, log_dir=log_dir)


init_hound = partial(_init_robot, config=HOUND)
"""Initializes the Hound robot"""

init_rhino = partial(_init_robot, config=RHINO)
"""Initializes the Rhino robot"""
