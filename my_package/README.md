# Algorithms and Data Structures

> `my_package` contains all the classes and functions that are used for this project

### Basic Features Implemented

- Sorting algorithms
    - Bubble sort ([sort.py](sort.py))
    - Selection sort ([sort.py](sort.py))
    - Insertion sort ([sort.py](sort.py))
- Searching algorithms
    - Linear search ([search.py](search.py))
    - Binary search ([search.py](search.py))

### Advanced Features

- Sorting algorithms
    - Counting sort ([sort.py](sort.py))
    - LSD Radix sort ([sort.py](sort.py))
    - Binary insertion sort ([timsort.py](timsort.py))
    - Timsort ([timsort.py](timsort.py))
    - Custom sort ([custom_sort.py](custom_sort.py))
- String pattern searching algorithm
    - KMP algorithm ([KMP.py](KMP.py))
- Data Structures
    - AVL Tree ([AVLTree.py](AVLTree.py))

## Detailed Descriptions

> A record of all my findings, struggles, and hardwork ｡゜(｀Д´)゜｡


### How Records are Stored

Records in my project are stored as dictionaries in a list. E.g.:

> `records = [
>     {"package":"Package 01", "customer":"Adams", "pax":1, "cost":20},
>     {"package":"Package 02", "customer":"Baker", "pax":2, "cost":39.90},
>     {"package":"Package 03", "customer":"Clark", "pax":3, "cost":44},
> ]`

Each record stores the package name, customer name, number of pax, and package cost per pax.
Each value could be retrieved with their respective keys.




### AVL Tree

![A tree?](/assets/tree.gif)

AVL tree is a **self-balancing Binary Search Tree** (BST). Like other self-balancing trees (e.g., Red Black Tree), AVL tree tries to **keep the height of the tree to its minimum** while maintaining a BST structure.

In AVL tree, a node of the tree is considered **balanced** if the absolute difference between the max height of the left and right subtrees are not more than 1. AVL tree maintains this balance by checking for the balance of each node whenever an **insertion or deletion** of node occurs. When a node is **unbalanced**, it balances itself by performing a series of rotations called **left-rotate** and **right-rotate**.

#### Why is a self-balancing BST needed? Is it useful?

First, let's talk about **binary search**, it is an algorithm known for its extremely fast `O(log(n))` time complexity. Its only issue is that it only works on sorted arrays, thus the **array must be sorted** before searching.

One approach would simply be to sort the array whenever binary search is performed. However, the extra time taken to sort the given array will make the operation even slower than a linear search.

