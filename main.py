import os
import requests
import img2pdf
import glob
import shutil
from lxml import html
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

auth = GoogleAuth()
drive = GoogleDrive(auth)

def upload_pdf(path, pdf_name):
    gfile = drive.CreateFile({ 'parents': [{ 'id': str(drive_folder_id) }], 'title': pdf_name})
    gfile.SetContentFile(path)
    gfile.Upload()

def save_pdf(pdf_name, path, output_path):
    images_folder = glob.glob(path + '*.png')
    file_path = './' + output_path + '/' + pdf_name + '.pdf'
    with open(file_path, 'wb') as pdf:
        pdf.write(img2pdf.convert(images_folder))
        upload_pdf(file_path, pdf_name)
    # Remove every .png image
    shutil.rmtree(path)

# Create base folder
try:
    folder_name = 'tmp'
    os.mkdir(folder_name)
except FileExistsError:
    print('Folder already exists.')

# Read values from .env file
with open('.env', 'r') as env:
    for line in env.readlines():
        pair = line.split('=')
        os.environ[pair[0]] = pair[1].rstrip()

chapters = 2 #os.environ['CHAPTERS']
base_url = os.environ['URL']
drive_folder_id = os.environ['DRIVE_FOLDER_ID']
drive_link = os.environ['DRIVE_LINK']

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
    save_pdf('Chapter ' + str(i + 1), "./%s/%s/" %(folder_name, chapter_folder), folder_name)
    print('Chapter ' + str(i + 1) + ' finished!')
print('Finished! Drive link: ' + drive_link)
