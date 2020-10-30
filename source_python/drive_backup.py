from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
FOLDER_ID = '1jbP1V40sl7hlSuRbmQhYtGQUFvuZv7IE'

def init_service():
    store = file.Storage('../.config/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../.config/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service

def delete_old_data(drive_service, files_names):
    for file_name in files_names:
        results = drive_service.files().list(q="name='"+file_name+"'", fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if len(items) > 0:
            items_id = [v['id'] for v in items]
            for item_id in items_id:
                try:
                    drive_service.files().delete(fileId=item_id).execute()
                except:
                    print ('An error occurred')

def upload_data(drive_service, files_names):
    for file_name in files_names:
        folder_id = FOLDER_ID
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload("../database/ETF_files/" + file_name,
                                mimetype='text/csv',
                                resumable=True)
        file_to_upload = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print ('File ID: %s' % file_to_upload.get('id'))

#Main
files_names = ["BMOM_DATA.csv", "LN1L_DATA.csv", "LSP5_DATA.csv", "LYFB_DATA.csv"]

drive_service = init_service()
delete_old_data(drive_service, files_names)
upload_data(drive_service, files_names)

