from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from UserSpider import config_chrome_path, config_is_ubuntu


import threading
def debug_print_thread(msg, exe=True):
    if exe: print('[*', threading.get_ident(), '*]', msg)

class SongSpider:
    def __init__(self, songUrl, proxy_url):
        self.songUrl = songUrl
        self.id = -1
        self.name = ''
        self.album_id = -1
        self.comments_num = -1
        self.similar_song_ids = []
        self.artists = []

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('user-agent={0}'.format('MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'))
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        if config_is_ubuntu:
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--proxy-server={}'.format(proxy_url))
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # debug_print_thread("we are using proxy sever with url " + proxy_url)
        #chrome_options.add_argument('--proxy-server=http://183.165.11.69:4216')

        self.driver = driver = webdriver.Chrome(config_chrome_path, options=chrome_options)
#         script = '''Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
# '''
#         self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})


    def getPageSource(self):

        self.driver.get(self.songUrl)
        
        #WebDriverWait(self.driver, 5).until(
        #    EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        #)
        
        #frame = self.driver.find_elements_by_tag_name('iframe')[0]
        #self.driver.switch_to.frame(frame)

        return self.driver.page_source

    def getIdFromUrl(self):

        return int(self.songUrl.split('=')[1])

    def getSongRequiredTuple(self):
        res = [self.id, self.name, self.album_id, self.comments_num]
        if(len(res) > 5): res = res[0:4]
        res.extend(self.similar_song_ids)
        
        while len(res) < 9:
            res.append(-1)
        return tuple(res)

    def getSongArtistsList(self):
        res = []
        for i in self.artists:
            res.append((self.id, i))
        return res

    def getInfo(self, html):

        try:
            bs = BeautifulSoup(html, 'html.parser')
            title = bs.find('em', {'class', 'f-ff2'}).get_text() 
            self.name = title

            self.id = self.getIdFromUrl()

            album_id = bs.find('a', {'href': re.compile("/album*")})["href"]
            album_id = int(album_id.split('=')[1])
            self.album_id = album_id

            comments = bs.find('span', {'id': 'cnt_comment_count'}).get_text()
            comments = int(comments)
            self.comments_num = comments

            recommands = bs.findAll('a', {'class', 's-fc1'})
            for recommand in recommands:
                recommand_id = int(recommand['href'].split('=')[1])
                self.similar_song_ids.append(recommand_id)


            artists = bs.findAll('a', {'class': 's-fc7', 'href': re.compile('/artist*')})
            for artist in artists:
                artist_id = int(artist['href'].split('=')[1])
                self.artists.append(artist_id)
            return "ok"
        except AttributeError:
            return "error"
        except:
            return "error"
        finally:
            self.driver.close()


#return tuple(tuple(song_info), list[tuples of song_artists])

def timeit(func, **arg):
    start = time.time()
    func(arg)
    end = time.time()
    return (end-start)

if __name__ == "__main__":
    sp = SongSpider('https://music.163.com/#/song?id=186453', 'as')
    start = time.time()
    a = sp.getPageSource()
    print(a)
    end = time.time()
    print('dynamic rendering ' , end-start)
    start = time.time()
    sp.getInfo(a)
    end = time.time()
    print('static analysing ' , end-start)



