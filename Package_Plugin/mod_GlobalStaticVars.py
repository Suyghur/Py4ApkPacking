# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description :


class GlobalStaticVars:
    def __init__(self):
        pass

    # 读取某个属性时方便所以加上{}
    __ANDROID_NS__ = '{http://schemas.android.com/apk/res/android}'

    __ANDROID_NS__WRITE__ = 'http://schemas.android.com/apk/res/android'

    __PROJECT_PATH__ = ''
    __PROJECT_TEMP_PATH__ = ''
    __APKS_PATH__ = ''
    __RES_PATH__ = ''
    __TOOLS_PATH__ = ''

    # 输出目录
    __OUTPUT_PATH__ = __PROJECT_PATH__ + '/out'
    __OUTPUT_ASSETS_PATH__ = __OUTPUT_PATH__ + '/assets'
    __OUTPUT_RES_PATH__ = __OUTPUT_PATH__ + '/res'
    __OUTPUT_LIB_PATH__ = __OUTPUT_PATH__ + '/lib'
    __OUTPUT_SMALI_PATH = __OUTPUT_PATH__ + '/smali'
