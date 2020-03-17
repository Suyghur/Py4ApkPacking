# # _*_coding:utf-8_*_
# # Created by #Suyghur, on 2019-05-07.
# # Copyright (c) 2019 3KWan.
# # Description :
# import logging
# import logging.config
# import os
# import pathlib
#
#
# from fcore.constants.const_app_config import App
#
#
#
# def get_log_path() -> str:
#     if not pathlib.Path(App.LOG_PATH).exists():
#         os.makedirs(App.LOG_PATH)
#     return App.LOG_FILE_NAME
#
#
# class Logger:
#     __doc__ = "Logger"
#     # logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     file_handler = logging.FileHandler(get_log_path(), "w", "UTF-8")
#     file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     file_handler.setFormatter(file_formatter)
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(file_formatter)
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def info(msg, doc=None):
#         Logger.file_handler.setLevel(logging.INFO)
#         logger = logging.getLogger(doc)
#         logger.setLevel(logging.INFO)
#         logger.addHandler(Logger.file_handler)
#         logger.addHandler(Logger.stream_handler)
#         logger.info(msg)
#
#         return logger
#
#     @staticmethod
#     def debug(msg, doc=None):
#         Logger.file_handler.setLevel(logging.DEBUG)
#         logger = logging.getLogger(doc)
#         logger.setLevel(logging.DEBUG)
#         logger.addHandler(Logger.file_handler)
#         logger.addHandler(Logger.stream_handler)
#         if App.OWN_DEBUG_MODE:
#             logger.debug(msg)
#
#     @staticmethod
#     def warning(msg, doc=None):
#         Logger.file_handler.setLevel(logging.WARNING)
#         logger = logging.getLogger(doc)
#         logger.setLevel(logging.WARNING)
#         logger.addHandler(Logger.file_handler)
#         logger.addHandler(Logger.stream_handler)
#         logger.warning(msg)
#
#     @staticmethod
#     def error(msg, doc=None):
#         try:
#             Logger.file_handler.setLevel(logging.ERROR)
#             logger = logging.getLogger(doc)
#             logger.setLevel(logging.ERROR)
#             logger.addHandler(Logger.file_handler)
#             logger.addHandler(Logger.stream_handler)
#             logger.error(msg)
#         except Exception as e:
#             print(str(e))
#
#
# if __name__ == "__main__":
#     Logger.info("hahah")
#     Logger.debug("hahah")
#     Logger.error("hahah")
