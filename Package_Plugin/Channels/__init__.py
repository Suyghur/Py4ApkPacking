# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : channels unit test
from Package_Plugin.Channels.ch_OppoChannel import OppoChannel

if __name__ == '__main__':
    baseChannel = OppoChannel()
    baseChannel.copyChannelResource()
    baseChannel.modifyChannelConfig('')
    baseChannel.generateChannelApk('', '', '', '')
