"""Command-line interface for csv_value_counter."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .counter import ColumnNotFoundError, count_values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-value-counter",
        description="Count occurrences of values in a column of a CSV file.",
    )
    parser.add_argument("csv_path", help="Path to the CSV file to read.")
    parser.add_argument(
        "-c", "--column", required=True, help="Name of the column to count values from."
    )
    parser.add_argument(
        "-v",
        "--values",
        help=(
            "Comma-separated list of specific values to count, and the order to "
            "display them in (e.g. 'Male,Female'). If omitted, all distinct "
            "values found in the column are counted."
        ),
    )
    parser.add_argument(
        "-e", "--encoding", default="utf-8", help="File encoding (default: utf-8)."
    )
    parser.add_argument(
        "--json", action="store_true", help="Output the result as JSON instead of plain text."
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    values = args.values.split(",") if args.values else None

    try:
        counts = count_values(args.csv_path, args.column, values=values, encoding=args.encoding)
    except (FileNotFoundError, ColumnNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(counts, indent=2))
    else:
        width = max((len(key) for key in counts), default=0)
        for key, count in counts.items():
            print(f"{key.ljust(width)} : {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
