import requests
from lxml import etree
import time
from urllib import request
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
        url = 'http://music.163.com/'
        proxy_dict = {
            'http': proxy
        }
        try:
            start_time = time.time()
            response = requests.get(url, proxies=proxy_dict, timeout=5)
            contents = response.content.decode('utf-8')
            if response.status_code == 200 and contents.find("n-for404") == -1:
                # print(contents)
                end_time = time.time()
                print('代理可用：' + proxy)
                print('耗时:' + str(end_time - start_time))
                valid_proxy_list.append(proxy)
                if len(valid_proxy_list) >= 5:
                    return valid_proxy_list
            else:
                print('代理超时')
        except:
            print('代理不可用--------------->'+proxy)
    return valid_proxy_list


def API_read_proxy(API_Url):
    API_Proxys = []
    content = request.urlopen(API_Url).read()
    API_Proxys = content.splitlines()
    for proxy in API_Proxys:
        proxy = "http://" + proxy
    return API_Proxys
    



if __name__ == '__main__':
    proxy_list = API_read_proxy()
    # proxy_list = []
    valid_proxy_list = check_all_proxy(proxy_list)
    print('--'*30)
    print(valid_proxy_list)

