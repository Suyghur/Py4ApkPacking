# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-02-06.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of create the R file
from Package_Plugin.Tools.tl_CmdToolKit import CmdToolKit
from Package_Plugin.mod_GlobalStaticVars import GlobalStaticVars


class RJavaToolKit:

    def __init__(self):
        pass

    # 生成R.java文件
    @staticmethod
    def rCreate():
        genPath = GlobalStaticVars.__PROJECT_TEMP_R_PATH__
        androidJar = GlobalStaticVars.__TOOLS_PATH__ + '/android.jar'
        resPath = genPath + '/res'
        manifestPath = genPath + '/AndroidManifest.xml'
        bashScript = 'aapt package -f -m -J' + genPath + ' -S ' + resPath + ' -I ' + androidJar + ' -M ' + manifestPath
        if CmdToolKit.execCmdLine(bashScript):
            print '生成R.java成功'
            return True
        else:
            print '生成R.java失败'
            return False

    # 编译R.java文件
    @staticmethod
    def rBuild(_packageGenName):
        package = _packageGenName.replace('.', '/')

    # 生成R.java文件的R.jar
    @staticmethod
    def rBuildJar():
        pass

    # 将R.java转化为Dex文件
    @staticmethod
    def rBuildDex():
        pass

    # 生成Smali文件
    @staticmethod
    def rBuildDexOutSamli():
        pass

    # 替换Smali文件
    @staticmethod
    def rSamliCopy2Project():
        pass
