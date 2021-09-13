import os
import requests
import json
import yaml
import re
import time

from function_base import fnGetDirsInDir, fnGetFilesInDir, fnGetFilesInDir2, fnGetFileTime
from function_base import fnEmpty, fnLog, fnBug, fnErr

from class_opml import opml
_opml = None

_now = int(time.time())
_local_time = time.localtime(_now)
_local_time_format = time.strftime('%Y-%m-%d %H:%M:%S', _local_time)

# 用于输出 opml
_baseUrl = None

def read_json(file):
    if(os.path.exists(file) == True):
        file_byte = open(file, 'r', encoding='utf8')
        file_info = file_byte.read()
        result = json.loads(file_info)
        file_byte.close()
    else:
        result = {}
    return result
# 读取 JSON


def read_yml(file):
    if(os.path.exists(file) == True):
        file_byte = open(file, 'r', encoding='utf8')
        file_info = file_byte.read()
        result = yaml.load(file_info, Loader=yaml.FullLoader)
        file_byte.close()
    else:
        result = {}
    return result
# 读取 YML


def for_instances(host_list, route_info):
    (title, path) = (route_info["title"], route_info["path"])
    fnLog(title)
    fnLog(path)
    name = path.replace("/", "_")
    for host in host_list:
        url = "%s%s" % (host, path)
        if (get_xml(url, name)):
            fnLog("抓取成功")
            break
        fnLog("---")
    return (title, path, name)
# 遍历 RSSHub 实例


def for_routes(route_list, host_list):
    global _opml, _baseUrl
    readme_data = ""
    for route_info in route_list:
        (title, path, name) = for_instances(host_list, route_info)
        route_info_str = "title: %s\n\n" % title
        route_info_str += "path: [%s](xml/%s.xml \"%s\") 「[raw](xml/%s.xml?raw=true \"%s\")」\n\n" % (
            path, name, title, name, title)
        _opml.addItem(title, '%s/xml/%s.xml' % (_baseUrl, name))
        readme_data += route_info_str
        print("----")
    return readme_data
# 遍历路由


def get_xml(url, name):
    rlt = False
    xml_file = os.path.join(os.getcwd(), "xml/%s.xml" % name)
    fnLog(url)
    try:
        r = requests.get(url, timeout=5)
        fnLog(r.status_code)
        if (r.status_code == 200):
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(r.text)
            rlt = True
    except:
        fnLog("err")
    return rlt
# 抓取内容并写入文件


def update_readme(file, data):
    insert = "---start---\n\n"+_local_time_format+"\n\n"+data+"\n---end---"
    # 获取README.md内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(
        r'---start---(.|\n)*?---end---', insert, content, 1)

    with open(file, 'w', encoding='utf-8', newline="\n") as f:
        f.write(new_content)

    fnLog("更新 README 成功")

    return True
# 更新 readme


def main():
    global _opml, _baseUrl
    _opml = opml()
    # 配置路径
    _confg_json = os.path.join(os.getcwd(), "config.json")
    _config_yml = os.path.join(os.getcwd(), "config.yml")

    # 配置读取
    _confg_data = read_json(_confg_json)
    if not any(_confg_data):
        _confg_data = read_yml(_config_yml)
    # print(_confg_data)
    _routes = _confg_data["routes"]
    _instances = _confg_data["instances"]

    if "baseUrl" in _confg_data:
        _baseUrl = _confg_data["baseUrl"]
    else:
        _baseUrl = ""

    print("-----")

    # README.md
    _readme_file = os.path.join(os.getcwd(), "README.md")

    _readme_data = for_routes(_routes, _instances)

    update_readme(_readme_file, _readme_data)

    # opml 存放
    _out_opml = os.path.join(os.getcwd(), "rss.opml")
    _opml.saveToFile(_out_opml)
    fnLog(["更新 OPML 成功", _out_opml])
    fnLog()
# main


main()

fnLog("当前时间戳：%s, %s" % (_now, _local_time_format))
fnLog()
