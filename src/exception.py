# -------------------------------------------------------------
# Import the built-in sys module.
# The sys module provides functions and variables that interact
# with the Python interpreter.
#
# In this file, we use sys.exc_info() to get detailed information
# about an exception (error), such as:
# 1. Error Type
# 2. Error Message
# 3. Traceback (File name and Line number)
# -------------------------------------------------------------
import sys


# -------------------------------------------------------------
# Import the custom logger created in the project.
#
# This logger is used to write logs into a log file instead of
# printing everything on the terminal.
#
# Although it is imported here, it is not used in this file.
# It may be used later while logging errors.
# -------------------------------------------------------------
from src.logger import logging


# -------------------------------------------------------------
# Function Name: error_message_detail
#
# Purpose:
# Create a detailed error message that contains:
# - Python file name
# - Line number where the error occurred
# - Original error message
#
# Parameters:
# err          -> The original exception object.
#
# error_detail -> Usually the sys module.
#                 We use it because sys.exc_info() returns
#                 complete information about the current exception.
# -------------------------------------------------------------
def error_message_detail(err, error_detail: sys):

    # ---------------------------------------------------------
    # sys.exc_info() returns a tuple of three values:
    #
    # (Exception Type,
    #  Exception Object,
    #  Traceback Object)
    #
    # Example:
    #
    # (
    #   <class 'ZeroDivisionError'>,
    #   ZeroDivisionError('division by zero'),
    #   <traceback object>
    # )
    #
    # We only need the traceback object because it contains
    # information about the file name and line number.
    #
    # "_" means "Ignore this value".
    # ---------------------------------------------------------
    _, _, exc_tb = error_detail.exc_info()


    # ---------------------------------------------------------
    # Traceback object stores information about where
    # the exception happened.
    #
    # exc_tb.tb_frame
    #        ↓
    # Current stack frame
    #
    # exc_tb.tb_frame.f_code
    #        ↓
    # Code object
    #
    # exc_tb.tb_frame.f_code.co_filename
    #        ↓
    # Returns the Python file name.
    #
    # If traceback is None, return "Unknown".
    # ---------------------------------------------------------
    file_name = (
        exc_tb.tb_frame.f_code.co_filename
        if exc_tb
        else "Unknown"
    )


    # ---------------------------------------------------------
    # Create a readable error message.
    #
    # Example Output:
    #
    # Error occurred in python script name [train.py]
    # line number [45]
    # error message [division by zero]
    # ---------------------------------------------------------
    error_message = (
        "Error occurred in python script name [{}] "
        "line number [{}] "
        "error message [{}]"
    ).format(

        # File where error occurred
        file_name,

        # Line number where error occurred
        exc_tb.tb_lineno if exc_tb else "Unknown",

        # Actual error message
        str(err)
    )


    # ---------------------------------------------------------
    # Return the complete error message.
    # ---------------------------------------------------------
    return error_message


# =============================================================
# Custom Exception Class
#
# Every custom exception should inherit from Python's
# built-in Exception class.
#
#                 Exception
#                      │
#                      ▼
#             CustomException
#
# This allows our class to behave like a normal Python exception
# while also providing additional information.
# =============================================================
class CustomException(Exception):


    # ---------------------------------------------------------
    # Constructor
    #
    # Runs automatically whenever an object is created.
    #
    # Example:
    #
    # raise CustomException(e, sys)
    #
    # Python internally does:
    #
    # obj = CustomException(e, sys)
    # obj.__init__(e, sys)
    # ---------------------------------------------------------
    def __init__(self, message, error_detail: sys):


        # -----------------------------------------------------
        # Call the constructor of the parent Exception class.
        #
        # This stores the original exception message.
        #
        # Equivalent to:
        #
        # Exception.__init__(self, message)
        # -----------------------------------------------------
        super().__init__(message)


        # -----------------------------------------------------
        # Generate the detailed error message by calling
        # error_message_detail().
        #
        # Store it inside this object.
        #
        # Example:
        #
        # self.error_message =
        #
        # Error occurred in python script name [train.py]
        # line number [25]
        # error message [division by zero]
        # -----------------------------------------------------
        self.error_message = error_message_detail(
            message,
            error_detail
        )


    # ---------------------------------------------------------
    # __str__()
    #
    # This special method is automatically called whenever
    # Python needs the string representation of an object.
    #
    # Example:
    #
    # print(exception)
    #
    # Python automatically executes:
    #
    # exception.__str__()
    # ---------------------------------------------------------
    def __str__(self):

        # Return the detailed error message instead of the
        # default Python exception text.
        return self.error_message

