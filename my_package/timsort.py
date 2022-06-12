"""
Jabriel Seah 211973E Group 02

Timsort Function
----------------
As the sorting functions are tailored for the project,
a key is needed to access the value in the dictionaries in the list of records.

Timsort, a sorting algorithm that took me over a week to implement
At least it was worth the trouble, I had fun doing it :P

It's performance was clearly above regular sorts,
especially when the array is partially sorted.

Timsort really performs tremendously better then regular merge sort
My test code for verifying that is in test_tim.py

Resources I had to go through to understand timsort:
(This is but just half of it)
- https://hackernoon.com/timsort-the-fastest-sorting-algorithm-youve-never-heard-of-36b28417f399
- https://www.geeksforgeeks.org/timsort/
- https://medium.com/@rscheiwe/the-case-for-timsort-349d5ce1e414
- https://github.com/python/cpython/blob/main/Objects/listsort.txt
- https://github.com/python/cpython/blob/main/Objects/listobject.c
- https://www.wild-inter.net/publications/munro-wild-2018
- https://www.youtube.com/watch?v=snYTAyyR4VE
- https://www.youtube.com/watch?v=Yk4CBisILaw
- https://www.youtube.com/watch?v=o8y9uYygLcw

Here, some beautiful looking text:
████████╗██╗███╗░░░███╗░██████╗░█████╗░██████╗░████████╗
╚══██╔══╝██║████╗░████║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝
░░░██║░░░██║██╔████╔██║╚█████╗░██║░░██║██████╔╝░░░██║░░░
░░░██║░░░██║██║╚██╔╝██║░╚═══██╗██║░░██║██╔══██╗░░░██║░░░
░░░██║░░░██║██║░╚═╝░██║██████╔╝╚█████╔╝██║░░██║░░░██║░░░
░░░╚═╝░░░╚═╝╚═╝░░░░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░
"""
from .misc import greater_than, less_than


MIN_GALLOP = 7  # Minimum wins to gallop


def timsort(array:list, key:str, reverse:bool=False) -> None:
    """ Sorts an array using timsort algorithm """

    n = len(array)  # Length of array
    remaining = n  # Length of array left that needs merging

    min_gallop = MIN_GALLOP  # Minimum wins for galloping

    min_run = compute_minrun(n)  # Minimum length of a run

    # Stacks for storing runs and powers found
    runs = []
    powers = []

    low = 0  # Index of low limit of run
    while remaining:

        # Get length of next run
        count, decreasing = count_run(array, key, low, low+remaining-1, reverse=reverse)

        # If run is strictly descending, reverse run in-place
        if decreasing:
            reverse_run(array, low, low+count-1)

        # If length of run is less than minrun, extend run
        if count < min_run:
            force = min(min_run, remaining)  # Length to force size of run into
            bin_insertion_sort(array, key, low, low+force-1, reverse=reverse)
            count = force

        # Store value of current low and count
        curr_low, curr_count = low, count

        # If runs stack is not empty
        if runs:

            # Find power of run
            prev_low, prev_count = runs[-1]
            power = powerloop(prev_low, prev_count, curr_count, n)

            # While power is smaller than power at top of stack
            while powers and power <= powers[-1]:
                powers.pop()  # Remove old power from stack
                prev_prev_low, prev_prev_count = runs[-2]
                if prev_prev_count <= prev_count:
                    min_gallop = merge_lo(array, key, prev_prev_low, prev_prev_count, prev_low, prev_count, min_gallop, reverse=reverse)
                else:
                    min_gallop = merge_hi(array, key, prev_prev_low, prev_prev_count, prev_low, prev_count, min_gallop, reverse=reverse)

                runs.pop()  # Remove old prev run from stack
                runs[-1][1] += prev_count  # Set new low and count of current run
                prev_low, prev_count = runs[-1]  # Get updated values of previous run

            # Add power to stack
            powers.append(power)

        # Append to runs information of current run
        runs.append([curr_low, curr_count])

        remaining -= count  # Reduce remaining by length of run
        low += count

    curr_low, curr_count = runs[-1]
    for i in range(len(runs)-2, -1, -1):
        prev_low, prev_count = runs[i]
        if prev_count <= curr_count:
            min_gallop = merge_lo(array, key, prev_low, prev_count, curr_low, curr_count, min_gallop, reverse=reverse)
        else:
            min_gallop = merge_hi(array, key, prev_low, prev_count, curr_low, curr_count, min_gallop, reverse=reverse)

        # Calculate new low and count
        curr_low = prev_low
        curr_count += prev_count


