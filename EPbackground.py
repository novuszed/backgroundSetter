import subprocess
import os
from socket import timeout
import glob
import time
import schedule
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from sys import stdin

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""


photos=[]
#grabs the mac username for directory path
username = os.getlogin()
path = "/Users/%s/Desktop/EP/" % username
picturesList = []
def folder_exist():

    if(os.path.exists(path)):
        return 1
    else:
        os.mkdir(path,0o777)

def downloadPhotos():
    counter=0
    imgurUrlPattern = re.compile(r'(http://imgur.com/(.*))(\?.*)?')
    for i in photos:

        fileLocation = os.path.join(path,str(counter)+".jpg")
        if(not os.path.isfile(fileLocation)):
            opener=urllib.request.URLopener()
            opener.addheader('User-Agent','whatever')
            if 'flickr' in i:
                continue
            if 'http' not in i:
                continue
            if 'http://imgur.com/' in i:
                mo =imgurUrlPattern.search(i)
                imgurFilename = mo.group(2)
                i = "http://i.imgur.com/"+ imgurFilename+".jpg"
#                if '?' in imgurFilename:
#                    imgurFilename = imgurFilename[:imgurFilename.find('?')]

            opener.retrieve(i,fileLocation)
            counter+=1

def findPhotos():
    link="https://www.reddit.com/r/EarthPorn/"
    page = None
    while page is None:
        try:
            page = urlopen(link)
        except urllib.error.URLError:
            print("URL error. Exiting...")

        except urllib.error.HTTPError:
            print("HTTP error. Exiting...")

        except timeout:
            print("Timed out")

    soup = bs(page.read(),"html.parser")
    pictures = soup.find_all('a', {'class':'thumbnail'}, href=True)

    for i in pictures:
        if(i['href'][0:4]=="http"):
            photos.append(i['href'])
    downloadPhotos()

def deletePhotos():
    for photo in picturesList:
        os.remove(photo)
    photos[:]=[]
    initiate()

def findPicturesList():
    picturesList = glob.glob(path+"*.jpg")
    return picturesList
def set_desktop_background():
    picturesList=findPicturesList()
    print(picturesList)
    for filename in picturesList:
        subprocess.Popen(SCRIPT%filename, shell=True)
        print("set at "+filename)
        time.sleep(3598)
    deletePhotos()

def initiate():
    #check if folder exists, if it doesnt, it creates one
    folder_exist()
    #Finds the photos and download them. Try until success
    findPhotos()
    set_desktop_background()
initiate()
schedule.every().minutes.do(set_desktop_background)

while 1:
    schedule.run_pending()
    time.sleep(1)
