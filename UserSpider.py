from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import re
from database_demo import db_cls
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import threading
def debug_print_thread(msg, exe=True):
    if exe: print('[*', threading.get_ident(), '*]', msg)

class UserSpider:
    def __init__(self, Url, proxy_url):
        self.songUrl = Url
        self.id = int(self.songUrl.split('=')[1])
        self.lv = -1
        self.gender = -1

        self.homeUrl = 'https://music.163.com/#/user/home?id='+str(self.id)
        self.followersUrl = 'https://music.163.com/#/user/follows?id=' + str(self.id)
        self.songRankUrl = 'https://music.163.com/#/user/songs/rank?id=' + str(self.id)

        self.recent_song_list = []
        self.follows_id_list = []    
        self.playlists = []

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--proxy-server={}'.format(proxy_url))
        #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('user-agent={0}'.format('MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'))
        debug_print_thread("we are using proxy sever with url " + proxy_url)
        self.driver_home = webdriver.Chrome("../chromedriver", options=chrome_options)
        self.driver_recent_songs = webdriver.Chrome("../chromedriver", options=chrome_options)
        self.driver_follows = webdriver.Chrome("../chromedriver", options=chrome_options)
        script = '''Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
'''
        #self.driver_home.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        #self.driver_recent_songs.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        #self.driver_follows.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

        # HOME INFOMATION PAGE https://music.163.com/#/user/home?id=287829691
        # Followers information page https://music.163.com/#/user/follows?id=287829691
        # all song ranks page https://music.163.com/#/user/songs/rank?id=287829691


    def getPageSource(self, pageUrl, driver):
        driver.get(pageUrl)
        
        WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        )
        
        frame = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.frame(frame)

        return driver.page_source

    def getRecentSongs(self):
        pageSource = self.getPageSource(self.songRankUrl, self.driver_recent_songs)
        bs = BeautifulSoup(pageSource, 'html.parser')
        # print(self.songRankUrl)
        # print(pageSource)
        recent_songs = bs.findAll('a', {'href':re.compile('/song*')})
        # print(recent_songs)
        for i in recent_songs:
            song_id = int(i.attrs['href'].split('=')[1])
            # print(i.get_text())
            self.recent_song_list.append(song_id)
        

    def getUserBasicInfo(self):
        pageSource = self.getPageSource(self.homeUrl, self.driver_home)
        bs = BeautifulSoup(pageSource, 'html.parser')

        userLv = bs.find('span', {'class': 'lev u-lev u-icn2 u-icn2-lev'}).get_text()
        self.lv = int(userLv.replace("'", ""))
        #icn u-icn u-icn-01 this class means the user is a male
        #icn u-icn u-icn-02 02 class means the user is a female
        #icn u-icn u-icn-00 this means the user doesnt specifies its gender

        genderIcon = bs.find('i', {'class': re.compile('icn u-icn u-icn-*')}).attrs['class']
        if 'u-icn-00' in genderIcon:
            self.gender = 0
        elif 'u-icn-01' in genderIcon:
            self.gender = 1
        elif 'u-icn-02' in genderIcon:
            self.gender = 2
        else: self.gender = 0 #default gender

        playlists = bs.findAll('a', {'href': re.compile('/playlist*')})
        for item in playlists:
            playlist_id = int(item.attrs['href'].split('=')[1])
            self.playlists.append(playlist_id)

    def getFollows(self):
        pageSource = self.getPageSource(self.followersUrl, self.driver_follows)
        bs = BeautifulSoup(pageSource, 'html.parser')

        follow_user_lists = bs.findAll('a', {'href': re.compile('/user/home*')})
        for item in follow_user_lists:
            if(item.get_text() == item.attrs['title']):
                userid = int(item.attrs['href'].split('=')[1])
                self.follows_id_list.append(userid)
 

    def UserConditionSatisfy20Songs(self):
        return len(self.recent_song_list) >= 20

       

    def getAllContents(self):
        try:
            self.getRecentSongs()
            if len(self.recent_song_list) < 20:
                return error
            self.getUserBasicInfo()
            self.getFollows()
            return "ok"
        except:
            return "error"

    #return the user info tuple
    def get_user_info(self):
        return (self.id, self.lv, self.gender)

    #return the recent songs user heard as a list
    def get_user2song_list(self):
        res = []
        for song in self.recent_song_list:
            res.append((self.id, song))
        return res


    def get_user2songlist_list(self):
        res = []
        for songlist in self.playlists:
            res.append((self.id, songlist))
        return res

    def get_follow_list(self):
        res = []
        for user in self.follows_id_list:
            res.append((self.id, user))
        return res



if __name__ == "__main__":
    up = UserSpider('https://music.163.com/#/user/home?id=280574719', 'asasasa')
    up.getAllContents()
    print('userinfo', up.get_user_info())
    print('user recent songs', up.get_user2song_list())
    print('user song lists', up.get_user2songlist_list())
    print('user follow list', up.get_follow_list())

    db = db_cls(db_filename="pj_data.db")
    db.write_User_infos(
        user_infos_list=[up.get_user_info()],
        user2song_list=up.get_user2song_list(),
        user2songlist_list=up.get_user2songlist_list(),
        follow_list=up.get_follow_list()
    )
    db.create_index()

    print(db.read_Data(sql_query="Select * FROM User_Table"))
    db.close_db()

