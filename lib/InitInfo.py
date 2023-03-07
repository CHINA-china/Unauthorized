import argparse
from colorama import init
from urllib.parse import urlparse


class Class_InitInfo():

    def __init__(self):
        pares = argparse.ArgumentParser(description="eg: python Unauthorized.py -u http://example.com")
        pares.add_argument('-u', '--url', required=True, type=str, help="【必选参数】指定一个URL，浏览器地址栏复制下来的效果更佳")
        pares.add_argument('-d', '--dict', default='dict\dict.txt', type=str,
                           help="【可选参数】指定自定义的字典，字典格式需和默认字典一致。")
        self.args = pares.parse_args()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        self._url = urlparse(self.args.url)
        self.url_port = self._url.netloc
        self.url_protocol = self._url.scheme
        self.Url_Domain = self.url_protocol + '://' + self.url_port

    def Info(self):
        # """初始化，提示信息"""
        logo = """ 
             _    _                   _   _                _             _ 
            | |  | |                 | | | |              (_)           | |
            | |  | |_ __   __ _ _   _| |_| |__   ___  _ __ _ _______  __| |
            | |  | | '_ \ / _` | | | | __| '_ \ / _ \| '__| |_  / _ \/ _` |
            | |__| | | | | (_| | |_| | |_| | | | (_) | |  | |/ /  __/ (_| |
             \____/|_| |_|\__,_|\__,_|\__|_| |_|\___/|_|  |_/___\___|\__,_|
                                                            {}
              """.format("©Unauthorized")

        init(autoreset=True)
        print(f"\033[1;35m{logo}\033[0m")
