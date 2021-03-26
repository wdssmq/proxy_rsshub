# Functions
import os
import time


def fnEmpty(arg):
    return 1
# 什么也不做


def fnLog(msg="", tip=None):
    if not tip is None:
        tip = " ← %s" % tip
    else:
        tip = ""
    if not any(msg):
        print("")
    else:
        print("_%s%s" % (msg, tip))
# 输出信息


def fnBug(msg, tip):
    fnLog("[debug]%s" % msg, tip)
# debug输出


def fnErr(msg, tip=None):
    fnLog("_[err]%s" % msg, tip)
# 错误信息


def fnGetDirsInDir(path):
    return [x for x in os.listdir(path) if os.path.isdir(x)]
# 获取子文件夹


def fnGetFilesInDir(path):
    return [x for x in os.listdir(path) if not os.path.isdir(x)]
# 获取文件夹中的文件


def fnGetFilesInDir2(path, ext):
    return [x for x in os.listdir(path) if not os.path.isdir(x) and os.path.splitext(x)[1] == ext]
# 获取指定后缀的文件


def fnGetFileTime(file):
    # mtime = time.ctime(os.stat(file).st_mtime)  # 文件的修改时间
    # ctime = time.ctime(os.stat(file).st_ctime)  # 文件的创建时间
    mtime = os.stat(file).st_mtime  # 文件的修改时间
    ctime = os.stat(file).st_ctime  # 文件的创建时间
    return (int(mtime), int(ctime))