def compute_minrun(n:int) -> int:
    """ Computes and return the minimum length of a run from 16 - 32 """

    # As python implemetation of insertion sort is not fast enough
    # A minrun of value 32 is chosen instead of the original 64    

    r = 0  # Becomes 1 if any 1 bits are shifted off

    # Take the first 5 bits of n
    while n >= 32:
        r |= n & 1
        n >>= 1

    # Return calculated value of min run
    return n + r


def powerloop(s1:int, n1:int, n2:int, n:int) -> int:
    """ Return power of run """
    power = 0  # power calculated

    # midpoints a and b:
    # a = s1 + n1/2
    # b = s1 + n1 + n2/2 = a + (n1 + n2)/2

    a = (2 * s1) + n1  # 2*a
    b = a + n1 + n2    # 2*b

    while True:
        power += 1

        if a >= n:  # n is before a
            a -= n
            b -= n

        elif b >= n:  # n is before b
            break

        # n is after a and b
        a <<= 1
        b <<= 1

    return power


def bin_insertion_sort(array:list, key:str, start:int, end:int, reverse:bool=False) -> None:
    """ Sorts an array using binary insertion sort algorithm """

    # Go through the elements and make comparisions
    for i in range(start+1, end+1):

        e = array[i]  # Current element

        j = i-1  # Index of element left of current element

        # Get index of position to insert element in
        pos = bin_search(array, key, e[key], start, j, reverse=reverse)

        # Shift elements to the right to perform insertion
        while j >= pos:
            array[j+1] = array[j]
            j -= 1

        # Insert element in sorted sub-array
        array[j+1] = e


def bin_search(array:list, key:str, target, low:int, high:int, reverse:bool=False) -> int:
    """ Binary searches the subarray for the index to insert element """

    # Loop till index out of range
    while low <= high:

        mid = (low + high) >> 1  # Index of middle element

        # If middle element is less than target
        if less_than(array[mid][key], target, reverse=reverse):
            low = mid + 1

        # If middle element is more than target
        elif greater_than(array[mid][key], target, reverse=reverse):
            high = mid - 1

        # If middle element matches target
        else:

            # Return index to insert element
            return mid + 1

    # Return low if not found
    return low


def count_run(array:list, key:str, low:int, high:int, reverse:bool=False) -> tuple[int, bool]:
    """ Returns the length of the run beginning at low """

    # If low is at end of list
    if low == high:
        return 1, False  # Return length of run, not decreasing

    count = 2  # Count of length of the run
    low += 1

    # If run is strictly decreasing
    if less_than(array[low][key], array[low-1][key], reverse=reverse):

        # Count length of natural run
        for i in range(low+1, high+1):

            # Break if is increasing
            if less_than(array[i][key], array[i-1][key], reverse=reverse):
                count += 1
            else:
                break
        
        # Return length of run, decreasing
        return count, True

    # Else, run is increasing
    else:

        # Count length of natural run
        for i in range(low+1, high+1):

            # Break if is decreasing
            if less_than(array[i][key], array[i-1][key], reverse=reverse):
                break
            else:
                count += 1
        
        # Return length of run, not decreasing
        return count, False


def reverse_run(array:list, low:int, high:int) -> None:
    """ Reverses a run from low to high in-place """
    while low < high:
        array[low], array[high] = array[high], array[low]
        low += 1
        high -= 1


