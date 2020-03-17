# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/5/7
#
# 此文件用于编写打包脚本的主要逻辑
import os

from fcore.base import apk_utils, handle_xml
from fcore.entity.result import Task
from fcore.util.router import Router


def pack(task: Task) -> bool:
    # TODO 检查母包接入是否正确
    try:
        # change xml config and so on
        newPackageName = task.params_info.game_params.game_package_name

        # copy channel sdk resources.
        ret = apk_utils.copyResource(task, Router.WORKSPACE_PATH + "/channel")
        if ret:
            print("整合渠道SDK资源失败")
            return False
        else:
            print("整合渠道SDK资源成功")

        # copy common sdk resources.
        ret = apk_utils.copyResource(task, Router.WORKSPACE_PATH + "/common")
        if ret:
            print("整合融合SDK资源失败")
            return False

        handle_xml.do_common_provider(newPackageName)
        print("整合3k融合SDK资源成功")

        # auto handle icon
        apk_utils.append_channel_icon_mark()
        print("处理icon成功")

        # copy channel special resources common, game, channel, decompile_dir
        ret = apk_utils.copyChannelSpecialResources()
        if ret:
            print("copy channel special resources failure...")
            return False

        print("整合渠道特殊资源成功")

        # generate common and channel's bagparams to apk
        is_auto_change_orientation = apk_utils.obtain_direction(Router.WORKSPACE_PATH + "/channel")
        if apk_utils.add_channel_params(task, is_auto_change_orientation):
            print("添加渠道参数成功")
        else:
            print("添加渠道参数失败")

        # if handle_media_params(task, Router.DECOMPILE_PATH):
        #     print("处理媒体参数成功")

        # interaction cpu supports
        apk_utils.handle_cpu_support()

        # modify yml
        apk_utils.modify_yml(task)
        print("修改yml")

        # modify root application extends
        apk_utils.modify_application_extends(Router.WORKSPACE_PATH + "/channel")
        print("修改application继承关系")

        # modify game name if channel specified
        apk_utils.modify_game_name(task)

        # # interaction to split dex
        # apk_utils.split_dex(task, workspace, decompile_dir, ext_smali_dir)
        #
        # if handle_channel_package(task, decompile_dir, workspace, mod, ext_infos):
        #     return True
        # else:
        #     return False
        return True
    except Exception as e:
        print(e)
        return False
