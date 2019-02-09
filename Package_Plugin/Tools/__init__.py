# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : tools unit test
from Package_Plugin.Tools.tl_DexGameToolKit import DexGameToolKit
from Package_Plugin.Tools.tl_FileToolKit import FileToolKit
from Package_Plugin.Tools.tl_KKKToolKit import KKKToolKit
from Package_Plugin.Tools.tl_XmlToolKit import XmlToolKit

if __name__ == '__main__':
    # KKKToolKit.updateManifestXmlGameId('/Users/suyghur/Android/AndroidManifest.xml', '100')
    print DexGameToolKit.isDexGame('92')
