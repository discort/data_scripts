import httplib2
import argparse
import urllib.parse
import logging

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from bs4 import BeautifulSoup
import requests


from config import (GOOGLE_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_URI,
                    GOOGLE_REDIRECT_URI)


DISCOVERY_URL = "https://sheets.googleapis.com/$discovery/rest?version=v4"

# Allows read/write access to the user's sheets and their properties.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"


def _check_redirect_uri(auth_uri):
    """
    Check for denied access
    Args:
        auth_uri:str - authorized url from step1 of flow

    Returns:
        'urllib.parse.ParseResult'
    """
    result = urllib.parse.urlparse(auth_uri)
    if 'error' in result.query or 'code' not in result.query:
        raise ValueError("Access denied")
    return result


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

    # def _get_credentials(self):
    #     flow = OAuth2WebServerFlow(
    #         client_id=GOOGLE_CLIENT_ID,
    #         client_secret=GOOGLE_CLIENT_SECRET,
    #         scope=SCOPES,
    #         redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    #     )
    #     #authorize_url = flow.step1_get_authorize_url()
    #     #redirect_uri = _check_redirect_uri(auth_uri)
    #     #code = redirect_uri.query.split("=")[1]
    #     credentials = flow.step2_exchange("4/s6VEbURXen3vbsSbecwOF2fyqHidc5EI5TUR3-ggr4g")
    #     return credentials


def create_parser():
    parser = argparse.ArgumentParser(description="Process Google Sheet ID parsing")
    parser.add_argument(metavar="gsheet_id")
    return parser


def get_authtorization_code():
    data = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": SCOPES
    }
    response = requests.get(AUTH_URI, params=data, allow_redirects=False)
    print(response.headers.get('location'))
    print(response.text)
    return response


def get_credentials():
    store = Storage("test.json")
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        flow.user_agent = "test"
        credentials = tools.run_flow(flow, store)

    return credentials


class GoogleSession:
    def __init__(self, url_login, url_auth, login, passwd):
        self.session = requests.session()
        #login_html = self.session.get(url_login)
        #soup_login = BeautifulSoup(login_html.content).find('form').find_all('input')
        #data = {}
        #for u in soup_login:
        #    if u.has_attr('value'):
        #        data[u['name']] = u['value']

        #data['Email'] = login
        #data['Passwd'] = passwd
        #self.post(url_auth, data=data)

    def get(self, url, **kwargs):
        return self.session.get(url).text

    def post(self, url, data, **kwargs):
        return self.session.post(url, data=data).text


def get_session():
    url_login = "https://accounts.google.com/ServiceLogin"
    url_auth = "https://accounts.google.com/ServiceLoginAuth"
    session = GoogleSession(url_login, url_auth, login, password)
    return session
    #print(session.get("http://plus.google.com"))


def get_authorization_code(auth_uri, session):
    """
    Obtain a `code` provided by the authorization server
    """
    approval_page = session.get(auth_uri)
    approval_form = BeautifulSoup(approval_page).find('form')
    print(approval_form)
    approval_url = approval_form.get('action')
    print(approval_url)
    inputs = approval_form.find_all('input')
    data = {}
    for u in inputs:
        if u.has_attr('value'):
            data[u['name']] = u['value']

    data["submit_access"] = True
    code_page = session.post(approval_url, data)
    soap_code = BeautifulSoup(code_page).find('input')
    code = soap_code.get('value')
    return code


def get_flow_credentials():
    flow = OAuth2WebServerFlow(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scope=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
        #access_type="offline"
    )
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)
    session = get_session()

    code = get_authorization_code(auth_uri, session)
    print("code={}".format(code))
    credentials = flow.step2_exchange(code)
    return credentials


def open_spreadsheet():
    import gspread
    credentials = SignedJwtAssertionCredentials(client_email, private_key.encode(), SCOPES)
    gc = gspread.authorize(credentials)
    sht1 = gc.open_by_key('1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4')
    print(sht1)


def main():
    my_gsheet_url = "https://docs.google.com/spreadsheets/d/1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4/edit#gid=0"
    # client = Client()
    # spreadsheet_id = "1RMgVoyTdIaQ6k4WNIzWw74pUSf-wBTkq2Xa5jwIGbS4"
    # gsheet = client.open_spreadsheet(spreadsheet_id)
    # authenticate_client()
    #get_flow_credentials()
    open_spreadsheet()


if __name__ == "__main__":
    main()
