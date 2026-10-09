"""
BrowserHistory Engine Implementation Using Two Stack ADTs.

This module encapsulates browser history management logic using two custom
Stack ADT instances (Back Stack and Forward Stack) alongside a current URL pointer.
It guarantees LIFO navigation semantics and strict encapsulation.
"""

from typing import List, Optional, Tuple
from urllib.parse import urlparse

from stack_adt import Stack


class InvalidURLError(ValueError):
    """Exception raised when an invalid or unsafe URL is supplied."""
    pass


def normalize_and_validate_url(raw_url: str) -> str:
    """
    Validate and normalize a user-provided URL.

    Rules:
    - Strips leading/trailing whitespace.
    - Automatically prepends 'https://' if no scheme is provided.
    - Restricts schemes strictly to 'http' and 'https' (blocks javascript:, file:, data:, etc.).
    - Requires a valid network location (hostname).

    Args:
        raw_url (str): The raw URL string provided by the user.

    Returns:
        str: The normalized, validated URL.

    Raises:
        InvalidURLError: If the URL is empty, contains unsafe schemes, or lacks a valid host.
    """
    if not raw_url or not raw_url.strip():
        raise InvalidURLError("URL cannot be empty.")

    clean_url = raw_url.strip()

    # Disallow dangerous schemes explicitly
    lower_raw = clean_url.lower()
    disallowed_schemes = ("javascript:", "data:", "file:", "vbscript:", "about:")
    if any(lower_raw.startswith(prefix) for prefix in disallowed_schemes):
        raise InvalidURLError("Unsafe URL scheme detected. Only HTTP and HTTPS protocols are permitted.")

    # Automatically add https:// if no scheme is present
    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    parsed = urlparse(clean_url)

    if parsed.scheme.lower() not in ("http", "https"):
        raise InvalidURLError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are supported.")

    if not parsed.netloc or "." not in parsed.netloc:
        # Check if it's localhost or an IP, or at least has a valid hostname
        if parsed.netloc.lower() not in ("localhost", "127.0.0.1") and "." not in parsed.netloc:
            raise InvalidURLError("Invalid domain name or hostname.")

    return clean_url


