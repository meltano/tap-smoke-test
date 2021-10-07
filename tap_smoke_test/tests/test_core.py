"""Tests standard tap features using the built-in SDK tests library."""

import pytest
from os import path
from singer_sdk.testing import get_standard_tap_tests, Tap

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

def test_schema_gen_exception():
    config = {
        "streams": [
            {
                "stream_name": "test",
                "input_filename": path.join(FIXTURE_DIR, "pageviews-data.jsonl"),
                "schema_gen_exception": True,
            }
        ]
    }

    with pytest.raises(Exception, match='Smoke test schema call failing with exception'):
        tap = TapSmokeTest(config=config, parse_env_config=False)


def test_client_exception():
    config = {
        "streams": [
            {
                "stream_name": "test",
                "input_filename": path.join(FIXTURE_DIR, "pageviews-data.jsonl"),
                "client_exception": True,
            }
        ]
    }

    tap = TapSmokeTest(config=config, parse_env_config=False)
    tap.run_discovery()
    with pytest.raises(Exception, match='Smoke test client failing with exception'):
       tap.sync_all()
