# pylint: disable=E1101

import io
import pickle
import os.path
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

CLIENT_ID_FILE = "creds/client_id.json"
STORAGE_FILE = 'creds/storage.pickle'

SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive']

MIME_TYPES = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}


class GClient:

    def __init__(self):
        self.__service = build('drive', 'v3', credentials=self.get_creds())

    def get_creds(self):
        # Based on https://developers.google.com/drive/api/v3/quickstart/python

        creds = None
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_ID_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(STORAGE_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def gerr_nice(self, e):
        return f'Remote returned HTTP {e.resp.status}: {e. _get_reason().strip()}'

    def get(self, file_id: str, ext: str):
        try:
            mime = MIME_TYPES[ext]
        except KeyError as e:
            return None, Exception(f"Unknown file format {ext}")

        try:
            content = self.__service.files().export_media(fileId=file_id, mimeType=mime)
            metadata = self.__service.files().get(fileId=file_id).execute()
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, content)

            done = False
            while not done:
                _, done = downloader.next_chunk()
        except googleapiclient.errors.HttpError as e:
            return None, Exception(self.gerr_nice(e))

        metadata['content'] = fh.getvalue()
        metadata['sourceMIME'] = metadata['mimeType']
        metadata['mimeType'] = mime
        metadata['extension'] = ext

        return metadata, None

    def delete(self, file_id, trash=True):
        return None  # TODO enable this in production.

        try:
            if trash:
                self.__service.files().update(fileId=file_id, body={
                    'trashed': True}).execute()
            else:
                self.__service.files().delete(fileId=file_id).execute()

            return None
        except Exception as e:
            return e
