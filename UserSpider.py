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
from selenium.webdriver.common.proxy import ProxyType, Proxy
config_chrome_path = "../chromedriver"
config_is_ubuntu = True



uas=[
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 ",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]


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
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy_url
        prox.ssl_proxy = proxy_url
        # prox.socks_proxy = proxy_url
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        if(config_is_ubuntu):
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('user-agent={0}'.format(random.choice(uas)))
        # debug_print_thread("we are using proxy sever with url " + proxy_url)
        self.driver_home = webdriver.Chrome(config_chrome_path, options=chrome_options, desired_capabilities=capabilities)
        self.driver_recent_songs = webdriver.Chrome(config_chrome_path, options=chrome_options,  desired_capabilities=capabilities)
        #self.driver_recent_songs.set_page_load_timeout(10)
        self.driver_follows = webdriver.Chrome(config_chrome_path, options=chrome_options,  desired_capabilities=capabilities)
#         script = '''Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
# '''
#         self.driver_home.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
#         self.driver_recent_songs.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
#         self.driver_follows.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script}}

        # HOME INFOMATION PAGE https://music.163.com/#/user/home?id=287829691
        # Followers information page https://music.163.com/#/user/follows?id=287829691
        # all song ranks page https://music.163.com/#/user/songs/rank?id=287829691


    def getPageSource(self, pageUrl, driver):
        driver.get(pageUrl)
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        )
        
        frame = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.frame(frame)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )

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
        # if len(self.recent_song_list) < 20:
        #     print(pageSource)
        

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
                return "error"
            self.getUserBasicInfo()
            self.getFollows()
            return "ok"
        except:
            return "error"
        finally:
            self.driver_home.quit()
            self.driver_recent_songs.quit()
            self.driver_follows.quit()

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
    up = UserSpider('https://music.163.com/#/user/home?id=533335591', 'asd')
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
    # db.create_index()

    print(db.read_Data(sql_query="Select * FROM User_Table"))
    db.close_db()

