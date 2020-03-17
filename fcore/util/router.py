# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :local router
import json


class Router:
    ROOT_PATH = ""
    LOG_PATH = ""
    ASSETS_PATH = ""
    WORKSPACE_PATH = ""

    COMMON_SDK_PATH = ""
    CHANNEL_SDK_PATH = ""
    ORIGIN_APK_PATH = ""

    COMPILE_PATH = ""
    DECOMPILE_PATH = ""
    APKTOOL231 = ""
    APKTOOL232 = ""
    DX_JAR = ""
    BAKSMALI_JAR = ""

    ORIGIN_APK = ""
    OUTPUT_APK = ""

    COMMON_SCRIPT_PATH = ""
    GAME_SCRIPT_PATH = ""

    RESOURCE_PATH = ""

    @staticmethod
    def init(config_path: str) -> None:
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            router_json = config["router"]
            Router.ROOT_PATH = router_json["root_path"]
            Router.LOG_PATH = Router.ROOT_PATH + router_json["log_path"]
            Router.ASSETS_PATH = Router.ROOT_PATH + router_json["assets_path"]
            Router.WORKSPACE_PATH = Router.ROOT_PATH + router_json["workspace_path"]

            Router.COMMON_SDK_PATH = Router.ASSETS_PATH + "/common"
            Router.CHANNEL_SDK_PATH = Router.ASSETS_PATH + "/channel"
            Router.PLUGIN_SDK_PATH = Router.ASSETS_PATH + "/plugin"
            Router.ORIGIN_APK_PATH = Router.ASSETS_PATH + "/origin"

            Router.ORIGIN_APK = Router.WORKSPACE_PATH + "/origin.apk"
            Router.OUTPUT_APK = Router.WORKSPACE_PATH + "/output.apk"
            Router.COMMON_SCRIPT_PATH = Router.WORKSPACE_PATH + "/script/common"
            Router.GAME_SCRIPT_PATH = Router.WORKSPACE_PATH + "/script/game"
            Router.RESOURCE_PATH = Router.WORKSPACE_PATH + "/resource"

            Router.COMPILE_PATH = Router.WORKSPACE_PATH + "/decompile"
            Router.DECOMPILE_PATH = Router.WORKSPACE_PATH + "/decompile"

            Router.APKTOOL231 = Router.ASSETS_PATH + "/apktool/apktool231.jar"
            Router.APKTOOL232 = Router.ASSETS_PATH + "/apktool/apktool232.jar"
            Router.DX_JAR = Router.ASSETS_PATH + "/apktool/dx.jar"
            Router.BAKSMALI_JAR = Router.ASSETS_PATH + "/apktool/baksmali.jar"
