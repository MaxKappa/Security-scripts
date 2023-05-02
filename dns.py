### DNS enumeration and subdomain discover script with security trails API
import argparse
import requests
class DNS():

    def __init__(self, url):
        self.url = url
        self.sectrails = 'https://api.securitytrails.com/v1/domain/'+self.url
        self.header = {'apikey': 'token', 'Content-Type': 'application/json'}
        self.subdomain = False


    def dns_enum(self):
        try:
            response = requests.get(self.sectrails, headers=self.header)
            if response.status_code == 200:
                print(response.text)
            else:
                print("[-] Error connecting to API")
        except:
            print("[-] Error connecting to API")

    def subdomain_discover(self):
        self.sectrails += '/subdomains'
        try:
            response = requests.get(self.sectrails, headers=self.header)
            if response.status_code == 200:
                self.parse_subdomain(response)
            else:
                print("[-] Error status code: "+str(response.status_code))
        except:
           print("[-] Error connecting to API")
        
    def parse_subdomain(self, response):
        res = response.json()
        #Banner.banner()
        print("TOTAL SUBDOMAINS: "+str(res['subdomain_count'])+ '\n')
        for line in res['subdomains']:
            print(line+'.'+self.url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS enumeration and subdomain discover script with security trails API')
    parser.add_argument('-u', '--url', help='URL to enumerate', required=True)
    parser.add_argument('-s', '--subdomain', help='Subdomain discover', action='store_true')
    args = parser.parse_args()
    dns = DNS(args.url)
    if args.subdomain:
        dns.subdomain_discover()
    else:
        dns.dns_enum()
