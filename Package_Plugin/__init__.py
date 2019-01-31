# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-11.
# Copyright (c) 2019 3KWan.
# Description : Package_Plugin unit test

from Package_Plugin.mod_BatchChannelPackTool import BatchChannelPackTool

if __name__ == '__main__':
    testChannel = BatchChannelPackTool.checkPlatform('12')
    print type(testChannel)
