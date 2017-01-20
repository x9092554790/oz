from googleapiclient import sample_tools
import argparse

def getService(uri):
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
    # argparser.add_argument('start_date', type=str,
    #                    help=('Start date of the requested date range in '
    #                          'YYYY-MM-DD format.'))
    # argparser.add_argument('end_date', type=str,
    #                    help=('End date of the requested date range in '
    #                          'YYYY-MM-DD format.'))
    # argv = [uri, start_date, end_date]
    argv = [uri]
    return sample_tools.init(argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

def execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()

service, flags = getService("http://questoz.ru")
start_date = '2017-01-01'
end_date = '2017-01-10'

request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['page'],
    'rowLimit': 10
}
response = execute_request(service, flags.property_uri, request)
print response