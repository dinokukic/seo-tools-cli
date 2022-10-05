from dns import resolver
from smtplib import SMTP
import socket
import socks
import argparse
import time
import csv
import re

def cli():

    parser = argparse.ArgumentParser(
      prog='indx',
      description='Validate if emails exist in bullk')

    parser.add_argument('path_or_url',
                         metavar='path',
                         type=str,
                         help='URL or path to csv file')

    args = parser.parse_args()



    class SocksSMTP(SMTP):

        def __init__(self,
                host='',
                port=0,
                local_hostname=None,
                timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                source_address=None,
                proxy_type=None,
                proxy_addr=None,
                proxy_port=None,
                proxy_rdns=True,
                proxy_username=None,
                proxy_password=None,
                socket_options=None):

            self.proxy_type=proxy_type
            self.proxy_addr=proxy_addr
            self.proxy_port=proxy_port
            self.proxy_rdns=proxy_rdns
            self.proxy_username=proxy_username
            self.proxy_password=proxy_password
            self.socket_options=socket_options
            # if proxy_type is provided then change the socket to socksocket
            # else behave like a normal SMTP class.
            if self.proxy_type:
                self._get_socket = self.socks_get_socket

            super(SocksSMTP, self).__init__(host, port, local_hostname, timeout, source_address)

        def socks_get_socket(self, host, port, timeout):
            if self.debuglevel>0:
                self._print_debug('connect: to', (host, port), self.source_address)
            return socks.create_connection((host, port),
                    timeout=timeout,
                    source_address=self.source_address,
                    proxy_type=self.proxy_type,
                    proxy_addr=self.proxy_addr,
                    proxy_port=self.proxy_port,
                    proxy_rdns=self.proxy_rdns,
                    proxy_username=self.proxy_username,
                    proxy_password=self.proxy_password,
                    socket_options=self.socket_options)


    def getMXRecords(domain):
        try:
            mx_record = resolver.resolve(domain, 'MX')
            exchanges = [exchange.to_text().split() for exchange in mx_record]
            return exchanges
        except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers) as e:
            print(e)
            exchanges = []

    def verifyEmail(email, mx):
        with SocksSMTP(mx) as smtp:
            host_exists = True
            smtp.helo() 
            print(smtp.helo())
            smtp_mail = smtp.mail('hello@linkout.io') 
            resp = smtp.rcpt(email)
            print(resp)
            if resp[0] == 250: 
                return True
            elif resp[0] == 550:
                return False
            else:
                print(resp[0])

    email_list = open(args.path_or_url, 'r')

    filename = 'email_val_' + str(int(time.time())) + '.csv'

    with open(filename, 'w') as status_codes:
        status_writer = csv.writer(status_codes, delimiter=',')
        status_writer.writerow(['Email Address', 'Is Processed', 'Is Valid'])
    
        for email in email_list:
            print('Processing: ' + email)

            valid_format = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

            if valid_format == None:
                status_writer.writerow([email, 'No - Bad Syntax', False])

            domain = email.split("@")[-1]
            mx_records = getMXRecords(domain.strip())
            print(mx_records)
            for m in mx_records:
                try:
                    is_valid = verifyEmail(email, m[1])
                    if is_valid:
                        status_writer.writerow([email, True, True])
                    else:
                        status_writer.writerow([email, True, False])
                except:
                    status_writer.writerow([email, False, False])






















    #####################
        # for email in email_list:
            
        #     valid_format = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        #     if valid_format == None:
        #         status_writer.writerow([email, 'No - Bad Syntax', False])

        #     domain = email.split('@')[1]

        #     records = resolver.query(domain, 'MX')
        #     mxRecord = str(records[0].exchange)

        #     host = socket.gethostname()

        #     server = smtplib.SMTP()
        #     server.set_debuglevel(0)

        #     server.connect(mxRecord)
        #     server.helo(host)
        #     server.mail('test@indx.site')
        #     code, message = server.rcpt(str(addressToVerify))
        #     server.quit()

        #     if code == 250:
        #         status_writer.writerow([email, True, True])
        #     else:
        #         status_writer.writerow([email, True, False])