def merge_lo(array:list, key:str, s1:int, n1:int, s2:int, n2:int, min_gallop:int, reverse:bool=False) -> int:
    """ Merges two runs A and B at index s1 and s2 with length n1 and n2 where n1 < n2 """

    a_count = 0  # Number of times A won in a row
    b_count = 0  # Number of times B won in a row

    # Copy elements of smaller run into temp array,
    # and leave the longer run at the right of original array
    # This decreases the amount of space needed to merge the 2 runs
    # merge_lo merges the runs when n1 < n2

    temp = array[s1:s1+n1]  # Create temp array storing smaller run A

    i = 0   # Pointer for A (in temp array)
    j = s2  # Pointer for B (in original array)
    k = s1  # Pointer for merging runs

    # Perform merge and galloping
    while True:

        # Merge till either pointer i or j goes out of range,
        # or condition for galloping has been met
        while True:

            # If B[j] < A[i] (B won)
            if less_than(array[j][key], temp[i][key], reverse=reverse):
                array[k] = array[j]
                j += 1

                # End merging if j goes out of range
                if j >= s2 + n2:
                    # Copy temp content into array if any
                    copy_A(array, temp, k+1, i, n1)
                    return min_gallop  # Return new value of min_gallop

                b_count += 1  # Increase counter since B won
                a_count = 0   # Set A counter to back to 0

                # Break if won enough for galloping
                if b_count >= min_gallop:
                    break

            # Else A[i] <= B[j] (A won)
            else:
                array[k] = temp[i]
                i += 1

                # End merging if i goes out of range
                if i >= n1:
                    return min_gallop  # Return new value of min_gallop

                a_count += 1  # Increase counter since A won
                b_count = 0   # Set B counter to back to 0

                # Break if won enough for galloping
                if a_count >= min_gallop:
                    break

            k += 1  # k index increment

        # Artificially increased values so that it can be decreased
        min_gallop += 1
        a_count += 1
        b_count += 1
        k += 1  # Increase k as break statement skipped increment

        # Gallop will continue till a_count or b_count is bellow min_gallop
        while a_count >= min_gallop or b_count >= min_gallop:
            min_gallop -= min_gallop > 1  # Make it easier to enter galloping mode

            # Find B[j] in A
            found_index = gallop_B_right(temp, key, array[j][key], i, n1-i, reverse=reverse)

            # Get a_count
            a_count = found_index - i

            # Merge elements till found index
            while i < found_index:
                array[k] = temp[i]
                i += 1
                k += 1

            # If all elements in A has been merged
            if i == n1:
                return min_gallop  # Return new value of min_gallop

            # Insert target into correct index
            array[k] = array[j]
            j += 1
            k += 1

            if j == s2 + n2:
                # Copy temp content into array if any
                copy_A(array, temp, k, i, n1)
                return min_gallop  # Return new value of min_gallop

            # Find A[i] in B
            found_index = gallop_A_right(array, key, temp[i][key], j, s2+n2-j, reverse=reverse)

            # Get b_count
            b_count = found_index - j

            # Merge elements till found index
            while j < found_index:
                array[k] = array[j]
                j += 1
                k += 1

            # If all elements in B has been merged
            if j == s2 + n2:
                # Copy temp content into array if any
                copy_A(array, temp, k, i, n1)
                return min_gallop  # Return new value of min_gallop

            # Insert target into correct index
            array[k] = temp[i]
            i += 1
            k += 1

            # If all elements in A has been merged
            if i == n1:
                return min_gallop  # Return new value of min_gallop

        min_gallop += 1  # Penalise it for leaving galloping mode


