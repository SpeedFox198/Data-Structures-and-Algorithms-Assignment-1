"""
Jabriel Seah 211973E Group 02

Custom Sort
-----------
A custom sort targetted specifically for this application.
Sort is built around the idea that updating of 1 record
results in an almost sorted array.


The Issue
---------
After searching and updating a record,
the records will no longer be sorted.
That is not how an application is supposed to be like
and it's not nice at all to leave it as it is, unsorted.
So I've decided to sort the array in the same order as how it did previously.

I could just sort it using any sorting algorithm,
but that would not be great as it will be too slow.
Since only 1 element is out-of-place,
there should be a faster way to sort it.


Thought Process
---------------
The initial idea was to implement timsort here too
which will work fantastically well as
timsort is used for partially sorted array.

I then thought that I should make it even
more optimised and specific as timsort is
too general and works for all datasets.

I then thought of making a sort meant for
sorting only 1 out-of-place element.


The Algorithm
-------------
The algorithm is pretty simple.
It is sort of a miniature modified insertion sort.

As only 1 element is out of place,
I only need to find that one element.

I used binary search to find the index of
the specific object in the array before updating the record.

Then, if the new value should be inserted to the left,
I'll perform insertion of only 1 element to the left.
Else, if it should be to the right, I'll instead
perform insertion of only 1 element to the right.

There's also a case where the update of the value did not mess up the sequence
of the array at all (new value is still larger than left and smaller than right).
In that case we will just skip the operation.


Footnote
--------
After writing this algorithm, I decided to search online
if there was any article takling this problem before
and came across this interesting solution proposed by someone
which solves a slightly more general case as compared to mine:
https://cs.stackexchange.com/questions/139914/sort-an-array-with-a-constant-number-of-unsorted-elements
"""
from .misc import greater_than, less_than
from .search import binary_search


def custom_search(array:list, key:str, target) -> int:
    """ Binary search for and returns index of target object using key """

    # Binary search of possible indexes target might reside in
    found_indexes = binary_search(array, target[key], key)

    found = -1  # Index of found object

    # Loop through found indexes to locate object
    for i in found_indexes:
        if array[i] is target:  # If element strictly is the same object in memory
            found = i
            break

    return found  # Return index of object if found, else -1


def custom_sort(array:list, key:str, target, index:int) -> None:
    """ Inserts target object into the correct index in the array in-place """

    # Target doesn't need sorting if:
    # 1. Target is last element of array and has max value in array
    # 2. Target is first element of array and has min value in array

    # Low and high limits of the array
    low, high = 0, len(array) - 1

    # Value of target for comparing
    value = target[key]

    # If target value is greater than right element and not last element
    if index < high and greater_than(value, array[index+1][key]):

        # Perform insertion of target towards right of array
        j = index + 1
        while j <= high and greater_than(value, array[j][key]):
            array[j-1] = array[j]
            j += 1

        # Insert target in correct index in array
        array[j-1] = target

    # If target value is less than left element and not first element
    elif index > low and less_than(value, array[index-1][key]):

        # Perform insertion of target towards left of array
        j = index - 1
        while j >= low and less_than(value, array[j][key]):
            array[j+1] = array[j]
            j -= 1

        # Insert target in correct index in array
        array[j+1] = target
