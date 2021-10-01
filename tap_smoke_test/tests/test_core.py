"""Tests standard tap features using the built-in SDK tests library."""

from os import path
from singer_sdk.testing import get_standard_tap_tests

from tap_smoke_test.tap import TapSmokeTest

FIXTURE_DIR = path.join(
    path.dirname(path.realpath(__file__)),
    "../../demo-data",
)

BASIC_CONFIG = {
    "streams": [
        {
            "stream_name": "test",
            "input_filename": path.join(FIXTURE_DIR, "pageviews-data.jsonl"),
        }
    ]
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapSmokeTest, config=BASIC_CONFIG)
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
