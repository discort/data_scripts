import httplib2
import argparse
import logging

import requests
from apiclient import discovery
from oauth2client import client


from config import GOOGLE_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_URI


DISCOVERY_URL = "https://sheets.googleapis.com/$discovery/rest?version=v4"

# Allows read/write access to the user's sheets and their properties.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class BaseClient:
    """Class for working with google services"""

    def create_service(self, service_name, version, discovery_url, *args, **kwargs):
        """"""
        pass


class Client(BaseClient):
    """Class for working with google spreadsheets"""
    def __init__(self, email=None, password=None):
        self._email = email
        self._password = password

    def create_service(self, discovery_url):
        """"""
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URL)
        return service

    def open_spreadsheet(self, spreadsheet_id):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URL)
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Sheet1')
        return result.execute().get('values', [])

    def _get_credentials(self):
        credentials = client.GoogleCredentials(
            access_token=GOOGLE_API_KEY,
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            refresh_token=None,
            token_expiry=None,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent='Python lib'
        )
        return credentials


def _send_request_get(url):
    request = requests.get(url, auth=("odiscort@gmail.com", "lbc26071991"))
    return request


def create_parser():
    parser = argparse.ArgumentParser(description="Process Google Sheet ID parsing")
    parser.add_argument(metavar="gsheet_id")
    return parser


def main():
    my_gsheet_url = "https://docs.google.com/spreadsheets/d/1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4/edit#gid=0"
    client = Client()
    spreadsheet_id = "1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4"
    gsheet = client.open_spreadsheet(spreadsheet_id)
    print(gsheet)
    pass


if __name__ == "__main__":
    main()
