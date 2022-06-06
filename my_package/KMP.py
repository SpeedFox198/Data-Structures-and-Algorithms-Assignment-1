"""
Jabriel Seah 211973E Group 02

KMP Pattern Searching
---------------------
Pattern searching algorithm

Original KMP searches for index of matched pattern in text,
modified it to searching for existence of pattern in text for simplicity.
The function was also made to be not case-sensitive

References:
https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
https://iq.opengenus.org/kmp-vs-boyer-moore-algorithm/
https://www.youtube.com/watch?v=4jY57Ehc14Y
"""


def KMP_search(pattern:str, text:str) -> bool:
    """ Returns if pattern is found in text """
    n = len(text)     # Length of text
    m = len(pattern)  # Length of pattern

    # Perform non case sensitive search
    pattern = pattern.lower()
    text = text.lower()

    lps = [0] * m  # List length of longest prefix that is also suffix

    compute_lps(pattern, m, lps)  # Compute and generate lps

    # i - pointer for text
    # j - pointer for pattern
    i = j = 0

    # Search till i goes past text
    while i < n:

        # If characters matches
        if text[i] == pattern[j]:
            i += 1
            j += 1

        # If characters does not match

        # Case 1: parts of pattern is matched
        elif j > 0:
            # Move pointer j to matching suffix
            j = lps[j-1]

        # Case 2: pattern is completely not matched
        else:
            i += 1

        # If pattern is fully matched
        if j == m:
            return True  # Returns True if pattern is found

    # Returns False if pattern is not found
    return False


def compute_lps(pattern:str, m:int, lps:list) -> None:
    """ Computes and creates lps based on pattern """
    length = 0  # Length of longest prefix that is also a suffix
    i = 1       # Pointer of character in pattern

    # Start comparing from 2nd character
    while i < m:

        # If matching character is found
        if pattern[i] == pattern[length]:
            length += 1      # Increase length
            lps[i] = length  # Assign length to current index
            i += 1           # Increase i pointer

        # If character does not match

        # Case 1: length is not 0
        elif length > 0:
            # Decrease length to previous value
            length = lps[length-1]

        # Case 2: length is 0
        else:
            # Simply move to next element
            i += 1


if __name__ == "__main__":
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print(KMP_search(pattern, text))  # True

    text = "onionionspl"
    pattern = "onions"
    print(KMP_search(pattern, text))  # True

    text = "aaaaaaaaaaaaaaaaaaaaaab"
    pattern = "aaaaaab"
    print(KMP_search(pattern, text))  # True

    text = "ababcabcabababd"
    pattern = "ababd"
    print(KMP_search(pattern, text))  # True

    text = "ababcabcababab"
    pattern = "ababd"
    print(KMP_search(pattern, text) == False)
