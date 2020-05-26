import requests
from lxml import etree
import time
def get_all_proxy():
    url = 'http://www.xicidaili.com/nn/1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html_ele = etree.HTML(response.text)
    ip_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
    port_ele = html_ele.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
    proxy_list = []
    for i in range(0,len(ip_eles)):
        proxy_str = 'http://' + ip_eles[i] + ':' + port_ele[i]
        proxy_list.append(proxy_str)
    return proxy_list

def check_all_proxy(proxy_list):
    valid_proxy_list = []
    for proxy in proxy_list:
        url = 'http://music.163.com/'
        proxy_dict = {
            'http': proxy
        }
        try:
            start_time = time.time()
            response = requests.get(url, proxies=proxy_dict, timeout=5)
            if response.status_code == 200:
                end_time = time.time()
                print('代理可用：' + proxy)
                print('耗时:' + str(end_time - start_time))
                valid_proxy_list.append(proxy)
                return valid_proxy_list
            else:
                print('代理超时')
        except:
            print('代理不可用--------------->'+proxy)
    return valid_proxy_list

if __name__ == '__main__':
    proxy_list = get_all_proxy()
    valid_proxy_list = check_all_proxy(proxy_list)
    print('--'*30)
    print(valid_proxy_list)

