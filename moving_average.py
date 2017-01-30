import os
import sys
import argparse
import logging

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from config import (SERVICE_CREDENTIALS, WINDOW_SIZE, WINDOW_TYPE, HEADER_ROW_NUMBER,
                    LOG_TO, LOGGER)


logger = logging.getLogger(__name__)

# For acquiring an access token
SCOPES = ['https://spreadsheets.google.com/feeds']


class WorksheetError(Exception):
    """An exception during performing of worksheet"""
    pass


def configure_logging(logger):
    if not os.path.exists(LOG_TO):
        os.mkdir(LOG_TO)

    file_handler = logging.FileHandler(os.path.join(LOG_TO, LOGGER['file']))
    file_handler.setLevel(LOGGER['level'])
    file_handler.setFormatter(LOGGER['formatter'])

    logger.addHandler(file_handler)
    logger.setLevel(file_handler.level)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Process Google Sheet ID")
    parser.add_argument('sheet_id', help="Google Sheet ID")
    return parser.parse_args(args)


def open_spreadsheet(key, credentials=None):
    """
    Open spreadsheet specified by key

    Args:
        key:str - A key of a spreadsheet as it appears in a URL in a browser.
        credentials:`oath2client.OAuth2Credentials` - client credentials

    Returns:
        `gspread.Spreadsheet` instance.
    """
    if not credentials:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            SERVICE_CREDENTIALS,
            SCOPES,
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
    If the column does not exist creating the column.

    Args:
        sheet: `gspread.Worksheet` - The class for worksheet object

    Returns:
        None
    """
    records = sheet.get_all_records(head=HEADER_ROW_NUMBER)
    moving_average = calculate_moving_average(records, sheet.title)
    cells_range = get_result_cells_range(sheet, records)

    for cell, mean in zip(cells_range, moving_average):
        cell.value = mean

    # Update in batch
    sheet.update_cells(cells_range)


def calculate_moving_average(records, title):
    """
    Calculate moving average of daily visitors on the Google Worksheet

    Args:
        records:list - A list of dictionaries
        title:str - The title of the worksheet

    Returns:
        List of caculated values values
    """
    df = pd.DataFrame(records)
    if df.empty:
        raise WorksheetError("Empty worksheet: `{0}`".format(title))

    # Check worksheet for mandatory columns
    mandatory_columns = ('Date', 'Visitors')
    for col in mandatory_columns:
        if col not in df.columns:
            raise WorksheetError("Worksheet `{0}` does not contain mandatory column `{1}`"
                                 .format(title, col))

    # To prevent for MA calculation from scratch
    df['Visitors'] = df['Visitors'].fillna(0)

    df['Moving Average'] = df['Visitors'].rolling(window=WINDOW_SIZE,
                                                  win_type=WINDOW_TYPE).mean()

    values = df['Moving Average'].fillna('').tolist()
    return values


def get_result_cells_range(sheet, records):
    """
    Get a list of cells for `Moving Average` values

    Args:
        sheet:`gspread.Worksheet` - The class for worksheet object
        records:list - The list of dicts of existins records

    Returns:
        a list of `gspread.Cell` instances
    """
    MA_cell = get_or_create_ma_cell(sheet, records)
    start_ma_cell = gspread.utils.rowcol_to_a1(MA_cell.row + 1, MA_cell.col)

    date_cell = sheet.find('Date')
    date_values = sheet.col_values(date_cell.col)
    date_values = list(filter(None, date_values))  # Remove empty strings

    end_ma_cell = gspread.utils.rowcol_to_a1(len(date_values), MA_cell.col)

    cell_list = sheet.range("{start}:{end}".format(start=start_ma_cell, end=end_ma_cell))
    return cell_list


def get_or_create_ma_cell(sheet, records, default_label='Moving Average'):
    """
    Create or get `Moving Average` header cell

    Args:
        sheet:`gspread.Worksheet` - The class for worksheet object
        records:list - The list of dicts of existins records
        default_label:str - `Moving Average` header label

    Returns:
        `gspread.Cell` instance - MA header cell
    """
    try:
        MA_cell = sheet.find(default_label)
    except gspread.exceptions.CellNotFound:
        last_column_idx = len(records[0]) + 1
        sheet.update_cell(HEADER_ROW_NUMBER, last_column_idx, default_label)
        MA_cell = sheet.cell(HEADER_ROW_NUMBER, last_column_idx)
    return MA_cell


def main():
    configure_logging(logger)
    logger.info("Service is running...")
    try:
        args = parse_args(sys.argv[1:])
        logger.info("parsed args: {0}".format(args))
        spreadsheet = open_spreadsheet(args.sheet_id)
        logger.info("Spreadsheet with id={0} is opening".format(spreadsheet.id))

        process_spreadsheet(spreadsheet)
        logger.info("Processing completed")
    except Exception:
        logger.exception("Error ocurred during processing Sheet:{0}".format(args.sheet_id))

    # spreadsheet_id = "1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4"
    # spreadsheet_id2 = "1YZbtdIKOIlpyib8oncLW9jbVbFvde07-GaxT3CSHkDI"


if __name__ == "__main__":
    main()
