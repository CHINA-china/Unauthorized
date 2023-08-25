import argparse
from colorama import init
from urllib.parse import urlparse



class Class_InitInfo():

    def __init__(self):
        pares = argparse.ArgumentParser(description="eg: python Unauthorized.py -u http://example.com")
        pares.add_argument('-u', '--url', required=True, type=str, help="【必选参数】指定一个URL，浏览器地址栏复制下来的效果更佳")
        pares.add_argument('-t', '--time_out', required=False, type=int, help="【选填参数】设置超时时间，默认0.5秒")
        pares.add_argument('-T', '--threading', required=False, type=int, help="【选填参数】设置线程数量，默认50线程")
        pares.add_argument('-d', '--domain', required=False, type=str, help="【选填参数】测试单个js链接中的path时，将path与该值拼接")
        pares.add_argument('-c', '--common', required=False, action='store_true', help="【选填参数】指定此参数只检测字典内路径")
        self.args = pares.parse_args()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        self._url = urlparse(self.args.url)
        self.js_domain = self.args.domain
        self.url_port = self._url.netloc
        self.url_protocol = self._url.scheme
        self.Url_Domain = self.url_protocol + '://' + self.url_port
        self.html_reports = []

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
        print(f"\033[1;32m{logo}\033[0m")
