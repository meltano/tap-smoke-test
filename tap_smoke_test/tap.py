"""SmokeTest tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_smoke_test.streams import FromJSONLStream


class TapSmokeTest(Tap):
    """SmokeTest tap class."""

    name = "tap-smoke-test"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "schema_inference_record_count",
            th.IntegerType,
            default=5,
            required=False,
            description="How many records of the source data should be used for schema inference/construction.",
        ),
        th.Property(
            "streams",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "stream_name",
                        th.StringType,
                        required=True,
                    ),
                    th.Property(
                        "input_filename",
                        th.StringType,
                        required=True,
                        description="Path to a jsonl file containingrecords to use for mock data.",
                    ),
                    th.Property(
                        "client_exception",
                        th.BooleanType,
                        required=False,
                        default=False,
                        description=("Whether we should simulate failing by having the client raise an exception."),
                    ),
                    th.Property(
                        "schema_gen_exception",
                        th.BooleanType,
                        required=False,
                        default=False,
                        description="Whether we should simulate failing by "
                        "raising an exception during schema inference.",
                    ),
                    th.Property(
                        "loop_count",
                        th.IntegerType,
                        required=False,
                        default=1,
                        description=("The number of times we should playback the input file."),
                    ),
                )
            ),
            required=True,
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Stream instances.
        """
        streams = []
        for s in self.config["streams"]:
            stream = FromJSONLStream(tap=self, name=s["stream_name"])
            streams.append(stream)

        return streams
