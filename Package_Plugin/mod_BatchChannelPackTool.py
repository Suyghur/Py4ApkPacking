# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description :
from Package_Plugin.Channels import *
from Package_Plugin.Tools.tl_ApkToolKit import ApkToolKit
from Package_Plugin.Tools.tl_KKKToolKit import KKKToolKit


class BatchChannelPackTool:

    def __init__(self):
        pass

    # 检查打包环境
    def checkPackingEnv(self):
        pass

    # 初始化打包环境
    @staticmethod
    def prePackingEnv():
        # 反编译母包
        print '反编译母包'
        if ApkToolKit.decompileApk('a', 'b', 'c'):
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
        base.copyChannelResource()
        base.modifyChannelConfig()
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
