## Basic usage
1. Obtain OAuth2 credentials from [Google Developers Console](https://console.developers.google.com/project)
  * Create a new project (or select the one you have).
  * Under “API & auth”, in the API enable “Drive API”.
  * Go to “Credentials” and choose “New Credentials > Service Account Key”.
  You will automatically download a JSON file with this data.
  This is how this file may look like:
  ```
  {
    "private_key_id": "16c … c7b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "611 … hd@developer.gserviceaccount.com",
    "client_id": "107 … hd.apps.googleusercontent.com",
    "type": "service_account"
  }
  ```
  * Go to Google Sheets and share your spreadsheet with an email you have in your `json_key['client_email']`. Otherwise you’ll get a `SpreadsheetNotFound` exception when trying to open it.

2. Paste obtained data to `config.py` file.

3. Install requirements with `python3.5`.
```
pip install -r requirements.txt
```

4. Run the script
```
python moving_average.py <Google Sheet Id>
```

## Run tests
```
py.test tests
```