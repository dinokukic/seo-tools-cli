import argparse
import requests
import time
import csv

def cli():
    parser = argparse.ArgumentParser(
          prog='statuscodes',
          description='Get Status Codes for a set of URLs')


    parser.add_argument('path_or_url',
                        metavar='path',
                        type=str,
                        help='URL or path to csv file')


    args = parser.parse_args()

    url_list = open(args.path_or_url, 'r')

    filename = 'status_codes_' + str(int(time.time())) + '.csv'

    with open(filename, 'w') as status_codes:
        status_writer = csv.writer(status_codes, delimiter=',')
        status_writer.writerow(['URL', 'Status Code'])

        count = 1
        for url in url_list:
            print(count, end = '\r')
            response = requests.get(url.strip(), allow_redirects=False)

            status_writer.writerow([url.strip(), response.status_code])
      
            count += 1

    print('Done! Saved as: ' + filename)