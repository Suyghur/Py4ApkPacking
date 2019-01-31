# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of XML
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree


class XmlToolKit:
    # 读取某个属性时方便所以加上{}
    __ANDROID_NS__ = '{http://schemas.android.com/apk/res/android}'

    __ANDROID_NS__WRITE__ = 'http://schemas.android.com/apk/res/android'

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
            return application.get(XmlToolKit.__ANDROID_NS__ + 'name')
        except Exception, e:
            print 'getManifestXmlApplicationName fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中application的appName
    @staticmethod
    def getManifestAppNameValue(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            application = manifest.find('application')
            return application.get(XmlToolKit.__ANDROID_NS__ + 'label')[8:]
        except Exception, e:
            print 'getManifestAppName fail , error msg : ' + str(e)

    # 获取AndroidManifest.xml中application的iconName
    @staticmethod
    def getManifestXmlIconNameValue(_manifestPath):
        try:
            manifest = XmlToolKit.loadManifest(_manifestPath)
            application = manifest.find('application')
            return application.get(XmlToolKit.__ANDROID_NS__ + 'icon')[10:]
        except Exception, e:
            print 'getManifestXmlIconNameValue fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml重的package
    @staticmethod
    def updateManifestXmlPackageName(_manifestPath, _packageName):
        try:
            tree = ElementTree.parse(_manifestPath)
            manifest = tree.getroot()
            manifest.set('package', _packageName)
            tree.write(_manifestPath)
        except Exception, e:
            print 'updateManifestXmlPackageName fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml中的versionCode和versionName
    @staticmethod
    def updateManifestXmlVersionCodeAndName(_manifestPath, _versionCode, _versionName):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            manifest = tree.getroot()
            if 'platformBuildVersionCode' in manifest.attrib:
                print 'delete platformBuildVersionCode'
                del manifest.attrib['platformBuildVersionCode']
            if 'platformBuildVersionName' in manifest.attrib:
                print 'delete platformBuildVersionName'
                del manifest.attrib['platformBuildVersionName']
            manifest.set(XmlToolKit.__ANDROID_NS__ + 'versionCode', _versionCode)
            manifest.set(XmlToolKit.__ANDROID_NS__ + 'versionName', _versionName)
            tree.write(_manifestPath)
        except Exception, e:
            print 'updateManifestXmlVersionCode fail , error msg : ' + str(e)

    # 更新AndroidManifest.xml中application的label
    @staticmethod
    def updateManifestXmlApplicationLabel(_manifestPath, _newLabel):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            application.set(XmlToolKit.__ANDROID_NS__ + 'label', _newLabel)
            tree.write(_manifestPath)
        except Exception, e:
            print 'updateManifestXmlApplicationLabel fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个Activity
    @staticmethod
    def removeManifestXmlActivity(_manifestPath, _activityName):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            activity = application.find("./activity[@" + XmlToolKit.__ANDROID_NS__ + "name'" + _activityName + "']")
            if activity is not None:
                application.remove(activity)
            else:
                print 'can not find the ' + _activityName
            tree.write(_manifestPath)
        except Exception, e:
            print 'removeManifestXmlActivity fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个service
    @staticmethod
    def removeManifestXmlService(_manifestPath, _serviceName):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            service = application.find("./service[@" + XmlToolKit.__ANDROID_NS__ + "name'" + _serviceName + "']")
            if service is not None:
                application.remove(service)
            else:
                print 'can not find the ' + _serviceName
            tree.write(_manifestPath)
        except Exception, e:
            print 'removeManifestXmlService fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个receiver
    @staticmethod
    def removeManifestXmlReceiver(_manifestPath, _receiverName):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            receiver = application.find("./receiver[@" + XmlToolKit.__ANDROID_NS__ + "name'" + _receiverName + "']")
            if receiver is not None:
                application.remove(receiver)
            else:
                print 'can not find the ' + _receiverName
            tree.write(_manifestPath)
        except Exception, e:
            print 'removeManifestXmlReceiver fail , error msg : ' + str(e)

    # 删除AndroidManifest.xml文件某个provider
    @staticmethod
    def removeManifestXmlProvider(_manifestPath, _providerName):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            provider = application.find("./provider[@" + XmlToolKit.__ANDROID_NS__ + "name'" + _providerName + "']")
            if provider is not None:
                application.remove(provider)
            else:
                print 'can not find the ' + _providerName
            tree.write(_manifestPath)
        except Exception, e:
            print 'removeManifestXmlProvider fail , error msg : ' + str(e)

    # 往AndroidManifest.xml文件application节点修改或增加meta-data子节点
    @staticmethod
    def updateManifestXmlMetaDataValue(_manifestPath, _metaDataName, _metaDataValue):
        try:
            ElementTree.register_namespace('android', XmlToolKit.__ANDROID_NS__WRITE__)
            tree = ElementTree.parse(_manifestPath)
            application = tree.find('.//application')
            metaData = application.find("./meta-data[@" + XmlToolKit.__ANDROID_NS__ + "name='" + _metaDataName + "']")
            if metaData is None:
                ElementTree.SubElement(application, 'meta-data',
                                       {XmlToolKit.__ANDROID_NS__ + 'name': _metaDataName,
                                        XmlToolKit.__ANDROID_NS__ + 'value': _metaDataValue})
            else:
                metaData.set(XmlToolKit.__ANDROID_NS__ + 'value', _metaDataValue)
            tree.write(_manifestPath)
        except Exception, e:
            print 'updateManifestXmlMetaDataValue fail , error msg : ' + str(e)

    @staticmethod
    def dealXml(_xmlPath, _fileType):
        try:
            tree = ElementTree.parse(_xmlPath)
            ElementTree.dump(tree)
        except Exception, e:
            print 'dealXml' + str(e)
