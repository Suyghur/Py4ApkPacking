# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/5/7
#
# 对于apk包的处理
import os
import shutil
import time
from xml.etree import ElementTree as ET

from PIL import Image

from fcore.base import handle_xml, sdk_helper
from fcore.entity.result import Task
from fcore.util import fio, command, java, fprop
from fcore.util.router import Router

android_ns = 'http://schemas.android.com/apk/res/android'


# def load_apktool_cfg() -> list:
#     ret = ConfigToolkit.read_option_value(App.APP_CONFIG_FILE, "APKTOOL_232_CFG", "group_id")
#     return ret.split(",")

def rename_package_name(decompile_dir, new_package_name):
    """
    替换AndroidManifest.xml中的package,补全缺省的activity、service、provider和receiver写法
    :param decompile_dir:
    :param new_package_name:
    :return:
    """
    manifest = decompile_dir + "/AndroidManifest.xml"
    ET.register_namespace("android", android_ns)
    tree = ET.parse(manifest)
    root = tree.getroot()
    old_package_name = root.attrib.get("package")

    compile_sdk_version = "{" + android_ns + "}compileSdkVersion"
    compile_sdk_version_code_name = "{" + android_ns + "}compileSdkVersionCodename"
    name = "{" + android_ns + "}name"

    # 删除compileSdkVersion和compileSdkVersionCodename
    if compile_sdk_version in root.attrib:
        del root.attrib[compile_sdk_version]

    if compile_sdk_version_code_name in root.attrib:
        del root.attrib[compile_sdk_version_code_name]
    application = root.find(".//application")
    if application is not None:
        activity_list = root.find(".//application").findall("activity")
        service_list = root.find(".//application").findall("service")
        receiver_list = root.find(".//application").findall("receiver")
        provider_list = root.find(".//application").findall("provider")

        # handle activity
        if activity_list is not None and len(activity_list) > 0:
            for activity in activity_list:
                activity_name = activity.get(name)
                if activity_name[0:1] == ".":
                    activity_name = old_package_name + activity_name
                elif activity_name.find(".") == -1:
                    activity_name = old_package_name + "." + activity_name
                activity.set(name, activity_name)

                # 查找intent-filter的action是否需要替换
                intent_filters = activity.findall("intent-filter")
                if intent_filters is None or len(intent_filters) <= 0:
                    continue
                for intent_filter in intent_filters:
                    actions = intent_filter.findall("action")
                    if actions is None or len(actions) <= 0:
                        continue

                    for action in actions:
                        action_name = action.attrib[name]
                        if action_name == old_package_name:
                            action.set(name, new_package_name)
                        # 融合sdk游戏Activity的标记
                        elif action_name == old_package_name + ".MAIN":
                            action.set(name, new_package_name + ".MAIN")

        # handle service
        if service_list is not None and len(service_list) > 0:
            for service in service_list:
                service_name = service.get(name)
                if service_name[0:1] == ".":
                    service_name = old_package_name + service_name
                elif service_name.find(".") == -1:
                    service_name = old_package_name + "." + service_name
                service.set(name, service_name)

        # handle receiver
        if receiver_list is not None and len(receiver_list) > 0:
            for receiver in receiver_list:
                receiver_name = receiver.get(name)
                if receiver_name[0:1] == '.':
                    receiver_name = old_package_name + receiver_name
                elif receiver_name.find('.') == -1:
                    receiver_name = old_package_name + '.' + receiver_name
                receiver.set(name, receiver_name)

        # handle provider
        if provider_list is not None and len(provider_list) > 0:
            for provider in provider_list:
                provider_name = provider.get(name)
                if provider_name[0:1] == ".":
                    provider_name = old_package_name + provider_name
                elif provider_name.find(".") == -1:
                    provider_name = old_package_name + '.' + provider_name
                provider.set(name, provider_name)

    root.set("package", new_package_name)
    tree.write(manifest, "UTF-8")
    return old_package_name


def copyResource(task: Task, sdkDir):
    """
    Copy comsdk resources to the apk decompile dir
        Merge manifest.xml
        Merge all res xml if the xml already exists in target apk.
        copy all others resources
    :return:
    """
    # start to merge manifest.xml
    manifestFrom = sdkDir + "/SDKManifest.xml"
    manifestFromTemp = manifestFrom
    manifestTo = Router.DECOMPILE_PATH + "/AndroidManifest.xml"

    if task.params_info.game_params.game_orientation == 1:  # 'portrait'
        manifestFrom = manifestFrom[:-4] + "_portrait.xml"
    else:
        manifestFrom = manifestFrom[:-4] + "_landscape.xml"

    if not os.path.exists(manifestFrom):
        manifestFrom = manifestFromTemp

    if os.path.exists(manifestFrom):
        # merge into xml
        bRet = mergeManifest(manifestTo, manifestFrom)
        if bRet:
            print("merge manifest file success.")
        else:
            print("merge manifest file failed.")
            return 1

    # copyRes
    copyFrom = sdkDir + "/res"
    copyTo = Router.DECOMPILE_PATH + "/res"

    if os.path.exists(copyFrom):
        copyResToApk(copyFrom, copyTo)

    # copyAssets
    assetsFrom = sdkDir + "/assets"
    assetsTo = Router.DECOMPILE_PATH + "/assets"
    if os.path.exists(assetsFrom):
        copyResToApk(assetsFrom, assetsTo)

    # copyLibs
    libFrom = sdkDir + "/libs"
    libTo = Router.DECOMPILE_PATH + "/lib"
    if os.path.exists(libFrom):
        copyLibs(libFrom, libTo)


