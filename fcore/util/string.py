# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-27.
# Copyright (c) 2020 3KWan.
# Description :


def dict_2_str(data: dict) -> str:
    return repr(data).replace("'", '"')


def is_empty(content: str) -> bool:
    if content is None or content.strip() == "":
        return True
    else:
        return False
