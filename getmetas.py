import argparse
import requests
import time
import csv
from bs4 import BeautifulSoup

def cli():
    parser = argparse.ArgumentParser(
          prog='getmetas',
          description='Get a list of URLs from a sitemap')
    
    parser.add_argument('path_to_csv',
                        metavar='path',
                        type=str,
                        help='Path to your CSV file')



    args = parser.parse_args()

    url_list = open(args.path_to_csv, 'r')

    filename = 'titles_desc_' + str(int(time.time())) + '.csv'

    with open(filename, 'w') as status_codes:
        status_writer = csv.writer(status_codes, delimiter=',')
        status_writer.writerow(['URL', 'Title', 'Meta Description'])

        for url in url_list:
            response = requests.get(url.strip())

            soup = BeautifulSoup(response.text, features='lxml')

            title = soup.title.string if soup.title else 'No Title'
            meta_desc = soup.find('meta', {'name' : 'description'})
            meta_description = meta_desc['content'] if meta_desc else "No Meta Description"

            status_writer.writerow([url.strip(), title, meta_description])

    print('Done! Saved as: ' + filename)