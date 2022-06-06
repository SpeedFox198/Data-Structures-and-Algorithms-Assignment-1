"""
Jabriel Seah 211973E Group 02

Sort Functions
--------------
As the sorting functions are tailored for the project,
a key is needed to access the value in the dictionaries in the list of records.
Some sort functions are also made to compare strings as required by the assignment.

References:
- https://www.geeksforgeeks.org/counting-sort/
- https://www.geeksforgeeks.org/radix-sort/
- https://www.geeksforgeeks.org/lower-bound-on-comparison-based-sorting-algorithms/
"""
from .misc import greater_than, less_than


def bubble_sort(array:list, key:str) -> None:
    """ Sorts an array using optimised bubble sort algorithm """

    n = len(array)  # Get length of array

    # Loop through array, max possible iterations is n
    for i in range(n):

        is_sorted = True  # Flag: True if array is sorted (optimisation)

        # Go through the elements and make comparisions
        for j in range(n-i-1):

            k = j + 1  # Index of next element

            # Sort elements
            if greater_than(array[j][key], array[k][key]):
                is_sorted = False
                array[j], array[k] = array[k], array[j]

        # Break if array is already sorted (optimisation)
        if is_sorted:
            break


def selection_sort(array:list, key:str) -> None:
    """ Sorts an array using selection sort algorithm """
    for i in range(len(array)):

        k = i  # Index of minimum value

        # Go through the elements and make comparisions
        for j in range(i+1, len(array)):

            # If element is smaller, set min index
            if less_than(array[j][key], array[k][key]):
                k = j

        # Swap the min element with the 1st element
        array[i], array[k] = array[k], array[i]


def insertion_sort(array:list, key:str, start:int=0, end:int=None) -> None:
    """ Sorts an array using insertion sort algorithm """

    # Set end to last index of not specified
    if end is None:
        end = len(array) - 1

    # Go through the elements and make comparisions
    for i in range(start+1, end+1):

        e = array[i]  # Current element

        j = i-1  # Index of element left of current element

        # Shift all elements greater than e to the right
        while j >= start and less_than(e[key], array[j][key]):
            array[j+1] = array[j]
            j -= 1

        # Insert element in sorted sub-array
        array[j+1] = e


def counting_sort(array:list, key:str, place:int=1, multiply:int=1, count_len:int=10) -> None:
    """
    Sorts an array using counting sort algorithm

    Args:
        array (list): The list to be sorted
        key (str): The key to access the value in the list
        place (:obj:`int`, optional): The place (digit) to look at while counting
        multiply (:obj:`int`, optional): The value to multiply value by for counting (used for sorting floats)
        count_len (:obj:`int`, optional): Length of counting array needed (range of possible values)
    """

    # Get a copy of the original list
    original = array.copy()

    # Initialise count array
    count = [0] * count_len

    # Count occurance of each elements in array
    for e in original:
        index = int(((e[key]*multiply) // place) % count_len)  # Get index based on value of e
        count[index] += 1

    # Store the cummulative count
    for i in range(1, count_len):
        count[i] += count[i - 1]

    # Place elements in array according to index counted
    for e in reversed(original):  # Reversed for stable sort
        index = int(((e[key]*multiply) // place) % count_len)  # Get index based on value of e
        array[count[index] - 1] = e
        count[index] -= 1


def radix_sort(array:list, key:str, decimal_places:int=0) -> None:
    """ Sorts an array using radix sort algorithm """

    # Find the maximum number to know number of digits
    # As we are exploring algorithms here,
    # I've decided to write out the code for finding max myself,
    # instead of using my old code which uses the built-in function
    # maximum = max(array, key=lambda x: x[key])[key]
    maximum = array[0][key]
    for i in range(1, len(array)):
        if array[i][key] > maximum:
            maximum = array[i][key]

    # If sorting floats, multiply values by number of decimal places
    multiply = 10 ** decimal_places
    maximum *= multiply  # Maximum also has to be multiplied by this value

    # Do counting sort for every digit
    place = 1
    while maximum >= place:
        counting_sort(array, key, place=place, multiply=multiply)
        place *= 10


# Test code
if __name__ == "__main__":
    my_list = [
        {"a": 4, "b":23, "c":240, "d":10.0},
        {"a": 1, "b":12, "c":123, "d":9.9},
        {"a": 3, "b":53, "c":736, "d":1.2},
        {"a": 7, "b":34, "c":223, "d":10.0},
        {"a": 5, "b":11, "c":240, "d":5.4}
    ]

    # Original list
    print("my_list:")
    print("\n".join(map(str, my_list)))

    # Bubble sort
    print("\nBubble sort (a):")
    bubble_sort(my_list, "a")
    print("\n".join(map(str, my_list)))

    # Selection sort
    print("\nSelection sort (b):")
    selection_sort(my_list, "b")
    print("\n".join(map(str, my_list)))

    # Insertion sort
    print("\nInsertion sort (c):")
    insertion_sort(my_list, "c")
    print("\n".join(map(str, my_list)))

    # Counting sort
    print("\nCounting sort (a):")
    counting_sort(my_list, "a")
    print("\n".join(map(str, my_list)))

    # Radix sort
    print("\nRadix sort (c):")
    radix_sort(my_list, "c")
    print("\n".join(map(str, my_list)))

    print("\nRadix sort (d):")
    radix_sort(my_list, "d", decimal_places=1)
    print("\n".join(map(str, my_list)))
