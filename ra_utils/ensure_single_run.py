# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import os
import typing


class LockTaken(Exception):
    """Raised by ensure single run, when the named lock is already taken, and the
    current run is aborted"""

    pass


def _is_lock_taken(lock_name: str) -> bool:
    """Test if the lock file exists, and if it does, if it is all whitespaces
    Args:
        lock_name: the name of the lock file to test

    Returns: a boolean representing whether the lock is taken

    """
    try:
        # This is a special case, this will only happen if the lock is already taken,
        # or something has crashed hard and the lock has been manually reset, wrong
        lock = open(lock_name, "r")
        lock_content = lock.read()
        lock.close()
        # if there is no content in the lock file, or the content is all
        # whitespaces the lock isn't taken
        locked: bool = not ((not lock_content) or lock_content.isspace())

        print(locked)
    except FileNotFoundError:
        # This is the normal case
        return False
    return locked


def ensure_single_run(
    func: typing.Callable,
    lock_name: str,
) -> typing.Any:
    """Wrapper function that ensures that no more than a single instance of a function
    is running at any given time. Checks if a lock for the function already exists, and
    is taken, or not. If a lock exists it raises a StopIteration exception. If no lock
    is taken creates a lock file, executes the function, removes the lock file, and
    returns the result of the function.

    The lock file contains the pid of the process which has taken it so that it is
    possible to see if the process is still running

    Args:
        func: Function to be wrapped, to ensure that it only runs once
        lock_name: Name of the lock file
        logger: Logger to be used for output

    Returns:
        return_value: the return value of the wrapped function

    """
    locked = _is_lock_taken(lock_name=lock_name)

    if not locked:
        with open(file=lock_name, mode="w") as lock:
            lock.write(f"pid={os.getpid()}")
            lock.flush()

        try:
            return_value = func()
        except Exception as e:
            raise e
        finally:
            os.remove(lock_name)
    else:
        raise LockTaken
    return return_value
