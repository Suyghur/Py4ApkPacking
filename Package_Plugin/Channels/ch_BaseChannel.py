# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description : the base channel clz
import abc

from Package_Plugin import GlobalStaticVars
from Package_Plugin.Tools.tl_ApkToolKit import ApkToolKit
from Package_Plugin.Tools.tl_FileToolKit import FileToolKit


class BaseChannel:
    __metaclass__ = abc.ABCMeta

    # 复制渠道资源
    @abc.abstractmethod
    def copyChannelResource(self):
        pass

    # 修改渠道资源
    @abc.abstractmethod
    def modifyChannelConfig(self, _channelConfig):
        pass

    # 重编译,签名并生成渠道Apk文件
    @abc.abstractmethod
    def generateChannelApk(self, _apkLabel, _signFilePath, _signAlias, _signPwd):
        pass

    # 清除apks目录的output文件夹(如果存在),拷贝根目录output文件夹至apks目录
    @staticmethod
    def copyOutputDir():
        print 'copyOutputDir'
        return True

    # 拷贝tool/channels/渠道/assets目录的文件(如果存在)至apks/output/assets目录
    @staticmethod
    def copyAssets(_channelAssetsPath):
        print 'copyAssets'
        return True

    # 拷贝tool/channels/渠道/res目录的文件(如果存在)至apks/output/res目录
    @staticmethod
    def copyRes(_channelResPath):
        print 'copyRes'
        return True

    # 拷贝tool/channels/渠道/lib目录的文件(如果存在)至apks/output/lib目录
    @staticmethod
    def copyLib(_channelLibPath):
        print 'copyLib'
        return True

    # 拷贝tool/channels/渠道/smali目录的文件至apks/output/smali目录
    @staticmethod
    def copySmali(_channelSmaliPath):
        print 'copySmali'
        return True

    # 替换AndroidManifest.xml中的特殊permission和application节点
    @staticmethod
    def replacePermissionAndApplicationNode(_permissionConfig, _applicationConfig):
        print 'replacePermissionAndApplicationNode'
        return True

    # 获取并处理通用渠道参数配置
    @staticmethod
    def dealCommonChannelConfig(_channelConfig, _isMoreIcon=False):
        print 'dealCommonChannelConfig'
        return True

    # 处理横竖屏和闪屏
    @staticmethod
    def dealOrientationAndSplash(_hasSplash=False, _channelSplashPath=None):
        print 'dealOrientationAndSplash'
        return True

    # 重编译
    @staticmethod
    def reCompile():
        if ApkToolKit.compileApk(GlobalStaticVars.__OUTPUT_PATH__, GlobalStaticVars.__APKS_PATH__):
            print 'reCompile success'
            return True
        else:
            print 'reCompile fail'
            return False

    # 重签名
    @staticmethod
    def reSigned(_apkLabel, _signFilePath, _signPwd, _signFileAlias):
        if ApkToolKit.signedApk(GlobalStaticVars.__APKS_PATH__, GlobalStaticVars.__APKS_PATH__ + '/' + _apkLabel,
                                _signFilePath, _signPwd, _signFileAlias):
            print 'reSigned success'
            return True
        else:
            print 'reSigned fail'
            return False

    # 清除临时文件
    @staticmethod
    def clearTempFile():
        if FileToolKit.deleteFile(GlobalStaticVars.__APKS_PATH__):
            print 'clearTempFile success'
            return True
        else:
            print 'clearTempFile fail'
            return False
