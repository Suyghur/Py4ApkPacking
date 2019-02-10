# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description :
from Package_Plugin import GlobalStaticVars
from Package_Plugin.Channels import *
from Package_Plugin.Tools.tl_ApkToolKit import ApkToolKit
from Package_Plugin.Tools.tl_KKKToolKit import KKKToolKit


class BatchChannelPackTool:

    def __init__(self):
        pass

    # 检查打包环境
    def checkPackingEnv(self):
        # 检查打包传入参数
        # 检查本地配置
        pass

    # 初始化打包环境
    @staticmethod
    def prePackingEnv():
        # 反编译母包
        print '反编译母包'
        if ApkToolKit.decompileApk('a', GlobalStaticVars.__OUTPUT_PATH__, 'c'):
            print '反编译母包成功'
        else:
            print '反编译母包失败'
            return False
        # 母包处理
        if KKKToolKit.dealOriginPkg():
            print '母包资源处理成功'
        else:
            print '母包资源处理失败'
            return False

        return True

    @staticmethod
    def doPacking(_platformId):
        # 初始化BaseChannel
        base = BatchChannelPackTool.checkPlatform(_platformId)
        # 拷贝渠道资源
        base.copyChannelResource()
        # 处理渠道资源
        base.modifyChannelConfig()
        # 回编译并签名
        base.generateChannelApk()
        return True

    @staticmethod
    def finishPacking(self):
        # 打包完成,回调通知
        pass

    # 初始化渠道对象,通过字典模拟switch-case
    # @param _platformId : 渠道id
    # @return 类对象
    @staticmethod
    def checkPlatform(_platformId):
        switcher = {
            '12': OppoChannel()
        }
        return switcher.get(_platformId, 'no platform')
