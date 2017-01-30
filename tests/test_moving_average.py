import json
import pytest
from pytest_mock import mocker

from moving_average import (parse_args, process_worksheet, WorksheetError,
                            calculate_moving_average, get_or_create_ma_cell)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def load_fixture(fixture_name):
    fixture_path = 'tests/fixtures/{}'.format(fixture_name)
    with open(fixture_path) as data_file:
        data = json.load(data_file)
    return data


def test_arg_parsing():
    args = parse_args(["valid_id_012345"])
    assert args.sheet_id == "valid_id_012345"

    with pytest.raises(SystemExit):
        parse_args([])


def test_empty_worksheet():
    with pytest.raises(WorksheetError) as ex:
        calculate_moving_average([], 'Sheet1')
    assert 'empty worksheet' in ex.value.__str__().lower()


def test_sheet_without_mandatory_columns():
    data = [{'test1': 666}, {'test2': 777}]
    with pytest.raises(WorksheetError) as ex:
        calculate_moving_average(data, 'Sheet1')
    assert 'does not contain mandatory column' in ex.value.__str__().lower()


ma_fixtures = [
    (load_fixture('consistent_dates.json'),
     load_fixture('consistent_dates_result.json')),
    (load_fixture('inconsistent_dates.json'),
     load_fixture('inconsistent_dates_result.json'))
]


@pytest.mark.parametrize("source_data, expected", ma_fixtures)
def test_moving_average(source_data, expected):
    result = calculate_moving_average(source_data, 'Sheet1')
    assert result == expected


def test_get_or_create_ma_cell(worksheet, mocker):
    records = load_fixture('consistent_dates.json')

    # Test if 'Moving Average' column does not exist
    mocker.patch.object(worksheet, 'update_cell')
    worksheet.update_cell.return_value = None
    get_or_create_ma_cell(worksheet, records)
    worksheet.update_cell.assert_called_with(1, 5, 'Moving Average')

    # Test if 'Moving Average' column does exists
    mocker.patch.object(worksheet, 'find')
    worksheet.find.return_value = Struct(row=2, col=5)
    get_or_create_ma_cell(worksheet, records)
    worksheet.find.assert_called_with('Moving Average')
