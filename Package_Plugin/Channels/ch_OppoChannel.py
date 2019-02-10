# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-12.
# Copyright (c) 2019 3KWan.
# Description : Oppo channel packaging impl clz
from Package_Plugin import GlobalStaticVars
from Package_Plugin.Channels.ch_BaseChannel import BaseChannel


class OppoChannel(BaseChannel):
    __CHANNEL_PATH__ = GlobalStaticVars.__PROJECT_RES_CHANNEL_PATH__ + '/oppo'
    __ASSETS_PATH__ = __CHANNEL_PATH__ + '/assets'
    __LIB_PATH__ = __CHANNEL_PATH__ + '/lib'
    __RES_PATH__ = __CHANNEL_PATH__ + '/res'
    __SMALI_PATH__ = __CHANNEL_PATH__ + '/smali'
    __PERMISSION_PATH__ = __CHANNEL_PATH__ + '/config/permission.xml'
    __APPLICATION_PATH = __CHANNEL_PATH__ + '/config/application.xml'

    def __init__(self):
        print 'OppoChannel Packing'

    def copyChannelResource(self):
        # 清除apks目录的output文件夹(如果存在),拷贝根目录output文件夹至apks目录
        print '清除apks目录的output文件夹(如果存在),拷贝根目录output文件夹至apks目录'
        if super(OppoChannel, self).copyOutputDir():
            print '拷贝output文件夹成功...'
        else:
            print '拷贝output文件夹失败...'
            return False

        # 拷贝tool/channels/渠道/assets目录的文件(如果存在)至apks/output/assets目录
        print '拷贝tool/channels/渠道/assets目录的文件(如果存在)至apks/output/assets目录'
        if super(OppoChannel, self).copyAssets(''):
            print '拷贝渠道assets文件成功'
        else:
            print '拷贝渠道assets文件失败'
            return False

        # 拷贝tool/channels/渠道/res目录的文件(如果存在)至apks/output/res目录
        print '拷贝tool/channels/渠道/res目录的文件(如果存在)至apks/output/res目录'
        if super(OppoChannel, self).copyRes(''):
            print '拷贝渠道res文件成功'
        else:
            print '拷贝渠道res文件失败'
            return False

        # 拷贝tool/channels/渠道/lib目录的文件(如果存在)至apks/output/lib目录
        print '拷贝tool/channels/渠道/lib目录的文件(如果存在)至apks/output/lib目录'
        if super(OppoChannel, self).copyLib(''):
            print '拷贝渠道lib文件成功'
        else:
            print '拷贝渠道lib文件失败'

        # 拷贝tool/channels/渠道/smali目录的文件至apks/output/smali目录
        print '拷贝tool/channels/渠道/smali目录的文件至apks/output/smali目录'
        if super(OppoChannel, self).copySmali(''):
            print '拷贝渠道smali文件成功'
        else:
            print '拷贝渠道smali文件失败'

        return True

    def modifyChannelConfig(self, _channelConfig):
        # 替换AndroidManifest.xml中的特殊permission和application节点
        print '替换AndroidManifest.xml中的特殊permission和application节点'
        if super(OppoChannel, self).replacePermissionAndApplicationNode('', ''):
            print '替换AndroidManifest.xml成功'
        else:
            print '替换AndroidManifest.xml失败'

        # 获取并处理通用渠道参数配置
        print '获取并处理通用渠道参数配置'
        if super(OppoChannel, self).dealCommonChannelConfig(''):
            print '通用渠道参数配置处理成功'
        else:
            print '通用渠道参数配置处理失败'

        # 处理横竖屏和闪屏
        print '处理横竖屏和闪屏'
        if super(OppoChannel, self).dealOrientationAndSplash():
            print '处理横竖屏和闪屏成功'
        else:
            print '处理横竖屏和闪屏失败'

        return True

    def generateChannelApk(self, _apkLabel, _signFilePath, _signAlias, _signPwd):
        # 重编译
        print '重编译'
        if super(OppoChannel, self).reCompile():
            print '重编译成功'
        else:
            print '重编译失败'

        # 重签名
        print '重签名'
        if super(OppoChannel, self).reSigned(_apkLabel, _signFilePath, _signPwd, _signAlias):
            print '重签名成功'
        else:
            print '重签名失败'

        # 清除临时文件
        print '清除临时文件'
        if super(OppoChannel, self).clearTempFile():
            print '清除临时文件成功'
        else:
            print '清除临时文件失败'

        return True
