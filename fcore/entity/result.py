# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :
import json

from fcore.entity.bean.bag_info import BagInfo
from fcore.entity.bean.keystore_info import KeystoreInfo
from fcore.entity.bean.params_info import ParamsInfo
from fcore.entity.bean.script_info import ScriptInfo
from fcore.entity.bean.sdk_info import SdkInfo
from fcore.entity.bean.task_info import TaskInfo
from fcore.util.cipher import cipher
from fcore.util.string import dict_2_str


class ResultInfo:

    def __init__(self, json_str: str):
        json_obj = json.loads(json_str)
        self.__status = json_obj["status"]
        self.__msg = json_obj["msg"]
        self.__result = json_obj["result"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def msg(self) -> str:
        return self.__msg

    @property
    def result(self) -> dict:
        return self.__handle_result()

    def __handle_result(self) -> dict:
        p = ""
        ts = ""
        if self.__result:
            if "p" in self.__result:
                p = self.__result["p"]
            if "ts" in self.__result:
                ts = self.__result["ts"]
            aes_key = cipher.get_16low_md5(ts + ts[::-1])
            raw = cipher.urldecode(cipher.AesCipher.decrypt(cipher.urldecode(p), aes_key))
            result = json.loads(raw)
            print("解析数据 : " + dict_2_str(result))
            return result


class Task:

    def __init__(self, result: dict):
        self.__task_info = result["task_info"]
        self.__bag_info = result["bag_info"]
        self.__sdk_info = result["sdk_info"]
        self.__keystore_info = result["keystore_info"]
        self.__script_info = result["script_info"]
        self.__params_info = result["params_info"]
        self.__ext = result["ext"]

    @property
    def task_info(self) -> TaskInfo:
        return TaskInfo(self.__task_info)

    @property
    def bag_info(self) -> BagInfo:
        return BagInfo(self.__bag_info)

    @property
    def keystore_info(self) -> KeystoreInfo:
        return KeystoreInfo(self.__keystore_info)

    @property
    def script_info(self) -> ScriptInfo:
        return ScriptInfo(self.__script_info)

    @property
    def sdk_info(self) -> SdkInfo:
        return SdkInfo(self.__sdk_info)

    @property
    def params_info(self) -> ParamsInfo:
        return ParamsInfo(self.__params_info)

    @property
    def ext(self) -> dict:
        return self.__ext
