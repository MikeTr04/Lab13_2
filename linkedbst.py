"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import random
import time
import sys


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right:
                    stack.push(node.right)
                if node.left:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        lst = []

        def print_level(root, level, lst1):
            if root is None:
                return None
            if level == 1:
                lst1.append(root.data)
            elif level > 1:
                print_level(root.left, level - 1, lst)
                print_level(root.right, level - 1, lst)

        root = self._root
        height1 = self.height()
        for i in range(height1):
            print_level(root, i + 1, lst)
        return lst

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left and current_node.right:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(pos):
            """Return the height of the subtree rooted at Position p."""
            if pos is None or not pos.left and not pos.right:
                return 0
            else:
                return 1 + max(height1(child) for child in [pos.left, pos.right])

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """

        def helper():
            """Helper for count of vertices of the tree"""
            cnt = 0
            itr = self.inorder()
            for _ in itr:
                cnt += 1
            return cnt

        number = helper()
        if self.height() < 2 * log(2 * (number + 1)) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        ans = []
        for number in list(self.inorder()):
            if low <= number <= high:
                ans.append(number)
        if len(ans) > 0:
            return ans
        return None

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        elems = self.inorder()

        def rb1(elems):
            if len(elems) == 0:
                return None
            mid = len(elems) // 2
            node = BSTNode(elems[mid])
            node.left = rb1(elems[:mid])
            node.right = rb1(elems[mid + 1 :])
            return node

        self._root = rb1(list(elems))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        min_num = 10**32
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node1 = stack.pop()
                if item < node1.data <= min_num:
                    min_num = node1.data
                if node1.right:
                    stack.push(node1.right)
                if node1.left:
                    stack.push(node1.left)
        if min_num != 10**32:
            return min_num
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        max_num = -(10**32)
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node1 = stack.pop()
                if max_num <= node1.data < item:
                    max_num = node1.data
                if node1.left:
                    stack.push(node1.left)
                if node1.right:
                    stack.push(node1.right)
        if max_num != -(10**32):
            return max_num
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as file1:
            lines = file1.readlines()
        for idx in range(len(lines)):
            lines[idx] = lines[idx].strip("\n")

        random_words = random.sample(lines, 10000)
        # Number 1: sorted list
        start = time.time()
        for word in random_words:
            for pos in range(len(lines)):
                if lines[pos] == word:
                    break
        end = time.time()
        delta = end - start
        print(f"Result 1: {delta}")

        # Number 2: tree (recursion limit error)
        sys.setrecursionlimit(1000000)
        tree = LinkedBST()
        for pos in range(len(lines)):
            tree.add(lines[pos])
        start = time.time()
        for word in random_words:
            tree.find(word)
        end = time.time()
        delta = end - start
        print(f"Result 2: {delta}")

        # Number 3: shuffled list
        random.shuffle(lines)
        tree1 = LinkedBST()
        for pos in range(len(lines)):
            tree1.add(lines[pos])
        start = time.time()
        for word in random_words:
            tree1.find(word)
        end = time.time()
        delta = end - start
        print(f"Result 3: {delta}")

        # Number 4: balanced tree
        tree.rebalance()
        start = time.time()
        for word in random_words:
            tree.find(word)
        end = time.time()
        delta = end - start
        print(f"Result 4: {delta}")


tree = LinkedBST([5, 4, 6, 3, 8, 19])
tree.demo_bst("words.txt")
