import argparse
import requests
import time
import csv

def cli():
    parser = argparse.ArgumentParser(
          prog='statuscodes',
          description='Get Status Codes for a set of URLs')

    parser.add_argument('a',
                         action='store',
                         choices=['validate', 'check'],
                         help='add validate argument to validate the URLs from a csv file')

    parser.add_argument('path_or_url',
                        metavar='path',
                        type=str,
                        help='URL or path to csv file')


    args = parser.parse_args()

    url_list = csv.reader(open(args.path_or_url, 'r'), delimiter=',')

    filename = ''
    if args.a == 'validate':
        filename = 'redirects_val_' + str(int(time.time())) + '.csv'
    elif args.a == 'check':
        filename = 'redirects_check_' + str(int(time.time())) + '.csv'

    with open(filename, 'w') as redirects:
        redirect_writer = csv.writer(redirects, delimiter=',')
        if args.a == 'validate':
            redirect_writer.writerow(['Source URL', 'Target URL', 'Matching Redirect', '# of Redirects', 'Status Codes', 'URL List'])


            for url in url_list:
                source_url = url[0]
                target_url = url[1]

                response = requests.get(source_url.strip())

                if len(response.history) > 0:
                    redirect_statuses = ''
                    url_list = ''
                    last_url = response.url
                    count = 1
                    for r in response.history:
                        print('current url: ' + r.url + '\n status code:' + str(r.status_code))
                        redirect_statuses += str(r.status_code) + ' > '
                        url_list += r.url + ' > '
                        count += 1

                    print('current url: ' + r.url + '\n status code:' + str(response.status_code))
                    redirect_statuses += str(response.status_code)
                    url_list += response.url
                    last_url = response.url
                            
                    if target_url == last_url:
                        redirect_writer.writerow([source_url, target_url, True, count, redirect_statuses, url_list])
                    else:
                        redirect_writer.writerow([source_url, target_url, False, count, redirect_statuses, url_list])
                else:
                    if target_url == response.url:
                        redirect_writer.writerow([source_url, target_url, True, 0, response.status_code, response.url])
                    else:
                        redirect_writer.writerow([source_url, target_url, True, 0, response.status_code, response.url])
        elif args.a == 'check':
            redirect_writer.writerow(['Start URL', '# of Redirects', 'Status Codes', 'URL List'])
            for url in url_list:
                source_url = url[0]

                response = requests.get(source_url.strip())
                if len(response.history) > 0:
                    redirect_statuses = ''
                    url_list = ''
                    last_url = response.url
                    count = 1
                    for r in response.history:
                        print('current url: ' + r.url + '\n status code:' + str(r.status_code))
                        redirect_statuses += str(r.status_code) + ' > '
                        url_list += r.url + ' > '
                        count += 1
                    print('current url: ' + r.url + '\n status code:' + str(response.status_code))
                    redirect_statuses += str(response.status_code)
                    url_list += response.url
                    last_url = response.url

                    redirect_writer.writerow([source_url, count, redirect_statuses, url_list])
                else:  
                    redirect_writer.writerow([source_url, 0, response.status_code, response.url])