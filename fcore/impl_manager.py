# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-25.
# Copyright (c) 2020 3KWan.
# Description :
import json
import os
import shutil
import sys
import time
from typing import Optional, Tuple

from fcore.api import api_manager
from fcore.base import resource, invoke_script, switch, handle_xml, apk_utils, pack_core
from fcore.base.dao import get_common_sdk_size, get_channel_sdk_size
from fcore.base.handle_v3 import handle_v3_origin, handle_v3_common_params
from fcore.entity.result import Task
from fcore.util import android, java, env
from fcore.util.net.host import Host
from fcore.util.net.upload import Upload
from fcore.util.router import Router
from fcore.util.string import dict_2_str


class ImplManager:

    def __init__(self):
        print("Curr Python Version : " + env.get_py_version())
        print("Curr System Platform : " + sys.platform)
        print("Working directory : " + os.getcwd())
        config_path = os.getcwd() + "/config.json"
        Router.init(config_path)
        Host.init(config_path)
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            switch.DB_ENABLE = config["db_cfg"]["enable"]
            switch.WX_ENABLE = config["notify_wx_cfg"]["enable"]

    @staticmethod
    def get_task(task_id: str = "") -> Optional[Task]:
        """
        @param task_id
        @return Task对象
        """
        data = {
            "task_id": task_id,
            "ext": {}
        }
        return api_manager.api_get_task(data)

    def __report(self, data: dict, file_link: str = "") -> bool:
        """
        @param data 请求参数
        @param file_link log文件地址
        @return 是否继续执行
        """
        if "" != file_link:
            result = api_manager.api_report_status(data, True, file_link)
        else:
            result = api_manager.api_report_status(data)
        print("解析结果：" + dict_2_str(result))
        if "is_stop" in result:
            if result["is_stop"] == 0:
                return True
            else:
                return False
        else:
            return False

    def execute(self, task: Task) -> bool:
        """
        @param task task对象
        @return 是否执行成功
        """
        task_id = task.task_info.task_id
        common_sdk_version = task.sdk_info.common_sdk.version
        channel_sdk_version = task.sdk_info.channel_sdk.version
        self.data = {
            "task_id": task_id,
            "package_id": list(task.params_info.common_params.package_chanle.keys())[0],
            "status_code": 0,
            "bag_url": '',
            "common_sdk_version": common_sdk_version,
            "channel_sdk_version": channel_sdk_version,
            "ext": {
                "package_size": 0,
                "rh_sdk_size": 0,
                "channel_sdk_size": 0,
                "plugin_size": 0,
                "rh_time": 0,
                "from_time": 0,
            }
        }

        if not self.__init_workspace(task) or not self.__pack(task):
            # 上报打包失败和日志
            self.data["status_code"] = 1204
            self.__report(self.data)

            # 企业微信机器人提醒
            err_msg = "打包失败，任务ID={0}，子包ID={1}".format(task_id, self.data["package_id"])
            self.api_send_msg_2_wx(err_msg)
            return False

    def __init_workspace(self, task: Task) -> bool:
        signal = 0
        try:
            signal = 0
            # 清空现有工作空间
            print("清空现有工作空间")
            if os.path.exists(Router.WORKSPACE_PATH):
                shutil.rmtree(Router.WORKSPACE_PATH)
            os.mkdir(Router.WORKSPACE_PATH)
            os.mkdir(Router.WORKSPACE_PATH + "/script")
            # os.mkdir(Router.WORKSPACE_PATH + "/channel")
            # os.mkdir(Router.WORKSPACE_PATH + "/plugin")

            result, plugin_sdk_size = resource.check_sdk_resource(task)
            if result:
                # 拷贝处理打包资源
                common_sdk_path = Router.COMMON_SDK_PATH + "/" + task.sdk_info.common_sdk.version
                shutil.copytree(common_sdk_path, Router.WORKSPACE_PATH + "/common")
                channel_sdk_path = Router.CHANNEL_SDK_PATH + "/" + task.params_info.common_params.channel_name
                shutil.copytree(channel_sdk_path, Router.WORKSPACE_PATH + "/channel")
                signal = signal + 1

            # 读取融合、渠道、插件大小
            self.data["ext"]["rh_sdk_size"] = get_common_sdk_size(task.sdk_info.common_sdk.version)
            self.data["ext"]["channel_sdk_size"] = get_channel_sdk_size(task.params_info.common_params.channel_name,
                                                                        task.sdk_info.channel_sdk.version)
            self.data["ext"]["plugin_size"] = plugin_sdk_size

            if resource.check_origin_bag(task):
                shutil.copy(
                    Router.ORIGIN_APK_PATH + "/" + task.bag_info.group_id + "/" + task.bag_info.game_id + ".apk",
                    Router.WORKSPACE_PATH + "/origin.apk")
                signal = signal + 1

            if resource.check_keystore(task):
                signal = signal + 1

            if resource.check_common_script(task):
                signal = signal + 1

            if resource.check_game_script(task):
                signal = signal + 1

            if resource.check_game_resource(task):
                signal = signal + 1

            if signal == 6:
                return True
        except Exception as e:
            print(e)
        return False

    @staticmethod
    def __decompile():
        # 反编译母包
        if android.decompile_apk():
            return True
        else:
            return False

    def __pack(self, task: Task) -> bool:
        start_time = int(time.time())  # 融合处理的起始时间

        if not self.__decompile():
            return False

        # 处理母包中的融合代码、融合资源
        if not handle_v3_origin():
            return False
        old_package_name = handle_xml.replace_package_name(task.params_info.game_params.game_package_name)
        ext = {
            "old_package_name": old_package_name,
            "gen_path": Router.ROOT_PATH
        }
        # 处理融合sdk代码和资源
        if os.path.exists(Router.COMMON_SDK_PATH + "/" + task.sdk_info.common_sdk.version):
            # 转换sdk代码
            if not java.jar2dex(Router.WORKSPACE_PATH + "/common", Router.WORKSPACE_PATH + "/common"):
                return False
            if not java.dex2smali(Router.WORKSPACE_PATH + "/common/classes.dex", Router.DECOMPILE_PATH + "/smali"):
                return False
        else:
            return False
        # 处理渠道sdk代码和资源
        if os.path.exists(Router.CHANNEL_SDK_PATH + "/" + task.params_info.common_params.channel_name):
            # 转换sdk代码
            if not java.jar2dex(Router.WORKSPACE_PATH + "/channel/libs", Router.WORKSPACE_PATH + "/channel/libs"):
                return False
            if not java.dex2smali(Router.WORKSPACE_PATH + "/channel/libs/classes.dex",
                                  Router.DECOMPILE_PATH + "/smali"):
                return False
        else:
            return False

        if not pack_core.pack(task):
            return False

        # 处理插件sdk代码和资源（如果需要）
        if task.task_info.has_plugin_sdk > 0:
            for plugin_sdk in task.sdk_info.plugin_sdk:
                plugin_sdk_path = Router.WORKSPACE_PATH + "/plugin/" + plugin_sdk["file_name"]
                # 转换sdk代码
                if not java.jar2dex(plugin_sdk_path, plugin_sdk_path):
                    return False
                if not java.dex2smali(plugin_sdk_path + "/classes.dex", Router.DECOMPILE_PATH + "/smali"):
                    return False

        # 执行融合脚本
        if not invoke_script.common(task, ext):
            return False
        # 执行渠道脚本
        if not invoke_script.channel(task, ext):
            return False
        # 执行插件脚本（如果需要）
        if task.task_info.has_plugin_sdk > 0:
            for plugin_name in task.sdk_info.plugin_sdk:
                if not invoke_script.plugin(task, plugin_name, ext):
                    return False
        # 执行游戏脚本（非坦克前线）
        if task.bag_info.group_id != "5":
            if not invoke_script.game(task, ext):
                return False

        # generate new R.java
        if apk_utils.generate_r_file(task.params_info.game_params.game_package_name):
            print("generate new R.java success")
        else:
            print("generate new R.java failure")
            return False
        android.split_dex()

        # 融合处理时间
        self.data["ext"]["rh_time"] = int(time.time()) - start_time

        # 处理融合sdk参数
        channel_id = task.params_info.common_params.channel_id
        for package_id in task.params_info.common_params.package_chanle:
            start_time = int(time.time())  # 统计处理分包起始时间
            if task.bag_info.group_id == "5":
                if not invoke_script.game(task, ext):
                    return False
            if not handle_v3_common_params(channel_id, package_id):
                return False
            if not self.__compile():
                return False
            signed, new_apk = self.__sign(task, package_id)

            if not signed:
                return False

            # 上传包做
            bag_url = self.__upload(task, new_apk)
            if bag_url is None and bag_url == '':
                return False

            # 上报打包状态
            self.data["package_id"] = package_id
            self.data["status_code"] = 1210
            self.data["bag_url"] = bag_url
            self.data["ext"]["package_size"] = os.path.getsize(Router.OUTPUT_APK)
            self.data["ext"]["from_time"] = int(time.time()) - start_time  # 分包处理时间
            if not self.__report(self.data):
                return True

        return True

    @staticmethod
    def __compile() -> bool:
        return android.compile_apk()

    @staticmethod
    def __sign(task: Task, package_id) -> Tuple[bool, str]:
        if apk_utils.sign(task):
            if not os.path.exists(Router.ROOT_PATH + "/output/" + task.params_info.common_params.game_id):
                os.makedirs(Router.ROOT_PATH + "/output/" + task.params_info.common_params.game_id)
            new_apk = Router.ROOT_PATH + "/output/" + task.params_info.common_params.game_id + "/" + apk_utils.format_output_name(
                task, package_id)
            shutil.copy(Router.WORKSPACE_PATH + "/output.apk", new_apk)
            return True, new_apk
        else:
            return False, ""

    @staticmethod
    def __upload(task: Task, file_path: str) -> str:
        timestamp = str(int(time.time()))  # 当前时间
        game_id = task.params_info.common_params.game_id
        version_code = task.params_info.game_params.game_version_code
        platform_id = task.params_info.common_params.channel_id
        cnt = 0
        while cnt <= 3:
            url = Upload.upload_file(file_path, timestamp, game_id, version_code, platform_id)
            if url is None:
                cnt += 1
                print("上传失败，重试第 " + str(cnt) + " 次")
                continue
            return url

    @staticmethod
    def api_send_msg_2_wx(err_msg: str):
        api_manager.api_send_msg_2_wx(err_msg)
