# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-02-06.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of create the R file
from Package_Plugin.Tools.tl_CmdToolKit import CmdToolKit
from Package_Plugin.Tools.tl_FileToolKit import FileToolKit
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
    def rBuild(_packageName):
        packageName = _packageName.replace('.', '/')
        path = GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/' + packageName
        bashScript = 'javac -encoding UTF-8 -source 1.6 -target 1.6 ' + path + '/R.java'
        if CmdToolKit.execCmdLine(bashScript):
            print '编译R.java成功'
            return True
        else:
            print '编译R.java失败'
            return False

    # 生成R.java文件的R.jar
    @staticmethod
    def rBuildJar(_packageName):
        firstPackage = _packageName[0:_packageName.index('.')]
        bashScript = 'cd ' + GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + 'jar cvf r.jar ' + firstPackage
        if CmdToolKit.execCmdLine(bashScript):
            print '生成R.jar成功'
            return True
        else:
            print '生成R.jar失败'
            return False

    # 将R.java转化为Dex文件
    @staticmethod
    def rBuildDex():
        bashScript = 'java -jar ' + GlobalStaticVars.__TOOLS_DEX_JAR_PATH__ + ' --dex --output=' + GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/r.dex ' + GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/r.jar'
        if CmdToolKit.execCmdLine(bashScript):
            print '生成R.dex成功'
            return True
        else:
            print '生成R.dex失败'
            return False

    # 生成Smali文件
    @staticmethod
    def rBuildDexOutSamli():
        bashScript = 'java -jar ' + GlobalStaticVars.__TOOLS_BAKSMALI_JAR_PATH__ + ' ' + GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/r.dex --output=' + GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/out'
        if CmdToolKit.execCmdLine(bashScript):
            print '生成R.smali文件成功'
            return True
        else:
            print '生成R.smali文件失败'
            return False

    # 替换Smali文件
    @staticmethod
    def rSamliCopy2Project(_originSmaliPath):
        if FileToolKit.copyFile(GlobalStaticVars.__PROJECT_TEMP_R_PATH__ + '/out', _originSmaliPath):
            print '替换R.smali文件成功'
            return True
        else:
            print '替换R.smali文件失败'
            return False
