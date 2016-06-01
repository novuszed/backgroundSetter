import subprocess
import os
from socket import timeout
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

def folder_exist():

    if(os.path.exists(path)):
        return 1
    else:
        os.mkdir(path,0o777)

def downloadPhotos():
    counter=0
    for i in photos:

        fileLocation = os.path.join(path,str(counter)+".jpg")
        if(not os.path.isfile(fileLocation)):
            urllib.request.urlretrieve(i,fileLocation)
            counter+=1

def findPhotos():
    link="https://www.reddit.com/r/EarthPorn/"
    try:
        page = urlopen(link)
    except urllib.error.URLError:
        print("URL error. Exiting...")
        return
    except urllib.error.HTTPError:
        print("HTTP error. Exiting...")
        return
    except timeout:
        print("Timed out")
        return
    soup = bs(page.read(),"html.parser")
    pictures = soup.find_all('a', {'class':'thumbnail'}, href=True)

    for i in pictures:
        if(i['href'][0:4]=="http"):
            photos.append(i['href'])

"""

def create_photo_Folder():
    if(not photo_exist()):
        os.mkdir(path, 0755)


def helpMessage():

def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)

"""

def main():
    folder_exist()
    findPhotos()
    downloadPhotos()
if __name__=='__main__':
    main()