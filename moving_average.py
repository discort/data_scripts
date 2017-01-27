import argparse
import logging

import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials

from config import SERVICE_CREDENTIALS, WINDOW_SIZE


logger = logging.getLogger(__name__)

# Allows read/write access to the user's sheets and their properties.
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

SCOPE = ['https://spreadsheets.google.com/feeds']


class WorksheetError(Exception):
    """An exception during performing of worksheet"""
    pass


def parse_options():
    parser = argparse.ArgumentParser(description="Process Google Sheet ID")
    parser.add_argument('sheet_id', help="Google Sheet ID")
    return parser.parse_args()


def open_spreadsheet(key):
    """
    Open spreadsheet specified by key

    Args:
        key:str - A key of a spreadsheet as it appears in a URL in a browser.

    Returns:
        `gspread.Spreadsheet` instance.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        SERVICE_CREDENTIALS,
        SCOPE,
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(key)
    return spreadsheet


def process_spreadsheet(spreadsheet):
    """
    Args:
        spreadsheet:`gspread.Spreadsheet` instance - For working with spreadsheet object

    Returns:
        None
    """
    for worksheet in spreadsheet.worksheets():
        process_worksheet(worksheet)


def process_worksheet(sheet):
    """
    Calculate the moving average of daily visitors and write it column `Moving Average`.
    If the column does not exist it creates the column.

    Args:
        sheet: `gspread.Worksheet` - The class for worksheet object

    Returns:
        None
    """
    df = pd.DataFrame(sheet.get_all_records())
    if df.empty:
        raise WorksheetError("Empty worksheet: `{0}`".format(sheet.title))

    print(df)

    # Check worksheet for mandatory columns
    mandatory_columns = ('Date', 'Visitors')
    for col in mandatory_columns:
        if col not in df.columns:
            raise WorksheetError("Worksheet `{0}` does not contain mandatory column `{1}`"
                                 .format(sheet.title, col))

    # To prevent for MA calculation from scratch
    df['Visitors'] = df['Visitors'].fillna(0)

    df['Moving Average'] = df['Visitors'].rolling(window=WINDOW_SIZE).mean()

    df['Visitors'] = df['Visitors'].astype(int)

    print(df)


def main():
    options = parse_options()
    print(options)
    spreadsheet = open_spreadsheet(options.sheet_id)
    print(spreadsheet)
    process_spreadsheet(spreadsheet)
    # spreadsheet_id = "1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4"
    # spreadsheet_id2 = "1YZbtdIKOIlpyib8oncLW9jbVbFvde07-GaxT3CSHkDI"


if __name__ == "__main__":
    main()
