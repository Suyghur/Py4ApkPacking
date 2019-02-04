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
    # 读取某个属性时方便所以加上{}
    __ANDROID_NS__ = '{http://schemas.android.com/apk/res/android}'

    __ANDROID_NS__WRITE__ = 'http://schemas.android.com/apk/res/android'

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
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        gmPageActivity = application.find(
            "./activity[@" + KKKToolKit.__ANDROID_NS__ + "name='cn.kkk.commonsdk.GmPageActivity']")
        if gmPageActivity is None:
            ElementTree.SubElement(application, 'activity',
                                   {KKKToolKit.__ANDROID_NS__ + 'name': 'cn.kkk.commonsdk.GmPageActivity',
                                    KKKToolKit.__ANDROID_NS__ + 'screenOrientation': 'portrait',
                                    KKKToolKit.__ANDROID_NS__ + 'configChanges': 'orientation|screenSize|keyboardHidden',
                                    KKKToolKit.__ANDROID_NS__ + 'theme': '@android:style/Theme.Light',
                                    KKKToolKit.__ANDROID_NS__ + 'windowSoftInputMode': 'adjustResize'})
        else:
            gmPageActivity.set(KKKToolKit.__ANDROID_NS__ + 'screenOrientation', 'portrait')
            gmPageActivity.set(KKKToolKit.__ANDROID_NS__ + 'configChanges', 'orientation|screenSize|keyboardHidden')
            gmPageActivity.set(KKKToolKit.__ANDROID_NS__ + 'theme', '@android:style/Theme.Light')
            gmPageActivity.set(KKKToolKit.__ANDROID_NS__ + 'windowSoftInputMode', 'adjustResize')
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def addPermissionsGrantActivity(_manifestPath, _orientation):
        if _orientation == '0':
            screenOrientation = 'landscape'
        else:
            screenOrientation = 'portrait'
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        grantActivity = application.find(
            "./activity[@" + KKKToolKit.__ANDROID_NS__ + "name='cn.impl.common.util.PermissionsGrantActivity']")
        if grantActivity is None:
            ElementTree.SubElement(application, 'activity',
                                   {KKKToolKit.__ANDROID_NS__ + 'name': 'cn.impl.common.util.PermissionsGrantActivity',
                                    KKKToolKit.__ANDROID_NS__ + 'screenOrientation': screenOrientation,
                                    KKKToolKit.__ANDROID_NS__ + 'configChanges': 'orientation|screenSize|keyboardHidden'})
        else:
            grantActivity.set(KKKToolKit.__ANDROID_NS__ + 'screenOrientation', screenOrientation)
            grantActivity.set(KKKToolKit.__ANDROID_NS__ + 'configChanges', 'orientation|screenSize|keyboardHidden')
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def addWelcomeActivity(_manifestPath):
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        # WelcomeAcitivity???
        welcomeActivity = application.find(
            "./activity[@" + KKKToolKit.__ANDROID_NS__ + "name='cn.kkk.commonsdk.WelcomeAcitivity']")
        if welcomeActivity is None:
            ElementTree.SubElement(application, 'activity',
                                   {KKKToolKit.__ANDROID_NS__ + 'name': 'cn.kkk.commonsdk.WelcomeAcitivity',
                                    KKKToolKit.__ANDROID_NS__ + 'configChanges': 'keyboard|keyboardHidden|layoutDirection|navigation|orientation|screenLayout|screenSize|smallestScreenSize'})
        else:
            welcomeActivity.set(KKKToolKit.__ANDROID_NS__ + 'configChanges',
                                'keyboard|keyboardHidden|layoutDirection|navigation|orientation|screenLayout|screenSize|smallestScreenSize')
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def remove3KMetaData(_manifestPath):
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        metaData = application.findall('./meta-data')
        originName = ['3KWAN_Appkey', '3KWAN_ChanleId', '3KWAN_AppID', '3KWAN_Platform_ChanleId', '3KWAN_HasLogo']
        name = []
        # 减少比较次数
        for item in metaData:
            name.append(item.get(KKKToolKit.__ANDROID_NS__ + 'name'))
        for i in originName:
            if i in name:
                application.remove(metaData[name.index(i)])
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def updateManifestXmlGameId(_manifestPath, _gameId):
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        metaData = application.find("./meta-data[@" + KKKToolKit.__ANDROID_NS__ + "name='3KWAN_GAMEID']")
        metaData.set(KKKToolKit.__ANDROID_NS__ + 'value', _gameId)
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def updateManifestXmlGameName(_manifestPath, _gameName):
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        metaData = application.find("./meta-data[@" + KKKToolKit.__ANDROID_NS__ + "name='3KWAN_GAMENAME']")
        metaData.set(KKKToolKit.__ANDROID_NS__ + 'value', _gameName)
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

    @staticmethod
    def deal3KChanleId(_manifestPath, _ChanleId, _PackageId):
        ElementTree.register_namespace('android', KKKToolKit.__ANDROID_NS__WRITE__)
        tree = ElementTree.parse(_manifestPath)
        application = tree.find('.//application')
        chanleId = application.find("./meta-data[@" + KKKToolKit.__ANDROID_NS__ + "name='3KWAN_ChanleId']")
        packageId = application.find("./meta-data[@" + KKKToolKit.__ANDROID_NS__ + "name='3KWAN_PackageID']")
        chanleId.set(KKKToolKit.__ANDROID_NS__ + 'value', _ChanleId)
        packageId.set(KKKToolKit.__ANDROID_NS__ + 'value', _PackageId)
        tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')

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
