"""Custom client handling, including SmokeTestStream base class."""
import json
import logging

from typing import Optional, Iterable, Generator
from urllib.parse import urlparse

import requests
from singer_sdk.streams import Stream

from tap_smoke_test.reader import LocalReader, HTTPReader


class SmokeTestStream(Stream):
    """Stream class for SmokeTest streams."""

    @property
    def reader(self) -> "InputReader":
        """Obtain an InputReader (either local or remote) based on input_filename's url scheme"""
        path = urlparse(self.stream_config["input_filename"])
        if path.scheme in ["file", ""]:
            return LocalReader(self.stream_config["input_filename"])
        elif path.scheme in ["http", "https"]:
            return HTTPReader(self.stream_config["input_filename"])
        else:
            raise Exception(f"Unsupported scheme [{path.scheme}] for input_filename.")

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.
        """

        i = 0
        while i < self.stream_config["loop_count"]:
            i += 1
            logging.debug("%s starting loop: %d" % (self.name, i))
            for entry in self.reader.read():
                yield json.loads(entry)

        if self.stream_config.get("client_exception", False):
            logging.warning("raising smoke test client exception")
            raise Exception("Smoke test client failing with exception")
