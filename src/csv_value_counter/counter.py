"""Core logic for counting values in a CSV column."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable, Union


class ColumnNotFoundError(ValueError):
    """Raised when the requested column does not exist in the CSV header."""


def count_values(
    csv_path: Union[str, Path],
    column: str,
    values: Iterable[str] | None = None,
    encoding: str = "utf-8",
) -> dict[str, int]:
    """Count occurrences of each value in a column of a CSV file.

    Args:
        csv_path: Path to the CSV file. Must have a header row.
        column: Name of the column (header) to count values from.
        values: Optional iterable of specific values to count, and the order
            to return them in (e.g. ``["Male", "Female"]``). Values not seen
            in the file are still included in the result with a count of 0.
            If omitted, every distinct value found in the column is counted,
            in the order first encountered.
        encoding: Text encoding used to open the file. Defaults to "utf-8".

    Returns:
        A dict mapping each value to how many times it appeared.

    Raises:
        FileNotFoundError: If csv_path does not exist.
        ColumnNotFoundError: If the CSV header does not contain `column`.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    counts: Counter[str] = Counter()

    with path.open(newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or column not in reader.fieldnames:
            available = reader.fieldnames or []
            raise ColumnNotFoundError(
                f"Column '{column}' not found in CSV header. "
                f"Available columns: {', '.join(available)}"
            )

        wanted = set(values) if values is not None else None
        for row in reader:
            value = row[column]
            if wanted is None or value in wanted:
                counts[value] += 1

    if values is not None:
        return {v: counts.get(v, 0) for v in values}
    return dict(counts)
