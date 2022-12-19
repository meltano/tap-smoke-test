"""Custom client handling, including SmokeTestStream base class."""

from __future__ import annotations

import json
import logging
from typing import Iterable
from urllib.parse import urlparse

from singer_sdk.streams import Stream

from tap_smoke_test.reader import HTTPReader, InputReader, LocalReader


class SmokeTestStream(Stream):
    """Stream class for SmokeTest streams."""

    @property
    def stream_config(self) -> dict:
        """Return the config for this particular stream name instance.

        Returns:
            The stream config for this stream name.
        """
        for conf in self.config["streams"]:
            if conf["stream_name"] == self.name:
                return conf

        return {}

    @property
    def reader(self) -> InputReader:
        """Obtain an InputReader on input_filename's url scheme.

        Can be a local or remote file, or a web url.

        Returns:
            InputReader: An InputReader instance for the input_filename.

        Raises:
            Exception: If the input_filename's url scheme is not supported.
        """
        path = urlparse(self.stream_config["input_filename"])
        if path.scheme in ["file", ""]:
            return LocalReader(self.stream_config["input_filename"])
        elif path.scheme in ["http", "https"]:
            return HTTPReader(self.stream_config["input_filename"])
        else:
            raise Exception(f"Unsupported scheme [{path.scheme}] for input_filename.")

    def get_records(self, context: dict | None) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        Args:
            context: Used to identify a specific slice of the stream if partitioning is
                required for the stream. Most implementations do not require
                partitioning and should ignore the `context` argument.

        Raises:
            Exception: If the client_exception config is set to True.

        Yields:
            Each row in the stream as a dictionary.
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
