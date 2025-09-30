import os
import csv
from datetime import datetime

class Logger:
    """
    A simple CSV logger.
    """
    def __init__(self, log_dir: str, file_name_prefix: str):
        """
        Initializes the logger and creates the log file.

        Args:
            log_dir (str): The directory where log files will be stored.
            file_name_prefix (str): A prefix for the log file name.
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name_prefix}_{timestamp}.csv"
        self.log_file_path = os.path.join(log_dir, file_name)
        
        try:
            self.file_handle = open(self.log_file_path, 'w', newline='')
            self.writer = csv.writer(self.file_handle)
        except IOError as e:
            raise IOError(f"Could not create or open log file {self.log_file_path}: {e}")

    def log(self, data: list, is_header: bool = False):
        """
        Writes a row of data to the log file and prints it to the terminal.

        Args:
            data (list): A list of values to be written as a CSV row.
            is_header (bool): If true, treats the data as the header row.
        """
        try:
            # Write to CSV file
            self.writer.writerow(data)
            
            # Log to terminal
            log_message = ", ".join(map(str, data))
            if is_header:
                print(f"LOG HEADER: {log_message}")
            else:
                # For data, we can format it for better alignment if needed, but simple is fine.
                print(f"LOG DATA: {log_message}")

        except Exception as e:
            print(f"Error writing to log file: {e}")

    def close(self):
        """
        Closes the log file.
        """
        if self.file_handle:
            self.file_handle.close()