def copyChannelSpecialResources():
    """
    Copy channel resources to decompile folder. for example icon resources, assets and so on.
    :return:
    """

    res_path = Router.WORKSPACE_PATH + "/channel"
    targetResPath = Router.DECOMPILE_PATH
    assetsPath = os.path.join(res_path, 'assets')
    libsPath = os.path.join(res_path, 'libs')
    resourcePath = os.path.join(res_path, 'res')

    targetAssetsPath = os.path.join(targetResPath, 'assets')
    targetLibsPath = os.path.join(targetResPath, 'lib')
    targetResourcePath = os.path.join(targetResPath, 'res')

    if os.path.exists(assetsPath):
        copyResToApk(assetsPath, targetAssetsPath)

    if os.path.exists(libsPath):
        copyResToApk(libsPath, targetLibsPath)

    if os.path.exists(resourcePath):
        copyResToApk(resourcePath, targetResourcePath)

    return 0


def mergeManifest(targetManifest, sdkManifest):
    """
    Merge comsdk SdkManifest.xml to the apk AndroidManifest.xml
    :param channel:
    :param targetManifest:
    :param sdkManifest:
    :return:
    """
    if not os.path.exists(targetManifest) or not os.path.exists(sdkManifest):
        print("the manifest file is not exists.targetManifest:" + targetManifest + ";sdkManifest:" + sdkManifest)
        return False

    ET.register_namespace('android', android_ns)
    targetTree = ET.parse(targetManifest)
    targetRoot = targetTree.getroot()

    ET.register_namespace('android', android_ns)
    sdkTree = ET.parse(sdkManifest)
    sdkRoot = sdkTree.getroot()

    f = open(targetManifest, encoding='UTF-8', errors='ignore')
    targetContent = f.read()
    f.close()

    permissionConfigNode = sdkRoot.find('permissionConfig')
    if permissionConfigNode is not None and len(permissionConfigNode) > 0:
        for child in list(permissionConfigNode):
            key = '{' + android_ns + '}name'
            val = child.get(key)
            if val is not None and len(val) > 0:
                attrIndex = targetContent.find(val)
                if -1 == attrIndex:
                    targetRoot.append(child)

    # 不需要对application进行处理
    appConfigNode = sdkRoot.find('applicationConfig')
    appNode = targetRoot.find('application')
    if appConfigNode is not None:
        for child in list(appConfigNode):
            appNode.append(child)

    targetTree.write(targetManifest, 'UTF-8')
    return True


# def copyAppResources(task, decompile_dir):
#     """
#     Copy game res files to apk.
#     :param common:
#     :param game:
#     :param decompile_dir:
#     :return:
#     """
#     resPath = const.ORIGNBAG_PATH + str(task.group_id) + const.SKEW_SIGNAL + str(task.orign_game_id) + "/res"
#     resPath = path_utils.get_full_path(resPath)
#     if not os.path.exists(resPath):
#         Logger.error("the game " + str(task.orign_game_id) + " has no extra res folder")
#         return
#
#     assetsPath = os.path.join(resPath, 'assets')
#     libsPath = os.path.join(resPath, 'libs')
#     resourcePath = os.path.join(resPath, 'res')
#
#     targetAssetsPath = os.path.join(decompile_dir, 'assets')
#     targetLibsPath = os.path.join(decompile_dir, 'lib')
#     targetResourcePath = os.path.join(decompile_dir, 'res')
#
#     copyResToApk(assetsPath, targetAssetsPath)
#     copyResToApk(libsPath, targetLibsPath)
#     copyResToApk(resourcePath, targetResourcePath)


# def copyAppRootResources(task, decompile_dir):
#     """
#     Copy game root files to apk. the files will be in the root path of apk
#     :param common:
#     :param game:
#     :param decompile_dir:
#     :return:
#     """
#     resPath = const.ORIGNBAG_PATH + str(task.group_id) + const.SKEW_SIGNAL + str(task.orign_game_id) + "/root"
#     resPath = path_utils.get_full_path(resPath)
#
#     if not os.path.exists(resPath):
#         return
#
#     targetResPath = path_utils.get_full_path(decompile_dir)
#     copyResToApk(resPath, targetResPath)
#     return


def copyResToApk(copyFrom, copyTo):
    """
    Copy two resource folders
    :param game:
    :param src_dir:
    :param destDir:
    :return:
    """
    if not os.path.exists(copyTo):
        os.makedirs(copyTo)

    if os.path.isfile(copyFrom) and not mergeResXml(copyFrom, copyTo):
        fio.copy_files(copyFrom, copyTo)
        return

    for f in os.listdir(copyFrom):
        sourcefile = os.path.join(copyFrom, f)
        targetfile = os.path.join(copyTo, f)

        if os.path.isfile(sourcefile):
            if not os.path.exists(copyTo):
                os.makedirs(copyTo)

            if mergeResXml(sourcefile, targetfile):
                continue

            if os.path.exists(targetfile):
                fio.del_file_folder(targetfile)

            destfilestream = open(targetfile, 'wb')
            sourcefilestream = open(sourcefile, 'rb')
            destfilestream.write(sourcefilestream.read())
            destfilestream.close()
            sourcefilestream.close()

        if os.path.isdir(sourcefile):
            copyResToApk(sourcefile, targetfile)


