
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

FILES = (
    ('test.txt', None),
    ('test.txt', 'application/vnd.google-apps.document'),
)


def simpleupload(service):

    for filename, mimeType in FILES:
        
        #Set metadata for each file to be uploaded
        metadata = {'name': filename}
        if mimeType:
            metadata['mimeType'] = mimeType

        #Upload call for each file
        result = service.files().create(body=metadata, media_body=filename).execute()

        #Print result for each file
        if result:
            print ('Sucessful Uploaded "%s" (%s)' % (filename, result['mimeType']))


def main():
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and 
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    #Service endpoint
    service = discovery.build('drive', 'v3', http=http)

    simpleupload(service)



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    

if __name__ == '__main__':
    main()