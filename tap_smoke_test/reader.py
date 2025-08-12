"""Core code for handling input readers."""

from __future__ import annotations

import abc
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)


def trim_prefix(string: str, prefix: str) -> str:
    """Trim a given prefix from a string if present.

    Args:
        string: The string to trim.
        prefix: The prefix to trim.

    Returns:
        The string with the prefix trimmed.
    """
    return string[len(prefix) :] if string.startswith(prefix) else string[:]


class InputReader(abc.ABC):
    """Generic class with a read() call yielding lines."""

    def __init__(self, input_filename: str) -> None:
        """Initialize an InputReader.

        Args:
            input_filename: The path to the file to read.
        """
        self.input_filename = input_filename

    @abc.abstractmethod
    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line."""


class LocalReader(InputReader):
    """An InputReader supporting reading files from local paths."""

    @override
    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line.

        Yields:
            Each line in the input file.
        """
        logger.debug("reading local file: %s", self.input_filename)
        with Path(self.input_filename.removeprefix("file://")).open() as f:
            yield from f


class HTTPReader(InputReader):
    """An InputReader supporting reading files from remote HTTP(s) urls."""

    @override
    def read(self) -> Generator[str, None, None]:
        """Read the input file and yield each line.

        Yields:
            Each line in the input file.

        Raises:
            Exception: If the fetch of the remote file fails.
        """
        logger.debug("reading remote file: %s", self.input_filename)
        r = requests.get(self.input_filename)
        if r.ok:
            yield from r.iter_lines()
        else:
            raise Exception(f"Fetch of remote payload failed. status: [{r.status_code}], reason: [{r.reason}]")
