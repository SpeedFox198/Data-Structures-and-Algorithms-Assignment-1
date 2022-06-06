"""
Jabriel Seah 211973E Group 02

Miscellaneous Functions
-----------------------
Contains utility functions used in the project.
"""

def print_records(array, indexes, count=False) -> None:
    """ Print all records with indexes """

    # Max padding values (Default value set to length of title +3)
    paddings = {"package":15, "customer":16, "pax":13, "cost":19}

    # Get paddings needed
    for i in indexes:
        record = array[i]
        for key, item in record.items():

            # Get padding needed
            if isinstance(item, float):
                padding = len(f"{item:.2f}") + 3
            else:
                padding = len(str(item)) + 3

            if paddings[key] < padding:
                paddings[key] = padding

    # If indexing (count) of records is needed
    if count:
        paddings["count"] = len(indexes)//10 + 4

    # Dashes
    max_length = sum(paddings.values())
    dashes = "=" * max_length

    # Print header
    print(dashes)
    if count: print(f"{'#':<{paddings['count']}}", end="")
    print(
        f"{'Package Name':<{paddings['package']}} "
        f"{'Customer Name':<{paddings['customer']}} "
        f"{'No. of pax':<{paddings['pax']}} "
        f"{'Package Cost/pax'}"
    )
    print(dashes)

    # If indexes provided is falsey (empty iterable)
    if not indexes:
        print(f"{'  No records found  ':-^{max_length}}")

    # Print Records
    for i, j in enumerate(indexes, start=1):
        record = array[j]
        if count: print(f"{i:<{paddings['count']}}", end="")
        print(
            f"{record['package']:<{paddings['package']}} "
            f"{record['customer']:<{paddings['customer']}} "
            f"{record['pax']:<{paddings['pax']}} "
            f"{record['cost']:.2f}"
        )
    print(dashes)


def input_int(prompt:str, err_msg:str, low:int=None, high:int=None,
              range_err:str=None, low_err:str=None, high_err:str=None) -> int:
    """
    Prompts user to input a valid integer within range

    Args:
        prompt (str): The prompt for user input
        err_msg (str): Default error message to display
        low (:obj:`int`, optional): Minimum allowed value for integer
        high (:obj:`int`, optional): Maximum allowed value for integer 
        range_err (:obj:`str`, optional): Default error message when value is not within range
        low_err (:obj:`str`, optional): Error message when value lower than low
        high_err (:obj:`str`, optional): Error message when value higher than high

    Returns:
        int: Integer value of user input

    Raises:
        ValueError: Raised when low value specified is greater than high value
    """

    # Check that low <= high
    if low is not None and high is not None and low > high:
        raise ValueError("value of low should be less than or equals to value of high")

    # Loop till correct input
    while True:

        try:  # Get user input
            value = int(input(prompt))

        except ValueError:  # If not valid int
            print(err_msg)

        else:  # Check for low and high ranges if specified

            # If less than low
            if low is not None and value < low:

                # Priority: low_err, range_err, err_msg
                if low_err is not None:
                    print(low_err)
                elif range_err is not None:
                    print(range_err)
                else:
                    print(err_msg)

            # If greater than high
            elif high is not None and value > high:

                # Priority: high_err, range_err, err_msg
                if high_err is not None:
                    print(high_err)
                elif range_err is not None:
                    print(range_err)
                else:
                    print(err_msg)

            # Return result if no error
            else:
                return value


