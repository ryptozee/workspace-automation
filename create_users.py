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

# [START admin_sdk_directory_quickstart]
from __future__ import print_function

import csv
import time
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file USER_TOKEN.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
USER_TOKEN = "user_token.json"
CREDENTIALS = "credentials.json"
CSV = "google_workspace_users.csv"

def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file USER_TOKEN stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(USER_TOKEN):
        creds = Credentials.from_authorized_user_file(USER_TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USER_TOKEN, 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    print('Inserting users into workspace')

    with open(CSV, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:

        # Create a dictionary with the user's data
            user_data = {
                'primaryEmail': row['Email Address'],
                'name': {
                    'givenName': row['First Name'],
                    'familyName': row['Last Name']
                },
                'suspended': False,
                'password': row['Password'],
                'changePasswordAtNextLogin': True,
                'organizations':[
                {
                    'title': row['Employee Title']
                }
                ],
                'orgUnitPath': row['Org Unit Path']
            }
        
            # Call the Admin SDK Directory API
            # Create the new users
            results = service.users().insert(body=user_data).execute()

    # Waiting for 20 seconds before listing out the new users
    time.sleep(20)
    
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=10,
                                   orderBy='email').execute()
    
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'{0} ({1})'.format(user['primaryEmail'],
                                      user['name']['fullName']))


if __name__ == '__main__':
    main()
# [END admin_sdk_directory_quickstart]
