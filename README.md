# GPurge

This is a utility that converts Google Documents, Sheets, etc. to physical files. `gpurge` can search in a local folder (typically a fully-synced Google Drive folder) recursively and convert all `.godc` and `gsheet` files to `.docx` and `xlsx`, respectively.

## Prerequisites

- Python 3.6 or greater

- [Google Drive Python Client Library V3](https://developers.google.com/drive/api/v3/quickstart/python#step_2_install_the_google_client_library)

```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

- [Turn on Drive API](https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the). Save the `credentials.json` file as `creds/client_id.json` in the same folder as the `gpurge.py` file.


## Usage

Run `./gpurge.py -h`.

## Google Docs are great, why convert to MS Word?

Here are some scenarios that make sense to do this:

- You want to archive your files and guarantee that you have access to their _content_ 20 years from now. Google [killed](https://en.wikipedia.org/wiki/List_of_Google_products) a great many products in the past, and it is not unlikely that they will discontinue Google Docs at some point in the future.   

- Be able to perform bulk operations on these documents locally, such as searching.

- You need to port your files to another system. How many applications out there can process `.gdoc` files, other than Google Docs? 
