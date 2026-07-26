import json
import subprocess
import sys
from pathlib import Path

import pytest

from csv_value_counter import ColumnNotFoundError, count_values

SAMPLE_CSV = """id,name,gender
1,Alice,Female
2,Bob,Male
3,Carol,Female
4,Dave,Male
5,Eve,Male
"""


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(SAMPLE_CSV, encoding="utf-8")
    return csv_path


def test_counts_all_distinct_values(sample_csv: Path) -> None:
    assert count_values(sample_csv, "gender") == {"Female": 2, "Male": 3}


def test_counts_only_requested_values_in_order(sample_csv: Path) -> None:
    assert count_values(sample_csv, "gender", values=["Male", "Female"]) == {
        "Male": 3,
        "Female": 2,
    }


def test_missing_value_defaults_to_zero(sample_csv: Path) -> None:
    result = count_values(sample_csv, "gender", values=["Male", "Nonbinary"])
    assert result == {"Male": 3, "Nonbinary": 0}


def test_unknown_column_raises(sample_csv: Path) -> None:
    with pytest.raises(ColumnNotFoundError):
        count_values(sample_csv, "not_a_column")


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        count_values(tmp_path / "missing.csv", "gender")


def test_cli_text_output(sample_csv: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "csv_value_counter.cli", str(sample_csv), "-c", "gender"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Female" in result.stdout
    assert "Male" in result.stdout


def test_cli_json_output(sample_csv: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "csv_value_counter.cli",
            str(sample_csv),
            "-c",
            "gender",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    assert data == {"Female": 2, "Male": 3}
