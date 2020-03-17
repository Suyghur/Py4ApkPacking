# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :


class TaskInfo:
    def __init__(self, info: dict):
        self.__task_id = info["task_id"]
        self.__is_majia = info["is_majia"]
        self.__is_white_bag = info["is_white_bag"]
        self.__is_debug_bag = info["is_debug_bag"]
        self.__has_plugin_sdk = info["has_plugin_sdk"]

    @property
    def task_id(self) -> str:
        return self.__task_id

    @property
    def is_majia(self) -> int:
        return self.__is_majia

    @property
    def is_white_bag(self) -> int:
        return self.__is_white_bag

    @property
    def is_debug_bag(self) -> int:
        return self.__is_debug_bag

    @property
    def has_plugin_sdk(self) -> int:
        return self.__has_plugin_sdk
