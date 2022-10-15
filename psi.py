import argparse
import requests
import time
import csv

def cli():
      PSI_URL='https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

      parser = argparse.ArgumentParser(
          prog='psi',
          description='Get Page Speed Insights for one or more URLs')


      parser.add_argument('n',
                             action='store',
                             choices=['s', 'm'],
                             help='set if you want results for a single (s) (URL) or multiple (m) URLs (CSV)')

      parser.add_argument('path_or_url',
                             metavar='path',
                             type=str,
                             help='URL or path to csv file')

      parser.add_argument('api_key',
                             type=str,
                             help='Your API key')

      args = parser.parse_args()

      if args.n == 'm':

          url_list = open(args.path_or_url, 'r')
      
          with open('psi_results_' + str(int(time.time())) + '.csv', 'w') as csvresults:
                  results_writer = csv.writer(csvresults, delimiter=',')
                  results_writer.writerow(['URL', 'Speed Index', 'CLS', 'LCP', 'FID', 'TBT', 'FCP', 'TTI'])
      
                  count = 1
                  for url in url_list:
                      print(count, end = '\r')
                      params = {
                          'url': url.strip(),
                          'strategy': 'mobile',
                          'category': ['performance'],
                          'key': args.api_key
                      }
      
                      response = requests.get(PSI_URL, params)
      
                      speed_index = str(response.json()['lighthouseResult']['audits']['speed-index']['score'] * 100)
                      CLS = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['cumulativeLayoutShift'])
                      LCP = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['largestContentfulPaint'])
                      FID = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['maxPotentialFID'])
                      TBT = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['totalBlockingTime'])
                      FCP = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['firstContentfulPaint'])
                      TTI = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['interactive'])
      
                      results_writer.writerow([url.strip(), speed_index, CLS, LCP, FID, TBT, FCP, TTI])
      
                      count += 1
      
      else:
        params = {
                'url': args.path_or_url,
                'strategy': 'mobile',
                'category': ['performance'],
                'key': args.api_key
        }

        response = requests.get(PSI_URL, params)

        print('Speed Index: ' + str(response.json()['lighthouseResult']['audits']['speed-index']['score'] * 100))
        print('CLS: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['cumulativeLayoutShift']))
        print('LCP: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['largestContentfulPaint']))
        print('FID: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['maxPotentialFID']))
        print('TBT: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['totalBlockingTime']))
        print('FCP: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['firstContentfulPaint']))
        print('TTI: ' + str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['interactive']))

        print('For one URL you may want to check https://pagespeed.web.dev/')




