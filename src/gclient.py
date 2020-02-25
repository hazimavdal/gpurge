# pylint: disable=E1101

import io
from httplib2 import Http
import googleapiclient
from googleapiclient import discovery
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload

CLIENT_ID_FILE = "creds/client_id.json"
STORAGE_FILE = 'storage.json'

SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive']

MIME_TYPES = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}


class GClient:

    def __init__(self):
        self.__service = discovery.build(
            'drive', 'v3', http=self.get_creds().authorize(Http()))

    def get_creds(self):
        store = file.Storage(STORAGE_FILE)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
            creds = tools.run_flow(flow, store)
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
