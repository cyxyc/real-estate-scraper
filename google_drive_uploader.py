
# https://www.youtube.com/watch?v=tamT_iGoZDQ

# pip install google-api-python-client
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES =  ['https://www.googleapis.com/auth/drive' ]

SERVICE_ACCOUNT_FILE = "service_account.json"

PARENT_FOLDER_ID = "1I4fb84DOshnn3dPETMMZdmUvAfaCfQtV" 

def authenticate():
    
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_photo(file_path):
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': "hello3",
        'parents': [PARENT_FOLDER_ID]
    }

    file = drive_service.files().create(body=file_metadata, media_body=file_path).execute()

        # Get the file ID
    file_id = file.get('id')

    # Get the file's metadata
    file_metadata = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()

    # Get the URL of the file
    file_url = file_metadata.get('webViewLink')
    print(file_url)

upload_photo("hjk.png")