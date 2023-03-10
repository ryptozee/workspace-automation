# Google Workspace Users Creation Script

This script creates new users in Google Workspace using the Admin SDK Directory API. Before using the script, make sure you have the necessary scopes enabled for your Google Cloud project and the Admin SDK Directory API and Google Drive API enabled. You also need to create a project in the Google Cloud Console and download the client secrets file.

## Prerequisites

-   A Google Cloud project with the Admin SDK Directory API and Google Drive API enabled
-   The necessary scopes enabled for your project
-   The client secrets file downloaded from the Google Cloud Console
-   Python 3.x installed on your machine

## Setup

1.  Clone or download this repository to your local machine.
2. Create a python virtual environment inside the scripts directory. This is done to isolate the dependencies and libraries needed for the project from those installed system-wide. 
3. To create a virtual environment, ran the following command in the terminal:
    `virtualenv workspace-automation`
    
4.  Activated the virtual environment by running the following command in the terminal: `source workspace-automation/bin/activate`
    
5.  Install the required packages by running `pip install -r requirements.txt` in your command prompt or terminal.

6.  Provide the path to your client secrets file in the `CREDENTIALS` variable in the script.

8.  Provide the path to your CSV file containing user data in the `CSV` variable in the script. Ensure that the CSV file contains the necessary fields for creating a new user, such as ```Email Address```, ```First Name```, ```Last Name```, ```Password```, ```Employee Title```, and ```Org Unit Path```.

## Usage

To create new users in your Google Workspace domain, run `python create_users.py`. This uses the Admin SDK Directory API to create new users.

Next, run `python create_group.py` to create one Google group and add the new users to the group.

Lastly, run `python create_drive.py` to create two Google Drive shared folders with the following permissions:
-   The first folder should allow external sharing.
-   The second folder should not allow external sharing.

Original source code modified: https://github.com/googleworkspace/python-samples/blob/main/admin_sdk/directory/quickstart.py