import re
import time
import requests
from lib import InitInfo


class Class_FindPath(InitInfo.Class_InitInfo):

    def Request_Js(self, user_input_url):
        """
            用于爬取用户传入的url中的js链接，返回一个js列表
            respones：用户传入url的响应包
            js_path_list：获取到的js列表（未清洗）
        """
        respones = requests.get(url=user_input_url, headers=self.header, verify=False)
        if respones.status_code == 200:
            js_path_list = re.findall('\<script.*?src=(.*?\.js).*?\<\/script\>', respones.text)
            # 将获取到的JS列表，进行清洗
            return self.Js_Screen(js_path_list)

    def Js_Screen(self, js_path_list):
        """
            用于对Request_Js函数返回的js列表进行过过滤、去重
            js_path_list：Request_Js函数返回值（未清洗的js列表）
            key_list：第三方js库关键字
            js_screen_path_list:经过清洗的js列表
        """
        # 将数据去重
        js_screen = list(set(js_path_list))
        # 定义一个列表，用于下面for循环匹配删除元素使用
        js_screen_path_list = []
        for i in js_screen:
            js_screen_path_list.append(i)
        # 定义一个常见第三方js库关键字
        key_list = ["vue", "react", "jquery", "qrcode", "echart", "viewer", "lazy", "photoswipe", "moment", "day",
                    "video", "swiper", "lodash", "anime", "require", "angular", "/ui", "storage", "base",
                    "util.js"]
        for key in key_list:
            for js in js_screen:
                # 将js和key匹配
                screen_js = re.findall(key, js, re.IGNORECASE)
                # 判断是否匹配上关键字，为true就在列表中删除
                if screen_js:
                    # 匹配上关键字的在列表删除
                    if js in js_screen_path_list:
                        js_screen_path_list.remove(js)
                else:
                    # 对 ./开头的js链接进行去除 .
                    # 既不是./和/开头的直接删除
                    if js.split("/")[0] == "":
                        pass
                    elif js.split("/")[0] == ".":
                        s_re = js.replace("./", "/")
                        if js in js_screen_path_list:
                            js_screen_path_list.remove(js)
                        if s_re not in js_screen_path_list:
                            js_screen_path_list.append(s_re)
                    else:
                        if js.split("/")[0] == '".':
                            s_re = js.replace('".', "")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        elif js.split("/")[0] == "'.":
                            s_re = js.replace("'.", "")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        elif js.split("/")[0] == "'":
                            s_re = js.replace("'", "")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        elif js.split("/")[0] == '"':
                            s_re = js.replace('"', "")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        elif js.split('"')[0] == '':
                            s_re = js.replace('"', "/")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        elif js.split("'")[0] == '':
                            s_re = js.replace("'", "/")
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
                            if s_re not in js_screen_path_list:
                                js_screen_path_list.append(s_re)
                        else:
                            s_re = "/" + js
                            js_screen_path_list.append(s_re)
                            if js in js_screen_path_list:
                                js_screen_path_list.remove(js)
        # 将清洗干净的js进行提取path
        return self.Request_Path(js_screen_path_list)

    def Request_Path(self, js_screen_path_list):
        """
            用于对Js_Screen函数返回的js列表进行请求，获取其中的path路径
            js_screen_path_list：清洗过的js列表
            respones：js的响应包
            path_list：正则匹配到的path
            lists ：返回的path列表
        """
        lists = []
        for js_path in js_screen_path_list:
            respones = requests.get(url=self.Url_Domain + js_path, headers=self.header, verify=False)
            print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time())))+str(self.Url_Domain + js_path))
            if respones.status_code == 200:
                path_list = re.findall(
                    r'[\'"]((?:\/|\.\.\/|\.\/)[^\/\>\< \)\(\{\}\,\'\"\\][^\>\< \)\(\{\}\,\'\"\\]*?)[\'"]',
                    respones.text)
                # 去除空列表
                if len(path_list) > 0:
                    lists.extend(path_list)
            else:
                continue
        return self.Path_Screen(lists)

    def Path_Screen(self, lists):
        """
            用于对Request_Path函数返回的path列表进行过滤、去重
            path_list：Request_Path函数的返回值（未清洗的path列表）
            respones：js的响应包
            path_screen_list：清洗过的path列表
            js_temp：path提取出来的js列表
        """
        # 列表去重
        path_list = list(set(lists))
        key_list = ['.png', 'login', '.jpeg', '.jpg', '.svg', '.vue', '.ttf', '.gif', '.mp4', '.mp3', '.css']
        # 定义一个列表，用于下面for循环匹配删除元素使用
        path_screen_list = []
        # 复制path_list的元素进去
        for i in path_list:
            path_screen_list.append(i)
        # js临时列表
        js_temp = []
        # 循环匹配，去除包含关键字的path
        for path in path_list:
            for key in key_list:
                # 将path和key匹配
                screen_path = re.findall(key, path, re.IGNORECASE)
                # 判断是否匹配上关键字，为true就在列表中删除
                if screen_path:
                    if path in path_screen_list:
                        path_screen_list.remove(path)
                # 如果爬取到js链接，就继续进行js清洗，获取path
            # 将path里提取出来的js和path分离
            if ".js" in path:
                temp = [path]
                js_temp.extend(temp)
        return path_screen_list, js_temp

    def While_Requests_Js(self, Js_temp):
        path_screen_list, js_temp = self.Js_Screen(Js_temp)
        path_list_tmp = []
        path_list_tmp.extend(path_screen_list)
        while True:
            if len(js_temp) > 0:
                self.While_Requests_Js(js_temp)
            else:
                break
        path_list_tmp = list(set(path_list_tmp))
        return path_list_tmp