Another possible approach was to maintain a sorted array, and keep it sorted when values are updated. This approach is not bad, but we still need to perform a `O(n*log(n))` time sorting everytime a value is updated. Even [Timsort](#timsort), which boast extreme speed for partially sorted arrays, and my [Custom Sort](#custom-sort), with a `O(n)` time complexity, are still not good enough. We could do better than this.

So, I took a different approach, to maintain a BST for performing searches. However, time taken for searches in a BST **depends on its height**, a skewed tree might take `O(n)` time for searching in worst cases.

Thus, I chose to implement a **self-balancing** AVL tree. I also chose this tree over another self-balancing Red-Black tree due to AVL tree creating a more balanced tree than Red-Black tree does.

#### Handling duplicate records

Just like all my other implementations of searches, I have decided to handle having records with the **same keys** in my AVL Tree. To do this, I came up with a couple of solutions.

The simplest method for each `Node` to store records in a **list**.

Searching of keys will yield a copy of this list (to prevent change of data to list maintained by node). Insertion will create a new node if the key is unique, and append to the list if the key already exists. Likewise, deletion will simply pop the item from the list, and only remove the node if the list becomes empty.

The only issue with the list method is that during deletion of a record, it takes **linear time** to find for the position of the record in the list, and also a worse case of **linear time** to pop the record out of the list. Although this isn't a huge issue as I don't think the list will ever become very long. If only there was a better method.

Another method I considered was to use a python **dictionary/set** (as you know these things has `O(1))` operations).

The challenge I faced was that **mutable objects** could not and should not be hashed. An interesting suggestion I saw on stackoverflow was to use `id` as the key in the dictionary, this kinda works but it's not good for too many reasons.

To solve this, I could change the way I store my records, for each dictionary add a key to uniquely identify them, then use this value as the key in the dictionary. However, I am not very willing to change the whole structure of my records just to cater to storing it in a Node.

In the end, I opted for my initial idea of using a list.

My friend who also did this project chose to use a [**doubly linked list**](https://github.com/KJHJason/Data-Structures-And-Algorithms/blob/master/NYP-DSA-Assignment/src/data_structures/DoublyLinkedList.py) of using a  instead of a simple list. Although the time complexity for searching for a record in a doubly linked list is still **linear** the removing of this record becomes a **constant time operation** instead. A slight improvement to the list approach.

#### Time complexities
- Searching of keys: `O(log(n))`
- Insertion of nodes: `O(log(n))`
- Deletion of nodes: `O(log(n))`
- Updating key in a node: `O(log(n))` _Since updating is essentially insertion + deletion_

#### Overall difficulty level: **Hard**

AVL tree is much more **complex** than a simple BST tree, even with documents and codes online, it still takes time and effort to implement it successfully.

To make things more complicated, I have decided to **handle duplicate records**. The idea I had, and implemented, was for each node to **store a list of records** with the same value, and to only delete the node when list of records is empty. This also made other methods more complicated.




### Timsort

Timsort is an extremely fast stable hybrid sorting algorithm that is optimised for efficiently sorting real world data. Timsort is a sort that builds around the idea that data in real world have natural occurring sorted sequences (called “runs”).

#### Basic idea

The simplest explanation is that timsort uses insertion sort (an algorithm that sorts smaller arrays extremely fast) for the smaller subarrays (runs) and merges them using merging from merge sort.

#### Calculating minrun

Merging performs the most optimally when merging 2^i number of arrays. Thus, a minimum length of a run is chosen from the range 32 to 64 to achieve optimal merging.

In my code, values from 16 to 32 were used instead due to python implementations of insertion sort being too slow.

#### Counting runs

Timsort searches for natural ascending runs in the array and stores these runs in a stack. If the run is strictly descending, the run is being reversed in-place. If the run found is too short, timsort artificially increases its length using binary insertion sort.

Binary insertion sort is used as it requires less comparisons to insert the value (comparisons are very costly) (I have implemented binary insertion in my code too)

#### Merging conditions

The issue with merging natural runs is that adjacent runs might not be of equal length (merging must be done with adjacent runs for stability). Thus, there are some rules followed for deciding which runs to merge. Recently, the original rule used in Python’s timsort has been replaced by a more optimal rule used in powersort.

Powersort merges runs by calculating their power. Runs are being merged by comparing each run’s power. (If interested in the math behind powersort, take a look at here is a video explaining it very well.)

This new rule is extremely powerful as it allows merging of natural runs to be performed optimally.

#### Galloping

When merging 2 runs A and B, if timsort finds out that a huge chunk of B should be in front of A[0], it starts “galloping” to help it merge much faster than normal merging.

Galloping basically searches for index of A[0] in B so that there will be less comparisons involved. In cases of random data where it is slower to gallop, it is made harder to enter galloping. This compromise allows timsort to merge using galloping only when it’s paying off.

#### Memory efficient merge

To reduce temporary memory needed to hold the runs when merging, timsort copies the smaller run of the two into a temp array and leaves the other run in the original array. This allows less memory to be taken up when merging as the longer run is using the space in the original array when merging.

#### Stability: stable

Timsort uses `insertion sort` and `merging` which are both stable algorithms.
When searching for natural runs, timsort only searches for **strictly decereasing** runs to reverse for stability.

#### Time complexities

Best case: `O(n)`
Average case: `O(n*log(n))`
Worst case: `O(n*log(n))`

#### Overall difficulty level: **Extremely Difficult (to the point where I questioned the meaning of life)**

Many online implementations of timsort did not include the true key elements of timsort in it. Most of the components mentioned above are not implemented in most of the codes online. Also, information on all of these is either hard to find or hard to understand. I even resorted to reading the source code of Python’s timsort written in C language and its documentations. This took me 1 whole week to implement. (QAQ)




## Custom Sort

> To be added
