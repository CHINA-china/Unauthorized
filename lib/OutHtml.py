import time
from lib import InitInfo


def Html(jsonList):
    table_head = "<!DOCTYPE html>\n" \
                 "<html>\n" \
                 "<head>\n" \
                 "<meta charset='UTF-8'>\n" \
                 "<style type='text/css'>\n" \
                 "a{text-decoration:none}a:link {color:green;text-decoration:none;}\n" \
                 "a:visited {color:green;text-decoration:none;}\n" \
                 "a:hover {color:green;text-decoration:none;}\n" \
                 "a:active {color:green;text-decoration:none;}\n" \
                 "tr{color: red;}\n" \
                 "table {color:#333333; width:100%; border-collapse:collapse; text-align:center;}\n" \
                 "table th {background-color:#97CEFA; padding:8px; border-color:#97CEFA;}\n" \
                 "table td {padding:8px; border-color:#97CEFA;}\n" \
                 "</style>\n" \
                 "</head>\n"

    table_th = ''
    for title in jsonList[0]:
        table_th = table_th + '<th style="color:black">' + str(title) + '</th>'
    table_th = '<tr>' + table_th + '</tr>\n'

    table_tr = ''
    for i in range(0, len(jsonList)):
        for n, m in enumerate(jsonList[i]):
            if n == 0:
                jsonList[i][m] = '<tr><td>' + str(jsonList[i][m])
            table_tr = table_tr + '<a href="{}"    target="_blank">'.format(str(jsonList[i][m])) + str(jsonList[i][m]) + '</a></td><td>'

        table_tr = table_tr[0:-3] + '/tr>\n'
    table_body = "<body>\n" \
                 "<table border='1'>\n" \
                 "<caption>目标：{}</caption>\n".format(InitInfo.Class_InitInfo().url_port)
    table_body = table_body + table_th + table_tr + '</table>\n</body>\n'

    tableCode = table_head + table_body + '</html>'
    filename = InitInfo.Class_InitInfo().url_port
    filename = filename.replace(r":", "_")
    html_write = open(r'reports/'+ filename + "_" + time.strftime('%Y-%m-%d') + '.html', "w",
                      encoding="utf-8")
    html_write.write(tableCode)