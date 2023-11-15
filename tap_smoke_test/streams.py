"""Stream type classes for tap-smoke-test."""

from __future__ import annotations

import json
import logging

from genson import SchemaBuilder

from tap_smoke_test.client import SmokeTestStream


class FromJSONLStream(SmokeTestStream):
    """Stream class that can infer a schema dynamically from a JSONL file of records."""

    _inferred_schema = None

    @property
    def schema(self) -> dict:
        """Dynamically infer the json schema from the source data.

        This is only performed once - and reused there after to cut down on IO.

        Returns:
            The schema for this stream.

        Raises:
            Exception: If the schema_gen_exception config is set to True.
        """
        if self._inferred_schema:
            logging.debug("%s stream retrieved inferred schema from cache" % self.name)
            return self._inferred_schema

        logging.debug("%s stream running schema inference" % self.name)
        if self.stream_config.get("schema_gen_exception", False):
            logging.warning("raising smoke test schema exception")
            raise Exception("Smoke test schema call failing with exception")

        builder = SchemaBuilder()
        for count, entry in enumerate(self.reader.read()):
            if count > self.config["schema_inference_record_count"]:
                logging.info("%s stream max schema_inference_record_count hit" % self.name)
                break
            record = json.loads(entry)
            builder.add_object(record)

        self._inferred_schema = builder.to_schema()
        return self._inferred_schema
