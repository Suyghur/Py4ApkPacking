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
        # 处理values目录下的xml
        KKKToolKit.delete3KStyle(resPath + '/values/styles.xml')
        KKKToolKit.delete3KString(resPath + '/values/strings.xml')
        KKKToolKit.delete3KColor(resPath + '/values/colors.xml')
        KKKToolKit.delete3KDimens(resPath + '/values/dimens.xml')
        KKKToolKit.delete3KIds(resPath + '/values/ids.xml')
        FileToolKit.deleteFile(resPath + '/values/public.xml')

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
    def updateManifestXmlGameId(_manifestPath, _gameId):
        pass

    @staticmethod
    def updateManifestXmlGameName(_manifestPath, _gameName):
        pass

    @staticmethod
    def deal3KChanleId(_channelConfig):
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
                    resources.remove(item)
            tree.write(_stylePath, xml_declaration=True, encoding='utf-8', method='xml')
        else:
            print 'delete3KStyle fail , can not find ' + _stylePath

    # 删除strings.xml中3k样式
    @staticmethod
    def delete3KString(_stringPath):
        if FileToolKit.isExist(_stringPath):
            tree = ElementTree.parse(_stringPath)
            resources = tree.getroot()
            for item in resources.findall('string'):
                if 'kkk' in item.get('name'):
                    resources.remove(item)
            tree.write(_stringPath, xml_declaration=True, encoding='utf-8', method='xml')
        else:
            print 'delete3KString fail , can not find ' + _stringPath

    @staticmethod
    def delete3KColor(_colorPath):
        if FileToolKit.isExist(_colorPath):
            tree = ElementTree.parse(_colorPath)
            resources = tree.getroot()
            for item in resources.findall('color'):
                if 'kkk' in item.get('name'):
                    resources.remove(item)
            tree.write(_colorPath, xml_declaration=True, encoding='utf-8', method='xml')
        else:
            print 'delete3KString fail , can not find ' + _colorPath

    @staticmethod
    def delete3KDimens(_dimenPath):
        if FileToolKit.isExist(_dimenPath):
            tree = ElementTree.parse(_dimenPath)
            resources = tree.getroot()
            for item in resources.findall('dimen'):
                if 'kkk' in item.get('name'):
                    resources.remove(item)
            tree.write(_dimenPath, xml_declaration=True, encoding='utf-8', method='xml')
        else:
            print 'delete3KString fail , can not find ' + _dimenPath

    @staticmethod
    def delete3KIds(_idsPath):
        if FileToolKit.isExist(_idsPath):
            tree = ElementTree.parse(_idsPath)
            resources = tree.getroot()
            for item in resources.findall('item'):
                if 'kkk' in item.get('name'):
                    resources.remove(item)
            tree.write(_idsPath, xml_declaration=True, encoding='utf-8', method='xml')
        else:
            print 'delete3KString fail , can not find ' + _idsPath