def input_float(prompt:str, err_msg:str, low:float=None, high:float=None,
                range_err:str=None, low_err:str=None, high_err:str=None) -> float:
    """
    Prompts user to input a valid float within range

    Args:
        prompt (str): The prompt for user input
        err_msg (str): Default error message to display
        low (:obj:`float`, optional): Minimum allowed value for float
        high (:obj:`float`, optional): Maximum allowed value for float 
        range_err (:obj:`str`, optional): Default error message when value is not within range
        low_err (:obj:`str`, optional): Error message when value lower than low
        high_err (:obj:`str`, optional): Error message when value higher than high

    Returns:
        float: Float value of user input

    Raises:
        ValueError: Raised when low value specified is greater than high value
    """

    # Check that low <= high
    if low is not None and high is not None and low > high:
        raise ValueError("value of low should be less than or equals to value of high")

    # Loop till correct input
    while True:

        try:  # Get user input
            value = float(input(prompt))

        except ValueError:  # If not valid int
            print(err_msg)

        else:  # Check for low and high ranges if specified

            # If less than low
            if low is not None and value < low:

                # Priority: low_err, range_err, err_msg
                if low_err is not None:
                    print(low_err)
                elif range_err is not None:
                    print(range_err)
                else:
                    print(err_msg)

            # If greater than high
            elif high is not None and value > high:

                # Priority: high_err, range_err, err_msg
                if high_err is not None:
                    print(high_err)
                elif range_err is not None:
                    print(range_err)
                else:
                    print(err_msg)

            # Return result if no error
            else:
                return value


def input_str(prompt:str, err_msg:str, min_len:int=None, max_len:int=None,
              range_err:str=None, min_err:str=None, max_err:str=None) -> str:
    """
    Prompts user to input a valid string within range

    Args:
        prompt (str): The prompt for user input
        err_msg (str): Default error message to display
        min_len (:obj:`int`, optional): Minimum allowed length for string
        max_len (:obj:`int`, optional): Maximum allowed length for string 
        range_err (:obj:`str`, optional): Default error message when value is not within range
        min_err (:obj:`str`, optional): Error message when value lower than min_len
        max_err (:obj:`str`, optional): Error message when value higher than max_len

    Returns:
        str: String value of user input

    Raises:
        ValueError: Raised when min length specified is greater than max length
    """

    # Check that min_len <= max_len
    if min_len is not None and max_len is not None and min_len > max_len:
        raise ValueError("minimum length should be less than or equals to maximum length")

    # Loop till correct input
    while True:

        # Get user input
        value = input(prompt)

        # Check for minimum and maximum length if specified

        # If less than low
        if min_len is not None and len(value) < min_len:

            # Priority: min_err, range_err, err_msg
            if min_err is not None:
                print(min_err)
            elif range_err is not None:
                print(range_err)
            else:
                print(err_msg)

        # If greater than high
        elif max_len is not None and len(value) > max_len:

            # Priority: max_err, range_err, err_msg
            if max_err is not None:
                print(max_err)
            elif range_err is not None:
                print(range_err)
            else:
                print(err_msg)

        # Return result if no error
        else:
            return value


def equals_to(x, y) -> bool:
    """ Returns True if x is equals to y """

    # Perform non-case-sensitive comparison
    if isinstance(x, str):
        x = x.lower()
        y = y.lower()  # Assume y is also a str

    return x == y


def greater_than(x, y) -> bool:
    """ Returns True if x is greater than y """

    # Perform non-case-sensitive comparison
    if isinstance(x, str):
        x = x.lower()
        y = y.lower()  # Assume y is also a str

    return x > y


def less_than(x, y) -> bool:
    """ Returns True if x is less than y """

    # Perform non-case-sensitive comparison
    if isinstance(x, str):
        x = x.lower()
        y = y.lower()  # Assume y is also a str

    return x < y


# Test code
if __name__ == "__main__":

    # Tiny records
    records = [
        {"package":"Sentosa staycation", "customer":"Jabriel Seah", "pax":1, "cost":9999.99},
        {"package":"Sentosa staycation", "customer":"Jaron", "pax":1, "cost":9999.99},
        {"package":"Some random package", "customer":"Clarence", "pax":4, "cost":100.30},
    ]

    # Print records
    print_records(records, range(len(records)))
    print()

    # Print records (with numberings)
    print_records(records, range(len(records)), count=True)

    # Input int
    print(input_int("Enter the int: ", "Proper int pls", 0, 5,
                    low_err="int > 0 pls", high_err="int < 5 pls"))

    # Input float
    print(input_float("Enter the float: ", "Proper float pls", 0.1, 3, "0.1 < float < 3 pls"))
