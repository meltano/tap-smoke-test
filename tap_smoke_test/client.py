"""Custom client handling, including SmokeTestStream base class."""
import json
import logging

from typing import Optional, Iterable

from singer_sdk.streams import Stream


class SmokeTestStream(Stream):
    """Stream class for SmokeTest streams."""

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.
        """
        lcount = 0
        while lcount < self.stream_config["loop_count"]:
            lcount += 1
            logging.debug("%s starting loop: %d" % (self.name, lcount))
            with open(self.stream_config["input_filename"], mode="r") as f:
                for entry in f:
                    yield json.loads(entry)

        if self.config.get("client_exception", False):
            logging.warning("raising smoke test client exception")
            raise Exception("Smoke test client failing with exception")
