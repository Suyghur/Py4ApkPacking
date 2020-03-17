# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/5/7
#
# 此文件用于编写打包脚本的主要逻辑

import os.path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
import os
import os.path
import platform

androidNS = 'http://schemas.android.com/apk/res/android'


def getSdkParamByKey(channel, key):
    if "bagparams" in channel:
        params = channel['bagparams']
        for p in params:
            if p['name'] == key:
                return p['value']

    return None


def getSuperClassNameInSmali(decompileDir, smaliPath):
    f = open(smaliPath, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:

        if line.strip().startswith('.super'):
            line = line[6:].strip()
            return line[1:-1].replace('/', '.')

    return None


def findSmaliPathOfClass(decompileDir, className):
    print("findSmaliPathOfClass:%s", className)

    className = className.replace(".", "/")

    for i in range(1, 10):
        smaliPath = "smali"
        if i > 1:
            smaliPath = smaliPath + str(i)

        path = decompileDir + "/" + smaliPath + "/" + className + ".smali"

        print(path)

        if os.path.exists(path):
            return path

    return None


def findApplicationClass(decompileDir):
    manifestFile = decompileDir + "/AndroidManifest.xml"
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return None

    applicationClassName = applicationNode.get(key)

    return applicationClassName


def findRootApplicationSmali(decompileDir):
    applicationClassName = findApplicationClass(decompileDir)

    if applicationClassName is None:
        Logger.debug("findRootApplicationSmali: applicationClassName:%s", applicationClassName)
        return None

    return findRootApplicationRecursively(decompileDir, applicationClassName)


def findRootApplicationRecursively(decompileDir, applicationClassName):
    smaliPath = findSmaliPathOfClass(decompileDir, applicationClassName)

    if smaliPath is None or not os.path.exists(smaliPath):
        print("smaliPath not exists or get failed.%s", smaliPath)
        return None

    superClass = getSuperClassNameInSmali(decompileDir, smaliPath)
    if superClass is None:
        return None

    if superClass == 'android.app.Application':
        return smaliPath
    else:
        return findRootApplicationRecursively(decompileDir, superClass)


def modifyRootApplicationExtends(decompileDir, applicationClassName):
    applicationSmali = findRootApplicationSmali(decompileDir)
    if applicationSmali is None:
        print("the applicationSmali get failed.")
        return

    print("modifyRootApplicationExtends: root application smali:%s", applicationSmali)

    modifyApplicationExtends(applicationSmali, applicationClassName)


# 将Application改为继承指定的applicationClassName
def modifyApplicationExtends(applicationSmaliPath, applicationClassName):
    print("modify Application extends " + applicationSmaliPath + "; " + applicationClassName)

    applicationClassName = applicationClassName.replace(".", "/")

    f = open(applicationSmaliPath, 'r')
    lines = f.readlines()
    f.close()

    result = ""
    for line in lines:

        if line.strip().startswith('.super'):
            result = result + '\n' + '.super L' + applicationClassName + ';\n'
        elif line.strip().startswith('invoke-direct') and 'android/app/Application;-><init>' in line:
            result = result + '\n' + '      invoke-direct {p0}, L' + applicationClassName + ';-><init>()V'
        elif line.strip().startswith('invoke-super'):
            if 'attachBaseContext' in line:
                result = result + '\n' + '      invoke-super {p0, p1}, L' + applicationClassName + ';->attachBaseContext(Landroid/content/Context;)V'
            elif 'onConfigurationChanged' in line:
                result = result + '\n' + '      invoke-super {p0, p1}, L' + applicationClassName + ';->onConfigurationChanged(Landroid/content/res/Configuration;)V'
            elif 'onCreate' in line:
                result = result + '\n' + '      invoke-super {p0}, L' + applicationClassName + ';->onCreate()V'
            elif 'onTerminate' in line:
                result = result + '\n' + '      invoke-super {p0}, L' + applicationClassName + ';->onTerminate()V'
            else:
                result = result + line

        else:
            result = result + line

    f = open(applicationSmaliPath, 'w')
    f.write(result)
    f.close()

    return 0


# 删除AndroidManifest.xml中指定的组件，比如activity,service,provider等
# typeName:组件类型， 比如activity,service,provider,receiver
# name：组件名称， 比如com.3k.comsdk.UniLoginActivity
def removeMinifestComponentByName(decompileDir, typeName, componentName):
    manifestFile = decompileDir + "/AndroidManifest.xml"
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return

    activityNodeLst = applicationNode.findall(typeName)
    if activityNodeLst is None:
        return

    for activityNode in activityNodeLst:

        name = activityNode.get(key)
        if name == componentName:
            applicationNode.remove(activityNode)
            break

    tree.write(manifestFile, 'UTF-8')
    print("remove " + componentName + " from AndroidManifest.xml")

    return componentName


# 将指定java文件中的类的package值给修改为指定的值
def replaceJavaPackage(javaFile, newPackageName):
    if not os.path.exists(javaFile):
        print("getJavaPackage failed. java file is not exists." + javaFile)
        return 1

    f = open(javaFile, 'r')
    lines = f.readlines()
    f.close()

    content = ""
    for l in lines:
        c = l.strip()
        if c.startswith('package'):
            content = content + 'package ' + newPackageName + ';\r\n'
        else:
            content = content + l

    f = open(javaFile, 'wb')
    f.write(content)
    f.close()

    return 0


# 修改或者替换meta-data  目前只是替换application节点下面的meta-data
def handle_meta_data(tree, meta_data_key, meta_data_value):
    name = "{" + androidNS + "}name"
    value = "{" + androidNS + "}value"
    root = tree.getroot()
    #
    # application_node = root.find("application")
    # if application_node is None:
    #     Logger.error("application node is not exists in AndroidManifest.xml")
    #     return

    b_found = False
    meta_datas = root.find(".//application").findall("meta-data")

    if meta_datas is not None:
        for meta_data in meta_datas:
            if meta_data.get(name) == meta_data_key:
                b_found = True
                meta_data.set(value, str(meta_data_value))
                break

    if not b_found:
        meta_node = SubElement(root.find(".//application"), "meta-data")
        meta_node.set(name, meta_data_key)
        meta_node.set(value, str(meta_data_value))
