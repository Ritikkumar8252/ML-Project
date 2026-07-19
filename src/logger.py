# -------------------------------------------------------------
# Import the built-in logging module.
#
# The logging module is used to record events that happen while
# the program is running.
#
# Instead of using print(), professional applications use
# logging because logs can be saved in files.
#
# Example:
#
# logging.info("Program Started")
# logging.warning("Memory is almost full")
# logging.error("Database Connection Failed")
# -------------------------------------------------------------
import logging


# -------------------------------------------------------------
# Import the os module.
#
# os stands for Operating System.
#
# It provides functions to work with:
#
# • Files
# • Folders (Directories)
# • File paths
# • Environment Variables
#
# Example:
#
# os.getcwd()
# os.mkdir()
# os.path.join()
# -------------------------------------------------------------
import os


# -------------------------------------------------------------
# Import datetime class from datetime module.
#
# datetime is used for handling date and time.
#
# Example:
#
# Current Date
# Current Time
# Current Year
#
# Here we use it to create a unique log file name.
# -------------------------------------------------------------
from datetime import datetime


# =============================================================
# Create Log File Name
# =============================================================

# datetime.now()
#
# Returns the current date and time.
#
# Example:
#
# 2026-07-19 10:25:35
#
# strftime() converts date/time into a formatted string.
#
# Format:
#
# %m -> Month
# %d -> Day
# %Y -> Year
# %H -> Hour (24-hour format)
# %M -> Minute
# %S -> Second
#
# Example Output:
#
# 07_19_2026_10_25_35.log
#
# Every run creates a different file.
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# =============================================================
# Create Logs Folder Path
# =============================================================

# os.getcwd()
#
# Returns the current working directory.
#
# Example:
#
# C:\Users\Ritik\Desktop\ML_Project
#
# os.path.join()
#
# Joins multiple folder names correctly according to the
# operating system.
#
# Instead of writing:
#
# "C:\\Users\\Ritik\\Desktop\\logs"
#
# Python builds the path automatically.
#
# Result:
#
# C:\Users\Ritik\Desktop\ML_Project\logs\07_19_2026_10_25_35.log
logs_path = os.path.join(
    os.getcwd(),
    "logs",
    LOG_FILE
)


# =============================================================
# Create Directory
# =============================================================

# os.makedirs()
#
# Creates directories.
#
# Syntax:
#
# os.makedirs(path)
#
# If the directory already exists,
# exist_ok=True prevents Python from throwing an error.
#
# Example:
#
# logs/
#
# will be created automatically if it doesn't exist.
os.makedirs(logs_path, exist_ok=True)


# =============================================================
# Create Complete Log File Path
# =============================================================

# Join the folder path with the log file name.
#
# Example:
#
# C:\Users\Ritik\Desktop\ML_Project
#        ↓
# logs
#        ↓
# 07_19_2026_10_25_35.log
LOG_FILE_PATH = os.path.join(
    logs_path,
    LOG_FILE
)


# =============================================================
# Configure Logging
# =============================================================

logging.basicConfig(

    # Save all logs into this file.
    filename=LOG_FILE_PATH,

    # Format of every log message.
    #
    # %(asctime)s -> Date and Time
    #
    # %(lineno)d -> Line Number
    #
    # %(name)s -> Logger Name
    #
    # %(levelname)s -> Log Level
    #
    # %(message)s -> Actual Log Message
    #
    # Example:
    #
    # [2026-07-19 10:45:32]
    # 25
    # root
    # INFO
    # Program Started
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",

    # Minimum level to store.
    #
    # DEBUG
    # INFO
    # WARNING
    # ERROR
    # CRITICAL
    #
    # Since INFO is selected,
    # INFO and all levels above it will be stored.
    level=logging.INFO,
)

# -------------------------------------------------------------
# This special condition checks whether this file is being
# executed directly or imported into another Python file.
#
# Every Python file has a built-in variable called __name__.
#
# Case 1: If you run this file directly
#
#     python logger.py
#
# Python automatically sets:
#
#     __name__ = "__main__"
#
# So the condition becomes:
#
#     if "__main__" == "__main__":
#
# which is True, and the code inside this block executes.
#
# -------------------------------------------------------------
# Case 2: If another file imports this file
#
#     from src.logger import logging
#
# Python sets:
#
#     __name__ = "logger"
#
# So the condition becomes:
#
#     if "logger" == "__main__":
#
# which is False, and the code inside this block is skipped.
#
# This allows us to write test code that only runs when the
# file is executed directly, but not when it is imported.
# -------------------------------------------------------------
if __name__ == "__main__":

    # Write an INFO log indicating that logger.py was run
    # directly (not imported).
    logging.info("Logger module executed directly.")

    # Write another sample INFO log message.
    # This is useful for testing whether logging is configured
    # correctly and the log file is being created successfully.
    logging.info("This is a log message.")