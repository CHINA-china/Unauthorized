import re
import time
import requests
import urllib3
import warnings
from lib import InitInfo
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Class_FindPath(InitInfo.Class_InitInfo):
    def __init__(self):
        super().__init__()
        self.js_path_list = []
        # 数据去重
        self.js_screen = []
        # 删除了的元素列表
        self.remove_list = []
        # 防止重复获取js
        self.js_no_while = []

    def Request_Js(self, user_input_url):
        """
            用于爬取用户传入的url中的js链接，返回一个js列表
            respones：用户传入url的响应包
            js_path_list：获取到的js列表（未清洗）
        """
        respones = requests.get(url=user_input_url, headers=self.header, verify=False)
        if respones.status_code == 200:
            if '.js' in str(user_input_url).split('/')[-1]:
                temp = [str(user_input_url).replace(self.Url_Domain, "")]
                return self.Request_Path(temp)
            else:
                self.js_path_list = re.findall(r'<script.*?src\s*=\s*(?:([\'"])(.*?)\1|([^>\s?]+)).*?>', respones.text)
                self.js_path_list = [match[1] if match[1] != '' else match[2] for match in self.js_path_list]
                # 将获取到的JS列表，进行清洗
                return self.Js_Screen(self.js_path_list)
        else:
            print('[Erro]网站状态码为：{}，请先将网站用浏览器解析，或者检测网站是否可正常访问。'.format(respones.status_code))
            quit()

    def Js_Screen(self, js_path_list):
        """
            用于对Request_Js函数返回的js列表进行过过滤、去重
            js_path_list：Request_Js函数返回值（未清洗的js列表）
            key_list：第三方js库关键字
            js_screen_path_list:经过清洗的js列表
        """
        # 数据去重
        self.js_screen = list(set(js_path_list))
        # 清洗完的列表
        js_screen_path_list = []
        for i in self.js_screen:
            js_screen_path_list.append(i)
        # 定义一个常见第三方js库关键字
        for key in open(r'key/JsKey.txt', encoding='utf-8'):
            key = key.replace("\n", "")
            for js in self.js_screen:
                # 将js和key匹配
                screen_js = re.findall(key, js, re.IGNORECASE)
                # 判断是否匹配上关键字，为true就在列表中删除
                if screen_js:
                    # 匹配上关键字的在列表删除
                    if js in js_screen_path_list:
                        if key == "http" or key == "https":
                            print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time())))
                                  + str(js) + "[远程JS]")
                        else:
                            print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time())))
                                  + str(self.Url_Domain + js)+"[匹配上key：{}]".format(key))
                        self.remove_list.append(js)
                        js_screen_path_list.remove(js)
        for s in self.remove_list:
            if s in js_screen_path_list:
                js_screen_path_list.remove(s)

        temp = []
        for j in js_screen_path_list:
            temp.append(j)
        for js in temp:
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
                    if js in js_screen_path_list:
                        js_screen_path_list.remove(js)
                    js_screen_path_list.append(s_re)
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
        path_list = []
        for js_path in js_screen_path_list:
            respones = requests.get(url=self.Url_Domain + js_path, headers=self.header, verify=False)
            print(
                "[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + str(self.Url_Domain + js_path))
            if respones.status_code == 200:
                re_path1 = re.findall(r"[\'\"]([^\/\>\< \)\(\{\}\,\'\"\\][\w\/]*?\/[\w\/]*?)[\'\"]", respones.text)
                re_path2 = re.findall(
                    r'[\'\"]((?:\/|\.\.\/|\.\/)[^\/\>\< \)\(\{\}\,\'\"\\]+(?:\/[^\/\>\< \)\(\{\}\,\'\"\\]*)*)[\'\"]',
                    respones.text)
                for i in re_path1:
                    if i not in self.js_no_while:
                        path_list.append(i)
                for l in re_path2:
                    if l not in self.js_no_while:
                        path_list.append(l)
                # 去除空列表
                if len(path_list) > 0:
                    lists.extend(path_list)
            else:
                continue
        lists = list(set(lists))
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
        # 定义一个列表，用于下面for循环匹配删除元素使用
        path_screen_list = []
        # 复制path_list的元素进去
        for i in path_list:
            path_screen_list.append(i)
        # js临时列表
        js_temp = []
        # 删除列表
        remove_list = []
        # 循环匹配，去除包含关键字的path
        for path in path_list:
            for key in open(r'key/PathKey.txt', encoding='utf-8'):
                key = key.replace("\n", "")
                # 将path和key匹配
                screen_path = re.findall(key, path, re.IGNORECASE)
                # 判断是否匹配上关键字，为true就在列表中删除
                if screen_path:
                    if path in path_screen_list:
                        path_screen_list.remove(path)
                        remove_list.append(path)
            # 将path里的js分离
            if ".js" in path and path not in self.js_screen:
                # 防止重复循环获取js
                if path not in self.js_no_while:
                    self.js_no_while.append(path)
                    js_temp.append(path)
                    if path in path_screen_list:
                        path_screen_list.remove(path)
            if ".js" not in path:
                if path.split("/")[0] == "":
                    pass
                elif path.split("/")[0] == ".":
                    path_replace = path.replace("./", "/")
                    if path in path_screen_list:
                        path_screen_list.remove(path)
                    if path not in remove_list:
                        path_screen_list.append(path_replace)
                elif path.split("/")[0] == "..":
                    path_replace = path.replace("../", "/")
                    if path in path_screen_list:
                        path_screen_list.remove(path)
                    if path not in remove_list:
                        path_screen_list.append(path_replace)
                else:
                    path_replace = "/" + path
                    if path in path_screen_list:
                        path_screen_list.remove(path)
                    if path not in remove_list:
                        path_screen_list.append(path_replace)
        return path_screen_list, js_temp

    def While_Requests_Js(self, Js_temp):
        path_screen_list, js_temp = self.Js_Screen(Js_temp)
        path_list_tmp = []
        path_list_tmp.extend(path_screen_list)

        if len(js_temp) > 0:
            self.While_Requests_Js(js_temp)
        path_list_tmp = list(set(path_list_tmp))
        return path_list_tmp
