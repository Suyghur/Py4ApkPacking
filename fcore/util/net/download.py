# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-04.
# Copyright (c) 2020 3KWan.
# Description :
import os
from urllib import request

from tqdm import tqdm
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class DownloadHook(tqdm):
    # Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_block = 0

    def update_to(self, block_num: int, block_size: int, total_size: int):
        per = 100.0 * block_num * block_size / total_size
        if total_size is not None:
            self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num
        if per > 100 or per == 100:
            per = 100
            # ViewNotify.download_file_notify(Host.CODE_SUCCESS, "下载成功", per, self.mod)


class Download:
    TYPE_ZIP = 0
    TYPE_ICON = 1
    TYPE_LOGO = 2
    TYPE_SPLASH = 3
    TYPE_BG = 4
    TYPE_LOADING = 5

    __switch = {
        1: "icon",
        2: "logo",
        3: "splash",
        4: "bg",
        5: "loading"
    }

    @staticmethod
    def download_file(file_link: str, save_path: str, res_type: int = 0) -> str:
        try:
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            file_name = str(os.path.basename(file_link))
            if res_type in Download.__switch:
                file_name = file_name.replace(file_name.split(".")[0], Download.__switch[res_type])
            with DownloadHook(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=file_name) as hook:
                request.urlretrieve(file_link, save_path + "/" + file_name, hook.update_to)
                return file_name
        except Exception as e:
            print(e)
        return ""
