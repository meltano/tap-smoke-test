"""Tests standard tap features using the built-in SDK tests library."""
from __future__ import annotations

import re
from os import path
from unittest import mock

import pytest
from singer_sdk.testing import get_tap_test_class

from tap_smoke_test.tap import TapSmokeTest

FIXTURE_DIR = path.join(
    path.dirname(path.realpath(__file__)),
    "../demo-data",
)

BASIC_CONFIG = {
    "streams": [
        {
            "stream_name": "test",
            "input_filename": path.join(FIXTURE_DIR, "pageviews-data.jsonl"),
        }
    ]
}


TestTapSmokeTest = get_tap_test_class(TapSmokeTest, config=BASIC_CONFIG)


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

    with pytest.raises(Exception, match="Smoke test schema call failing with exception"):
        TapSmokeTest(config=config, parse_env_config=False)


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
    with pytest.raises(Exception, match="Smoke test client failing with exception"):
        tap.sync_all()


@mock.patch("requests.get")
class TestRemote:
    def _mock_response(self, status=200, content="CONTENT", raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.ok = status == 200
        mock_resp.reason = content
        mock_resp.content = content

        def _mock_iter_lines():
            yield from content.splitlines()

        mock_resp.iter_lines = _mock_iter_lines
        return mock_resp

    def test_remote_file(self, mock_get):
        config = {
            "streams": [
                {
                    "stream_name": "test",
                    "input_filename": "https://dev.local/test/file.jsonl",
                    "client_exception": False,
                }
            ]
        }

        mock_resp = self._mock_response(
            content='{"id":1,"description":"Red-headed woodpecker","verified":true,'
            '"views":27,"created_at":"2021-09-22T01:01:05Z"}'
        )
        mock_get.return_value = mock_resp

        tap = TapSmokeTest(config=config, parse_env_config=False)
        tap.run_discovery()
        tap.sync_all()

    def test_remote_file_non_2xx(self, mock_get):
        config = {
            "streams": [
                {
                    "stream_name": "test",
                    "input_filename": "https://dev.local/test/file.jsonl",
                    "client_exception": False,
                }
            ]
        }

        mock_resp = self._mock_response(content="Not found", status=404)
        mock_get.return_value = mock_resp

        pattern = re.escape("Fetch of remote payload failed. status: [404], reason: [Not found]")
        with pytest.raises(Exception, match=pattern):
            _ = TapSmokeTest(config=config, parse_env_config=False)
