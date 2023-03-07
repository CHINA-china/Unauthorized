import re
import requests
import json
import threading
from queue import Queue
from colorama import init
from lib import InitInfo

# 存放字典未授权检测结果
path_list = Queue()

seesion = requests.Session()


class Class_DictUnauthorized(InitInfo.Class_InitInfo):
    def Dict_Unauthorized(self):
        """
        dic_list:字典列表，存放的是dic字典
        dic ：由标题、URL、response的长度构成的字典
        length_list ：所有字典的length字段，用于去除length长度一样的字典
        """
        init(autoreset=True)
        while True:
            # 从对列取元素
            d = dict_queue.get()
            dict_queue.task_done()
            # request请求
            if d['method'] == 'GET':
                response = seesion.get(url=d['url'], headers=self.header,
                                       allow_redirects=False,
                                       verify=False)
            elif d['method'] == 'POST':
                response = seesion.post(url=d['url'], headers=self.header,
                                        allow_redirects=False,
                                        verify=False)
            else:
                continue

            if re.findall(d['re'], response.text) and response.status_code == int(d['state']):
                temp_dict = {
                    'info': d['info'],
                    'url': d['url']
                }
                path_list.put(temp_dict)
            if dict_queue.empty():
                break


# 对列
dict_queue = Queue()


def Threading(Domain, path, dict_path):
    # 对列，put数据

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
            dict_queue.put(temp_dic1)
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
            dict_queue.put(temp_dic2)
            for p in path:
                temp_dic3 = {
                    'url': Domain + p + d['url'],
                    'info': d['info'],
                    're': d['re'],
                    'method': d['method'],
                    'state': d['state'],
                }
                dict_queue.put(temp_dic3)
    # 多线程

    t_list = []
    for t in range(0, 51):
        t = Class_DictUnauthorized()
        t_threading = threading.Thread(target=t.Dict_Unauthorized)
        t_list.append(t_threading)
    for t in t_list:
        t.setDaemon(True)
        t.start()