def mergeResXml(copyFrom, copyTo):
    """
    Merge all android res xml
    :param copyFrom:
    :param copyTo:
    :return:
    """
    if not os.path.exists(copyTo):
        return False

    aryXml = ['strings.xml', 'styles.xml', 'colors.xml', 'dimens.xml', 'ids.xml', 'attrs.xml',
              'integers.xml', 'arrays.xml', 'bools.xml', 'drawables.xml', 'values.xml']
    basename = os.path.basename(copyFrom)

    if basename in aryXml:

        f = open(copyTo, 'r', encoding='UTF-8')

        targetContent = f.read()
        f.close()
        fromTree = ET.parse(copyFrom)
        fromRoot = fromTree.getroot()
        toTree = ET.parse(copyTo)
        toRoot = toTree.getroot()
        for node in list(fromRoot):
            val = node.get('name')
            if val is not None and len(val) > 0:
                valMatched = '"' + val + '"'
                attrIndex = targetContent.find(valMatched)
                if -1 == attrIndex:
                    toRoot.append(node)
                else:
                    print("The node " + val + " is already exists in " + basename)

        toTree.write(copyTo, 'UTF-8')
        return True
    return False


def copyLibs(srcDir, dstDir):
    """
    copy shared libraries
    :param srcDir:
    :param destDir:
    :return:
    """
    if not os.path.exists(srcDir):
        return

    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    for f in os.listdir(srcDir):
        sourcefile = os.path.join(srcDir, f)
        targetfile = os.path.join(dstDir, f)

        if sourcefile.endswith(".jar"):
            continue

        if os.path.isfile(sourcefile):
            if not os.path.exists(targetfile) or os.path.getsize(targetfile) != os.path.getsize(sourcefile):
                destfilestream = open(targetfile, 'wb')
                sourcefilestream = open(sourcefile, 'rb')
                destfilestream.write(sourcefilestream.read())
                destfilestream.close()
                sourcefilestream.close()

        if os.path.isdir(sourcefile):
            copyLibs(sourcefile, targetfile)


def getAppIconName(decompile_dir):
    """
    从AndroidManifest.xml中获取游戏图标的名称
    :param decompile_dir:
    :return:
    """
    manifestFile = decompile_dir + "/AndroidManifest.xml"
    ET.register_namespace('android', android_ns)
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return "ic_launcher"

    key = '{' + android_ns + '}icon'
    iconName = applicationNode.get(key)

    if iconName is None:
        return "ic_launcher"

    name = ""
    if "/" in iconName:
        results = iconName.split("/")
        name = results[1]
    else:
        name = iconName[10:]
    return name


