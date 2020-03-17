# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import json


class Host:
    HOST_URL = ""
    BASIC_URL_GET_TASK = ""
    BASIC_URL_REPORT_STATUS = ""
    BASIC_URL_WX_DEVELOPER = ""
    OSS_SERVICE_NAME = ""
    UPYUN_SERVICE = ""
    UPYUN_USERNAME = ""
    UPYUN_PASSWORD = ""

    @staticmethod
    def init(config_path) -> None:
        with open(config_path, "r", encoding="utf-8")as f:
            setting_json = json.load(f)
            host_json = setting_json["host"]
            mode = host_json["mode"]
        if mode == 2:
            Host.HOST_URL = host_json["dev"]
        elif mode == 1:
            Host.HOST_URL = host_json["test"]
        else:
            Host.HOST_URL = host_json["online"]

        Host.BASIC_URL_GET_TASK = Host.HOST_URL + "/?ct=AutoPackage&ac=getTaskInfo"
        Host.BASIC_URL_REPORT_STATUS = Host.HOST_URL + "/?ct=AutoPackage&ac=getStatusReport"
        Host.BASIC_URL_WX_DEVELOPER = host_json["wx_developer"]
        Host.OSS_SERVICE_NAME = host_json["oss_service_name"]
        Host.UPYUN_SERVICE = host_json["upyun_service"]
        Host.UPYUN_USERNAME = host_json["upyun_username"]
        Host.UPYUN_PASSWORD = host_json["upyun_password"]
