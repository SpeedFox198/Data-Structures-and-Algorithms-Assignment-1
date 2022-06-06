"""
Jabriel Seah 211973E Group 02

AVLTree
-------
AVL Tree is a self-balancing binary search tree
As the tree is tailored for the project,
a key is needed to access the value in the dictionaries in the list of records.
The tree's search function are also made for comparing strings as required by the assignment.

Assumtions made:
- The assumtion was made that there can be duplicate
  package names and customer names
  accross the different records.
- Thus, nodes are made to store all occurances of same value,
  and search function is made to return all occurances.

References:
- https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
- https://www.geeksforgeeks.org/avl-tree-set-2-deletion/
"""
from .misc import equals_to, greater_than, less_than


class Node:
    """ Represents a node in an AVL tree """

    def __init__(self, key:str, *datas):
        """ Initialises an AVL tree node """
        self.datas = list(datas)    # List of datas stored by node
        self.value = datas[0][key]  # Value of datas being stored
        self.left = None            # Left child of node
        self.right = None           # Right child of node
        self.height = 1             # Height of node

    def add(self, data):
        """ Adds new value into datas """
        self.datas.append(data)

    def remove(self, data):
        """ Removes value from datas """
        for i, value in enumerate(self.datas):

            # Removes and return data being found
            if data is value:
                return self.datas.pop(i)


class AVLTree:
    """ AVL Tree is a self-balancing binary search tree """

    def __init__(self, key:str, datas=()):
        """ Initialises an AVL tree """
        self.root = None  # Root of tree
        self.key = key  # Key used for accessing value

        for data in datas:
            self.insert(data)


    def insert(self, data):
        """ Inserts data into tree """
        self.root = self._insert(self.root, data)


    def delete(self, data):
        """ Deletes data from tree """
        self.root = self._delete(self.root, data)


    def search(self, item):
        """ Search for item and return list of datas if found """
        node = self.root  # Set current node to root

        # Search till data is found / not in tree
        while node is not None and not equals_to(node.value, item):

            if less_than(item, node.value):  # If data is less than node
                node = node.left  # Search left child of node

            elif greater_than(item, node.value):  # If data is greater than node
                node = node.right  # Search right child of node

        # Return empty list if not found
        if node is None:
            return []

        # Return list of datas if found
        else:
            # Make a copy so changes made to list does not affect node
            return node.datas.copy()


    def _insert(self, node:Node, data):
        """ Inserts data in subtree and returns new root of subtree """

        # Insert data into new node in tree
        if node is None:  # If no node, insert new node
            return Node(self.key, data)

        # Go to left child if data is less than node
        elif less_than(data[self.key], node.value):
            node.left = self._insert(node.left, data)

        # Go to right child if data is greater than node
        elif greater_than(data[self.key], node.value):
            node.right = self._insert(node.right, data)
        
        # If there's a node with equal value
        else:
            node.add(data)  # Add data to list of data
            return node     # Return the same node

        # Update height of the node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get balance factor
        balance = self.get_balance(node)

        # Rotate tree if node is umbalanced

        # Left Left case
        if balance > 1 and less_than(data[self.key], node.left.value):
            return self.right_rotate(node)

        # Right Right case
        if balance < -1 and greater_than(data[self.key], node.right.value):
            return self.left_rotate(node)

        # Left Right case
        if balance > 1 and greater_than(data[self.key], node.left.value):
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left case
        if balance < -1 and less_than(data[self.key], node.right.value):
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node


    def _delete(self, node:Node, data):
        """ Deletes data in subtree and returns new root of subtree """

        # Remove node containing data from tree
        if node is None:  # If no node, return None
            return node

        elif less_than(data[self.key], node.value):  # Go to left child if data is less than node
            node.left = self._delete(node.left, data)

        elif greater_than(data[self.key], node.value):  # Go to right child if data is greater than node
            node.right = self._delete(node.right, data)

        else:  # If data is equals to node

            # If node contains more than one data
            if len(node.datas) > 1:
                node.remove(data)  # Remove data from list of datas
                return node        # Node is kept at position

            # If node has no left child, return the right child
            elif node.left is None:
                new_node = node.right  # Set new node
                del node  # Ensures that node is garbage collected
                return new_node

            # If node has no right child, return the left child
            elif node.right is None:
                new_node = node.left  # Set new node
                del node  # Ensures that node is garbage collected
                return new_node

            # If node has 2 children (get inorder successor)
            successor = self.get_min_node(node.right)
            node.datas = successor.datas
            node.value = successor.value

            # Make successor only contain 0 record so that it'll be deleted
            successor_data = successor.datas[0]
            successor.datas = []

            # Delete the inorder successor
            node.right = self._delete(node.right, successor_data)

        # Update height of the node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get balance factor
        balance = self.get_balance(node)

        # Rotate tree if node is umbalanced

        # Left Left case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Right Right case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Left Right case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node


    def right_rotate(self, z:Node):

        # Get y and T3 (refer to geeksforgeeks for what they mean)
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Return new root
        return y


    def left_rotate(self, z:Node):

        # Get y and T2 (refer to geeksforgeeks for what they mean)
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Return new root
        return y


    def get_balance(self, node:Node):
        """ Returns balance factor of node """

        if node is None:  # If no node, return 0
            return 0

        # Balance = left child's height - right child's height
        return self.get_height(node.left) - self.get_height(node.right)


    @staticmethod
    def get_height(node):
        """ Returns height of node """

        if node is None:  # Returns 0 if no node
            return 0

        # Else, return height of node
        return node.height


    @staticmethod
    def get_min_node(node:Node):
        """ Returns node with the minimum value """

        # Node with the minimum value is the leftmost child node
        while node is not None and node.left is not None:
            node = node.left

        # Return leftmost node
        return node




# Extra functions for test code output
def _in_order(tree:AVLTree):
    return _in_order_helper(tree.root, tree.key)

def _in_order_helper(node:Node, key:str):
    if node is None:
        return ""
    return f"{_in_order_helper(node.left, key)} {node.value}({len(node.datas)}) {_in_order_helper(node.right, key)}"

def _print_tree(tree:AVLTree):  # Very ugly print tree function
    x = []
    for i in range(1, tree.get_height(tree.root)+1):
        x.append(" ".join(_print_tree_helper(tree.root, i, tree.key)))
    pad = len(x[-1])
    for i in x:
        print(f'{i:^{pad}}')

def _print_tree_helper(node:Node, j, key):
    j -= 1
    if node is None:
        return ("",)
    if j <= 0:
        return (f"{node.value}({len(node.datas)})",)

    return _print_tree_helper(node.left, j, key) + _print_tree_helper(node.right, j, key)


# Test codes
if __name__ == "__main__":
    records = [{"key":i} for i in "abcdefghij"+"ABCDEFGHIJ"]

    # A tree for testing
    myTree = AVLTree("key", records)

    # Inorder Traversal
    print("Inorder of AVL tree:")
    print(_in_order(myTree))

    print("\nOriginal Tree:")
    _print_tree(myTree)

    # You can observe from the output that the node's number decreased
    print(f"\nDelete {records[2]}")
    myTree.delete(records[2])
    _print_tree(myTree)


    # You can observe from the output that the tree balances itself
    print(f"\nDelete {records[0]} x2 + {records[2]} x1")
    myTree.delete(records[2])
    myTree.delete(records[0])
    myTree.delete(records[0])
    _print_tree(myTree)
