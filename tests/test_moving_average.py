import sys

import gspread
import json
import pytest
from unittest import mock
from pytest_mock import mocker

from moving_average import (parse_args, open_spreadsheet, process_worksheet, WorksheetError,
                            calculate_moving_average, process_spreadsheet, get_result_cells_range)


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


def test_get_result_cells_range(worksheet, mocker):
    records = load_fixture('consistent_dates.json')

    get_result_cells_range(worksheet, records)
