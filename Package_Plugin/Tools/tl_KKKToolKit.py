# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-19.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of 3K_OriginPackage
import os

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

from Package_Plugin.Tools import FileToolKit


class KKKToolKit:

    def __init__(self):
        pass

    @staticmethod
    def dealOriginPkg():
        pass

    @staticmethod
    def deleteAndCopy(_originPkgPath):
        smaliPath = _originPkgPath + '/smali'
        resPath = _originPkgPath + '/res'
        # 删除3K+融合代码
        FileToolKit.deleteFile(smaliPath + '/cn/kkk/commonsdk')
        FileToolKit.deleteFile(smaliPath + '/cn/impl')
        # 删除3K资源
        KKKToolKit.delete3KRes(resPath)

    @staticmethod
    def addGmPageActivity(_manifestPath):
        pass

    @staticmethod
    def addPermissionsGrantActivity(_manifestPath):
        pass

    @staticmethod
    def addWelcomeActivity(_manifestPath):
        pass

    @staticmethod
    def remove3KMetaData(_manifestPath):
        pass

    @staticmethod
    def delete3KRes(_resPath):
        for folder in os.listdir(_resPath):
            # print folder
            for document in os.listdir(_resPath + '/' + folder):
                if 'kkk' in document:
                    FileToolKit.deleteFile(_resPath + '/' + folder + '/' + document)

    # 删除styles.xml中3k样式
    @staticmethod
    def delete3KStyle(_stylePath):
        if FileToolKit.isExist(_stylePath):
            tree = ElementTree.parse(_stylePath)
            resources = tree.getroot()
            for item in resources.findall('style'):
                if 'kkk' in item.get('name') or 'KKK' in item.get('name') or 'radio' in item.get('name'):
                    resources.remove(i)
            tree.write(_stylePath)
        else:
            print 'delete3KStyle fail , can not find ' + _stylePath

    @staticmethod
    def delete3KString(_stringPath):
        if FileToolKit.isExist(_stringPath):
            tree = ElementTree.parse(_stringPath)
            resources = tree.getroot()
            for item in resources.findall('style'):
                if 'kkk' in item.get('name') or 'KKK' in item.get('name') or 'radio' in item.get('name'):
                    resources.remove(i)
            tree.write(_stringPath)
        else:
            print 'delete3KStyle fail , can not find ' + _stringPath

    @staticmethod
    def delete3KColor(_colorPath):
        pass

    @staticmethod
    def delete3KDimens(_dimenPath):
        pass

    @staticmethod
    def delete3KIds(_idsPath):
        pass

    @staticmethod
    def updateManifestXmlGameId(_manifestPath, _gameId):
        pass

    @staticmethod
    def updateManifestXmlGameName(_manifestPath, _gameName):
        pass

    @staticmethod
    def deal3KChanleId(_channelConfig):
        pass
