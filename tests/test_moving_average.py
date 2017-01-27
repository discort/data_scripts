import sys

import pytest

from moving_average import parse_args, process_worksheet, WorksheetError


class TestCommandLine:
    @classmethod
    def setup_class(cls):
        """Remove args passed to pytest runner"""
        for arg in sys.argv:
            if arg.startswith('test'):
                sys.argv.remove(arg)

    def test_with_empty_args(self):
        with pytest.raises(SystemExit):
            parse_args()

    def test_with_sheet_id(self):
        sys.argv.append('spreadsheet_id')
        assert parse_args().sheet_id == 'spreadsheet_id'


class TestProcessWorksheet:
    def test_empty_sheet(self, empty_worksheet):
        with pytest.raises(WorksheetError) as ex:
            process_worksheet(empty_worksheet)
        assert 'empty worksheet' in ex.value.__str__().lower()

    def test_sheet_without_mandatory_columns(self, dummy_worksheet):
        with pytest.raises(WorksheetError) as ex:
            process_worksheet(dummy_worksheet)
        assert 'does not contain mandatory column' in ex.value.__str__().lower()

    def test_success_MA_calc_with_consistent_dates(self):
        pass

    def test_success_MA_calcu_with_inconsistent_dates(self):
        pass
