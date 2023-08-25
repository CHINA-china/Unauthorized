# Unauthorized

### 一款高效率的前端未授权访问检测工具

![logo](https://github.com/CHINA-china/Unauthorize/blob/master/static/logo.png?raw=true)

## 免责声明
- 工具仅可用作学习，以及经过授权的渗透测试，否则后果自负。

## 工具特点

- 内置常见高频未授权访问路径字典
- 自动从前端js文件中提取泄露的接口进行测试
- 采用selenium框架实现对“#”传参网址的测试

## 环境搭建

- **安装依赖库**
```
pip install -r requirements.txt
```

- **下载浏览器driver驱动**

- 查看浏览器版本
![chrome](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/Install/chrome.png?raw=true)
- 下载对应版本驱动（若没有对应版本，可下载相近版本）
```
下载地址：https://registry.npmmirror.com/binary.html?path=chromedriver/                                  
```

![chrome](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/Install/drive1.png?raw=true)

![chrome](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/Install/drive2.png?raw=true)
- 将driver移动到python3根目录
![chrome](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/Install/python3.png?raw=true)

## 使用

- **简单使用**

- ❌使用姿势-->直接传入域名
- ✔使用姿势-->将需要测试的网址先用浏览器访问一遍，再复制地址传入
```
cd Unauthorized
python Unauthorized.py -u http://example.com
```
- **扩展使用**

- 自定义常见未授权路径字典
```
将需要添加的路径按格式添加到dict目录下的dict.txt即可
参数解释：
"info"：提示信息。
"method"：请求方法。
"url"：测试未授权访问的路径。
"state"：响应码，作为判断未授权的条件之一。
"re"：正则匹配关键字，作为判断未授权的条件之一。
```
- 不匹配某些js、path
```
将需要去除的js关键字加入到key目录下的JsKey.txt即可
将需要去除的path关键字加入到key目录下的PathKey.txt即可
```

- 设置超时时间（-t，默认为0.5秒）
```
cd Unauthorized
python Unauthorized.py -u http://example.com -t 3

# 该参数会影响到检测结果，请根据网页打开速度的快慢适当调节
# 当网址打开较慢时可将超时间调大，确保网址正常打开
```

- 设置线程数量（-T，默认为50线程）
```
cd Unauthorized
python Unauthorized.py -u http://example.com -T 100
```
- 只检测字典内路径（-c，程序会爬取path依次与字典内url拼接）
```
cd Unauthorized
python Unauthorized.py -u http://example.com -c
```

- 对单个js内泄露的path检测（-d，程序会将path与参数值拼接）
```
cd Unauthorized
# 网站为 http://example.com  普通格式
python Unauthorized.py -u http://example.com/js/test.js -d http://example.com
# 网站为 http://example.com/#/login  #号格式
python Unauthorized.py -u http://example.com/js/test.js -d http://example.com/#
# 网站为 http://example.com/web/  目录格式
python Unauthorized.py -u http://example.com/js/test.js -d http://example.com/web
```

- **效果展示**
![demo1](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/demo/demo1.png?raw=true)
![demo2](https://github.com/CHINA-china/Unauthorize/blob/master/static/picture/demo/demo2.png?raw=true)


## 更新

v20230825
1. 优化了输出结果。
2. 新增只对字典内路径进行拼接测试。

v20230325
1. 优化了path匹配正则。
2. 新增对单个js文件内的path未授权测试。

v20230319
1. 修复一些问题，增加进度条可视化。

v20230315
1. 增加自定义超时时间、线程数量功能。
2. 增加自定义关键字功能，程序将不匹配含关键字的js、path。


v20230308
1. 优化js提取，解决js重复提取问题。
2. 去除自定义字典功能，新增自动输出html报告功能。


## 引用
- 默认字典来自以下优秀项目：
  1. RouteVulScan (https://github.com/F6JO/RouteVulScan)






