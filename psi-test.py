import requests
import csv
import time

psi_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"



url_list = open('sturls - Sheet2.csv', 'r')

with open('results' + str(int(time.time())) + '.csv', 'w') as csvresults:
        results_writer = csv.writer(csvresults, delimiter=',')
        results_writer.writerow(['URL', 'Speed Index', 'CLS', 'LCP', 'FID', 'TBT', 'FCP', 'TTI'])

        
        for url in url_list:
            count = 1
            params = {
                'url': url.strip(),
                'strategy': 'mobile',
                'category': ['performance'],
                'key': 'AIzaSyDPi9YRsX0qUIXYOIF2s4xxUCZYj5kDOi0'
            }

            response = requests.get(psi_url, params)

            speed_index = str(response.json()['lighthouseResult']['audits']['speed-index']['score'] * 100)
            CLS = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['cumulativeLayoutShift'])
            LCP = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['largestContentfulPaint'])
            FID = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['maxPotentialFID'])
            TBT = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['totalBlockingTime'])
            FCP = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['firstContentfulPaint'])
            TTI = str(response.json()['lighthouseResult']['audits']['metrics']['details']['items'][0]['interactive'])

            results_writer.writerow([url.strip(), speed_index, CLS, LCP, FID, TBT, FCP, TTI])

            count += 1

            print(count, end = '\r')

    
    
    
    
    






