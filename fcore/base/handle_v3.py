# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-21.
# Copyright (c) 2019 3KWan.
# Description :
import os
import shutil

from fcore.util import fio, fprop
from fcore.util.router import Router
from fcore.util.string import is_empty

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


def handle_origin_res() -> bool:
    try:
        files = []
        fio.list_file(Router.DECOMPILE_PATH + "/res", files)
        for file in files:
            if "authsdk_" in file and os.path.exists(file):
                os.remove(file)
            if "umcsdk_" in file and os.path.exists(file):
                os.remove(file)
            if "kkk_" in file and os.path.exists(file):
                os.remove(file)

        xml_list = ["colors", "dimens", "ids", "public", "strings", "styles"]
        for f in xml_list:
            xml_path = Router.DECOMPILE_PATH + "/res/values/" + f + ".xml"

            if os.path.exists(xml_path):
                tree = elementTree.parse(xml_path)
                root = tree.getroot()
                for node in list(root):
                    attrib_name = node.attrib.get('name')
                    if attrib_name is None:
                        continue
                    if attrib_name.lower().startswith("authsdk_"):
                        print(attrib_name)
                        root.remove(node)
                    if attrib_name.lower().startswith("kkk_"):
                        print(attrib_name)
                        root.remove(node)
                tree.write(xml_path, "UTF-8")

        return True
    except Exception as e:
        print("handle_origin_res() error " + str(e))
    return False


def handle_origin_assets() -> bool:
    avenger_local = "avenger_local_local.properties"
    avenger_plugins = "avenger_plugins_config.xml"
    fuse_cfg = "fuse_cfg.properties"
    try:
        if os.path.exists(Router.DECOMPILE_PATH + "/assets/" + avenger_local):
            os.remove(Router.DECOMPILE_PATH + "/assets/" + avenger_local)
        if os.path.exists(Router.DECOMPILE_PATH + "/assets/" + avenger_plugins):
            os.remove(Router.DECOMPILE_PATH + "/assets/" + avenger_plugins)

        if os.path.exists(Router.DECOMPILE_PATH + "/assets/" + fuse_cfg):
            os.remove(Router.DECOMPILE_PATH + "/assets/" + fuse_cfg)

        if os.path.exists(Router.DECOMPILE_PATH + "/assets/kkk_fuse"):
            shutil.rmtree(Router.DECOMPILE_PATH + "/assets/kkk_fuse")

        return True
    except Exception as e:
        print("handle_origin_assets() error " + str(e))
    return False


def handle_smali() -> bool:
    try:
        if os.path.exists(Router.DECOMPILE_PATH + "/smali/com/didi"):
            shutil.rmtree(Router.DECOMPILE_PATH + "/smali/com/didi")
        if os.path.exists(Router.DECOMPILE_PATH + "/smali/com/tencent"):
            shutil.rmtree(Router.DECOMPILE_PATH + "/smali/com/tencent")
        if os.path.exists(Router.DECOMPILE_PATH + "/smali/cn/impl"):
            shutil.rmtree(Router.DECOMPILE_PATH + "/smali/cn/impl")
        if os.path.exists(Router.DECOMPILE_PATH + "/smali/cn/kkk"):
            shutil.rmtree(Router.DECOMPILE_PATH + "/smali/cn/kkk")
        return True
    except Exception as e:
        print("handle_smali() error " + str(e))
    return False


def handle_v3_common_params(channel_id: str, package_id: str):
    fuse_prop_file = Router.DECOMPILE_PATH + "/assets/fuse_cfg.properties"
    if not os.path.exists(fuse_prop_file):
        print("fuse_cfg.properties not exists")
        return False
    try:
        prop = fprop.parse(fuse_prop_file)
        # 写入融合渠道id
        if is_empty(channel_id):
            print("channel_id 不能为空")
            return False
        else:
            prop.put("3KWAN_Platform_ChanleId", channel_id)
        # 写入融合渠道id
        if is_empty(package_id):
            print("package_id 不能为空")
            return False
        else:
            prop.put("3KWAN_PackageID", package_id)
        prop.save()
        return True
    except Exception as e:
        print("handle_v3_common_params() error " + str(e))
        return False


# def handle_v3_media_params(task: Task, decompile_dir: str = Router.DECOMPILE_PATH) -> bool:
#     media_params_dict = params_obj.media_params_obj.get_media_dict
#     if media_params_dict is None or len(media_params_dict) <= 0:
#         return False
#     if fio.exists(decompile_dir + "/assets/fuse_cfg.properties"):
#         prop = fprop.parse(decompile_dir + "/assets/fuse_cfg.properties")
#         for key in media_params_dict:
#             prop.put(key, media_params_dict[key])
#         prop.save()
#     else:
#         Logger.error("fuse_cfg不存在")
#         return False


def handle_v3_origin() -> bool:
    if handle_origin_assets() and handle_origin_res() and handle_smali():
        print("handle_v3_origin() success")
        return True
    else:
        print("handle_v3_origin() error")
        return False
