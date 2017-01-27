import sys

import pytest

from moving_average import parse_options, process_worksheet, WorksheetError


class TestCommandLine:
    @classmethod
    def setup_class(cls):
        """Remove args passed to pytest runner"""
        for arg in sys.argv:
            if arg.startswith('test'):
                sys.argv.remove(arg)

    def test_with_empty_args(self):
        with pytest.raises(SystemExit):
            parse_options()

    def test_with_sheet_id(self):
        sys.argv.append('spreadsheet_id')
        assert parse_options().sheet_id == 'spreadsheet_id'


class TestProcessWorksheet:
    def test_empty_sheet(self, empty_worksheet):
        with pytest.raises(WorksheetError):
            process_worksheet(empty_worksheet)

    def test_sheet_without_mandatory_columns(self):
        pass

    def test_success_visitors_calculation_with_existing_average_column(self):
        pass

    def test_success_visitors_calculation_with_missing_average_column(self):
        pass
