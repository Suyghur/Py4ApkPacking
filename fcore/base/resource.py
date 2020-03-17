# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-04.
# Copyright (c) 2020 3KWan.
# Description :

import os
import shutil
from typing import Tuple, Any

from fcore.base import dao
from fcore.util import fio
from fcore.util.net.download import Download
from fcore.entity.result import Task
from fcore.util.router import Router
from fcore.util.string import is_empty

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


# ------ 检查sdk资源 ------
def check_sdk_resource(task: Task) -> Tuple[bool, Any]:
    result, plugin_sdk_size = __check_plugin_sdk(task)
    if __check_common_sdk(task) and __check_channel_sdk(task) and result:
        return True, plugin_sdk_size
    else:
        return False, plugin_sdk_size


def __check_common_sdk(task: Task) -> Tuple[bool, int]:
    # 查表取出本地的md5
    # md5为空直接下载，非空时进行对比，不一致时以服务端返回为较新版本
    sdk_info = task.sdk_info
    md5 = dao.get_common_sdk_md5(sdk_info.common_sdk.version)
    file_size = 0
    result = False, file_size

    if not os.path.exists(Router.COMMON_SDK_PATH):
        os.makedirs(Router.COMMON_SDK_PATH)

    if is_empty(md5):
        # file_name = os.path.basename(sdk_info.common_sdk.file_url)
        file_name = Download.download_file(sdk_info.common_sdk.file_url, Router.COMMON_SDK_PATH)
        file_size = os.path.getsize(Router.COMMON_SDK_PATH + "/" + file_name)
        # 解压
        if fio.unzip(Router.COMMON_SDK_PATH + "/" + file_name, Router.COMMON_SDK_PATH):
            os.remove(Router.COMMON_SDK_PATH + "/" + file_name)
            result = True, file_size
        else:
            return False, 0
        # 更新db
        if dao.insert_common_sdk_md5(sdk_info.common_sdk.version, sdk_info.common_sdk.file_md5, file_size):
            result = True, file_size
        else:
            return False, 0
    else:
        if sdk_info.common_sdk.file_md5 != md5:
            # 删除原来的文件夹
            print(Router.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version)
            if os.path.exists(Router.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version):
                shutil.rmtree(Router.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version)
            else:
                return False, 0
            # 下载
            # file_name = os.path.basename(sdk_info.common_sdk.file_url)
            file_name = Download.download_file(sdk_info.common_sdk.file_url, Router.COMMON_SDK_PATH)
            file_size = os.path.getsize(Router.COMMON_SDK_PATH + "/" + file_name)
            # 解压
            if fio.unzip(Router.COMMON_SDK_PATH + "/" + file_name, Router.COMMON_SDK_PATH):
                os.remove(Router.COMMON_SDK_PATH + "/" + file_name)
                result = True, file_size
            else:
                return False, 0
            # 更新db
            if dao.update_common_sdk_md5(sdk_info.common_sdk.version, sdk_info.common_sdk.file_md5, file_size):
                result = True, file_size
            else:
                return False, 0
        else:
            result = True, file_size
    return result


def __check_channel_sdk(task: Task) -> bool:
    # 查表取出本地的md5
    # md5为空直接下载，非空时进行对比，不一致时以服务端返回为较新版本
    channel_name = task.params_info.common_params.channel_name
    sdk_info = task.sdk_info
    md5 = dao.get_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version)
    result = False

    if not os.path.exists(Router.CHANNEL_SDK_PATH):
        os.makedirs(Router.CHANNEL_SDK_PATH)

    if is_empty(md5):
        # file_name = os.path.basename(sdk_info.channel_sdk.file_url)
        file_name = Download.download_file(sdk_info.channel_sdk.file_url, Router.CHANNEL_SDK_PATH)
        file_size = os.path.getsize(Router.CHANNEL_SDK_PATH + "/" + file_name)
        # 解压
        if fio.unzip(Router.CHANNEL_SDK_PATH + "/" + file_name, Router.CHANNEL_SDK_PATH):
            os.remove(Router.CHANNEL_SDK_PATH + "/" + file_name)
            result = True
        # 更新db
        if dao.insert_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version, sdk_info.channel_sdk.file_md5,
                                      file_size):
            result = True
    else:
        if sdk_info.channel_sdk.file_md5 != md5:
            # 删除原来的文件夹
            if os.path.exists(Router.CHANNEL_SDK_PATH + "/" + channel_name):
                shutil.rmtree(Router.CHANNEL_SDK_PATH + "/" + channel_name)
            # 下载
            # file_name = os.path.basename(sdk_info.channel_sdk.file_url)
            file_name = Download.download_file(sdk_info.channel_sdk.file_url, Router.CHANNEL_SDK_PATH)
            file_size = os.path.getsize(Router.CHANNEL_SDK_PATH + "/" + file_name)
            # 解压
            if fio.unzip(Router.CHANNEL_SDK_PATH + "/" + file_name, Router.CHANNEL_SDK_PATH):
                os.remove(Router.CHANNEL_SDK_PATH + "/" + file_name)
                result = True
            # 更新db
            if dao.update_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version, sdk_info.channel_sdk.file_md5,
                                          file_size):
                result = True
        else:
            result = True
    return result


