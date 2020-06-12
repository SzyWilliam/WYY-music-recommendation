import requests
from lxml import etree
import time
from urllib import request
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from UserSpider import config_chrome_path

def get_all_proxy():
    url = 'https://www.xicidaili.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html_ele = etree.HTML(response.text)
    ip_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
    # print(ip_eles)
    port_ele = html_ele.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
    proxy_list = []
    for i in range(0,len(ip_eles)):
        proxy_str = 'http://' + ip_eles[i] + ':' + port_ele[i]
        proxy_list.append(proxy_str)
    return proxy_list

def check_all_proxy(proxy_list):
    valid_proxy_list = []
    # proxy_list=["http://120.132.52.141:8888"]
    

    for proxy in proxy_list:
        chrome_opt = Options()
        chrome_opt.add_argument('--headless')
        chrome_opt.add_argument("--proxy-server={0}".format(proxy))
        driver = webdriver.Chrome(config_chrome_path, options=chrome_opt)
        driver.set_page_load_timeout(15)
        try:
            driver.get("https://music.163.com")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
        except:
            print(proxy, " reaches a timeout")
            driver.quit()
            continue
        
        source = driver.page_source
        print(source)
        driver.quit()
        valid_proxy_list.append(proxy)
        print(proxy, "available")


    return valid_proxy_list


def API_read_proxy(API_Url):
    API_Proxys = []
    content = request.urlopen(API_Url).read().decode('utf-8')
    API_Proxys = content.splitlines()
    for proxy in API_Proxys:
        proxy = "http://" + proxy
    return API_Proxys
    
def getProxy():
    url = 'http://kuyukuyu.com/agents/get?uuid=a4bbe602-f60a-4a8e-93e1-c2951dda34a8'
    return urlopen(url).read().decode('utf-8')


if __name__ == '__main__':
    # proxy_list = ["http://117.67.74.5:42785"]
    # valid_proxy_list = check_all_proxy(proxy_list)
    # print('--'*30)
    # print(valid_proxy_list)
    getProxy()
