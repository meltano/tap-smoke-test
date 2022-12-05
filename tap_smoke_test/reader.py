"""core code for handling input readers."""
import logging
from typing import Generator

import requests


def trim_prefix(self: str, prefix: str) -> str:
    """Trim a given prefix from a string if present."""
    if self.startswith(prefix):
        return self[len(prefix) :]
    else:
        return self[:]


class InputReader:
    """Generic class with a read() call yielding lines from the provided input_filename."""

    def __init__(self, input_filename: str):
        self.input_filename = input_filename

    def read(self) -> Generator[str, None, None]:
        pass


class LocalReader(InputReader):
    """An InputReader supporting reading files from local paths."""

    def read(self) -> Generator[str, None, None]:
        logging.debug("reading local file: %s" % self.input_filename)
        with open(trim_prefix(self.input_filename, "file://"), mode="r") as f:
            for entry in f:
                yield entry


class HTTPReader(InputReader):
    """An InputReader supporting reading files from remote HTTP(s) urls."""

    def read(self) -> Generator[str, None, None]:
        logging.debug("reading remote file: %s" % self.input_filename)
        r = requests.get(self.input_filename)
        if r.ok:
            for entry in r.iter_lines():
                yield entry
        else:
            raise Exception(
                f"Fetch of remote payload failed. status: [{r.status_code}], "
                f"reason: [{r.reason}]"
            )
