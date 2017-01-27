# -*- coding: utf-8 -*-
import os
import logging
from datetime import date

# 1. Head to Google Developers Console and create a new project (or select the one you have.)
# 2. Under “API & auth”, in the API enable “Drive API”.
# 3. Go to “Credentials” and choose “New Credentials > Service Account Key”.
# You will automatically download a JSON file with secret data.
# Copy the data to `config.py` from JSON file
# Make: export PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n"
SERVICE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "testing-156809",
    "private_key_id": "16c7eb2a02aea5306beab5352c6ea92841c44c7b",
    "private_key": os.environ.get('PRIVATE_KEY'),
    "client_email": "611098765609-compute@developer.gserviceaccount.com",
    "client_id": "107444024930240932124",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/611098765609-compute%40developer.gserviceaccount.com"
}
#print(os.environ.get('PRIVATE_KEY'))
#print(SERVICE_CREDENTIALS)


# The row number of the header of google sheet
HEADER_ROW_NUMBER = 1


# Size of the moving window. This is number of observations used for
# calculating the statistic. Each window will be a fixed size
WINDOW_SIZE = 5
WINDOW_TYPE = None


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Logging configuration
LOG_TO = os.path.join(BASE_DIR, 'logs')
LOGGER = dict(
    level=logging.DEBUG,
    file="log_{date:%Y-%m-%d}.log".format(date=date.today()),
    formatter=logging.Formatter(
        "%(asctime)s [%(thread)d:%(threadName)s] [%(levelname)s] - %(name)s:%(message)s"),
)
