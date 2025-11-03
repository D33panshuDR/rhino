
import time
import sys
from rhino.main import Rhino

# --- Configuration ---
# For SITL (Software In The Loop) simulation:
# CONNECTION_STRING = 'udp:127.0.0.1:14550'
# For a real vehicle connected via USB:
CONNECTION_STRING = '/dev/ttyACM0' 

# Rover RC Channel configuration (Default for ArduPilot)
THROTTLE_CHANNEL = 3
STEERING_CHANNEL = 1

def main():
    """
    Main function to run the drive example.
    """
    rhino_controller = None
    try:
        # Initialize the controller
        rhino_controller = Rhino(
            connection_string=CONNECTION_STRING,
            log_dir='logs',  
            file_name_prefix='hound',
            throttle_channel=THROTTLE_CHANNEL,
            steering_channel=STEERING_CHANNEL
        )

        print("\n--- Starting drive sequence ---")
        
        # Drive forward with a slight right turn for 2 seconds
        print("Driving forward and right for 2 seconds...")
        drive_duration = 3  # seconds
        start_time = time.time()
        
        while time.time() - start_time < drive_duration:
            # Send a command: 25% throttle, 0% right steer
            rhino_controller.send_velocity_cmd(throttle=0.25, steering=0)
            time.sleep(0.1) # Send commands at 10 Hz

        start_time = time.time()

        while time.time() - start_time < drive_duration:
            # Send a command: 25% throttle, 0% right steer
            rhino_controller.send_velocity_cmd(throttle=0.15, steering=0.7)
            time.sleep(0.1) # Send commands at 10 Hz

        start_time = time.time()
        
        while time.time() - start_time < drive_duration:
            # Send a command: 25% throttle, 0% right steer
            rhino_controller.send_velocity_cmd(throttle=0.15, steering=-0.7)
            time.sleep(0.1) # Send commands at 10 Hz

        # Stop the rover
        print("Stopping rover...")
        rhino_controller.send_velocity_cmd(throttle=0.0, steering=0.0)
        time.sleep(1) # Wait a moment to ensure stop command is processed

        print("--- Drive sequence complete ---")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        
    finally:
        # This block is crucial! It ensures that RC control is released
        # and connections are closed, even if an error occurs.
        if rhino_controller:
            print("Cleaning up resources...")
            rhino_controller.close()

if __name__ == "__main__":
    main()
