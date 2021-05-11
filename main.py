import os
import requests
from lxml import html

try:
    folder_name = input('Folder name: ')
    os.mkdir(folder_name)
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
    for index, img in enumerate(images, start = 1):
        with open('./' + folder_name + '/' + str(i +1) + '_' + str(index) + '.png', 'wb') as file:
            download = requests.get(img.attrib['src'])
            file.write(download.content)
    print('Chapter ' + str(i + 1) + ' finished!')