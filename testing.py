"""
Jabriel Seah 211973E Group 02

Testing Timsort
---------------
Here we push timsort to the limits and test it
After testing, my implementation of timsort was the clear winner :)

NOTE:
- Relative imports will need to be edited to prevent import errors
- The usage of greater_than and less_than has caused a huge function overhead
- Previous testing had yielded much greater differences in speed when the functions weren't used
- However the usage of the functions are necessary as we need to compare both strings and numbers
"""
from my_package.misc import greater_than, less_than
from my_package.timsort import timsort as my_timsort
from my_package.test_gallop import with_galloping as test_tim
from timeit import default_timer as timer
import random

# The above imports my implementation of timsort


# The below codes is the timsort code found in geeks4geeks
# https://www.geeksforgeeks.org/timsort/
# I've copied over their code directly and
# made little modifications for compatibility
# These codes are copied over for benchmarking

# Iterative Timsort function to sort the
# array[0...n-1] (similar to merge sort)
def theirTimSort(arr, key):
    n = len(arr)
    minRun = calcMinRun(n)

    # Sort individual subarrays of size RUN
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertionSort(arr, key, start, end)

    # Start merging from size RUN (or 32). It will merge
    # to form size 64, then 128, 256 and so on ....
    size = minRun
    while size < n:

        # Pick starting point of left sub array. We
        # are going to merge arr[left..left+size-1]
        # and arr[left+size, left+2*size-1]
        # After every merge, we increase left by 2*size
        for left in range(0, n, size << 1):

            # Find ending point of left sub array
            # mid+1 is starting point of right sub array
            mid = min(n - 1, left + size - 1)
            right = min(left + (2 * size) - 1, n - 1)

            # Merge sub array arr[left.....mid] &
            # arr[mid+1....right]
            if mid < right:
                merge(arr, key, left, mid, right)

        size <<= 1

def calcMinRun(n):
    """Returns the minimum length of a
    run from 23 - 64 so that
    the len(array)/minrun is less than or
    equal to a power of 2.
 
    e.g. 1=>1, ..., 63=>63, 64=>32, 65=>33,
    ..., 127=>64, 128=>32, ...
    """
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r

# This function sorts array from left index to
# to right index which is of size atmost RUN
def insertionSort(arr, key, left, right):
    for i in range(left+1, right+1):
        e = arr[i]
        j = i-1
        while j >= left and less_than(e[key], arr[j][key]):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = e

# Merge function merges the sorted runs
def merge(array, key, l, m, r):

    # original array is broken in two parts
    # left and right array
    len1, len2 = m - l + 1, r - m
    left = array[l : len1+l]
    right = array[m+1 : len2+m+1]

    i, j, k = 0, 0, l

    # after comparing, we merge those two array
    # in larger sub array
    while i < len1 and j < len2:
        if greater_than(left[i][key], right[j][key]):
            array[k] = right[j]
            j += 1

        else:
            array[k] = left[i]
            i += 1

        k += 1

    # Copy remaining elements of left, if any
    while i < len1:
        array[k] = left[i]
        k += 1
        i += 1

    # Copy remaining element of right, if any
    while j < len2:
        array[k] = right[j]
        k += 1
        j += 1


# The below is an implementation of mergesort directly gotten from geeks4geeks
# https://www.geeksforgeeks.org/merge-sort/

def mergeSort(arr, key):
    if len(arr) > 1:

         # Finding the mid of the array
        mid = len(arr)//2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        mergeSort(L, key)

        # Sorting the second half
        mergeSort(R, key)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if less_than(L[i][key], R[j][key]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def test(func, original_array, reverse=False, output_error=True):
    array = original_array.copy()
    sorted_array = sorted(array, key=lambda x:x["key"], reverse=reverse)
    params = ["key"]
    if reverse: params.append(reverse)
    try:
        start = timer()
        func(array, *params)
        end = timer()
    except IndexError as e:
        if output_error:
            with open("error.log", mode="a") as f:
                f.write(f"{original_array}\n")
        raise IndexError(e)
    is_sorted = array == sorted_array
    print(f"({'XO'[is_sorted]}) {func.__name__:<15} {end-start}")
    if not is_sorted and output_error:
        with open("error.log", mode="a") as f:
            f.write(f"{original_array}\n")
    return array


# Test codes
n = 100000  # Length of array
rate_of_unsortedness = 1000  # The larger the value, the more sorted partially_sorted is
range_of_numbers = 100
# Produce arrays for testing
partially_sorted = [{"key":(1,2)[not random.randint(0, rate_of_unsortedness)]*i} for i in range(n)]
completely_random = [{"key":random.randint(0, range_of_numbers)} for _ in range(n)]

# Print Length of array
print("Sorting array of length", n)

# Test on completely random arrays
print("Completely Random:")
for sort_func in (mergeSort, theirTimSort, my_timsort, test_tim):
    test(sort_func, completely_random)

# Test on partially sorted arrays
print("Partially Sorted:")
for sort_func in (mergeSort, theirTimSort, my_timsort, test_tim):
    test(sort_func, partially_sorted)


# Test on reverse functionality
print("\nReverse sort:\n")

print("Completely Random:")
test(my_timsort, completely_random, True)
test(test_tim, completely_random, True)

print("Partially Sorted:")
test(my_timsort, partially_sorted, True)
test(test_tim, partially_sorted, True)