def merge_hi(array:list, key:str, s1:int, n1:int, s2:int, n2:int, min_gallop:int, reverse:bool=False) -> int:
    """ Merges two runs A and B at index s1 and s2 with length n1 and n2 where n1 > n2 """

    a_count = 0  # Number of times A won in a row
    b_count = 0  # Number of times B won in a row

    # Copy elements of smaller run into temp array,
    # and leave the longer run at the left of original array
    # This decreases the amount of space needed to merge the 2 runs
    # merge_hi merges the runs when n1 > n2

    temp = array[s2:s2+n2]  # Create temp array storing smaller run B

    i = s1+n1-1  # Pointer for A (in original array)
    j = n2-1     # Pointer for B (in temp array)
    k = s2+n2-1  # Pointer for merging runs

    # Perform merge and galloping
    while True:

        # Merge till either pointer i or j goes out of range,
        # or condition for galloping has been met
        while True:

            # If A[i] > B[j] (A won)
            if greater_than(array[i][key], temp[j][key], reverse=reverse):
                array[k] = array[i]
                i -= 1

                # End merging if i goes out of range
                if i < s1:
                    # Copy temp content into array if any
                    copy_B(array, temp, k-1, j)
                    return min_gallop  # Return new value of min_gallop

                a_count += 1  # Increase counter since A won
                b_count = 0   # Set B counter to back to 0

                # Break if won enough for galloping
                if a_count >= min_gallop:
                    break

            # Else B[j] >= A[i] (B won)
            else:
                array[k] = temp[j]
                j -= 1

                # End merging if i goes our of range
                if j < 0:
                    return min_gallop  # Return new value of min_gallop

                b_count += 1  # Increase counter since B won
                a_count = 0   # Set A counter to back to 0

                # Break if won enough for galloping
                if b_count >= min_gallop:
                    break

            k -= 1  # k index decrement

        # Artificially increased values so that it can be decreased in 1st line of while loop
        min_gallop += 1
        a_count += 1
        b_count += 1
        k -= 1  # Decrease k as break statement skipped decrement

        # Gallop will continue till a_count or b_count is bellow min_gallop
        while a_count >= min_gallop or b_count >= min_gallop:
            min_gallop -= min_gallop > 1  # Make it easier to enter galloping mode

            # Find B[j] in A
            found_index = gallop_B_left(array, key, temp[j][key], i, i-s1, reverse=reverse)

            # Get a_count
            a_count = i - found_index

            # Merge elements till found index
            while i >= found_index:
                array[k] = array[i]
                i -= 1
                k -= 1

            # If all elements in A has been merged
            if i == s1-1:
                # Copy temp content into array if any
                copy_B(array, temp, k, j)
                return min_gallop  # Return new value of min_gallop

            # Insert target into correct index
            array[k] = temp[j]
            j -= 1
            k -= 1

            # If all elements in B has been merged
            if j == -1:
                return min_gallop  # Return new value of min_gallop

            # Find A[i] in B
            found_index = gallop_A_left(temp, key, array[i][key], j, j, reverse=reverse)

            # Get b_count
            b_count = j - found_index

            # Merge elements till found index
            while j >= found_index:
                array[k] = temp[j]
                j -= 1
                k -= 1

            # If all elements of B has been merged
            if j == -1:
                return min_gallop  # Return new value of min_gallop

            # Insert target into correct index
            array[k] = array[i]
            i -= 1
            k -= 1

            # If all elements of A has been merged:
            if i == s1-1:
                # Copy temp content into array if any
                copy_B(array, temp, k, j)
                return min_gallop  # Return new value of min_gallop

        min_gallop += 1  # Penalise it for leaving galloping mode


def gallop_A_right(run:list, key:str, target, index:int, max_offset:int, reverse:bool=False) -> int:
    """ Gallop right and find position to insert element of run A inside run B """
    prev_offset = 0  # Value of previous offset (low boundary in binary search)
    offset = 1       # Value of current offset (high boundary in binary search)

    # If target is less than or equals to first element of run
    if not greater_than(target, run[index][key], reverse=reverse):
        return index  # Return index to insert element

    # Gallop till run[index + prev_offset] < target <= run[index + offset]
    while offset < max_offset and less_than(run[index+offset][key], target, reverse=reverse):
        prev_offset = offset        # Set previous offset value
        offset = (offset << 1) + 1  # Increase offset

    # Prevent offset from going past limit
    if offset > max_offset:
        offset = max_offset

    # Change offset values to low and high indexes for binary search
    prev_offset += index
    offset += index

    # Binary search for position
    while prev_offset < offset:
        mid = (prev_offset + offset) >> 1
        if less_than(run[mid][key], target, reverse=reverse):
            prev_offset = mid + 1
        else:
            offset = mid

    # Return index to insert element
    return offset


