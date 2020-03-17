# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-10.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys

from fcore.entity.result import Task
from fcore.util.router import Router


def common(task: Task, ext: dict) -> bool:
    common_script = Router.COMMON_SCRIPT_PATH + "/common_script.py"
    if os.path.exists(common_script):
        print("common script : " + common_script)

        sys.path.append(Router.COMMON_SCRIPT_PATH)
        try:
            import common_script
            ret = common_script.invoke(task, Router.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["common_script"]
            sys.path.remove(Router.COMMON_SCRIPT_PATH)
            return ret
        except ImportError as e:
            print(e)
            return False


def channel(task: Task, ext: dict) -> bool:
    sdk_script = Router.WORKSPACE_PATH + "/channel/sdk_script.py"
    if os.path.exists(sdk_script):
        print("sdk script : " + sdk_script)
        sys.path.append(Router.WORKSPACE_PATH + "/channel")
        try:
            import sdk_script
            ret = sdk_script.invoke(task, Router.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["sdk_script"]
            sys.path.remove(Router.WORKSPACE_PATH + "/channel")
            return ret
        except ImportError as e:
            print(e)
            return False


def plugin(task: Task, plugin_name: str, ext: dict) -> bool:
    plugin_script = Router.WORKSPACE_PATH + "/plugin/" + plugin_name + "/plugin_script.py"
    if os.path.exists(plugin_script):
        print("plugin script : " + plugin_script)

        sys.path.append(Router.WORKSPACE_PATH + "/plugin/" + plugin_name)
        try:
            import plugin_script
            ret = plugin_script.invoke(task, Router.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["plugin_script"]
            sys.path.remove(Router.WORKSPACE_PATH + "/plugin/" + plugin_name)
            return ret
        except ImportError as e:
            print(e)
            return False


def game(task: Task, ext: dict) -> bool:
    game_script = Router.GAME_SCRIPT_PATH + "/game_script.py"
    if os.path.exists(game_script):
        print("game script : " + game_script)

        sys.path.append(Router.GAME_SCRIPT_PATH)
        try:
            import game_script
            ret = game_script.invoke(task, Router.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["game_script"]
            sys.path.remove(Router.GAME_SCRIPT_PATH)
            return ret
        except ImportError as e:
            print(e)
            return False
    else:
        return True