class BrowserHistory:
    """
    Browser History Manager backed by two Stack ADT instances.

    Architecture:
        - `_back_stack`: Stack containing URLs of previously visited pages.
        - `_forward_stack`: Stack containing URLs that can be revisited via forward navigation.
        - `_current_url`: Stores the URL of the active webpage.

    Time Complexity Guarantees:
        - `visit(url)`: O(1) - Pushing to back stack and resetting forward stack is O(1).
        - `back()`:      O(1) - Popping from back stack and pushing to forward stack is O(1).
        - `forward()`:   O(1) - Popping from forward stack and pushing to back stack is O(1).
        - `can_go_back()`: O(1) - Stack emptiness check is O(1).
        - `can_go_forward()`: O(1) - Stack emptiness check is O(1).
        - `get_current_url()`: O(1).
    """

    def __init__(self, initial_url: Optional[str] = None) -> None:
        """
        Initialize the browser history with two isolated Stack instances.

        Args:
            initial_url (Optional[str]): Optional starting URL to visit immediately.
        """
        self._back_stack: Stack[str] = Stack[str]()
        self._forward_stack: Stack[str] = Stack[str]()
        self._current_url: Optional[str] = None
        self._total_visits: int = 0
        self._last_action: str = "Initialized"

        if initial_url:
            self.visit(initial_url)

    def visit(self, url: str) -> str:
        """
        Navigate to a new URL.

        Semantics:
            1. If a current page is active, push it onto the Back Stack.
            2. Update the current page to the newly entered URL.
            3. Clear the Forward Stack (new history branch destroys forward lineage).
            4. Increment total visit counter.

        Args:
            url (str): The URL to navigate to (will be normalized and validated).

        Returns:
            str: The normalized current URL.

        Time Complexity: O(1)
        """
        normalized = normalize_and_validate_url(url)

        # If navigating to the exact same page, we can either re-visit or refresh.
        # Browser standard: if user explicitly enters a URL or navigates, current goes to back.
        if self._current_url is not None:
            self._back_stack.push(self._current_url)

        self._current_url = normalized
        self._forward_stack.clear()
        self._total_visits += 1
        self._last_action = f"Visited {normalized}"

        return self._current_url

    def back(self) -> Optional[str]:
        """
        Navigate to the previous page in history.

        Semantics:
            1. If the Back Stack is empty, navigation is a no-op; current page remains unchanged.
            2. If items exist, push the current page onto the Forward Stack.
            3. Pop the topmost URL from the Back Stack and assign it as the new current page.

        Returns:
            Optional[str]: The current URL after navigating back, or None if no page exists.

        Time Complexity: O(1)
        """
        if self._back_stack.is_empty():
            return self._current_url

        if self._current_url is not None:
            self._forward_stack.push(self._current_url)

        previous_url = self._back_stack.pop()
        self._current_url = previous_url
        self._last_action = f"Moved Back to {previous_url}"

        return self._current_url

    def forward(self) -> Optional[str]:
        """
        Navigate forward to the next page in history.

        Semantics:
            1. If the Forward Stack is empty, navigation is a no-op; current page remains unchanged.
            2. If items exist, push the current page onto the Back Stack.
            3. Pop the topmost URL from the Forward Stack and assign it as the new current page.

        Returns:
            Optional[str]: The current URL after navigating forward, or None if no page exists.

        Time Complexity: O(1)
        """
        if self._forward_stack.is_empty():
            return self._current_url

        if self._current_url is not None:
            self._back_stack.push(self._current_url)

        next_url = self._forward_stack.pop()
        self._current_url = next_url
        self._last_action = f"Moved Forward to {next_url}"

        return self._current_url

    def can_go_back(self) -> bool:
        """
        Check if backwards navigation is available.

        Returns:
            bool: True if the Back Stack is non-empty, False otherwise.

        Time Complexity: O(1)
        """
        return not self._back_stack.is_empty()

    def can_go_forward(self) -> bool:
        """
        Check if forward navigation is available.

        Returns:
            bool: True if the Forward Stack is non-empty, False otherwise.

        Time Complexity: O(1)
        """
        return not self._forward_stack.is_empty()

    def get_current_url(self) -> Optional[str]:
        """
        Retrieve the current active URL.

        Returns:
            Optional[str]: The current URL string, or None if no page has been visited.

        Time Complexity: O(1)
        """
        return self._current_url

    def get_back_stack_snapshot(self) -> List[str]:
        """
        Retrieve an immutable snapshot of URLs in the Back Stack.

        The snapshot returns items in top-to-bottom order (index 0 is the top,
        which will be popped next).

        Returns:
            List[str]: List of URLs currently in the Back Stack, top first.

        Time Complexity: O(n) where n is the number of elements in the Back Stack.
        """
        items = self._back_stack.snapshot()
        # Invert so index 0 is top (next to be popped)
        return list(reversed(items))

    def get_forward_stack_snapshot(self) -> List[str]:
        """
        Retrieve an immutable snapshot of URLs in the Forward Stack.

        The snapshot returns items in top-to-bottom order (index 0 is the top,
        which will be popped next).

        Returns:
            List[str]: List of URLs currently in the Forward Stack, top first.

        Time Complexity: O(m) where m is the number of elements in the Forward Stack.
        """
        items = self._forward_stack.snapshot()
        # Invert so index 0 is top (next to be popped)
        return list(reversed(items))

    def get_back_count(self) -> int:
        """
        Get the number of pages stored in the Back Stack.

        Time Complexity: O(1)
        """
        return self._back_stack.size()

    def get_forward_count(self) -> int:
        """
        Get the number of pages stored in the Forward Stack.

        Time Complexity: O(1)
        """
        return self._forward_stack.size()

    def get_total_visits(self) -> int:
        """
        Get the cumulative number of unique visits performed in this session.

        Time Complexity: O(1)
        """
        return self._total_visits

    def get_last_action(self) -> str:
        """
        Get the human-readable description of the last navigation action.

        Time Complexity: O(1)
        """
        return self._last_action
