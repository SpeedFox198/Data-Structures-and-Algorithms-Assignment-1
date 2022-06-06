"""
Jabriel Seah 211973E Group 02

Assignment 1 IT2553 Data Structures and Algorithms
--------------------------------------------------

Assumtions made:
- The assumtion was made that max number of pax a package will have
  is 100, (as extremely large numbers for this field is not very realistic).

Advanced features implemented:
- Counting sort
- Radix sort
- Binary insertion sort
- AVL tree
- Timsort
- Custom sort (self-implemented optimised insertion sort)

Resources referred to for this application:
- https://www.geeksforgeeks.org/counting-sort/
- https://www.geeksforgeeks.org/radix-sort/
- https://www.geeksforgeeks.org/lower-bound-on-comparison-based-sorting-algorithms/
- https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
- https://www.geeksforgeeks.org/avl-tree-set-2-deletion/
- https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
- https://iq.opengenus.org/kmp-vs-boyer-moore-algorithm/
- https://www.youtube.com/watch?v=4jY57Ehc14Y
- https://hackernoon.com/timsort-the-fastest-sorting-algorithm-youve-never-heard-of-36b28417f399
- https://www.geeksforgeeks.org/timsort/
- https://medium.com/@rscheiwe/the-case-for-timsort-349d5ce1e414
- https://github.com/python/cpython/blob/main/Objects/listsort.txt
- https://github.com/python/cpython/blob/main/Objects/listobject.c
- https://www.wild-inter.net/publications/munro-wild-2018
- https://www.youtube.com/watch?v=snYTAyyR4VE
- https://www.youtube.com/watch?v=Yk4CBisILaw
- https://www.youtube.com/watch?v=o8y9uYygLcw
"""
from my_package.misc import print_records, input_int, input_float, input_str
from my_package.sort import bubble_sort, selection_sort, insertion_sort, counting_sort, radix_sort
from my_package.search import linear_search, binary_search
from my_package.AVLTree import AVLTree
from my_package.timsort import timsort
from my_package.custom_sort import custom_search, custom_sort
from my_package.KMP import KMP_search


# List of staycation booking records
records = [
    {"package":"Sentosa staycation", "customer":"Jabriel Seah", "pax":1, "cost":9999.99},
    {"package":"Cheap stay @ Toa Payoh", "customer":"Waffles", "pax":1, "cost":10},
    {"package":"Package 01", "customer":"Daniel", "pax":2, "cost":300},
    {"package":"Package 02", "customer":"Waffles", "pax":10, "cost":1205.20},
    {"package":"Some random package", "customer":"Clarence", "pax":4, "cost":100.30},
    {"package":"Sentosa staycation", "customer":"Jaron", "pax":1, "cost":9999.99},
    {"package":"Mein Kampfy Chair", "customer":"Royston", "pax":12, "cost":35},
    {"package":"Studio Ghibli Staycation", "customer":"Totoro", "pax":100, "cost":734.25},
    {"package":"Json format staycation", "customer":"Json", "pax":5, "cost":100},
    {"package":"Package 03", "customer":"Joshua", "pax":83, "cost":5.50}
]

# A binary search tree of records sorted by package name
records_tree = AVLTree("package", records)

# Sort records initially using timsort by package name
timsort(records, "package")

# Methods for sorting
SORT_METHODS = ("package name", "customer name", "package cost", "no. of pax")
METHOD_NO = (None, 1, 0, 2, 2, 3, None)  # Which index of SORT_METHODS does method number correspond to
SORT_KEYS = ("package", "customer", "cost", "pax")  # Keys used for sorting in respective methods
sorted_by = 0  # Index of current sorted sequence

# Methods for searching
SEARCH_METHODS = ("customer name", "package name", "package name (improved)", "global search")

# Message to be printed for menu
MENU_MESSAGE = """Staycation Booking Records System
Enter the corresponding number to run the operation:
(1) Display all records
(2) List records from price range
(3) Sort records
(4) Search and update record
(5) Exit application"""