def gallop_A_left(run:list, key:str, target, index:int, max_offset:int, reverse:bool=False) -> int:
    """ Gallop left and find position to insert element of run A inside run B """
    prev_offset = 0  # Value of previous offset (low boundary in binary search)
    offset = 1       # Value of current offset (high boundary in binary search)

    # If target is greater than last element of run
    if greater_than(target, run[index][key], reverse=reverse):
        return index + 1  # Return index to insert element

    # Gallop till run[index - offset] < target <= run[index - prev_offset]
    while offset < max_offset and not less_than(run[index-offset][key], target, reverse=reverse):
        prev_offset = offset        # Set previous offset value
        offset = (offset << 1) + 1  # Increase offset

    # Prevent offset from going past limit
    if offset > max_offset:
        offset = max_offset

    # Change offset values to low and high indexes for binary search
    prev_offset, offset = index - offset, index - prev_offset

    # Binary search for position
    while prev_offset < offset:
        mid = (prev_offset + offset) >> 1
        if less_than(run[mid][key], target, reverse=reverse):
            prev_offset = mid + 1
        else:
            offset = mid

    # Return index to insert element
    return offset


def gallop_B_right(run:list, key:str, target, index:int, max_offset:int, reverse:bool=False) -> int:
    """ Gallop right and find position to insert element of run B inside run A """
    prev_offset = 0  # Value of previous offset (low boundary in binary search)
    offset = 1       # Value of current offset (high boundary in binary search)

    # If target is less than first element of run
    if less_than(target, run[index][key], reverse=reverse):
        return index

    # Gallop till run[index + prev_offset] <= target < run[index + offset]
    while offset < max_offset and not less_than(target, run[index+offset][key], reverse=reverse):
        prev_offset = offset        # Set previous offset value
        offset = (offset << 1) + 1  # Increase offset

    # Prevent offset from going past limit
    if offset > max_offset:
        offset = max_offset

    # Change offset values to low and high indexes for binary search
    prev_offset += index
    offset += index

    # Binary search for position
    while prev_offset < offset:
        mid = (prev_offset + offset) >> 1
        if less_than(target, run[mid][key], reverse=reverse):
            offset = mid
        else:
            prev_offset = mid + 1

    # Return index to insert element
    return offset


def gallop_B_left(run:list, key:str, target, index:int, max_offset:int, reverse:bool=False) -> int:
    """ Gallop left and find position to insert element of run B inside run A """
    prev_offset = 0  # Value of previous offset (low boundary in binary search)
    offset = 1       # Value of current offset (high boundary in binary search)

    # If target is greater than or eauals to last element of run
    if not less_than(target, run[index][key], reverse=reverse):
        return index + 1  # Return index to insert element

    # Gallop till run[index - offest] <= target < run[index - prev_offset]
    while offset < max_offset and less_than(target, run[index-offset][key], reverse=reverse):
        prev_offset = offset        # Set previous offset value
        offset = (offset << 1) + 1  # Increase offset

    # Prevent offset from going past limit
    if offset > max_offset:
        offset = max_offset

    # Change offset values to low and high indexes for binary search
    prev_offset, offset = index - offset, index - prev_offset

    # Binary search for position
    while prev_offset < offset:
        mid = (prev_offset + offset) >> 1
        if less_than(target, run[mid][key], reverse=reverse):
            offset = mid
        else:
            prev_offset = mid + 1

    # Return index to insert element
    return offset


def copy_A(array:list, temp:list, k:int, i:int, n:int) -> None:
    """ Copy content from A into original array """
    while i < n:
        array[k] = temp[i]
        i += 1
        k += 1


def copy_B(array:list, temp:list, k:int, j:int) -> None:
    """ Copy content from B into original array """
    while j >= 0:
        array[k] = temp[j]
        j -= 1
        k -= 1
