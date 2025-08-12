# tap-smoke-test

`tap-smoke-test` is a Singer tap for SmokeTest.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
uv tool install git+https://github.com/meltano/tap-smoke-test.git
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-smoke-test --about
```

The minimal config requires declaring an array of streams, each stream must define a `stream_name`, and `input_filename`
the path to an jsonl formatted file of mock data you would like to use. `input_filename` can be either the path to a local
file, or the URL of a HTTP(s) accessible file. Note that schemas are inferred on the fly - so no schema definitions need
to be provided.

```
{
  "streams": [
    {
      "stream_name":  "animals",
      "input_filename": "https://gitlab.com/meltano/tap-smoke-test/-/raw/main/demo-data/animals-data.jsonl"
    },
    {
      "stream_name":  "pageviews",
      "input_filename": "demo-data/pageviews-data.jsonl"
    }
  ]
}
```

While the tap isn't necessarily designed to ingest large amounts of mock data - you can iterate over and output the provided mock data
multiple times using the `loop_count` option to produce large amounts of output:

```
{
  "streams": [
    {
      "stream_name":  "animals",
      "input_filename": "demo-data/animals-data.json",
      "loop_count": 3
    },
    {
      "stream_name":  "pageviews",
      "input_filename": "demo-data/pageviews-data.json"
    }
  ]
}
```

In the example above, the animals-data.json records will be read and emitted as records 3 times.

```yml
# meltano.yml
  - name: tap-smoke-test
    variant: meltano
    pip_url: git+https://github.com/meltano/tap-smoke-test.git
    config:
      streams:
      - stream_name: "animals"
        input_filename: "https://gitlab.com/meltano/tap-smoke-test/-/raw/main/demo-data/animals-data.jsonl"
```

### Schema inference

This tap uses [genson](https://pypi.org/project/genson/) to attempt to dynamically infer the schema of the JSON input
files provided. To allow for detection of things like nullable fields, multiple records are inspected.
How many are inspected is controlled via the config option `"schema_inference_record_count"`:

```
{
  "schema_inference_record_count": 5,
  "streams": [
    {
      "stream_name":  "pageviews",
      "input_filename": "pageviews-data.json"
    }
  ]
}
```

### Bad actor options

Each configured stream can also be configured to misbehave. Right now this is limited to two scenarios where Exceptions
are triggered during invocation.

- `"client_exception": true` - will trigger an exception in `SmokeTestStream.get_records` once all records have been returned.
- `"schema_gen_exception": true` - will trigger an exception the first time schema inference is run.

```
{
  "schema_inference_record_count": 5,
  "streams": [
    {
      "stream_name":  "pageviews",
      "input_filename": "pageviews-data.json"
      "client_exception": true,
      "schema_gen_exception": true,
    }
  ]
}
```

Note: creative use of the schema_inference_record_count setting, also allows for simulating unexpected schema change's in records.

## Usage

You can easily run `tap-smoke-test` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Included example data sets

This tap currently ships with 2 example data sets:

- pageviews-data.jsonl - containing mock pageview like records
- animals-data.jsonl - containing a mock animal index with nulls

### Random record generation

In the future we'll likely support optional generation of random records, on the fly, at invocation time, using a library like [https://github.com/joke2k/faker](https://github.com/joke2k/faker).

### Executing the Tap Directly

```bash
tap-smoke-test --version
tap-smoke-test --help
tap-smoke-test --config demo-data/multiple-streams-config.json --discover
tap-smoke-test --config demo-data/multiple-streams-config.json
````

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # or see https://docs.astral.sh/uv/getting-started/installation/
uv sync
```

### Create and Run Tests

Create tests within the `tap_smoke_test/tests` subfolder and
  then run:

```bash
uv run pytest
```

You can also test the `tap-smoke-test` CLI interface directly using `uv run`:

```bash
uv run tap-smoke-test --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
uv tool install meltano
# Initialize meltano within this directory
cd tap-smoke-test
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-smoke-test --version
# OR run a test EL pipeline:
meltano run tap-smoke-test target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
