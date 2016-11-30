#!/usr/bin/python
#By Behdad Ahmadi
#Bugs fixed by Mr.Oplus
#Scripted in Python for easy use.
#It first logins to VK.com,then search for music and return links'
#Notice: YOU MUST HAVE A VK.COM ACCOUNT
#Twitter: behdadahmadi@mail.com


import requests
import urllib
from bs4 import BeautifulSoup as bs
import sys
import os
import argparse

reload(sys)
sys.setdefaultencoding('utf8')

headers={"Referer":"https://m.vk.com/login?role=fast&to=&s=1&m=1&email=xx"
,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}

greenColor = '\033[0;32;0m'
grayColor = '\033[0;35;0m'

def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r%2d%%" % percent)
    sys.stdout.flush()

    if percent == 100:
        print grayColor + '  Successfully downloaded\n'

def downloadSong(songLink,title):
    dl_path = os.getcwd()+'/Music/'
    dl_path = os.path.normpath(dl_path)
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
    musicPath = dl_path + "/" +title[0:60] + '.mp3'
    musicPath = os.path.normpath(musicPath)
    if not os.path.exists(musicPath):
        print 'Downloading {0}'.format(title)
        urllib.urlretrieve(songLink.split('?')[0],musicPath,dlProgress)
    else:
        print '{0} is already downloaded'.format(title)
def banner():
    dotname = "-" * 18
    print " "
    print dotname.center(20,'-')
    print ".:: " + 'VKdownloader' + " ::.".center(4)
    print "by Behdad Ahmadi".center(20)
    print "Twitter:behdadahmadi".center(20)
    print dotname.center(20,'-')



def search(text,cred):
    payload = {
        'email': cred[0],
        'pass': cred[1]
    }
    _session = requests.Session()
    login_page = _session.get('https://m.vk.com/login')
    login_url = bs(login_page.content,'html.parser').find('form')['action']
    _session.post(login_url,data=payload,headers=headers)

    search_query = 'https://m.vk.com/audio?act=search&q=' + text
    search_page = _session.get(search_query)
    if 'Not registered' in search_page.content:
        print 'Authenication error : Credentials are incorrect'
        sys.exit()
    items = bs(search_page.content,'html.parser').find_all('div',attrs={'class':'audio_item ai_has_btn'})
    labels = []
    for item in items:
        label = item.find('div',attrs={'class':'ai_label'})('span')
        song = str(label[0].text) + '-' + str(label[2].text) + '[]' + item.find('input')['value'].split('?')[0]
        labels.append(song)

    result = [len(items),labels]
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="your VK Username")
    parser.add_argument("password", help="your VK Password")
    parser.add_argument("song", help="Song Name")
    args = parser.parse_args()
    banner()

    username = args.username
    password = args.password
    query = args.song

    result = search(query,[username,password])
    print "{0} songs has been found".format(str(result[0]))
    print '\n'

    for idx,i in enumerate(result[1]):

        print greenColor + '({0})'.format(str(idx)) + ' ' + i.split('[]')[0]
        print i.split('[]')[1] + '\n'

    songs = raw_input('Select songs to download:\n')
    if '-' in songs:
        try:
            for i in range(int(songs.split('-')[0]),int(songs.split('-')[1])):
                downloadSong(result[1][i].split('[]')[1],result[1][i].split('[]')[0])
        except:
            print 'You select a song out of list'
            sys.exit()
    elif ',' in songs:
        print songs
        try:
            for i in songs.split(','):
                downloadSong(result[1][int(i)].split('[]')[1], result[1][int(i)].split('[]')[0])
        except:
            print 'You select a song out of list'
            sys.exit()
    else:
        try:
            downloadSong(result[1][int(songs)].split('[]')[1],result[1][int(songs)].split('[]')[0])
        except:
            print 'You select a song out of list'
            sys.exit()

if __name__ == '__main__':
    main()
