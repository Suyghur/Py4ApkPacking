# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-19.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of DexGame
from Package_Plugin.mod_ChannelRouteID import PlatformId


class DexGameToolKit:
    # 星辰奇缘
    __DEX_GAME_XCQY__ = '92'
    # 战争时刻
    __DEX_GAME_ZZSK__ = '131',
    # 战地黎明
    __DEX_GAME_ZDLM__ = '244',
    # 少年御灵师
    __DEX_GAME_SNYLS__ = '312',
    # 风色世界
    __DEX_GAME_FSSJ__ = '330',
    # 三国大亨
    __DEX_GAME_SGDH__ = '1538'

    def __init__(self):
        pass

    @staticmethod
    def isDexGame(_gameId):
        dexGame = [
            DexGameToolKit.__DEX_GAME_XCQY__,
            DexGameToolKit.__DEX_GAME_ZZSK__,
            DexGameToolKit.__DEX_GAME_ZDLM__,
            DexGameToolKit.__DEX_GAME_SNYLS__,
            DexGameToolKit.__DEX_GAME_FSSJ__,
            DexGameToolKit.__DEX_GAME_SGDH__
        ]
        if _gameId in dexGame:
            return True
        else:
            return False

    @staticmethod
    def isDexChannel(_channelId):
        dexChannel = [
            PlatformId.__CHANNEL_QIHU360__,
            PlatformId.__CHANNEL_XIAOMI__,
            PlatformId.__CHANNEL_LENOVO__
        ]

        if _channelId in dexChannel:
            return True
        else:
            return False
