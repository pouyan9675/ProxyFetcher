import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import subprocess
import re
import progressbar


def ping_server(ip):
    response = subprocess.Popen(["ping.exe", '-n', '1', '-w', '500', ip], stdout=subprocess.PIPE)
    m = re.findall("time=\d+ms", str(response.communicate()[0]))
    if len(m) > 0:
        return m[0].split('=')[1]
    else:
        return '0'


print('Fetching proxies from server...')
r = requests.get('https://webcache.googleusercontent.com/search?q=cache:i-T5gKOF0GEJ:https://free-proxy-list.net/+&cd=3&hl=en&ct=clnk&gl=ir')

soup = BeautifulSoup(r.content, 'html.parser')
proxies = []
rows = soup.find('tbody').find_all('tr')
pp = []
for row in rows:
    proxy = {}
    tmp = row.find_all('td')
    proxy['ip'] = tmp[0].string
    proxy['port'] = tmp[1].string
    proxy['country'] = tmp[3].string
    proxy['anonymity'] = tmp[4].string
    proxy['update'] = tmp[7].string
    pp.append([proxy['ip'], proxy['port'], proxy['country'], proxy['anonymity'], proxy['update']])
    proxies.append(proxy)

print(tabulate(pp, headers=['IP', 'PORT', 'Country', 'Anonymity', 'Last Update']))
print('Checking servers...')
index = 0
up_servers = []
bar = progressbar.ProgressBar(max_value=100)
for i in range(100):
    proxy = proxies[i]
    ping = ping_server(proxy['ip'])
    if ping is not '0':
        up_servers.append([proxy['ip'], proxy['port'], proxy['country'], proxy['anonymity'], ping])
    index += 1
    bar.update(index)

print(tabulate(up_servers, headers=['IP', 'PORT', 'Country', 'Anonymity', 'Ping']))
