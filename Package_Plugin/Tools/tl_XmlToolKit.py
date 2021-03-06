# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of XML
import os

from Package_Plugin.mod_GlobalStaticVars import GlobalStaticVars

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree


class XmlToolKit:

    def __init__(self):
        pass

    @staticmethod
    def doc2XmlFile(_doc, fileName):
        pass

    @staticmethod
    def loadManifest(_manifestPath):
        try:
            tree = ElementTree.parse(_manifestPath)
            manifest = tree.getroot()
            return manifest
        except Exception, e:
            print 'loadManifest fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中的package
    @staticmethod
    def getManifestPackageName(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            return manifest.get('package')
        except Exception, e:
            print 'getAndroidManifestPackageName fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中application的name
    @staticmethod
    def getManifestXmlApplicationName(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            application = manifest.find('application')
            return application.get(GlobalStaticVars.__ANDROID_NS__ + 'name')
        except Exception, e:
            print 'getManifestXmlApplicationName fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中application的appName
    @staticmethod
    def getManifestAppNameValue(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            application = manifest.find('application')
            return application.get(GlobalStaticVars.__ANDROID_NS__ + 'label')[8:]
        except Exception, e:
            print 'getManifestAppName fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中application的iconName
    @staticmethod
    def getManifestXmlIconNameValue(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            application = manifest.find('application')
            return application.get(GlobalStaticVars.__ANDROID_NS__ + 'icon')[10:]
        except Exception, e:
            print 'getManifestXmlIconNameValue fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml重的package
    @staticmethod
    def updateManifestXmlPackageName(_manifestPath, _packageName):
        try:
            tree = ElementTree.parse(_manifestPath)
            manifest = tree.getroot()
            manifest.set('package', _packageName)
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'updateManifestXmlPackageName fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml中的versionCode和versionName
    @staticmethod
    def updateManifestXmlVersionCodeAndName(_manifestPath, _versionCode, _versionName):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            manifest = tree.getroot()
            if 'platformBuildVersionCode' in manifest.attrib:
                print 'delete platformBuildVersionCode'
                del manifest.attrib['platformBuildVersionCode']
            if 'platformBuildVersionName' in manifest.attrib:
                print 'delete platformBuildVersionName'
                del manifest.attrib['platformBuildVersionName']
            manifest.set(GlobalStaticVars.__ANDROID_NS__ + 'versionCode', _versionCode)
            manifest.set(GlobalStaticVars.__ANDROID_NS__ + 'versionName', _versionName)
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'updateManifestXmlVersionCode fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml中application的label
    @staticmethod
    def updateManifestXmlApplicationLabel(_manifestPath, _newLabel):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            application.set(GlobalStaticVars.__ANDROID_NS__ + 'label', _newLabel)
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'updateManifestXmlApplicationLabel fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个Activity
    @staticmethod
    def removeManifestXmlActivity(_manifestPath, _activityName):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            activity = application.find(
                "./activity[@" + GlobalStaticVars.__ANDROID_NS__ + "name'" + _activityName + "']")
            if activity is not None:
                application.remove(activity)
            else:
                print 'can not find the ' + _activityName
                return
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'removeManifestXmlActivity fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个service
    @staticmethod
    def removeManifestXmlService(_manifestPath, _serviceName):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            service = application.find("./service[@" + GlobalStaticVars.__ANDROID_NS__ + "name'" + _serviceName + "']")
            if service is not None:
                application.remove(service)
            else:
                print 'can not find the ' + _serviceName
                return
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'removeManifestXmlService fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个receiver
    @staticmethod
    def removeManifestXmlReceiver(_manifestPath, _receiverName):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            receiver = application.find(
                "./receiver[@" + GlobalStaticVars.__ANDROID_NS__ + "name'" + _receiverName + "']")
            if receiver is not None:
                application.remove(receiver)
            else:
                print 'can not find the ' + _receiverName
                return
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'removeManifestXmlReceiver fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个provider
    @staticmethod
    def removeManifestXmlProvider(_manifestPath, _providerName):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            provider = application.find(
                "./provider[@" + GlobalStaticVars.__ANDROID_NS__ + "name'" + _providerName + "']")
            if provider is not None:
                application.remove(provider)
            else:
                print 'can not find the ' + _providerName
                return
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'removeManifestXmlProvider fail , error msg : ' + str(e)

    # 往AndroidManifest.xml文件application节点修改或增加meta-data子节点
    @staticmethod
    def updateManifestXmlMetaDataValue(_manifestPath, _metaDataName, _metaDataValue):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            metaData = application.find(
                "./meta-data[@" + GlobalStaticVars.__ANDROID_NS__ + "name='" + _metaDataName + "']")
            if metaData is None:
                ElementTree.SubElement(application, 'meta-data',
                                       {GlobalStaticVars.__ANDROID_NS__ + 'name': _metaDataName,
                                        GlobalStaticVars.__ANDROID_NS__ + 'value': _metaDataValue})
            else:
                metaData.set(GlobalStaticVars.__ANDROID_NS__ + 'value', _metaDataValue)
            tree.write(_manifestPath, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'updateManifestXmlMetaDataValue fail , error msg : ' + str(e)

    # 筛选母包和渠道的xml文件
    @staticmethod
    def dealValuesXml():
        try:
            values = ['string', 'color', 'dimen', 'style']
            for xml in os.listdir(GlobalStaticVars.__OUTPUT_RES_PATH__ + '/values'):
                if 'origin' not in xml:
                    for i in values:
                        if i in xml:
                            origin = GlobalStaticVars.__OUTPUT_RES_PATH__ + '/values/origin_' + i + 's.xml'
                            channel = GlobalStaticVars.__OUTPUT_RES_PATH__ + '/values/' + i + 's.xml'
                            XmlToolKit.checkValuesXml(origin, channel, i)
        except Exception, e:
            print 'dealValuesXml fail , error msg : ' + str(e)

    # 处理values下xml中的重复字段
    @staticmethod
    def checkValuesXml(_originXml, _channelXml, _flag):
        try:
            ElementTree.register_namespace('android', GlobalStaticVars.__ANDROID_NS__WRITE__)
            originTree = ElementTree.parse(_originXml)
            channelTree = ElementTree.parse(_channelXml)
            originResources = originTree.getroot()
            channelResources = channelTree.getroot()
            for channelItem in channelResources.findall(_flag):
                for originItem in originResources.findall(_flag):
                    if channelItem.get('name') == originItem.get('name'):
                        originItem.set('name', originItem.get('name') + '1')
            originTree.write(_originXml, xml_declaration=True, encoding='utf-8', method='xml')
        except Exception, e:
            print 'dealValuesXml fail , error msg : ' + str(e)
