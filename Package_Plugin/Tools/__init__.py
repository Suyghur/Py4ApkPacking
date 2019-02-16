# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : tools unit test
import json

from Package_Plugin.Tools.tl_JsonToolKit import JsonToolKit

if __name__ == '__main__':
    a=JsonToolKit.file2Json('/Users/suyghur/Android/json.txt')
    print a