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

### AVL Tree

![A tree?](/assets/tree.gif)

AVL tree is a self-balancing Binary Search Tree (BST). Like other self-balancing trees (e.g., Red Black Tree), AVL tree tries to keep the height of the tree to its minimum while maintaining a BST structure.

In AVL tree, a node of the tree is considered balanced if the absolute difference between the max height of the left and right subtrees are not more than 1. AVL tree maintains this balance by checking for the balance of each node whenever an insertion or deletion of node occurs. When a node is unbalanced, it balances itself by performing a series of rotations called left-rotate and right-rotate.

#### Why is a self-balancing BST needed? Is it useful?

First, we talk about binary search, it is an algorithm known for its extremely fast O(log n) time complexity. Its only issue is that it only works on sorted arrays, thus the array must be sorted before searching.

One approach would simply be to sort the array whenever binary search is performed. However, the extra time taken to sort the given array will make the operation even slower than a linear search.

So, I took a different approach, to maintain a BST for performing searches. However, time taken for searches in a BST depends on its height, a skewed tree might take O(n) time for searching in worst cases.

Thus, I chose to implement a self-balancing AVL tree. I also chose this tree over another self-balancing Red-Black tree due to AVL tree creating a more balanced tree than Red-Black tree does.

#### Time complexities
- Searching of value: `O(log n)`
- Insertion of nodes: `O(log n)`
- Deletion of nodes: `O(log n)`
- Updating key in a node: `O(log n)` _Since updating is essentially insertion + deletion_

> Overall difficulty level: <bold style="color:#ffffff;weight">Hard</bold>
![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `#f03c15`
