import time
from lib import InitInfo
from lib import FindPath
from lib import DictUnauthorized
from lib import PathUnauthorized


def main():
    # 定义请求链接和请求头
    info = InitInfo.Class_InitInfo()
    info.Info()
    findpath = FindPath.Class_FindPath()

    print("[+]目标 " + info.url_protocol + '://' + info.url_port)
    # 爬取path

    print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "正在获取JS文件")
    path_screen_list, js_temp = findpath.Request_Js(info.args.url)
    # 从Path_Screen函数返回的js列表中深入递归提取path
    path_list_tmp = findpath.While_Requests_Js(js_temp)
    # 保存最终提取的path，并去重，除去开头小数点
    path = []
    p_temp = []
    path.extend(path_screen_list)
    path.extend(path_list_tmp)
    path = list(set(path))
    for p_t in path:
        p_temp.append(p_t)
    for p in p_temp:
        if p.split("/")[0] == '.':
            p_re = p.replace(".", "")
            if p in path:
                path.remove(p)
            if p_re not in path:
                path.append(p_re)
    print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time())))
          + "成功获取到", len(path), "个路径")

    # 检测前端泄露path未授权访问
    pathunauthorized = PathUnauthorized.Class_PathUnauthorized()
    pathunauthorized.Path_Unauthorized(path)

    # 检测字典未授权访问
    print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "开始检测字典内路径")
    DictUnauthorized.Threading(InitInfo.Class_InitInfo().Url_Domain, path, InitInfo.Class_InitInfo().args.dict)

    time.sleep(3)
    while True:
        if not DictUnauthorized.dict_queue.empty():
            print("\r" + "[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) +
                  "当前请求剩余:{}".format(DictUnauthorized.dict_queue.qsize()), end="", flush=True)
            if not DictUnauthorized.path_list.empty():
                i = DictUnauthorized.path_list.get()
                DictUnauthorized.path_list.task_done()
                print("\r" + f"\033[1;32m[Success]\033[0m\033[1;31m{i['info']}\033[0m",
                      f"\033[0;33m{i['url']}\033[0m", end='\n')
        else:
            print("\r" + "[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) +
                  "当前请求剩余:0     ")
            break
    print("\r"+"[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "检测已完成")


if __name__ == '__main__':
    main()
