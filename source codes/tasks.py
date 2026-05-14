"""
tasks.py  --  Business logic for the To-Do List CLI.


This module contains all operations that manipulate task lists.
It works purely with Python lists -- no file I/O, no printing.


Design rule: every function receives the current task list as input
and returns a (new_list, message) tuple. It never mutates in-place.

The message is an empty string on success, or an error string on failure.
"""

