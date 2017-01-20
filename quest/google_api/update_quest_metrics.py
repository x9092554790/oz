"""A simple example of how to access the Google Analytics API."""
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import os
from django.core.management import setup_environ
import server.settings

setup_environ(server.settings)

from quest.models import *

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email, key_file_location, scopes=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None


def get_pageviews(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='yesterday',
      end_date='today',
      metrics='ga:pageViews, ga:uniquePageViews',
      dimensions='ga:pagePath',
      filters='ga:pagePath=~^/quest/',
      sort='-ga:uniquePageviews').execute()


def printTable(results):
  table_format = "{:>30}"

  if results and isinstance(results, dict) and 'columnHeaders' in results:
      headers = results['columnHeaders']
      h_format = table_format * len(headers)
      header = h_format.format(*[h['name'] for h in headers])
      print header
      print "-"*len(header)

  if results and isinstance(results, dict) and 'rows' in results:
      rows = results['rows']
      for r in rows:
        r_format = table_format * len(r)
        print r_format.format(*r)

def updateDB(results):
    if results and isinstance(results, dict) and 'rows' in results:
        rows = results['rows']
        for path, v in {r[0]: {'views': r[1], 'uviews': r[2]} for r in rows}.items():
            url = path.rsplit('/', 1)[-1]
            try:
                q = Quest.objects.get(seo_url=url)
                q.view_count = int(v['views'])
                q.save()
            except:
                pass




def main():
  scope = ['https://www.googleapis.com/auth/analytics.readonly']
  service_account_email = 'service@ageless-granite-156009.iam.gserviceaccount.com'
  key_file_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Analytics-691f0dc58d05.p12")

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
  profile = get_first_profile_id(service)
  results = get_pageviews(service, profile)
  updateDB(results['rows'])

if __name__ == '__main__':
  main()
