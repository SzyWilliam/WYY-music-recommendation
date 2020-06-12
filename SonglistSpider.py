from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import re
from database_demo import db_cls

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class SonglistSpider:
    def __init__(self, url):
        self.url = url
        self.id = int(url.split('=')[1])
        self.songlistName = ''
        self.userid = -1
        self.playNum = -1
        self.favorNum = -1
        self.shareNum = -1
        self.commentsNum = -1
        self.songIdList = []
        self.tagList = []

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = driver = webdriver.Chrome("/Users/william/Desktop/global/chromedriver", options=chrome_options)
        htmlContent = self.getPageSource(self.url)
        self.bs = BeautifulSoup(htmlContent, 'html.parser')

    def getPageSource(self, pageUrl):
        self.driver.get(pageUrl)
        
        WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        )
        
        frame = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(frame)

        return self.driver.page_source

    def getSonglistBasicInfo(self):
        self.songlistName = self.bs.find('h2', {'class':'f-ff2 f-brk'}).get_text()
        self.userid = int(self.bs.find('span', {'class':'name'}).a.attrs['href'].split('=')[1])
        self.playNum = int(self.bs.find('strong', {'id':'play-count'}).get_text())

        raw_fav = self.bs.find('a', {'class': 'u-btni-fav'}).i.get_text()
        self.favorNum = int(raw_fav.replace('(', '').replace(')', ''))

        raw_share = self.bs.find('a', {'class': 'u-btni-share'}).i.get_text()
        self.shareNum = int(raw_share.replace('(', '').replace(')', ''))

        self.commentsNum = int(self.bs.find('span', {'id': 'cnt_comment_count'}).get_text())

    def getAllSongsInList(self):
        link_list = self.bs.findAll('a', {'href': re.compile('/song*')})
        for link in link_list:
            self.songIdList.append(int(link.attrs['href'].split('=')[1]))
        # print(self.songIdList)

    def getAllTags(self, GlobalTagHashMap):
        tag_list = self.bs.findAll('a', {'class': 'u-tag'})
        for tag in tag_list:
            tag_name = tag.get_text()
            # add all the names to global tag hashmap
            tag_index = GlobalTagHashMap.addNewTag(tag_name)
            self.tagList.append(tag_index)

    def getAllContent(self, GlobalTagHashMap):
        try:
            self.getSonglistBasicInfo()
            self.getAllSongsInList()
            self.getAllTags(GlobalTagHashMap)
            return "ok"
        except:
            return "error"


    def get_songlist_infos_list(self):
        # id：               歌单url截取出来的，必须转为整数形式输入，最大支持21亿的数字
        # songlist_name：    歌单名
        # userid：           创建者id
        # play_num：         播放数，整数形式，最大21亿
        # fav_num：          收藏数，整数形式，最大21亿
        # share_num：        转发数，整数形式，最大21亿
        # comments_num：     歌曲评论数量，整数形式，最大800w
        return (self.id, self.songlistName, self.userid, self.playNum, 
                self.favorNum, self.shareNum, self.commentsNum)

    def get_songlist2tag_list(self):
        res = []
        for tag_id = self.tagList:
            res.append((self.id, tag_id))
        return tuple(res)

    def get_songlist2song_list(self):
        res = []
        for song_id in self.songIdList:
            res.append((self.id, songid))
        return tuple(res)

            

    
if __name__ == "__main__":
    slp = SonglistSpider('https://music.163.com/#/playlist?id=4960389142')
    slp.getAllTags(None)
