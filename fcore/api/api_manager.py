# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-27.
# Copyright (c) 2020 3KWan.
# Description :
from typing import Optional

from fcore.base import switch
from fcore.entity.result import Task
from fcore.util.net.frequest import NetWorkManager
from fcore.util.net.host import Host
from fcore.util.string import dict_2_str

COMMON = {
    "class_type": 1,
    "server_version": "1.0.0",
    "client_version": "1.0.0"
}

URL = ""

TAG = "api_manager"


def api_get_task(data: dict) -> Optional[Task]:
    """
    :param data:
    :return
    """
    data["common"] = COMMON
    result = NetWorkManager.post(Host.BASIC_URL_GET_TASK, dict_2_str(data))
    if result.status == 0 and result.result:
        return Task(result.result)
    else:
        if result.status != 0:
            api_send_msg_2_wx("获取任务接口请求异常：" + result.msg)
        return None


def api_report_status(data: dict, upload: bool = False, file_link: str = "") -> dict:
    data["common"] = COMMON
    print("请求参数：" + dict_2_str(data))
    if upload:
        result = NetWorkManager.post(Host.BASIC_URL_REPORT_STATUS, dict_2_str(data), upload, file_link)
    else:
        result = NetWorkManager.post(Host.BASIC_URL_REPORT_STATUS, dict_2_str(data))
    if result.status == 0 and result.result:
        return result.result
    else:
        api_send_msg_2_wx("上报状态接口请求异常：" + result.msg)
        return {}


def api_polling_status():
    pass


def api_send_msg_2_wx(msg: str) -> str:
    if switch.WX_ENABLE:
        data = {
            "msgtype": "text",
            "text": {
                "content": msg,
            }
        }
        return NetWorkManager.send_msg_2_wx(Host.BASIC_URL_WX_DEVELOPER, data)
    else:
        return ""
