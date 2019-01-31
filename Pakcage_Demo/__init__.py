# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : demo unit test
from Pakcage_Demo.mod_PluginsManager import PluginsManager

if __name__ == '__main__':
    # ----- 启动时加载 ------
    # no params
    # mod1=__import__('Module_Plugin.Plugin1',fromlist=('Plugin1'))
    # clz1=getattr(mod1,'Plugin1')
    # clz1().PluginPrint()

    # ------ 使用时加载 ------
    # no params
    # mod3 = importlib.import_module('.Plugin1', 'Module_Plugin')
    # clz3=getattr(mod3,'Plugin1')
    # clz3().PluginPrint()

    # have params
    # mod4 = importlib.import_module('.Plugin2', 'Module_Plugin')
    # mod4.PluginPrintWithParam('123')

    # ------ 使用时加载 ------
    manager = PluginsManager()
    med1 = manager.dynamicLoadingPlugin('Channels.ch_OppoChannel', 'OppoChannel')
    med1().copyChannelResource()
