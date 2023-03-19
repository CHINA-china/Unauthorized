import time
from lib import DictUnauthorized
from lib import FindPath
from lib import InitInfo
from lib import PathUnauthorized
from lib import OutHtml


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
    pathunauthorized.Path_Unauthorized(path, pathunauthorized.args.time_out)
    # 检测字典未授权访问
    print("[{}]".format(time.strftime('%H:%M:%S', time.localtime(time.time()))) + "开始检测字典内路径")
    DictUnauthorized.Threading(InitInfo.Class_InitInfo().Url_Domain, path)
    DictUnauthorized.main(InitInfo.Class_InitInfo().args.threading)
    # 输出HTML用
    for i in DictUnauthorized.result_list:
        temp = {
            '标题': i['info'],
            '网址': i['url']
        }
        # 利用pathunauthorized对象调用html_reports
        pathunauthorized.html_reports.append(temp)
    if pathunauthorized.html_reports:
        OutHtml.Html(pathunauthorized.html_reports)
        print("\r" + "[{}]".format(
            time.strftime('%H:%M:%S', time.localtime(time.time()))) + "检测已完成，已在reports目录生成报告。")
        return 0
    else:
        print("\r" + "[{}]".format(
            time.strftime('%H:%M:%S', time.localtime(time.time()))) + "检测已完成，不存在未授权。")
        return 0

if __name__ == '__main__':
    main()
