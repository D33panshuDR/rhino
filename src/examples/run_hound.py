from rhino import init_hound
from time import sleep


def main():
    hound = init_hound(connection_str="<hound-connnection-str>")
    print(f"Initialized robot: {hound.name}")  # DEBUG

    print("Starting hound maneuver...")

    # Move forward for 3 sec
    print("FORWARD\t\t\t[3s]")
    hound.send_velocity_cmd(throttle=0.5, steering=0.0)
    sleep(3.0)

    # Stop for 1 sec
    print("STOP\t\t\t[1s]")
    hound.apply_brake()
    sleep(1.0)

    # Turn left for 2 sec
    print("TURN(LEFT)\t\t\t[1s]")
    hound.send_velocity_cmd(steering=-1.0)
    sleep(2.0)

    print("Hound maneuver complete")
    hound.close()


if __name__ == "__main__":
    main()
