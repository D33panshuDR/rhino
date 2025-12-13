from rhino import init_rhino
from time import sleep


def main():
    rhino = init_rhino(connection_str="<rhino-connnection-str>")
    print(f"Initialized robot: {rhino.name}")  # DEBUG

    print("Starting rhino maneuver...")

    # Move forward for 3 sec
    print("FORWARD\t\t\t[3s]")
    rhino.send_velocity_cmd(throttle=0.5, steering=0.0)
    sleep(3.0)

    # Stop for 1 sec
    print("STOP\t\t\t[1s]")
    rhino.apply_brake()
    sleep(1.0)

    # Turn left for 2 sec
    print("TURN(LEFT)\t\t\t[1s]")
    rhino.send_velocity_cmd(steering=-1.0)
    sleep(2.0)

    print("rhino maneuver complete")
    rhino.close()


if __name__ == "__main__":
    main()