def __check_plugin_sdk(task: Task) -> Tuple[bool, int]:
    if task.task_info.has_plugin_sdk != 1 or not task.sdk_info.plugin_sdk:
        return True, 0

    result = False
    plugin_dict = task.sdk_info.plugin_sdk
    total_file_size = 0
    for plugin_name in plugin_dict:
        file_name = Download.download_file(plugin_dict[plugin_name].file_url, Router.WORKSPACE_PATH + "/plugin")
        file_size = os.path.getsize(Router.WORKSPACE_PATH + "/plugin/" + file_name)
        total_file_size += file_size
        if fio.unzip(Router.WORKSPACE_PATH + "/plugin/" + file_name, Router.WORKSPACE_PATH + "/plugin/" + plugin_name):
            os.remove(Router.WORKSPACE_PATH + "/plugin/" + file_name)
            result = True
    return result, total_file_size


# ------ 检查sdk资源 ------


# ------ 检查母包资源 ------
def check_origin_bag(task: Task) -> bool:
    bag_info = task.bag_info
    md5 = dao.get_origin_bag_md5(bag_info.game_id, bag_info.group_id)
    result = False
    if not os.path.exists(Router.ORIGIN_APK_PATH):
        os.makedirs(Router.ORIGIN_APK_PATH)
    if is_empty(md5):
        file_name = Download.download_file(bag_info.file_url, Router.ORIGIN_APK_PATH + "/" + bag_info.group_id)
        if dao.insert_origin_bag_md5(bag_info.game_id, bag_info.group_id, bag_info.file_md5):
            os.rename(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + file_name,
                      Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
            result = True
    else:
        if bag_info.file_md5 != md5:
            if os.path.exists(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk"):
                os.remove(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
            file_name = Download.download_file(bag_info.file_url, Router.ORIGIN_APK_PATH + "/" + bag_info.group_id)
            if dao.update_origin_bag_md5(bag_info.game_id, bag_info.group_id, bag_info.file_md5):
                os.rename(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + file_name,
                          Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
                result = True
        else:
            if not os.path.exists(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk"):
                file_name = Download.download_file(bag_info.file_url, Router.ORIGIN_APK_PATH + "/" + bag_info.group_id)
                if dao.update_origin_bag_md5(bag_info.game_id, bag_info.group_id, bag_info.file_md5):
                    os.rename(Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + file_name,
                              Router.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
            result = True
    return result


# ------ 检查母包资源 ------


# ------ 检查签名文件资源 ------
def check_keystore(task: Task) -> bool:
    try:
        keystore_info = task.keystore_info
        file_name = Download.download_file(keystore_info.file_url, Router.WORKSPACE_PATH)
        if file_name != keystore_info.keystore_name:
            os.rename(Router.WORKSPACE_PATH + "/" + file_name,
                      Router.WORKSPACE_PATH + "/" + keystore_info.keystore_name)
        return True
    except Exception as e:
        print(e)
    return False


# ------ 检查签名文件资源 ------

# ------ 检查脚本资源 ------
def check_common_script(task: Task) -> bool:
    try:
        common_script_info = task.script_info.common_script
        if common_script_info is None:
            return True
        file_name = Download.download_file(common_script_info.file_url, Router.COMMON_SCRIPT_PATH)
        if file_name == common_script_info.file_name:
            if fio.unzip(Router.COMMON_SCRIPT_PATH + "/" + file_name, Router.COMMON_SCRIPT_PATH):
                os.remove(Router.COMMON_SCRIPT_PATH + "/" + file_name)
                return True

    except Exception as e:
        print(e)
    return False


def check_game_script(task: Task) -> bool:
    try:
        game_script_info = task.script_info.game_script
        if game_script_info is None:
            return True
        file_name = Download.download_file(game_script_info.file_url, Router.GAME_SCRIPT_PATH)
        if file_name == game_script_info.file_name:
            if fio.unzip(Router.GAME_SCRIPT_PATH + "/" + file_name, Router.GAME_SCRIPT_PATH):
                os.remove(Router.GAME_SCRIPT_PATH + "/" + file_name)
                return True

    except Exception as e:
        print(e)
    return False


# ------ 检查游戏资源 ------
def check_game_resource(task: Task) -> bool:
    try:
        icon_url = task.params_info.game_params.game_icon_url
        logo_url = task.params_info.game_params.game_logo_url
        splash_url = task.params_info.game_params.game_splash_url
        background_url = task.params_info.game_params.game_background_url
        loading_url = task.params_info.game_params.game_loading_url
        resource_url = task.params_info.game_params.game_resource_url

        if not is_empty(icon_url):
            icon = Download.download_file(icon_url, Router.RESOURCE_PATH, 1)
        if not is_empty(logo_url):
            logo = Download.download_file(logo_url, Router.RESOURCE_PATH, 2)
        if not is_empty(splash_url):
            splash = Download.download_file(splash_url, Router.RESOURCE_PATH, 3)
        if not is_empty(background_url):
            background = Download.download_file(background_url, Router.RESOURCE_PATH, 4)
        if not is_empty(background_url):
            loading = Download.download_file(loading_url, Router.RESOURCE_PATH, 5)
        if not is_empty(resource_url):
            resource = Download.download_file(resource_url, Router.RESOURCE_PATH)

        return True

    except Exception as e:
        print(e)
        return False

# ------ 检查游戏资源 ------
