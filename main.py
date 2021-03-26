import os
import requests
import json
import re

from function_base import fnGetDirsInDir, fnGetFilesInDir, fnGetFilesInDir2, fnGetFileTime
from function_base import fnEmpty, fnLog, fnBug, fnErr


def read_json(file):
    if(os.path.exists(file) == True):
        file_byte = open(file, 'r', encoding='utf8')
        file_info = file_byte.read()
        result = json.loads(file_info)
        file_byte.close()
    else:
        result = {}
    return result
# 读取JSON


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
    readme_data = ""
    for route_info in route_list:
        (title, path, name) = for_instances(host_list, route_info)
        route_info_str = "title: %s\n\n" % title
        route_info_str += "path: %s\n\n" % path
        route_info_str += "url: [%s](xml/%s \"%s\")" % (path, name, title)
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
    insert = "---start---\n\n"+data+"\n\n---end---"
    # 获取README.md内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(
        r'---start---(.|\n)*?---end---', insert, content, 1)

    with open(file, 'w', encoding='utf-8', newline="\n") as f:
        f.write(new_content)

    fnLog("更新 README 成功")

    return True


def main():
    # 配置路径
    _confg_file = os.path.join(os.getcwd(), "config.json")

    # 配置读取
    _confg_data = read_json(_confg_file)
    _routes = _confg_data["routes"]
    _instances = _confg_data["instances"]

    # README.md
    _readme_file = os.path.join(os.getcwd(), "README.md")

    # xml_dir
    _xml_dir = os.path.join(os.getcwd(), "xml")

    print("-----")

    _readme_data = for_routes(_routes, _instances)

    update_readme(_readme_file, _readme_data)
# main


main()
