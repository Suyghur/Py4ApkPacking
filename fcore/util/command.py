# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import importlib
import re
import subprocess
import sys


def exec_command(cmd) -> bool:
    print(cmd)
    cmd = cmd.replace('\\', '/')
    cmd = re.sub('/+', '/', cmd)
    try:
        importlib.reload(sys)
        # sys.setdefaultencoding('utf-8')

        s = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = s.communicate()

        # if platform.system() == "Windows":
        #     stdoutput = stdoutput.decode("gbk")
        #     erroutput = erroutput.decode("gbk")

        if s.returncode == 1:
            print(out)
            print(err)
            # Logger.error("*********ERROR********", "cmd_utils")
            # Logger.error(stdoutput)
            # Logger.error(erroutput)
            # Logger.error("*********ERROR********", "cmd_utils")
            # shell = "shell error : " + shell + " !!!exec Fail!!! "
            return False
        else:
            # Logger.info(stdoutput, "cmd_utils")
            # Logger.info(erroutput, "cmd_utils")
            # cmd = cmd + " !!!exec packing!!! "
            # Logger.info(shell, "cmd_utils")
            return True
    except Exception as e:
        print(e)
        return False
