import pytest

from py_simple import read_csv_column
from py_simple_package.src.py_simple.easy_csv import (
    read_csv_column as easy_csv_read_column,
)


def write_sample_csv(path):
    path.write_text(
        "Name,Age,City\nAlice,24,London\nBob,31,Paris\nCarol,42,Tokyo\n",
        encoding="utf-8",
    )


class TestReadCsvColumn:
    def test_read_csv_column_values(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        result = read_csv_column(str(csv_file), "Name")
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_numeric_strings(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        result = read_csv_column(str(csv_file), "Age")
        assert result == ["24", "31", "42"]

    def test_read_csv_column_filepath_kwargs(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        result = read_csv_column(filepath=str(csv_file), column="City")
        assert result == ["London", "Paris", "Tokyo"]

    def test_read_csv_column_file_path_kwargs(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        result = read_csv_column(file_path=str(csv_file), column_name="City")
        assert result == ["London", "Paris", "Tokyo"]

    def test_read_csv_column_direct_module_import(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        result = easy_csv_read_column(str(csv_file), "Name")
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("item;qty\napple;5\nbanana;10\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "item", delimiter=";")
        assert result == ["apple", "banana"]

    def test_read_csv_column_header_only_file_returns_empty_list(self, tmp_path):
        csv_file = tmp_path / "empty_data.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "Name")
        assert result == []

    def test_read_csv_column_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            read_csv_column(str(missing_file), "Name")

    def test_read_csv_column_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            read_csv_column(str(empty_file), "Name")

    def test_read_csv_column_missing_column_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_sample_csv(csv_file)

        with pytest.raises(ValueError, match="Column not found"):
            read_csv_column(str(csv_file), "Nonexistent")

    def test_read_csv_column_missing_required_args_raises_type_error(self):
        with pytest.raises(TypeError):
            read_csv_column()

        with pytest.raises(TypeError):
            read_csv_column(filepath="people.csv")

    def test_read_csv_column_row_with_missing_field(self, tmp_path):
        csv_file = tmp_path / "jagged.csv"
        csv_file.write_text("Name,Age,Role\nAlice,24,Engineer\nBob\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "Role")
        assert result == ["Engineer", ""]
