import requests


def print_recursive_dict(data, indent_spaces=3, indent_step=2, recursion=False):
    """Prints a formatted nested dictionary to the console.

    .. code-block::

        # example console output for an input of {'123':{'456':['aaa', 'bbb', 'ccc']}}

        "
            123 :
                    456 : aaa
                        bbb
                        ccc"

    Args:
        data (dict): Dictionary of values that can be converted to strings.
        indent_spaces (int, optional): Number of leading whitespaces to insert before each element. Defaults to 3.
        indent_step (int, optional): Number of whitespaces to increase the indentation by, for each level of ``dict`` nesting. Defaults to 2.
        recursion (bool, optional): Whether or not this method is being called by itself. Defaults to False.

    """

    # print a newline once, prior to the formatted dictionary
    if not recursion:
        print()

    # loop through the dictionary
    for key, value in data.items():

        # the right-justification for each key is equal to the length of the longest key
        rjust = len(max(data, key=len))

        # if the value is a dictionary, then recursively call this function to print the inner dictionary
        if isinstance(value, dict):
            print(" " * indent_spaces + f"{key.rjust(rjust)} : ")
            print_recursive_dict(
                list_to_string(value, rjust),
                indent_spaces
                + indent_step
                + rjust
                + 1,  # adjust the indentation level of the inner dictionary
                indent_step,
                True,
            )

        # if the value is not a dictionary, then print the key-value pair
        else:
            print(
                " " * indent_spaces
                + f"{key.rjust(rjust)} : {list_to_string(value, rjust + indent_spaces + 3)}"
            )


def list_to_string(value, leading_whitespaces=1):
    """Takes a list and returns a formatted string containing each element delimited by newlines.

    .. admonition:: TODO

        Incorporate :py:obj:`print_recursive_dict` for lists with dictionary elements, i.e. ``[{}, {}]``.

    Args:
        value (list): A list of elements that can be represented by strings.
        leading_whitespaces (int, optional): Number of leading whitespaces to insert before each element. Defaults to 1.

    Returns:
        str: Formatted string containing each element of the provided list delimited by newlines, with ``leading_whitespaces`` leading whitespaces before each element.

        .. code-block::

            # example returned string for an input of ['abc', 'def', 'ghi']

            " abc\\n def\\n ghi"
    """

    # just return the same value if it's not a list
    if not isinstance(value, list):
        return value
    # if the list is empty, then return a blank string
    elif len(value) == 0:
        return ""
    # if the list has only one element, then return that element
    elif len(value) == 1:
        return value[0]
    # if the list has more than one element, then return a string containing each element delimited by newlines
    # add leading_whitespaces number of leading whitespaces before each element
    else:
        return_string = str(value[0]) + "\n"
        for i in range(1, len(value)):
            return_string += (" " * leading_whitespaces) + str(value[i]) + "\n"
        return return_string.strip()


def convert_response(response: requests.Response):
    """Converts an API request response into a dictionary.

    .. admonition:: todo

        Incorporate response status/error checking, error handling, etc.

    Args:
        response (requests.Response): An API request response object.

    Returns:
        dict: Dictionary representation of the provided API request response.
    """

    return response.json()


def print_isp_loader(isp_name, left_align=19):
    """Prints a formatted line to the console, with no carriage return, in the form of:

    .. code-block::

         {isp_name} ..............

    Args:
        isp_name (str): Name of the ISP to be displayed.
        left_align (int, optional): Width of the printed text in its entirety, minus the trailing whitespace. Defaults to 19.
    """

    print(f"\n {isp_name} ".ljust(left_align, ".") + " ", end="", flush=True)


def print_divider():
    """Prints a divider to the console in the form of:

    .. code-block::

         --------------------------------------

    """

    print("\n -------------------------------------- ")