def append_channel_icon_mark() -> bool:
    """
    自动给游戏图标加上渠道SDK的角标
    没有角标，生成没有角标的ICON
    :param channel:
    :return:
    """
    # 先查询workspace/icon.png,如果存在，则优先以此png为先
    game_icon_path = Router.WORKSPACE_PATH + "/resource/icon.png"
    if not os.path.exists(game_icon_path):
        if os.path.exists(Router.WORKSPACE_PATH + "/resource/icon.jpg"):
            game_icon_path = Router.WORKSPACE_PATH + "/resource/icon.jpg"
        else:
            return True

    rl_img = Image.open(game_icon_path)

    ldpi_size = (36, 36)
    mdpi_size = (48, 48)
    hdpi_size = (72, 72)
    xhdpi_size = (96, 96)
    xxhdpi_size = (144, 144)
    xxxhdpi_size = (192, 192)

    xxxhdpi_icon = rl_img.resize(xxxhdpi_size, Image.ANTIALIAS)
    xxhdpi_icon = rl_img.resize(xxhdpi_size, Image.ANTIALIAS)
    xhdpi_icon = rl_img.resize(xhdpi_size, Image.ANTIALIAS)
    hdpi_icon = rl_img.resize(hdpi_size, Image.ANTIALIAS)
    mdpi_icon = rl_img.resize(mdpi_size, Image.ANTIALIAS)
    ldpi_icon = rl_img.resize(ldpi_size, Image.ANTIALIAS)

    ldpi_path = Router.DECOMPILE_PATH + "/res/drawable-ldpi"
    mdpi_path = Router.DECOMPILE_PATH + "/res/drawable-mdpi"
    hdpi_path = Router.DECOMPILE_PATH + "/res/drawable-hdpi"
    xhdpi_path = Router.DECOMPILE_PATH + "/res/drawable-xhdpi"
    xxhdpi_path = Router.DECOMPILE_PATH + "/res/drawable-xxhdpi"
    xxxhdpi_path = Router.DECOMPILE_PATH + "/res/drawable-xxxhdpi"

    mipmap_hdpi = Router.DECOMPILE_PATH + "/res/mipmap-hdpi"
    mipmap_ldpi = Router.DECOMPILE_PATH + "/res/mipmap-ldpi"
    mipmap_mdpi = Router.DECOMPILE_PATH + "/res/mipmap-mdpi"
    mipmap_xhdpi = Router.DECOMPILE_PATH + "/res/mipmap-xhdpi"
    mipmap_xxhdpi = Router.DECOMPILE_PATH + "/res/mipmap-xxhdpi"
    mipmap_xxxhdpi = Router.DECOMPILE_PATH + "/res/mipmap-xxxhdpi"

    if not os.path.exists(ldpi_path):
        os.makedirs(ldpi_path)

    if not os.path.exists(mdpi_path):
        os.makedirs(mdpi_path)

    if not os.path.exists(hdpi_path):
        os.makedirs(hdpi_path)

    if not os.path.exists(xhdpi_path):
        os.makedirs(xhdpi_path)

    if not os.path.exists(xxhdpi_path):
        os.makedirs(xxhdpi_path)

    if not os.path.exists(xxxhdpi_path):
        os.makedirs(xxxhdpi_path)

    # ===========mipmap============================
    if not os.path.exists(mipmap_hdpi):
        os.makedirs(mipmap_hdpi)

    if not os.path.exists(mipmap_ldpi):
        os.makedirs(mipmap_ldpi)

    if not os.path.exists(mipmap_mdpi):
        os.makedirs(mipmap_mdpi)

    if not os.path.exists(mipmap_xhdpi):
        os.makedirs(mipmap_xhdpi)

    if not os.path.exists(mipmap_xxhdpi):
        os.makedirs(mipmap_xxhdpi)

    if not os.path.exists(mipmap_xxxhdpi):
        os.makedirs(mipmap_xxxhdpi)

    game_icon_name = handle_xml.get_icon_name() + ".png"
    ldpi_icon.save(os.path.join(ldpi_path, game_icon_name), 'PNG')
    if os.path.exists(ldpi_path + "-v4"):
        ldpi_icon.save(os.path.join(ldpi_path + "-v4", game_icon_name), 'PNG')

    mdpi_icon.save(os.path.join(mdpi_path, game_icon_name), 'PNG')
    if os.path.exists(mdpi_path + "-v4"):
        mdpi_icon.save(os.path.join(mdpi_path + "-v4", game_icon_name), 'PNG')

    hdpi_icon.save(os.path.join(hdpi_path, game_icon_name), 'PNG')
    if os.path.exists(hdpi_path + "-v4"):
        hdpi_icon.save(os.path.join(hdpi_path + "-v4", game_icon_name), 'PNG')

    xhdpi_icon.save(os.path.join(xhdpi_path, game_icon_name), 'PNG')
    if os.path.exists(xhdpi_path + "-v4"):
        xhdpi_icon.save(os.path.join(xhdpi_path + "-v4", game_icon_name), 'PNG')

    xxhdpi_icon.save(os.path.join(xxhdpi_path, game_icon_name), 'PNG')
    if os.path.exists(xxhdpi_path + "-v4"):
        xxhdpi_icon.save(os.path.join(xxhdpi_path + "-v4", game_icon_name), 'PNG')

    xxxhdpi_icon.save(os.path.join(xxxhdpi_path, game_icon_name), 'PNG')
    if os.path.exists(xxxhdpi_path + "-v4"):
        xxxhdpi_icon.save(os.path.join(xxxhdpi_path + "-v4", game_icon_name), 'PNG')

    # ====================== mipcap ===============================================
    ldpi_icon.save(os.path.join(mipmap_ldpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_ldpi + "-v4"):
        ldpi_icon.save(os.path.join(mipmap_ldpi + "-v4", game_icon_name), 'PNG')

    mdpi_icon.save(os.path.join(mipmap_mdpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_mdpi + "-v4"):
        mdpi_icon.save(os.path.join(mipmap_mdpi + "-v4", game_icon_name), 'PNG')

    hdpi_icon.save(os.path.join(mipmap_hdpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_hdpi + "-v4"):
        hdpi_icon.save(os.path.join(mipmap_hdpi + "-v4", game_icon_name), 'PNG')

    xhdpi_icon.save(os.path.join(mipmap_xhdpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_xhdpi + "-v4"):
        xhdpi_icon.save(os.path.join(mipmap_xhdpi + "-v4", game_icon_name), 'PNG')

    xxhdpi_icon.save(os.path.join(mipmap_xxhdpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_xxhdpi + "-v4"):
        xxhdpi_icon.save(os.path.join(mipmap_xxhdpi + "-v4", game_icon_name), 'PNG')

    xxxhdpi_icon.save(os.path.join(mipmap_xxxhdpi, game_icon_name), 'PNG')
    if os.path.exists(mipmap_xxxhdpi + "-v4"):
        xxxhdpi_icon.save(os.path.join(mipmap_xxxhdpi + "-v4", game_icon_name), 'PNG')

    return True


def handle_cpu_support():
    """
    interaction cpu support
    :return:
    """
    # 删除前备份一分lib备用
    shutil.copytree(Router.DECOMPILE_PATH + "/lib", Router.WORKSPACE_PATH + "/backup_lib")

    # make sure so in armeabi and armeabi-v7a is same
    armeabiPath = os.path.join(Router.DECOMPILE_PATH, 'lib/armeabi')
    armeabiv7aPath = os.path.join(Router.DECOMPILE_PATH, 'lib/armeabi-v7a')

    if os.path.exists(armeabiPath) and os.path.exists(armeabiv7aPath):
        for f in os.listdir(armeabiPath):
            fv7 = os.path.join(armeabiv7aPath, f)
            if not os.path.exists(fv7):
                shutil.copy2(os.path.join(armeabiPath, f), fv7)

        for fv7 in os.listdir(armeabiv7aPath):
            f = os.path.join(armeabiPath, fv7)
            if not os.path.exists(f):
                shutil.copy2(os.path.join(armeabiv7aPath, fv7), f)


def modify_game_name(task: Task):
    """
    修改当前渠道的游戏名称,如果某个渠道的游戏名称特殊，可以配置gameName来指定。默认就是母包中游戏的名称

    :return:
    """
    modify_name = None
    if task.params_info.game_params.game_name is not None:
        modify_name = task.params_info.game_params.game_name

    manifestFile = Router.DECOMPILE_PATH + "/AndroidManifest.xml"
    ET.register_namespace('android', android_ns)
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    labelKey = '{' + android_ns + '}label'
    applicationNode = root.find('application')
    labelName = applicationNode.get(labelKey)

    if labelName is not None and labelName == "@string/app_name" and handle_app_name_in_string_xml(
            Router.DECOMPILE_PATH, modify_name):
        pass
    else:
        applicationNode.set(labelKey, modify_name)
        handle_app_name_in_string_xml(Router.DECOMPILE_PATH, modify_name)

    tree.write(manifestFile, 'UTF-8')


def handle_app_name_in_string_xml(decompile_dir, appName) -> bool:
    """
    修改strings.xml中的appName
    :param decompile_dir:
    :param appName:
    :return:
    """
    # 优先遍历出所有res的带有values文件夹
    try:
        all_folder = os.listdir(decompile_dir + "/res/")
        for folder in all_folder:
            if "values" in folder:
                string_file = decompile_dir + "/res/" + folder + "/strings.xml"
                values_file = decompile_dir + "/res/" + folder + "/values.xml"
                if os.path.exists(string_file):
                    tree = ET.parse(string_file)
                    root = tree.getroot()

                    for node in list(root):
                        name = node.attrib.get('name')
                        if name == 'app_name':
                            node.text = appName
                            tree.write(string_file, "UTF-8")
                if os.path.exists(values_file):
                    tree = ET.parse(values_file)
                    root = tree.getroot()

                    for node in list(root):
                        name = node.attrib.get('name')
                        if name == 'app_name':
                            node.text = appName
                            tree.write(values_file, "UTF-8")
        return True
    except Exception as e:
        print(e)
        return False


def modify_yml(task: Task):
    """
    修改apktool.yml 文件中的versionName,versionCode,minSdkVersion,targetSdkVersion
    """
    ymlPath = Router.DECOMPILE_PATH + "/apktool.yml"
    if not os.path.exists(ymlPath):
        return

    versionCode = None
    versionName = None
    if task.params_info.game_params.game_version_code is not None:
        versionCode = task.params_info.game_params.game_version_code

    if task.params_info.game_params.game_version_name is not None:
        versionName = task.params_info.game_params.game_version_name

    maxSdkVersion = None
    minSdkVersion = None
    targetSdkVersion = None

    isSDKConfiged = (minSdkVersion is not None) and (targetSdkVersion is not None)

    ymlFile = open(ymlPath, 'r')
    lines = ymlFile.readlines()
    ymlFile.close()

    handlingCompress = False

    newLines = []
    for line in lines:
        if 'versionCode' in line and versionCode is not None:
            newLines.append("  versionCode: '" + str(versionCode) + "'\n")
            handlingCompress = False
        elif 'versionName' in line and versionName is not None:
            newLines.append("  versionName: " + versionName + "\n")
            handlingCompress = False
        elif 'sdkInfo' in line and isSDKConfiged:
            handlingCompress = False
            continue
        elif 'minSdkVersion' in line and isSDKConfiged:
            handlingCompress = False
            continue
        elif 'targetSdkVersion' in line and isSDKConfiged:
            handlingCompress = False
            continue
        elif 'maxSdkVersion' in line and isSDKConfiged:
            handlingCompress = False
            continue
        elif 'renameManifestPackage' in line and ('null' not in line):
            newLines.append("  renameManifestPackage: " + task.params_info.game_params.game_package_name + "\n")
            handlingCompress = False
        elif 'doNotCompress:' in line:
            handlingCompress = True
            newLines.append(line)
        elif handlingCompress and line.startswith('-'):
            pass
        elif line is None or line == "" or line == "\n":
            pass
        else:
            handlingCompress = False
            if 'assets' not in line:
                newLines.append(line)

    if isSDKConfiged:
        newLines.append('sdkInfo:\n')
        if minSdkVersion is not None or minSdkVersion is not "":
            newLines.append("  minSdkVersion: '" + str(minSdkVersion) + "'\n")

        if targetSdkVersion is not None or targetSdkVersion is not "":
            newLines.append("  targetSdkVersion: '" + str(targetSdkVersion) + "'\n")
    if maxSdkVersion is not None:
        newLines.append("  maxSdkVersion: '" + str(maxSdkVersion) + "'\n")

    content = ''
    for line in newLines:
        content = content + line

    ymlFile = open(ymlPath, 'w')
    ymlFile.write(content)
    ymlFile.close()


def generate_r_file(new_package_name: str) -> bool:
    """
    use all new resources to generate the new R.java, and compile it ,then copy it to the target smali dir
    :param new_package_name:
    :param decompile_dir:
    :return:
    """
    decompile_dir = Router.DECOMPILE_PATH
    if not check_value_resources(decompile_dir):
        return False

    temp_path = os.path.dirname(decompile_dir)
    temp_path = temp_path + "/temp"

    if os.path.exists(temp_path):
        fio.del_file_folder(temp_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    res_path = os.path.join(decompile_dir, "res")
    target_res_path = os.path.join(temp_path, "res")
    fio.copy_files(res_path, target_res_path)

    gen_path = os.path.join(temp_path, "gen")
    if not os.path.exists(gen_path):
        os.makedirs(gen_path)

    manifest_path = os.path.join(decompile_dir, "AndroidManifest.xml")
    target_dex_path = os.path.join(temp_path, "classes.dex")

    return exec_generate_r(target_res_path, manifest_path, gen_path, target_dex_path, new_package_name)


def check_value_resources(decompile_dir) -> bool:
    res_path = decompile_dir + '/res'
    if not os.path.exists(res_path):
        return True

    removeDuplcatedValResources(res_path, "values")
    removeDuplcatedValResources(res_path, "values-large")
    for k in range(9, 30):
        removeDuplcatedValResources(res_path, "values-v" + str(k))

    # interaction drawable resource
    ldpi_path = decompile_dir + '/res/drawable-ldpi'
    mdpi_path = decompile_dir + '/res/drawable-mdpi'
    hdpi_path = decompile_dir + '/res/drawable-hdpi'
    xhdpi_path = decompile_dir + '/res/drawable-xhdpi'
    xxhdpi_path = decompile_dir + '/res/drawable-xxhdpi'
    xxxhdpi_path = decompile_dir + '/res/drawable-xxxhdpi'

    removeDuplicateDrawableRes(ldpi_path, ldpi_path + "-v4")
    removeDuplicateDrawableRes(mdpi_path, mdpi_path + "-v4")
    removeDuplicateDrawableRes(hdpi_path, hdpi_path + "-v4")
    removeDuplicateDrawableRes(xhdpi_path, xhdpi_path + "-v4")
    removeDuplicateDrawableRes(xxhdpi_path, xxhdpi_path + "-v4")
    removeDuplicateDrawableRes(xxxhdpi_path, xxxhdpi_path + "-v4")

    return True


def removeDuplcatedValResources(resDir, valFolder):
    valDir = os.path.join(resDir, valFolder)
    # begin interaction -v4 folder. same file can only exists in one
    valDirV4 = os.path.join(resDir, valFolder + "-v4")
    if os.path.exists(valDirV4):
        tempFiles = []
        fio.list_file(valDirV4, tempFiles, [])
        for f in tempFiles:
            if mergeResXml(f, os.path.join(valDir, os.path.basename(f))):
                fio.del_file_folder(f)

    # end interaction -v4
    valFiles = []
    if os.path.exists(valDir):
        fio.list_file(valDir, valFiles, [])

    if not valFiles or len(valFiles) <= 0:
        return 0

    names = ['string', 'style', 'color', 'dimen']
    targetFiles = {}
    existRes = {}

    for name in names:
        if name not in existRes:
            existRes[name] = {}

        for f in valFiles:
            if not isTargetResFile(f, name):
                continue

            if f in targetFiles:
                tree = targetFiles[f]
            else:
                tree = ET.parse(f)
                targetFiles[f] = tree

            root = tree.getroot()
            for node in list(root):
                item = {}
                attribName = node.attrib.get('name')
                if attribName is None:
                    continue

                tag = node.tag
                nodeName = tag + "_" + attribName
                val = node.text
                existItem = existRes[name].get(nodeName)

                if existItem is not None:
                    resVal = existItem.get('value')
                    root.remove(node)

                item['file'] = f
                item['name'] = nodeName
                item['value'] = val
                existRes[name][nodeName] = item

    for f in targetFiles.keys():
        targetFiles[f].write(f, 'UTF-8')

    return 0


def removeDuplicateDrawableRes(path1, path2):
    if not os.path.exists(path1) or not os.path.exists(path2):
        return

    duplicatedFiles = []

    for f1 in os.listdir(path1):
        for f2 in os.listdir(path2):
            if f1 == f2:
                duplicatedFiles.append(os.path.join(path2, f2))
                break

    for d in duplicatedFiles:
        os.remove(d)


def isTargetResFile(resFile, tagName):
    """
    resFile contain tagName?
    use this to interaction the resFile whether or not strings.xml, colors.xml, dimens.xml...
    :param resFile:
    :param tagName:
    :return:
    """
    if os.path.splitext(resFile)[1] != '.xml':
        return False

    if not os.path.exists(resFile):
        return False

    resTree = ET.parse(resFile)
    root = resTree.getroot()
    if root.tag != 'resources':
        return False

    for node in list(root):
        if node.tag == tagName:
            return True

    return False


def exec_generate_r(res_path, manifest_path, gen_path, target_dex_path, new_package_name) -> bool:
    """
    generate R.java for the new_package_name
    """
    if not os.path.exists(res_path):
        return False

    aapt_path = java.get_aapt_shell()
    android_path = Router.ASSETS_PATH + "/apktool/android.jar"
    shell = "%s p -f -m -J %s -S %s -I %s -M %s" % (aapt_path, gen_path, res_path, android_path, manifest_path)
    if not command.exec_command(shell):
        return False

    r_path = new_package_name.replace(".", "/")
    r_path = os.path.join(gen_path, r_path)
    r_path = os.path.join(r_path, "R.java")

    shell = java.get_javac_shell() + " -source 1.7 -target 1.7 -encoding UTF-8 %s" % (r_path)
    if not command.exec_command(shell):
        return False

    dex_tool_path = Router.ASSETS_PATH + "/apktool/dx.jar"
    shell = java.get_java_shell() + " -jar -Xmx2048m -Xms2048m %s --dex --output=%s %s" % (
        dex_tool_path, target_dex_path, gen_path)
    if not command.exec_command(shell):
        return False

    smali_path = os.path.join(Router.DECOMPILE_PATH, "smali")
    return java.dex2smali(target_dex_path, smali_path)


# def copy_extra_r(decompile_dir, params_obj:ParamsMol, new_package_name)->bool:
#     """
#     copy the new generated R.java to comsdk extra package
#     first:add a new param in comsdk channel config <param name="extra_r" value="the package need to generate R. em. com.facebook" />
#     for those comsdk which used R.*.* directly in code.
#     """
#     if params_obj.extra_r is None:
#         return True
#
#     new_package_names = params_obj.extra_r.split("|")
#     ret = 0
#     decompile_dir = path_utils.get_full_path(decompile_dir)
#     sdk_path = os.path.dirname(decompile_dir) + "/sdks"
#     resPath = os.path.join(sdk_path, params_obj.channel_id + "/res")
#
#     tempPath = os.path.dirname(decompile_dir)
#     tempPath = tempPath + "/temp"
#     genPath = os.path.join(tempPath, "gen")
#
#     rPath = new_package_name.replace('.', '/')
#     rPath = os.path.join(genPath, rPath)
#     rPath = os.path.join(rPath, "R.java")
#
#     if not os.path.exists(rPath):
#         Logger.error("copy extra R failed. the R.java is not exists:" + rPath)
#         return 1
#
#     for k in range(len(new_package_names)):
#         package_name = new_package_names[k]
#         tempPath = os.path.join(sdk_path, 'extraTemp' + str(k))
#         if os.path.exists(tempPath):
#             file_utils.del_file_folder(tempPath)
#
#         if not os.path.exists(tempPath):
#             os.makedirs(tempPath)
#
#         targetResPath = os.path.join(tempPath, "res")
#         file_utils.copy_files(resPath, targetResPath)
#
#         genPath = os.path.join(tempPath, "gen")
#         if not os.path.exists(genPath):
#             os.makedirs(genPath)
#
#         trPath = package_name.replace('.', '/')
#         trPath = os.path.join(genPath, trPath)
#         if not os.path.exists(trPath):
#             os.makedirs(trPath)
#
#         targetRPath = os.path.join(trPath, "R.java")
#         file_utils.copy_file(rPath, targetRPath)
#         file_utils.modifyFileContent(targetRPath, new_package_name, package_name)
#
#         cmd = '"%sjavac" -source 1.7 -target 1.7 -encoding UTF-8 "%s"' % (
#             path_utils.get_java_bin_path(), targetRPath)
#         ret = cmd_utils.exec_bash_shell(cmd)
#         if ret:
#             return 1
#
#         dexToolPath = path_utils.get_full_tool_path("/dx.jar")
#         heapSize = config_utils.get_jdk_heap_size()
#         targetDexPath = os.path.join(tempPath, "classes.dex")
#         cmd = path_utils.get_java_shell() + ' -jar -Xmx%sm -Xms%sm "%s" --dex --output="%s" "%s"' % (
#             heapSize, heapSize, dexToolPath, targetDexPath, genPath)
#         ret = cmd_utils.exec_bash_shell(cmd)
#         if ret:
#             return 1
#
#         smaliPath = os.path.join(decompile_dir, "smali")
#         ret = jar_utils.dex2smali(targetDexPath, smaliPath, "baksmali.jar")
#
#     return 0


def format_output_name(task: Task, package_id):
    """
    obtain output final apk name
    """
    format_str = "{task_id}_{game_name}_{channel_name}_{package_id}.apk"
    format_str = format_str.replace('{task_id}', str(task.task_info.task_id))
    format_str = format_str.replace('{game_name}', str(task.params_info.game_params.game_name))
    format_str = format_str.replace('{timestamp}', str(int(time.time())))
    format_str = format_str.replace('{channel_name}', task.params_info.common_params.channel_name)

    format_str = format_str.replace('{package_id}', str(package_id))
    return format_str


# def copy_root_res_files(apkfile, decompile_dir):
#     apkfile = path_utils.get_full_path(apkfile)
#     aapt = path_utils.get_full_tool_path("aapt")
#     decompile_dir = path_utils.get_full_path(decompile_dir)
#
#     igoreFiles = ["AndroidManifest.xml", "apktool.yml", "smali", "res", "original", "lib", "build",
#                   "assets", "unknown"]
#
#     for k in range(2, 20):
#         igoreFiles.append("smali_classes" + str(k))
#
#     igoreFileFullPaths = []
#     for ifile in igoreFiles:
#         fullpath = os.path.join(decompile_dir, ifile)
#         igoreFileFullPaths.append(fullpath)
#
#     addFiles = []
#     file_utils.list_file(decompile_dir, addFiles, igoreFileFullPaths)
#
#     if len(addFiles) <= 0:
#         return
#
#     addCmd = '"%s" add "%s"'
#     for f in addFiles:
#         fname = f[(len(decompile_dir) + 1):]
#         addCmd = addCmd + ' ' + fname
#
#     addCmd = addCmd % (aapt, apkfile)
#     currPath = os.getcwd()
#
#     os.chdir(decompile_dir)
#     cmd_utils.exec_bash_shell(addCmd)
#     os.chdir(currPath)


# def align(apkfile: str, target_file: str) -> bool:
#     """
#     zip align the apk file
#     :param apkfile:
#     :param target_file:
#     :return:
#     """
#     align = path_utils.get_full_tool_path("zipalign")
#     aligncmd = "%s -f -v 4 %s %s" % (align, apkfile, target_file)
#     if cmd_utils.exec_bash_shell(aligncmd) == 0:
#         return True
#     else:
#         return False

#
# def sign_apk(task:Task,keystore, apkfile) -> bool:
#     """
#     Sign apk
#     """
#
#     return sign(apkfile, keystore.keystore_password, keystore.keystore_alias,
#                 keystore.keystore_alias_password)


def sign(task: Task, sigalg: str = "SHA1withRSA") -> bool:
    apkfile = Router.WORKSPACE_PATH + "/output.apk"
    keystore = Router.WORKSPACE_PATH + "/" + task.keystore_info.keystore_name
    if not os.path.exists(keystore):
        print("the keystore file is not exists. " + keystore)
        return False
    sign_shell = java.get_jarsigner_shell() + " -digestalg SHA1 -sigalg %s -keystore %s -storepass %s -keypass %s %s %s" % (
        sigalg, keystore, task.keystore_info.keystore_password, task.keystore_info.keystore_alias_password, apkfile,
        task.keystore_info.keystore_alias)

    return command.exec_command(sign_shell)


# 获取是否自动修改横竖屏
def obtain_direction(sdkDestDir):
    sdkManifest = sdkDestDir + "/SDKManifest.xml"
    if not os.path.exists(sdkManifest):
        return "False"

    ET.register_namespace('android', android_ns)
    tree = ET.parse(sdkManifest)
    root = tree.getroot()

    applicationConfigNode = root.find('applicationConfig')
    if applicationConfigNode is None:
        return "False"

    isAutoChangeOrientation = applicationConfigNode.attrib.get('change_orientation')
    if isAutoChangeOrientation is None or isAutoChangeOrientation == "":
        return "False"
    else:
        return isAutoChangeOrientation


def add_channel_params(task: Task, change_orientation) -> bool:
    """
    add comsdk bagparams to apk.
    :param task:
    :param change_orientation:
    :return:
    """
    try:
        if not task.params_info.channel_params:
            return True
        is_v3_version = os.path.exists(Router.DECOMPILE_PATH + "/assets/fuse_cfg.properties")

        manifest_file = Router.DECOMPILE_PATH + "/AndroidManifest.xml"
        if not os.path.exists(manifest_file):
            print("can't find this file : " + manifest_file)
            return False
        ET.register_namespace("android", android_ns)
        tree = ET.parse(manifest_file)

        if is_v3_version:
            print("处理v3版本的3KWAN_DeployID和3KWAN_GAMEID")
            prop = fprop.parse(Router.DECOMPILE_PATH + "/assets/fuse_cfg.properties")
            if task.params_info.common_params.deploy_id != "":
                prop.put("3KWAN_DeployID", task.params_info.common_params.deploy_id)
            else:
                prop.delete("3KWAN_DeployID")
            if task.params_info.common_params.game_id != "":
                prop.put("3KWAN_GAMEID", task.params_info.common_params.game_id)
            prop.save()
        for param_key in task.params_info.channel_params:
            sdk_helper.handle_meta_data(tree, param_key, task.params_info.channel_params[param_key])

        if change_orientation == str(True):
            orientation = "{" + android_ns + "}screenOrientation"
            application_node = tree.find("application")
            if application_node is not None:
                activitys = application_node.findall("activity")
                if activitys is not None:
                    for activity in activitys:
                        orientation_name = activity.get(orientation)
                        if orientation_name is None or orientation_name is "":
                            continue

                        if orientation_name != "portrait" and orientation_name != "landscape" and orientation_name != "sensorLandscape":
                            continue

                        if task.params_info.game_params.game_params_obj.game_orientation == 1 or task.params_info.game_params.game_params_obj.game_orientation == "1":
                            activity.set(orientation, "portrait")
                        else:
                            activity.set(orientation, "sensorLandscape")

        tree.write(manifest_file, "utf-8")
        return True
    except Exception as e:
        print("add_channel_params() error " + str(e))
        return False


def modify_application_extends(sdkDestDir):
    """
    modify Root application extends
    :param decompile_dir:
    :return:
    """
    sdkManifest = sdkDestDir + "/SDKManifest.xml"
    if not os.path.exists(sdkManifest):
        return 0

    ET.register_namespace('android', android_ns)
    tree = ET.parse(sdkManifest)
    root = tree.getroot()

    applicationConfigNode = root.find('applicationConfig')
    if applicationConfigNode is None:
        return 0

    extendsApplication = applicationConfigNode.attrib.get('extendsApplication')
    if extendsApplication is None or extendsApplication == "":
        return 0

    sdk_helper.modifyRootApplicationExtends(Router.DECOMPILE_PATH, extendsApplication)

# def create_apk_name(game_label, chanle_id):
#     if game_label is None or game_label is "":
#         return
#
#     if ".apk" in game_label:
#         game_name_labels = str(game_label).split(".a")
#         if chanle_id is not None or chanle_id is not "":
#             return game_name_labels[0] + "_" + chanle_id + ".apk"
#         else:
#             return game_label
#     else:
#         if chanle_id is not None or chanle_id is not "":
#             return game_label + "_" + chanle_id + ".apk"
#         else:
#             return game_label
