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

class SongSpider:
    def __init__(self, songUrl):
        self.songUrl = songUrl
        self.id = -1
        self.name = ''
        self.album_id = -1
        self.comments_num = -1
        self.similar_song_ids = []
        self.artists = []

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = driver = webdriver.Chrome("/Users/william/Desktop/global/chromedriver", options=chrome_options)


    def getPageSource(self):

        self.driver.get(self.songUrl)
        
        WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        )
        
        frame = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(frame)

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


#return tuple(tuple(song_info), list[tuples of song_artists])


