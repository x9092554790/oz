from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

SCOPES = {
    'drive': 'https://www.googleapis.com/auth/drive'
}

PRIVATE_KEY = '/srv/www/server/quest/google_drive/service_private.json'
USER = "x9092554790@gmail.com"
ROOT_FOLDER = "0B--hrPHQQf6oUWxQaFBtRGhiOXc"

def getServiceAccountCredentials(scopes, user):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(PRIVATE_KEY, scopes=scopes)
    delegated_credentials = credentials.create_delegated(user)
    return delegated_credentials.authorize(Http())

def getDriveService(user):
    auth = getServiceAccountCredentials(SCOPES['drive'], user)
    return build('drive', 'v3', http=auth)

def getChildren(service, folders, order_by="createdTime desc", mime_type=None):
    page_token = None
    ret = []
    q = ""
    if len(folders) > 0:
        q += "("
    for f in folders:
        q += "'"+f+"' in parents or "
    if len(q) >= 4:
        q = q[:-4]
        q += ")"
    if mime_type:
        if len(q) > 0:
            q += " and "
        q += "mimeType='"+mime_type+"'"
    while True:
        children = service.files().list(q=q,
                             fields="nextPageToken, files(id, name)",
                             orderBy=order_by,
                             pageToken=page_token).execute()

        ret += children.get('files', [])

        page_token = children.get('nextPageToken', None)
        if page_token is None:
            break
    return ret

def getAllDays(service, root_folder):
    days_id = []
    months = getChildren(service, [root_folder], mime_type='application/vnd.google-apps.folder')
    months_id = []
    for month in months:
        months_id.append(month.get('id'))
    days = getChildren(service, months_id, mime_type='application/vnd.google-apps.folder')
    for day in days:
        days_id.append(day.get('id'))
    return days_id

def getAllImgs(service, folders):
    return getChildren(service, folders, mime_type='image/jpeg')
