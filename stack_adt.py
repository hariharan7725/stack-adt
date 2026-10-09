"""
Stack Abstract Data Type (ADT) Implementation.

This module provides a pure Python implementation of the Stack ADT
based on the Last-In, First-Out (LIFO) principle. Encapsulation is enforced
using a private internal list container.
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class EmptyStackError(Exception):
    """Exception raised when an operation is performed on an empty stack."""
    pass


class Stack(Generic[T]):
    """
    A custom implementation of the Stack Abstract Data Type (ADT).

    Follows the LIFO (Last-In, First-Out) principle.
    Encapsulation is strictly enforced by storing items in a private list attribute (_items).

    Time Complexities:
        - push:     O(1) amortized
        - pop:      O(1)
        - peek:     O(1)
        - is_empty: O(1)
        - size:     O(1)
        - clear:    O(1)
    """

    def __init__(self) -> None:
        """
        Initialize an empty stack with a private underlying storage container.

        Time Complexity: O(1)
        """
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """
        Push an item onto the top of the stack.

        Args:
            item (T): The element to push onto the stack.

        Time Complexity: O(1) amortized (Python dynamic array append)
        """
        self._items.append(item)

    def pop(self) -> T:
        """
        Remove and return the item at the top of the stack.

        Returns:
            T: The item removed from the top of the stack.

        Raises:
            EmptyStackError: If the stack is empty when pop is called.

        Time Complexity: O(1) (removing from the end of a dynamic array)
        """
        if self.is_empty():
            raise EmptyStackError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        """
        Return the item at the top of the stack without removing it.

        Returns:
            Optional[T]: The top item, or None if the stack is empty.

        Time Complexity: O(1) (indexed lookup at the end)
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Check whether the stack contains any items.

        Returns:
            bool: True if the stack has no items, False otherwise.

        Time Complexity: O(1)
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the total number of items currently in the stack.

        Returns:
            int: The item count.

        Time Complexity: O(1)
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Remove all items from the stack by resetting the internal container.

        Time Complexity: O(1)
        """
        self._items = []

    def snapshot(self) -> List[T]:
        """
        Return an immutable snapshot copy of stack elements in bottom-to-top order.

        This allows callers to inspect stack contents without exposing
        the internal mutable storage directly.

        Returns:
            List[T]: A shallow copy of items in the stack.

        Time Complexity: O(n) where n is the number of elements
        """
        return list(self._items)

    def __repr__(self) -> str:
        """
        Developer-friendly representation of the stack state.
        """
        return f"Stack(size={self.size()}, top={self.peek()})"