run = True  # Flag for running the program
while run:
    # Print welcome message
    print(MENU_MESSAGE)

    # Prompt for input for operation
    choice = input_int( "Enter number: ", "Please enter a number from 1 to 5!", low=1, high=5)

    if choice == 1:  # Display all records
        print("\nDisplaying all records:")
        print_records(records, range(len(records)))
        print()  # Blank line


    elif choice == 2:  # List records from price range

        # Print message
        print("\nList records from price range:")

        # Get minimum price (price should be positive)
        low = input_float(
            "Enter minimum price: ", "Please enter a valid number!",
            low=0, low_err="Number should be positive!"
        )

        # Get maximum price (max price should be >= min price)
        high = input_float(
            "Enter maximum price: ", "Please enter a valid number!",
            low=low, low_err="Max price should be greater or equals to min price!"
        )

        # Get indexes of values to display
        indexes = []
        for index, record in enumerate(records):

            # If record is within price range
            if low <= record["cost"] <= high:
                indexes.append(index)  # Append index of record

        # Display records
        print(f"\nDisplaying records from ${low:.2f} to ${high:.2f}:")
        print_records(records, indexes)
        print()  # Blank line


    elif choice == 3:  # Sort records
        # Print message
        print(
            "\nSelect method to sort the records:\n"
           f"Currently sorted by {SORT_METHODS[sorted_by]}\n"
            "(1) Sort by customer name\n"
            "(2) Sort by package name\n"
            "(3) Sort by package cost\n"
            "(4) Sort by package cost (improved)\n"
            "(5) Sort by no. of pax\n"
            "(6) Cancel"
        )

        # Get user choice
        method = input_int("Enter choice: ", "Please choose a method 1 to 6!", low=1, high=6)

        # Sort based on method chosen
        if METHOD_NO[method] == sorted_by:  # Skip if already sorted by method chosen
            pass

        elif method == 1:  # Sort record by Customer Name using Bubble sort
            bubble_sort(records, "customer")

        elif method == 2:  # Sort record by Package Name using Selection sort
            selection_sort(records, "package")

        elif method == 3:  # Sort record by Package Cost using Insertion sort
            insertion_sort(records, "cost")

        elif method == 4:  # Sort record by Package Cost using Insertion sort
            radix_sort(records, "cost", decimal_places=2)

        elif method == 5:  # Sort record by No. of Pax using Counting sort
            # Note: range of numbers will be 0 to 100 (length of 101)
            counting_sort(records, "pax", count_len=101)

        else:  # Cancel operation and return to menu
            print("Operation cancelled.\n")
            continue

        # If correct input, set sorted_by to index representing the current method of sort
        sorted_by = METHOD_NO[method]

        # Display records and break out of loop
        print(f"\nRecords sorted by {SORT_METHODS[sorted_by]}:")
        print_records(records, range(len(records)))
        print()  # Blank line


    elif choice == 4:  # Search and update records

        results = []  # Results yielded from search

        # Search continues till a result is yielded or user exits
        while not results:

            # Print message
            print(
                "\nSelect method to search records:\n"
                "(1) Search records by customer name\n"
                "(2) Search records by package name\n"
                "(3) Search records by package name (improved)\n"
                "(4) Global search\n"
                "(5) Cancel"
            )

            # Get user choice
            method = input_int("Enter choice: ", "Please choose a method 1 to 5!", low=1, high=5)

            if method == 5:  # Cancel operation and return to menu
                print("Operation cancelled.\n")
                break

            # Get search string
            q = input("Enter search: ")  # Used q because Google HAHAHAHAHA

            # Search based on method chosen
            if method == 1:  # Search record by Customer Name using Linear Search
                results = linear_search(records, q, "customer")

                sorted_list = records  # Set sorted_list to records

            elif method == 2:  # Search record by Package Name using Binary Search

                # In order to not re-order the records, a new list is being made
                sorted_list = records.copy()

                # Sort records using timsort
                timsort(sorted_list, "package")

                results = binary_search(sorted_list, q, "package")

            elif method == 3:  # Search record by Package Name in a binary search tree
                sorted_list = records_tree.search(q)

                # Set results to all indexes of sorted_list
                results = range(len(sorted_list))
            
            elif method == 4:  # Global search record for substring using KMP algorithm
                # Global search searches both package and customer name

                results = []  # Store results of found records
                patterns = q.split()  # Patterns to be searched

                # Go through each record
                for i, r in enumerate(records):

                    # Check every pattern entered in search
                    for pattern in patterns:

                        # If pattern matches with any of package or customer name
                        if KMP_search(pattern, r["package"]) or KMP_search(pattern, r["customer"]):
                            results.append(i)  # Add index to result
                            break

                sorted_list = records  # Set sorted_list to records

            # Print results from search
            print(f'\nSearched for "{q}" by {SEARCH_METHODS[method-1]}:')
            print_records(sorted_list, results, count=True)

        # If no results yielded exit operation
        if not results:
            continue

        record_index = 0  # Index of record to be updated

        # If more than one record is being found
        if len(results) > 1:
            record_index = input_int(
                "Enter number of record to be updated: ",
                "Please enter a proper number!",
                low=1, high=len(results),
                range_err="Number should be within the results!"
            )

            record_index -= 1  # Python counts from 0

        # Confirm update (I got lazy here, default assume yes)
        if input(f"Edit record #{record_index+1}? (Y/n): ").upper() != "N":

            # Get record
            record = sorted_list[results[record_index]]

            # Get new values for update
            index = input_str(
                "Enter package name: ", "Package name must not be empty!",
                min_len=1
            )
            customer = input_str(
                "Enter customer name: ", "Customer name must not be empty!",
                min_len=1
            )
            pax = input_int(
                "Enter number of pax: ", "Please enter a proper number!",
                low=1, low_err="Number of pax should be more than 0!",
                high=100, high_err="Max number of pax is 100!"
            )
            cost = input_float(
                "Enter package cost per pax: ", "Please enter a proper number!",
                low=0.01, low_err="Cost per pax should be more than 0!"
            )

            # Find index of record in records
            key = SORT_KEYS[sorted_by]
            record_pos = custom_search(records, key, record)

            # Delete old record from AVL tree
            records_tree.delete(record)

            # Assign values (do this after inputs in case of errors)
            record["package"] = index
            record["customer"] = customer
            record["pax"] = pax
            record["cost"] = cost

            # Insert updated record into AVL tree
            records_tree.insert(record)

            # Output records
            print("\nUpdated record:")
            print_records(sorted_list, (results[record_index],))

            # Due to update of record, array needs to be sorted again
            custom_sort(records, key, record, record_pos)

        else:  # If user entered N/n
            print("Operation cancelled.")

        print()  # Blank line


    else:  # Exit application
        print("Exiting application. Goodbye!")
        run = False
