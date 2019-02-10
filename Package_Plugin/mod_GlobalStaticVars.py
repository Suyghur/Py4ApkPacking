# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description :
import time


class GlobalStaticVars:
    def __init__(self):
        pass

    # 读取某个属性时方便所以加上{}
    __ANDROID_NS__ = '{http://schemas.android.com/apk/res/android}'
    __ANDROID_NS__WRITE__ = 'http://schemas.android.com/apk/res/android'

    # 打包工具路径
    __PROJECT_PATH__ = '/Users/suyghur/Android/test'

    # 资源路径
    __PROJECT_RES_PATH__ = __PROJECT_PATH__ + '/res'
    __PROJECT_KEYSTORE_PATH__ = __PROJECT_RES_PATH__ + '/keystore'
    __PROJECT_KEYSTORE_XML_PATH__ = __PROJECT_KEYSTORE_PATH__ + '/keystore.xml'
    __PROJECT_RES_COM_PATH__ = __PROJECT_RES_PATH__ + '/com'
    __PROJECT_RES_CHANNEL_PATH__ = __PROJECT_RES_PATH__ + '/channel'

    # 工具路径
    __TOOLS_PATH__ = __PROJECT_PATH__ + '/tools'
    __TOOLS_DEX_JAR_PATH__ = __TOOLS_PATH__ + '/dx/dx.jar'
    __TOOLS_BAKSMALI_JAR_PATH__ = __TOOLS_PATH__ + '/baksmali/baksmali.jar'
    __TOOLS_APKTOOL_JAR_PATH__ = __TOOLS_PATH__ + '/apktool'

    # 输出目录
    __APKS_PATH__ = '/{0}'.format(int(time.time()))
    __OUTPUT_PATH__ = __APKS_PATH__ + '/out'
    __OUTPUT_ASSETS_PATH__ = __OUTPUT_PATH__ + '/assets'
    __OUTPUT_RES_PATH__ = __OUTPUT_PATH__ + '/res'
    __OUTPUT_LIB_PATH__ = __OUTPUT_PATH__ + '/lib'
    __OUTPUT_SMALI_PATH = __OUTPUT_PATH__ + '/smali'

    # R文件路径
    __PROJECT_TEMP_PATH__ = __APKS_PATH__ + '/temp'
    __PROJECT_TEMP_R_PATH__ = __PROJECT_TEMP_PATH__ + '/r'
