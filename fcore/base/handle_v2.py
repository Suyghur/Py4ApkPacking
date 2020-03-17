# # _*_coding:utf-8_*_
# # Created by #Suyghur, on 2019-10-21.
# # Copyright (c) 2019 3KWan.
# # Description :handle commonsdk v2 version packing
# import os
#
# from application.fcore.utils import sdk_helper, path_utils, file_utils
# from application.library.constants.const_channel_config import Channel
# from application.library.constants.mod_const import const
# from application.library.logos.tl_log_toolkit import Logger
# from application.model.fcore.mol_params import ParamsMol
#
# try:
#     import xml.etree.cElementTree as elementTree
# except ImportError:
#     import xml.etree.ElementTree as elementTree
#
# android_ns = "http://schemas.android.com/apk/res/android"
#
#
# def del_smali_code(decompile_dir: str) -> bool:
#     """
#     delete 3k common comsdk smali code.
#     :param decompile_dir:
#     :return:
#     """
#     try:
#         if const.DELETE_SMALI_PATH is None or len(const.DELETE_SMALI_PATH) <= 0:
#             return True
#
#         for deletePath in const.DELETE_SMALI_PATH:
#             delete_path = path_utils.get_full_path(decompile_dir + deletePath)
#             if not os.path.exists(delete_path):
#                 Logger.error("can't find this folder path :" + delete_path)
#                 continue
#
#             file_utils.del_file_folder(delete_path)
#         return True
#     except Exception as e:
#         Logger.error("del_smali_code() error " + str(e))
#         return False
#
#
# def delete_so_file(decompile_dir: str) -> bool:
#     """
#     delete so file.
#     :param decompile_dir:
#     :return:
#     """
#     try:
#         so_file_path = path_utils.get_full_path(decompile_dir + "/lib")
#         if not os.path.exists(so_file_path):
#             Logger.error("can't find so path :" + so_file_path)
#             return False
#
#         so_files = []
#         file_utils.list_file(so_file_path, so_files, [])
#         if so_files is None or len(so_files) <= 0:
#             return True
#
#         for so_file in so_files:
#             if 'liblbs.so' in so_file:
#                 file_utils.del_file_folder(so_file)
#         return True
#     except Exception as e:
#         Logger.error("delete_so_file() error " + str(e))
#         return False
#
#
# def del_manifest_infos(decompile_dir: str) -> bool:
#     """
#     delete androidManifest infos
#     :param decompile_dir:
#     :return:
#     """
#     try:
#         # 删除cn.kkk.comsdk.LoginActivity
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.LoginActivity')
#         # 删除cn.kkk.comsdk.AccountActivity
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.AccountActivity')
#         # 删除cn.kkk.comsdk.ChargeActivity
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.ChargeActivity')
#         # 删除cn.kkk.comsdk.KkkService
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'service', 'cn.kkk.comsdk.KkkService')
#
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'service', 'cn.kkk.sdk.ui.floatview.FlyingBallService')
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.sdk.WebviewPageActivity')
#
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.unionpay.uppay.PayActivity')
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.unionpay.uppay.PayActivityEx')
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.alipay.sdk.app.H5PayActivity')
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity-alias', '.wxapi.WXPayEntryActivity')
#
#         # 删除3KWAN_HasLogo meta-data标签
#         sdk_helper.removeMinifestComponentByName(decompile_dir, 'meta-data', '3KWAN_HasLogo')
#         return True
#     except Exception as e:
#         Logger.error("del_manifest_infos() error " + str(e))
#         return False
#
#
# def del_3k_res(decompile_dir: str) -> bool:
#     """
#     delete 3k res eg:kkk_
#     :param decompile_dir:
#     :return:
#     """
#     try:
#         res_path = path_utils.get_full_path(decompile_dir + "/res")
#         if not os.path.exists(res_path):
#             Logger.error("can't find this res path : " + res_path)
#             return False
#
#         res_files = []
#         file_utils.list_file(res_path, res_files, [])
#         if res_files is None or len(res_files) <= 0:
#             return True
#
#         for res in res_files:
#             if "kkk_" in res:
#                 file_utils.del_file_folder(res)
#
#         # 开始删除字段
#         decompile_dir = path_utils.get_full_path(decompile_dir)
#         file_list = ["colors", "dimens", "ids", "public", "strings", "styles"]
#         for f in file_list:
#             fpath = decompile_dir + "/res/values/" + f + ".xml"
#             if os.path.exists(fpath):
#                 tree = elementTree.parse(fpath)
#                 root = tree.getroot()
#                 for node in list(root):
#                     item = {}
#                     attribName = node.attrib.get("name")
#                     if attribName is None:
#                         continue
#
#                     if attribName.lower().startswith("kkk_") or attribName.lower().startswith("tk_"):
#                         root.remove(node)
#                 tree.write(fpath, "UTF-8")
#
#         res_path = decompile_dir + "/res"
#         xml_list = []
#         file_utils.list_file(res_path, xml_list, [])
#         for xml in xml_list:
#             if os.path.basename(xml).lower().startswith("kkk_") or os.path.basename(xml).lower().startswith("tk_"):
#                 file_utils.del_file_folder(xml)
#
#         return True
#     except Exception as e:
#         Logger.error("del_3k_res() error " + str(e))
#         return False
#
#
# def handle_v2_media_params(params_obj: ParamsMol, decompile_dir) -> bool:
#     if params_obj.media_params_obj is None:
#         return False
#
#     if params_obj.media_params_obj.get_media_dict is None:
#         return False
#
#     manifest_path = path_utils.get_full_path(decompile_dir + "/AndroidManifest.xml")
#     if not os.path.exists(manifest_path):
#         Logger.error("can't find this file : " + manifest_path)
#         return False
#     try:
#         elementTree.register_namespace("android", android_ns)
#         tree = elementTree.parse(manifest_path)
#
#         for key in params_obj.media_params_obj.get_media_dict:
#             sdk_helper.handle_meta_data(tree, key, params_obj.media_params_obj.get_media_dict[key])
#
#         tree.write(manifest_path, "utf-8")
#         return True
#     except Exception as e:
#         Logger.error("handle_v2_media_params() error " + str(e))
#         return False
#
#
# def handle_v2_common_params(channel_name: str, package_id: str, package_chanle_dict: dict, decompile_dir: str) -> bool:
#     """
#
#     :param channel_name:
#     :param package_id:
#     :param package_chanle_dict:
#     :param decompile_dir:
#     :return:
#     """
#     manifest_path = path_utils.get_full_path(decompile_dir + "/AndroidManifest.xml")
#     if not os.path.exists(manifest_path):
#         Logger.error("AndroidManifest.xml not exists")
#         return False
#     try:
#         # 根据渠道标识获取本地融合渠道id
#         channel_id = Channel.get_channel_id(channel_name).get("channel_id")
#         if channel_id is None:
#             channel_id = ""
#         elementTree.register_namespace("android", android_ns)
#         tree = elementTree.parse(manifest_path)
#         root = tree.getroot()
#
#         application = root.find("application")
#         if application is None:
#             return False
#
#         name = "{" + android_ns + "}name"
#         value = "{" + android_ns + "}value"
#         create_package_id = True
#         create_chanle_id = True
#         create_platform_chanle_id = True
#
#         meta_datas = root.find(".//application").findall("meta-data")
#         if meta_datas is None:
#             package_id_node = elementTree.SubElement(application, "meta-data")
#             package_id_node.set(name, "3KWAN_PackageID")
#             package_id_node.set(value, package_id)
#
#             chanle_id_node = elementTree.SubElement(application, "meta-data")
#             chanle_id_node.set(name, "3KWAN_ChanleId")
#             chanle_id_node.set(value, package_chanle_dict[package_id])
#
#             platform_id_node = elementTree.SubElement(application, "meta-data")
#             platform_id_node.set(name, "3KWAN_Platform_ChanleId")
#             platform_id_node.set(value, channel_id)
#         else:
#             for meta_data in meta_datas:
#                 meta_data_name = meta_data.get(name)
#                 if meta_data_name == "3KWAN_PackageID":
#                     create_package_id = False
#                     meta_data.set(value, package_id)
#
#                 if meta_data_name == "3KWAN_ChanleId":
#                     create_chanle_id = False
#                     meta_data.set(value, package_chanle_dict[package_id])
#
#                 if meta_data_name == "3KWAN_Platform_ChanleId":
#                     create_platform_chanle_id = False
#                     meta_data.set(value, channel_id)
#             if create_package_id:
#                 package_id_node = elementTree.SubElement(application, "meta-data")
#                 package_id_node.set(name, "3KWAN_PackageID")
#                 package_id_node.set(value, package_id)
#
#             if create_chanle_id:
#                 chanle_id_node = elementTree.SubElement(application, "meta-data")
#                 chanle_id_node.set(name, "3KWAN_ChanleId")
#                 chanle_id_node.set(value, package_chanle_dict[package_id])
#
#             if create_platform_chanle_id:
#                 platform_id_node = elementTree.SubElement(application, "meta-data")
#                 platform_id_node.set(name, "3KWAN_Platform_ChanleId")
#                 platform_id_node.set(value, channel_id)
#
#         tree.write(manifest_path, "utf-8")
#         return True
#     except Exception as e:
#         Logger.error("handle_v2_common_params() error " + str(e))
#         return False
#
#
# def handle_v2_origin(decompile_dir: str) -> bool:
#     if del_smali_code(decompile_dir) and delete_so_file(decompile_dir) and del_3k_res(
#             decompile_dir) and del_manifest_infos(decompile_dir):
#         file_utils.del_system_label(decompile_dir, '$')
#         file_utils.del_system_label(decompile_dir, 'ic_launcher_foreground')
#         file_utils.del_system_label(decompile_dir, 'ic_launcher_background')
#         file_utils.del_file_folder(decompile_dir + "/res/mipmap-anydpi-v26")
#         file_utils.del_file_folder(decompile_dir + "/res/drawable-v24")
#         Logger.info("handle_v2_origin() success")
#         return True
#     else:
#         Logger.error("handle_v2_origin() error")
#         return False
