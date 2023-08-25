import re
import json
import warnings
import urllib3
import requests
from colorama import init
from tqdm import tqdm
from lib import InitInfo
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
session = requests.Session()
result_list = []
warnings.simplefilter('ignore', InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)


def check_url(url_dict):
    url = url_dict["url"]
    method = url_dict["method"]
    re_str = url_dict["re"]
    state = url_dict['state']
    try:
        if method == "GET":
            response = session.get(url=url, headers=header,
                                   allow_redirects=False,
                                   verify=False)
            url_dict["length"] = len(response.text)
        else:
            response = session.post(url=url, headers=header,
                                    allow_redirects=False,
                                    verify=False)

        if int(response.status_code) == int(state) and re.search(re_str, response.text) and "#" not in url:
            url_dict["length"] = len(response.text)
            return url_dict
    except:
        pass


url_list = []


def Threading(Domain, path):
    # 字典路径
    dict_path = r'dict\dict.txt'
    if len(path) == 0:
        for d in open(dict_path):
            d = json.loads(d)
            temp_dic1 = {
                'url': Domain + d['url'],
                'info': d['info'],
                're': d['re'],
                'method': d['method'],
                'state': d['state'],
            }
            url_list.append(temp_dic1)

    else:
        for d in open(dict_path):
            d = json.loads(d)
            temp_dic2 = {
                'url': Domain + d['url'],
                'info': d['info'],
                're': d['re'],
                'method': d['method'],
                'state': d['state'],
            }
            url_list.append(temp_dic2)
            for p in path:
                temp_dic3 = {
                    'url': Domain + p + d['url'],
                    'info': d['info'],
                    're': d['re'],
                    'method': d['method'],
                    'state': d['state'],
                }
                url_list.append(temp_dic3)


def main(Thread):
    if Thread is None:
        thread = 50
    else:
        thread = InitInfo.Class_InitInfo().args.threading
    with ThreadPoolExecutor(thread) as executor:
        futures = [executor.submit(check_url, url_dict) for url_dict in url_list]
        results = [future.result() for future in tqdm(futures, total=len(url_list))]

    # 匹配响应包长度，去重
    length_list = []
    for r in results:
        if r is not None:
            length_list.append(r['length'])
    for l in length_list:
        # 设置返回包长度出现的次数
        if length_list.count(l) <= 5:
            for result in results:
                if result is not None:
                    result_list.append(result)

    for result in result_list:
        print("\r" + f"\033[1;32m[Success]\033[0m\033[1;31m{result['info']}\033[0m",
              f"\033[0;33m{result['url']}\033[0m", end='\n')
