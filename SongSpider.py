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
from selenium.webdriver.common.proxy import ProxyType, Proxy
from UserSpider import config_chrome_path, config_is_ubuntu
import random
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
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy_url
        prox.ssl_proxy = proxy_url
        # prox.socks_proxy = proxy_url
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('user-agent={0}'.format(random.choice(uas)))
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        if config_is_ubuntu:
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--proxy-server=http://111.222.141.127:8118')
        # chrome_options.add_argument('--proxy-server={}'.format(proxy_url))
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # debug_print_thread("we are using proxy sever with url " + proxy_url)
        # chrome_options.add_argument('--proxy-server=http://114.98.27.147:4216')

        self.driver = webdriver.Chrome(config_chrome_path, options=chrome_options, desired_capabilities=capabilities)
#         script = '''Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
# '''
#         self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})


    def getPageSource(self):

        self.driver.get(self.songUrl)
        
        WebDriverWait(self.driver, 40).until(
           EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )
        
        frame = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(frame)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )

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
        except:
            print(html)
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



