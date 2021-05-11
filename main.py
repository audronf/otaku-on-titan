import os
import requests
from lxml import html

try:
    os.mkdir(input('Folder name: '))
except FileExistsError:
    print('Folder already exists.')

# Preset values in key=value format
with open('.env', 'r') as env:
    for line in env.readlines():
        pair = line.split('=')
        os.environ[pair[0]] = pair[1].rstrip()

chapters = os.environ['CHAPTERS']
base_url = os.environ['URL']

for i in range(int(chapters)):
    r = requests.get(base_url + str(i + 1))
    response = html.fromstring(r.text)
    images = response.xpath('//img')
    for img in images:
        print (img.attrib['src'])
