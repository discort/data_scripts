import pytest
import gspread
from unittest import mock
from xml.etree import ElementTree

import moving_average


CELLS_FEED = b"<?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:batch='http://schemas.google.com/gdata/batch' xmlns:gs='http://schemas.google.com/spreadsheets/2006'><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full</id><updated>2017-01-29T22:51:31.975Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>second_out</title><link rel='alternate' type='application/atom+xml' href='https://docs.google.com/spreadsheets/d/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/edit'/><link rel='http://schemas.google.com/g/2005#feed' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full'/><link rel='http://schemas.google.com/g/2005#post' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full'/><link rel='http://schemas.google.com/g/2005#batch' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/batch'/><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full?return-empty=true&amp;range=D2%3AD5'/><author><name>odiscort</name><email>odiscort@gmail.com</email></author><openSearch:totalResults>4</openSearch:totalResults><openSearch:startIndex>1</openSearch:startIndex><gs:rowCount>1000</gs:rowCount><gs:colCount>26</gs:colCount><entry><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R2C4</id><updated>2017-01-29T22:51:31.975Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>D2</title><content type='text'></content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R2C4'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R2C4/u06ps'/><gs:cell row='2' col='4' inputValue=''></gs:cell></entry><entry><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R3C4</id><updated>2017-01-29T22:51:31.975Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>D3</title><content type='text'></content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R3C4'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R3C4/u1la8'/><gs:cell row='3' col='4' inputValue=''></gs:cell></entry><entry><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R4C4</id><updated>2017-01-29T22:51:31.975Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>D4</title><content type='text'></content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R4C4'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R4C4/u2zuo'/><gs:cell row='4' col='4' inputValue=''></gs:cell></entry><entry><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R5C4</id><updated>2017-01-29T22:51:31.975Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>D5</title><content type='text'></content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R5C4'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R5C4/u4ef4'/><gs:cell row='5' col='4' inputValue=''></gs:cell></entry></feed>"
CELLS_ID_FEED = b"<?xml version='1.0' encoding='UTF-8'?><entry xmlns='http://www.w3.org/2005/Atom' xmlns:batch='http://schemas.google.com/gdata/batch' xmlns:gs='http://schemas.google.com/spreadsheets/2006'><id>https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R1C4</id><updated>2017-01-29T23:07:17.521Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#cell'/><title type='text'>D1</title><content type='text'>Moving Average</content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R1C4'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/cells/1aJRrnG2qnW-t0XVwWWY7baqaINv1yZKTMSzN3ekw00Q/oligch9/private/full/R1C4/mrd0sr'/><gs:cell row='1' col='4' inputValue='Moving Average'>Moving Average</gs:cell></entry>"


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    """
    Setup config for tests
    """
    test_credentials = {
        "type": "service_account",
        "project_id": "dummy_id",
        "private_key_id": "0123456",
        "private_key": "-----BEGIN PRIVATE KEY-----\DUMMY KEYn-----END PRIVATE KEY-----\n",
        "client_email": "dummy@developer.gserviceaccount.com",
        "client_id": "012345678",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.certurl.com"
    }
    monkeypatch.setattr(moving_average, 'SERVICE_CREDENTIALS', test_credentials)
    monkeypatch.setattr(moving_average, 'WINDOW_SIZE', 5)
    monkeypatch.setattr(moving_average, 'WINDOW_TYPE', None)
    monkeypatch.setattr(moving_average, 'HEADER_ROW_NUMBER', 1)

    monkeypatch.setattr(moving_average, 'configure_logging', lambda x: None)


@pytest.fixture(scope="function")
def client(monkeypatch):
    client = gspread.client.Client(auth={})

    def mock_cells_feed(*args, **kwags):
        return ElementTree.fromstring(CELLS_FEED)

    def mock_cells_cell_id_feed(*args, **kwags):
        return ElementTree.fromstring(CELLS_ID_FEED)

    monkeypatch.setattr(gspread.client.Client, 'get_cells_feed', mock_cells_feed)
    monkeypatch.setattr(gspread.client.Client, 'get_cells_cell_id_feed', mock_cells_cell_id_feed)

    return client


@pytest.fixture(scope="function")
def spreadsheet(client):
    return gspread.Spreadsheet(client, mock.MagicMock())


@pytest.fixture(scope="function")
def worksheet(spreadsheet):
    result = gspread.Worksheet(spreadsheet, mock.MagicMock())
    return result
