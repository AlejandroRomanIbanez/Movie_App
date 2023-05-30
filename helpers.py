YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
RESET_COLOR = "\033[0m"


def user_choice_color(string):
    """
    Adds color formatting to a string to display user choice.
    Parameters:
    string (str): The string to be formatted.
    Returns:
    str: The formatted string with color codes.
    """
    return MAGENTA + string + RESET_COLOR


def error_color(string):
    """
    Adds color formatting to a string to display error messages.
    Parameters:
    string (str): The string to be formatted.
    Returns:
    str: The formatted string with color codes.
    """
    return RED + string + RESET_COLOR


def input_color(string):
    """
    Adds color formatting to a string to display user input.
    Parameters:
    string (str): The string to be formatted.
    Returns:
    str: The formatted string with color codes.
    """
    return BLUE + string + RESET_COLOR


def return_to_menu():
    """
    Displays a message and waits for user input before returning to the main menu.
    """
    input(input_color("Press enter to continue"))