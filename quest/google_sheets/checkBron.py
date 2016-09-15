# -*- coding: utf-8 -*-
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

SCOPES = {
    'sheets': 'https://www.googleapis.com/auth/spreadsheets'
}

PRIVATE_KEY = '/srv/www/server/quest/google_sheets/My Project 2-39bab73c0f18.json'
USER = "x9092554790@gmail.com"
SPREADSHEET_ID = '1Bf9uC5_UkaEjk9KlOEx0OB-6_KxYuFTRDQCM1ozMdqo'
RANGE_NAME = u'Лист1!A1:A10'
DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

def getServiceAccountCredentials(scopes, user):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(PRIVATE_KEY, scopes=scopes)
    delegated_credentials = credentials.create_delegated(user)
    return delegated_credentials.authorize(Http())

def getSheetsService(user):
    auth = getServiceAccountCredentials(SCOPES['sheets'], user)
    return build('sheets', 'v4', http=auth, discoveryServiceUrl=DISCOVERY_URL)

def checkBron():
    service = getSheetsService(USER)
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME.encode('utf-8')).execute()
    values = result.get('values', [])
    print values

checkBron()
