# csv-value-counter
TEST EDIT

[![CI](https://github.com/ahortian/csv-value-counter/actions/workflows/ci.yml/badge.svg)](https://github.com/ahortian/csv-value-counter/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/csv-value-counter.svg)](https://pypi.org/project/csv-value-counter/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Count occurrences of values in any column of a CSV file — as a Python library or a
command-line tool. No dependencies beyond the Python standard library.

```
$ csv-value-counter mock_data/members.csv --column gender --values Male,Female
Male   : 454
Female : 445
```

## Features

- Works with any CSV that has a header row — just point it at a column name.
- Use it as an importable Python function, or as a standalone CLI.
- Optionally restrict/order the output to specific values (e.g. `Male,Female`)
  instead of every distinct value found.
- Plain-text or JSON output from the CLI.
- Zero third-party dependencies.

## Installation

Once published to PyPI:

```bash
pip install csv-value-counter
```

Until then (or to track the latest commit), install directly from GitHub:

```bash
pip install git+https://github.com/ahortian/csv-value-counter.git
```

## Quick start

### As a library

```python
from csv_value_counter import count_values

# Count every distinct value found in the "gender" column
counts = count_values("mock_data/members.csv", column="gender")
print(counts)
# {'Female': 445, 'Male': 454, 'Genderqueer': 16, 'Polygender': 13,
#  'Agender': 19, 'Genderfluid': 13, 'Non-binary': 20, 'Bigender': 20}

# Or restrict to specific values, in a specific order
counts = count_values(
    "mock_data/members.csv",
    column="gender",
    values=["Male", "Female"],
)
print(counts)
# {'Male': 454, 'Female': 445}
```

### As a CLI

```bash
# Count every distinct value in a column
csv-value-counter mock_data/members.csv --column gender

# Restrict/order the values shown
csv-value-counter mock_data/members.csv --column gender --values Male,Female

# JSON output, useful for piping into other tools (e.g. jq)
csv-value-counter mock_data/members.csv --column gender --json
```

## API reference

### `count_values(csv_path, column, values=None, encoding="utf-8")`

Counts occurrences of each value in a column of a CSV file.

| Parameter  | Type                          | Description                                                                                                                   |
|------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `csv_path` | `str \| pathlib.Path`         | Path to the CSV file. Must have a header row.                                                                                  |
| `column`   | `str`                         | Name of the column (header) to count values from.                                                                              |
| `values`   | `Iterable[str] \| None`       | Optional list of specific values to count, and the order to return them in. Values not seen in the file are still returned with a count of 0. If omitted, every distinct value found is counted, in first-seen order. |
| `encoding` | `str`                         | Text encoding used to open the file. Defaults to `"utf-8"`.                                                                    |

**Returns:** `dict[str, int]` mapping each value to its count.

**Raises:**
- `FileNotFoundError` — if `csv_path` does not exist.
- `csv_value_counter.ColumnNotFoundError` — if the CSV header does not contain `column`. The error message lists the columns that *are* available.

### CLI flags

| Flag              | Description                                                                 |
|-------------------|------------------------------------------------------------------------------|
| `csv_path`        | (positional) Path to the CSV file to read.                                  |
| `-c`, `--column`  | (required) Name of the column to count values from.                         |
| `-v`, `--values`  | Comma-separated list of values to count and their display order, e.g. `Male,Female`. |
| `-e`, `--encoding`| File encoding. Defaults to `utf-8`.                                          |
| `--json`          | Output as JSON instead of plain text.                                       |

Run `csv-value-counter --help` for the same reference at any time.

## Example dataset

`mock_data/members.csv` is a small sample dataset included in this repo for trying
the tool out. It has an `id, first_name, last_name, email, gender, ip_address`
header. See `examples/example_usage.py` for a runnable script that uses it.

## Development

```bash
git clone https://github.com/ahortian/csv-value-counter.git
cd csv-value-counter
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -v
```

The package uses a `src/` layout (`src/csv_value_counter/`):
- `counter.py` — core logic (`count_values`, `ColumnNotFoundError`)
- `cli.py` — argparse-based command-line wrapper around `counter.py`

## Releasing

1. Bump `version` in `pyproject.toml` and `__version__` in `src/csv_value_counter/__init__.py`.
2. On [PyPI](https://pypi.org), configure a **Trusted Publisher** for this project
   pointing at the `ahortian/csv-value-counter` repo and the `publish.yml` workflow
   (PyPI project settings → Publishing). This lets GitHub Actions publish without
   storing an API token.
3. Push a GitHub Release (tag it, e.g. `v0.1.0`) — `.github/workflows/publish.yml`
   builds the package and publishes it to PyPI automatically.

## License

[MIT](LICENSE) © Apichart Hortiangtham
