# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-11.
# Copyright (c) 2019 3KWan.
# Description : the manager for plugin
import importlib


class PluginsManager:
    __PACKAGE_PLUGIN_NAME__ = ''

    def __init__(self):
        self.__PACKAGE_PLUGIN_NAME__ = 'Package_Plugin'

    # 动态装载
    # @param _moduleName : 模块名
    # @param _clzName : 类名
    # @param _packageName : 包名
    # @return 类对象
    @classmethod
    def dynamicLoadingPlugin(self, _moduleName, _clzName, _packageName=__PACKAGE_PLUGIN_NAME__):
        mod = importlib.import_module('.' + _moduleName, _packageName)
        return getattr(mod, _clzName)

    # 静态装载
    # @param _moduleName : 模块名
    # @param _clzName : 类名
    # @param _packName : 包名
    # @return 类对象
    @classmethod
    def preLoadingPlugin(self, _moduleName, _clzName, _packageName='Module_Plugin'):
        mod = __import__(_packageName + "." + _moduleName, fromlist=[_clzName])
        return getattr(mod, _clzName)
