"""Example: count Male/Female members from mock_data/members.csv."""

from csv_value_counter import count_values

if __name__ == "__main__":
    counts = count_values("mock_data/members.csv", column="gender", values=["Male", "Female"])
    for gender, count in counts.items():
        print(f"{gender}: {count}")
