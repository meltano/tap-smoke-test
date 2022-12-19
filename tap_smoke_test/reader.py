"""Core code for handling input readers."""

from __future__ import annotations

import logging
from typing import Generator

import requests


def trim_prefix(string: str, prefix: str) -> str:
    """Trim a given prefix from a string if present.

    Args:
        string: The string to trim.
        prefix: The prefix to trim.

    Returns:
        The string with the prefix trimmed.
    """
    if string.startswith(prefix):
        return string[len(prefix) :]
    else:
        return string[:]


class InputReader:
    """Generic class with a read() call yielding lines."""

    def __init__(self, input_filename: str) -> None:
        """Initialize an InputReader.

        Args:
            input_filename: The path to the file to read.
        """
        self.input_filename = input_filename

    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line."""
        ...


class LocalReader(InputReader):
    """An InputReader supporting reading files from local paths."""

    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line.

        Yields:
            Each line in the input file.
        """
        logging.debug("reading local file: %s" % self.input_filename)
        with open(trim_prefix(self.input_filename, "file://")) as f:
            yield from f


class HTTPReader(InputReader):
    """An InputReader supporting reading files from remote HTTP(s) urls."""

    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line.

        Yields:
            Each line in the input file.

        Raises:
            Exception: If the fetch of the remote file fails.
        """
        logging.debug("reading remote file: %s" % self.input_filename)
        r = requests.get(self.input_filename)
        if r.ok:
            yield from r.iter_lines()
        else:
            raise Exception(
                f"Fetch of remote payload failed. status: [{r.status_code}], "
                f"reason: [{r.reason}]"
            )
