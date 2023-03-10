# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
# [START admin_sdk_directory_quickstart]
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# If modifying these scopes, delete the file DRIVE_TOKEN.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_TOKEN = "drive_token.json"
CREDENTIALS = "credentials.json"
EXTERNAL_FOLDER_NAME = "External Shared Folder"
INTERNAL_FOLDER_NAME = "Internal Shared Folder"
DOMAIN = "shingai.emea.flipservice.nl"

def create_folder(service, folder_name, permission_type):
    #Creates a new Google Drive folder.
    folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    if permission_type == 'external':
        permission = {'type': 'anyone', 'role': 'reader', 'allowFileDiscovery': True}
        service.permissions().create(fileId=folder['id'], body=permission).execute()
        print(f"Created folder '{folder_name}' with external sharing enabled.")
    else:
        domain_permission = {'type': 'domain', 'role': 'writer', 'domain': DOMAIN}
        service.permissions().create(fileId=folder['id'], body=domain_permission).execute()
        print(f"Created folder '{folder_name}' with internal sharing only.")

    return folder

def main():
    #Creates two Google Drive folders - one for external sharing and one for internal sharing.
    creds = None
    if os.path.exists(DRIVE_TOKEN):
        creds = Credentials.from_authorized_user_file(DRIVE_TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(DRIVE_TOKEN, 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    external_folder = create_folder(service, EXTERNAL_FOLDER_NAME, 'external')
    internal_folder = create_folder(service, INTERNAL_FOLDER_NAME, 'internal')

if __name__ == '__main__':
    main()
# [END admin_sdk_directory_quickstart]