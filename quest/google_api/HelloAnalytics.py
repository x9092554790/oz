from django.core.management import setup_environ
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import os



def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

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


def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='7daysAgo',
      end_date='today',
      metrics='ga:sessions').execute()

def get_pageviews(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='yesterday',
      end_date='today',
      metrics='ga:pageViews, ga:uniquePageViews',
      dimensions='ga:pagePath',
      filters='ga:pagePath=~^/quest/',
      sort='-ga:uniquePageviews').execute()


def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'View (Profile): %s' % results.get('profileInfo').get('profileName').encode('utf-8')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

  else:
    print 'No results found'

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

def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = 'service@ageless-granite-156009.iam.gserviceaccount.com'
  key_file_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Analytics-691f0dc58d05.p12")

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
  profile = get_first_profile_id(service)
  # print_results(get_results(service, profile))
  printTable(get_pageviews(service, profile))

if __name__ == '__main__':
  main()
