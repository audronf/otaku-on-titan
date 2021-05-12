import os
import requests
import img2pdf
import glob
from lxml import html

def save_pdf(pdf_name, path):
    images_folder = glob.glob(path + '*.png')
    with open(path + pdf_name + '.pdf', 'wb') as pdf:
        pdf.write(img2pdf.convert(images_folder))
    # Remove every .png image
    for img in images_folder:
        os.remove(img)

# Create base folder
try:
    folder_name = input('Folder name: ')
    os.mkdir(folder_name)
except FileExistsError:
    print('Folder already exists.')

# Read values from .env file
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
    try: 
        chapter_folder = 'Chapter ' + str(i + 1)
        os.mkdir('./' + folder_name + '/' + chapter_folder)
    except FileExistsError:
        print('Folder ' + chapter_folder + ' already exists.')
    for index, img in enumerate(images, start = 0):
        if index != 0:
            with open('./' + folder_name + '/' + chapter_folder + '/' + str(index) + '.png', 'wb') as file:
                download = requests.get(img.attrib['src'])
                file.write(download.content)
    save_pdf('Chapter' + str(i + 1), "./%s/%s/" %(folder_name, chapter_folder))
    print('Chapter ' + str(i + 1) + ' finished!')

