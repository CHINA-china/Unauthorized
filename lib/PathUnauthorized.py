import time
import requests
import urllib3
import warnings
from colorama import init
from functools import reduce
from selenium import webdriver
from lib import InitInfo
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 用于检验print的url状态码
session = requests.Session()
warnings.simplefilter('ignore', InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Class_PathUnauthorized(InitInfo.Class_InitInfo):

    def Path_Unauthorized(self, path, Driver_time):
        """
        dic_list:字典列表，存放的是dic字典
        dic ：由标题、URL、response的长度构成的字典
        length_list ：所有字典的length字段，用于去除length长度一样的字典
        """
        init(autoreset=True)
        # 检测dict路径未授权
        print("\r" + "[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "正在检测未授权访问")
        options = webdriver.ChromeOptions()
        options.add_argument('blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(options=options)
        dic_list = []
        # 设置超时时间，默认为0.5秒
        if Driver_time is None:
            driver_time = 0.5
        else:
            driver_time = self.args.time_out
        # 开始检测未授权访问
        for p in path:
            # 检测前端泄露路径未授权
            driver.set_page_load_timeout(driver_time)  # 设置超时时间
            # 根据网站传参的格式，进行不同的请求，增加运行速度
            if "#" in self.args.url:
                try:
                    driver.get(self.Url_Domain + '/#' + p)
                except Exception:
                    pass
                html = driver.page_source
                title = driver.title
                dic1 = {}
                dic1['title'] = title
                dic1['url'] = self.Url_Domain + '/#' + p
                dic1['length'] = len(html)
                dic_list.append(dic1)
                dic2 = {}
                try:
                    driver.get(self.Url_Domain + p)
                except Exception:
                    pass
                html2 = driver.page_source
                title2 = driver.title
                dic2['title'] = title2
                dic2['url'] = self.Url_Domain + p
                dic2['length'] = len(html2)
                dic_list.append(dic2)
            else:
                dic2 = {}
                try:
                    driver.get(self.Url_Domain + p)
                except Exception:
                    pass
                html2 = driver.page_source
                title2 = driver.title
                dic2['title'] = title2
                dic2['url'] = self.Url_Domain + p
                dic2['length'] = len(html2)
                dic_list.append(dic2)
        length_list = []
        list_temp = []
        for d in dic_list:
            length_list.append(d['length'])
        for l in length_list:
            # 设置返回包长度出现的次数
            if length_list.count(l) == 1:
                for d in dic_list:
                    if l == d['length']:
                        list_temp.append(d)
        # 对字典列表去重
        temp = lambda x, y: x if y in x else x + [y]
        reduce_list = reduce(temp, [[], ] + list_temp)
        for i in reduce_list:
            responses = session.get(url=i['url'], headers=self.header, verify=False)
            if responses.status_code == 200:
                print(f"\033[1;32m[Success]\033[0m\033[1;31m{i['title']}\033[0m",
                      f"\033[0;33m{i['url']}\033[0m")
                # 输出HTML用
                temp = {
                    '标题': i['title'],
                    '网址': i['url']
                }
                self.html_reports.append(temp)
