# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-11.
# Copyright (c) 2019 3KWan.
# Description : Package_Plugin unit test

from Package_Plugin.mod_GlobalStaticVars import GlobalStaticVars

if __name__ == '__main__':
    for i in range(50):
        print GlobalStaticVars.__APKS_PATH__
