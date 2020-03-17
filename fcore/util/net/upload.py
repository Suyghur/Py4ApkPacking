# _*_coding:utf-8_*_
# Created by #zgy, on 2020-03-09.
# Copyright (c) 2020 3KWan.
# Description :
import os

from tqdm import tqdm
from upyun import UpYunServiceException, UpYunClientException

from fcore.util.net import frequest
from fcore.util.net.host import Host


# class UploadHook:
#
#     def __call__(self, uploaded_size, total_size, status):
#         """
#         文件上传回调
#         :param uploaded_size: 远端文件大小
#         :param total_size: 文件总大侠
#         :param status: 状态
#         :return: None
#         """
#         if not status:
#             per = 100.0 * uploaded_size / total_size
#             print("---->uploading {0:.2f}%".format(per))
#         else:
#             print(" ----> uploading finish ")
#             print("---->uploading {0:.2f}%".format(100.0))


class UploadHook(tqdm):
    # Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_block = 0

    # def __call__(self, uploaded_size, total_size, status):
    #
    #     """
    #     文件上传回调
    #     :param uploaded_size: 远端文件大小
    #     :param total_size: 文件总大侠
    #     :param status: 状态
    #     :return: None
    #     """
    #     if not status:
    #         print("uploaded_size" + str(uploaded_size / 102400))
    #         print("total_size" + str(total_size / 1024000))
    #
    #         per = 100.0 * uploaded_size / total_size
    #         self.update((total_size - uploaded_size) / 1024)
    #         # print("---->uploading {0:.2f}%".format(per))
    #     else:
    #         print(" ----> uploading finish ")
    #         print("---->uploading {0:.2f}%".format(100.0))

    def update_to(self, uploaded_size, total_size, status):
        if not status:
            # print("uploaded_size" + str(uploaded_size))
            # print("total_size" + str(total_size))

            # per = 100.0 * uploaded_size / total_size
            self.update((total_size - uploaded_size) / 100 / 0.7)
        else:
            print(self.avg_time)
            # print(self.total)
            # print(self.miniters)
            # print("---->uploading {0:.2f}%".format(per))
        # else:
        #     print(" ----> uploading finish ")
        #     print("---->uploading {0:.2f}%".format(100.0))

        # per = 100.0 * block_num * block_size / total_size
        # if total_size is not None:
        #     self.total = total_size
        # self.update((block_num - self.last_block) * block_size)
        # self.last_block = block_num
        # if per > 100 or per == 100:
        #     per = 100
        # ViewNotify.download_file_notify(Host.CODE_SUCCESS, "下载成功", per, self.mod)
    # ViewNotify.download_file_notify(Host.CODE_SUCCESS, "下载成功", per, self.mod)


class Upload:

    @staticmethod
    def upload_file(file_path: str, timestamp: str, game_id: str, version_code: str, platform_id) -> str:
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as file:
                path = "/3kfast/{0}/{1}/{2}/{3}/{4}".format(timestamp, game_id, version_code, platform_id, file_name)
                with UploadHook(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=file_name) as hook:
                    res = frequest.upyun_manager.put(path, file, checksum=True, need_resume=True,
                                                     store=None, reporter=hook.update_to)
                    print("-----------------------")
                    print(res)
                    url = Host.OSS_SERVICE_NAME + path
                    return url

        except UpYunServiceException as se:
            print(" ----> upload bag file fail")
            print(" ----> Except an UpYunServiceException ...")
            print(" ----> Request Id : " + se.request_id)
            print(" ----> HTTP Status Code : " + str(se.status))
            print(" ----> Error code : " + se.err)
            print(" ----> Error Message : " + se.msg)
            return None
        except UpYunClientException as ce:
            print(" ----> upload bag file fail")
            print(" ----> Except an UpYunClientException ...")
            print(" ----> Error Message : " + ce.msg)
            return None
        except Exception as e:
            print(" ----> upload bag file fail")
            print("----> upload bag file fail {0}".format(str(e)))
            return None
