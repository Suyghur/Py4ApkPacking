# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-04.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys
# import time
#
# from fcore.util.net import frequest
# from fcore.util.net.upload import UploadHook

if __name__ == "__main__":
    print(os.getcwd())
    root_path = os.getcwd()
    # root_path = os.path.dirname(os.getcwd())
    print(root_path)
    sys.path.append(root_path)
    import fcore.impl_manager

    impl = fcore.impl_manager.ImplManager()
    task = impl.get_task()
    if task is not None:
        impl.execute(task)
    # timestamp = str(int(time.time()))  # 当前时间
    # game_id = "203"
    # version_code = "503"
    # platform_id = "3k_majia_v3"
    # file_path = "/Users/suyghur/Develop/Fast-Auto/output/203/1352_警戒2_3k_majia_v3_1584085251_26264.apk"
    # file_name = os.path.basename(file_path)
    # with open(file_path, "rb") as f:
    #     path = "/3kfast/{0}/{1}/{2}/{3}/{4}".format(timestamp, game_id, version_code, platform_id, file_name)
    #     print(path)
    #     res = frequest.upyun_manager.put(path, f, checksum=True, need_resume=True, store=None,
    #                                      reporter=UploadHook())
    #     print("-----------------------")
    #     # print(res)
    #     url = Host.OSS_SERVICE_NAME + path
    #     print(url)
    # # up = upyun.UpYun('yxupload', 'sdk3k', 'sdk3k123')
    # # path = "/3kfast/{0}/{1}/{2}/{3}/{4}".format(timestamp, game_id, version_code, platform_id, file_name)
    # # with open(file_path, "rb") as f:
    # #     res = up.put(path, f, checksum=True, need_resume=True, reporter=print_reporter)
    # #     print(res)

    # file_path = "/Users/suyghur/Develop/Fast-Auto/output/203/1352_警戒2_3k_majia_v3_26264.apk"
    # timestamp = str(int(time.time()))
    # game_id = "203"
    # version_code = "503"
    # platform_id = "3k_majia_v3"
    # file_name = os.path.basename(file_path)
    # with open(file_path, "rb") as file:
    #     path = "/3kfast/{0}/{1}/{2}/{3}/{4}".format(timestamp, game_id, version_code, platform_id, file_name)
    #     with UploadHook(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=file_name) as hook:
    #         res = frequest.upyun_manager.put(path, file, checksum=True, need_resume=True,
    #                                          store=None, reporter=hook.update_to)
    #         print("-----------------------")
    #         print(res)
