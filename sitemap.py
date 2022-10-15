import argparse
import xml.etree.ElementTree as et
import csv
import time
import requests


def cli():
    parser = argparse.ArgumentParser(
          prog='sitemap',
          description='Get a list of URLs from a sitemap')

    parser.add_argument('a',
                        action='store',
                        choices=['extract'],
                        help='add \'extract\' argument to extract URLs from a sitemap')
    
    parser.add_argument('url',
                        metavar='path',
                        type=str,
                        help='URL to a sitemap')



    args = parser.parse_args()



    r = requests.get(args.url)
    sitemap = r.content.decode('utf-8')

    tree = et.ElementTree(et.fromstring(sitemap))
    root = tree.getroot()

    ns = root.tag.split('}')[0][1:]

    nsmap = {'ns': ns}

    filename = 'sitemap_urls_' + str(int(time.time())) + '.csv'
    
    print(nsmap)

    with open(filename, 'w') as status_codes:
        status_writer = csv.writer(status_codes, delimiter=',')
        status_writer.writerow(['URL'])

        if root.tag.split('}')[1] == 'sitemapindex':
            for sitemap in root.findall('ns:sitemap', nsmap):
                sitemap_url = sitemap.find('ns:loc', nsmap).text

                resp = requests.get(sitemap_url)
                sm = resp.content.decode('utf-8')
                sm_tree = et.ElementTree(et.fromstring(sm))
                sm_root = sm_tree.getroot()
                
                for url in sm_root.findall('ns:url', nsmap):
                    page = url.find('ns:loc', nsmap).text
                    status_writer.writerow([page])

        elif root.tag.split('}')[1] == 'urlset':
            for url in root.findall('ns:url', nsmap):
                page = url.find('ns:loc', nsmap).text
                status_writer.writerow([page])

    print('Done! Saved as: ' + filename)
