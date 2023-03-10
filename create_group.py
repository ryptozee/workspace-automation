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
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# If modifying these scopes, delete the file GROUP_TOKEN.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.group.member']
GROUP_TOKEN = "group_token.json"
CREDENTIALS = "credentials.json"
CSV = "google_workspace_users.csv"
GROUP_NAME = "regular.users"
DOMAIN = "shingai.emea.flipservice.nl"

def create_group(service):
    """Creates a new Google group."""
    group = {
        "email": GROUP_NAME+"@"+DOMAIN,
        "name": GROUP_NAME,
        "description": "My group"
    }
    try:
        group = service.groups().insert(body=group).execute()
        print(f"Group '{GROUP_NAME}' created: {group['email']}")
        return group
    except HttpError as error:
        print(f"An error occurred while creating the group: {error}")
        return None

def add_members_to_group(service, group):
    """Adds members to a Google group."""
    # Open CSV file and read the list of members to be added
    with open(CSV, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Define the memmber object
                member = {
                    "email": row['Email Address'],
                    "role": "MEMBER"
                }
                # Call the API to add the member to the group
                service.members().insert(groupKey=group['email'], body=member).execute()
                print(f"Added '{row['Email Address']}' to group '{group['email']}'")
            except HttpError as error:
                print(f"An error occurred while adding '{row['Email Address']}' to the group: {error}")

def update_group_settings(service, group):
    #Updates the settings of the Google group.
    try:
        # Define the group settings object
        group_settings = {
            "whoCanViewMembership": "MANAGERS_CAN_VIEW",
            "whoCanEmailAllMembers": "ALL_MANAGERS_CAN_EMAIL",
            "showInGroupDirectory": False
        }
        # Call the API to update the group settings
        service.groups().update(groupKey=group['email'], body=group_settings).execute()
        print(f"Updated settings for group '{group['email']}'")
    except HttpError as error:
        print(f"An error occurred while updating settings for the group: {error}")

def main():
    """Creates a Google group and adds users to the group."""
    creds = None
    if os.path.exists(GROUP_TOKEN):
        creds = Credentials.from_authorized_user_file(GROUP_TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GROUP_TOKEN, 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    group = create_group(service)

    if group:
        add_members_to_group(service, group)
        update_group_settings(service, group)

if __name__ == '__main__':
    main()
# [END admin_sdk_directory_quickstart]

