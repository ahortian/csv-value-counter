# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

`csv-value-counter` is a small, dependency-free Python package (published as `csv-value-counter`
on PyPI, repo `ahortian/csv-value-counter`) that counts occurrences of values in a column of a
CSV file. It's usable both as an importable library and as a CLI.

## Commands

```bash
# Set up (uses the venv_agent virtualenv, or create your own with python -m venv .venv)
source venv_agent/bin/activate
pip install -e ".[dev]"

# Run the full test suite
pytest -v

# Run a single test
pytest tests/test_counter.py::test_counts_all_distinct_values -v

# Run the CLI against the bundled example dataset
csv-value-counter mock_data/members.csv --column gender

# Build distributable artifacts (sdist + wheel)
pip install build && python -m build
```

## Architecture

Package uses a `src/` layout: `src/csv_value_counter/`
- `counter.py` — all core logic lives here: `count_values()` reads a CSV via
  `csv.DictReader` and tallies a given column with `collections.Counter`. Raises
  `ColumnNotFoundError` (subclass of `ValueError`) if the requested column isn't in the
  header, and `FileNotFoundError` if the path doesn't exist.
- `cli.py` — thin argparse wrapper around `counter.count_values()`; the only place
  argument parsing and JSON/text output formatting happen. Entry point registered in
  `pyproject.toml` as `csv-value-counter = "csv_value_counter.cli:main"`.
- `__init__.py` — public API surface: re-exports `count_values` and `ColumnNotFoundError`.

Tests (`tests/test_counter.py`) cover both the library function directly and the CLI via
`subprocess`, using a small in-memory CSV fixture rather than `mock_data/members.csv`.

`mock_data/members.csv` is sample/demo data for the README and `examples/example_usage.py`,
not used by the test suite.

## Release process

Version is declared in two places that must be bumped together: `pyproject.toml`
(`[project].version`) and `src/csv_value_counter/__init__.py` (`__version__`). Publishing to
PyPI happens via `.github/workflows/publish.yml`, triggered by creating a GitHub Release, using
PyPI Trusted Publishing (OIDC) rather than a stored API token — see README.md "Releasing" for
the one-time setup required on PyPI's side.
