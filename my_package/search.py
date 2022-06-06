"""
Jabriel Seah 211973E Group 02

Search Functions
----------------
As the search functions are tailored for the project,
a key is needed to access the value in the dictionaries in the list of records.
Search functions are also made for comparing strings as required by the assignment.

Assumtions made:
- The assumtion was made that there can be duplicate
  package names and customer names
  accross the different records.
- Thus, search functions are made to find all occurances
  of the target instead of only the 1st occurance.
"""
from .misc import equals_to, greater_than, less_than

def linear_search(array:list, target, key:str) -> list:
    """ Linear searches an array for all occurance of target value """

    results = []  # Stores all matches of target value

    # Iterate through each element to find the target
    for i in range(len(array)):

        # If a match is found, append the index to list
        if equals_to(array[i][key].lower(), target):
            results.append(i)

    # Return a tuple of the result, empty tuple if none is found
    return results


def binary_search(array:list, target, key:str) -> range:
    """ Binary searches a sorted array for all occurance of target value """

    # Index of lower and upper bound of search
    low = 0
    high = len(array) - 1

    # Loop till index out of range
    while low <= high:

        mid = (low + high) >> 1  # Index of middle element

        # If middle element is less than target
        if less_than(array[mid][key], target):
            low = mid + 1

        # If middle element is greater than target
        elif greater_than(array[mid][key], target):
            high = mid - 1

        # If middle element matches target
        else:
            first = _binary_search_first(array, low, mid, high, target, key)
            last = _binary_search_last(array, low, mid, high, target, key)

            # Return range of indexes of matching elements
            return range(first, last+1)

    # Return an empty range(0) if not found
    return range(0)


def _binary_search_first(array:list, low:int, mid:int, high:int, target, key:str) -> int:
    """ Binary searches a sub-array for first occurance of target value """

    while low <= high:

        # When mid == target, either mid is 0 or target is larger than left element
        if equals_to(array[mid][key], target) and (mid == 0 or greater_than(target, array[mid-1][key])):
            break

        # If middle element is less than target
        elif less_than(array[mid][key], target):
            low = mid + 1

        # If middle element matches target
        else:
            high = mid - 1

        mid = (low + high) >> 1  # Index of middle element

    return mid


def _binary_search_last(array:list, low:int, mid:int, high:int, target, key:str) -> int:
    """ Binary searches a sub-array for last occurance of target value """

    last_index = len(array) - 1  # Index of last element of array

    while low <= high:

        # When mid == target, either mid is last index or target is smaller than left element
        if equals_to(array[mid][key], target) and (mid == last_index or less_than(target, array[mid+1][key])):
            break

        # If middle element is greater than target
        elif greater_than(array[mid][key], target):
            high = mid - 1

        # If middle element matches target
        else:
            low = mid + 1

        mid = (low + high) >> 1  # Index of middle element

    return mid


# Test code
if __name__ == "__main__":
    my_list = [
        {"a": "A", "b":"zf", "c":"CAA"},
        {"a": "Z", "b":"AS", "c":"ZDE"},
        {"a": "B", "b":"ss", "c":"CCC"},
        {"a": "X", "b":"SS", "c":"ABC"},
        {"a": "C", "b":"Sa", "c":"AAB"},
        {"a": "B", "b":"SB", "c":"LOL"},
        {"a": "B", "b":"Hi", "c":"SOS"}
    ]

    # List
    print("my_list:")
    print("\n".join(map(str, my_list)))

    # Linear sort
    print("\nLinear search (a):")
    print(tuple(linear_search(my_list, "c", "a")))  # (4)
    print(tuple(linear_search(my_list, "B", "a")))  # (2, 5, 6)
    print(tuple(linear_search(my_list, "f", "a")))  # ()


    # Sort list
    my_list.sort(key=lambda x: x["b"].lower())
    print("\nmy_list(sorted):")
    print("\n".join(map(str, my_list)))

    # Binary search
    print("\nBinary search (b):")
    print(tuple(binary_search(my_list, "Hi", "b")))  # (1,)
    print(tuple(binary_search(my_list, "ss", "b")))  # (4, 5)
    print(tuple(binary_search(my_list, "ZZ", "b")))  # ()
