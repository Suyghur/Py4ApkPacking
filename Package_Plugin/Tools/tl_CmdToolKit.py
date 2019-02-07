# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-02-06.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of the command-exec
import subprocess


class CmdToolKit:
    def __init__(self):
        pass

    @staticmethod
    def execCmdLine(_bashScript):
        p = subprocess.Popen(_bashScript, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
        status = p.wait()
        for line in p.stdout.readlines():
            print line
        return status
