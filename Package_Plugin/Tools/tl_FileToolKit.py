# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of file
import os
import shutil


class FileToolKit:
    def __init__(self):
        pass

    # 复制文件或者目录,复制前后文件完全一样
    @staticmethod
    def copyFile(_resFilePath, _disFolder):
        try:
            # 如果是文件
            if os.path.isfile(_resFilePath):
                shutil.copy(_resFilePath, _disFolder)
                return True
            # 如果是目录
            else:
                shutil.copytree(_resFilePath, _disFolder)
                return True
        except Exception, e:
            print 'copyFile fail , error msg : \t' + str(e)
            return False

    # find apk file
    @staticmethod
    def findApk(_currentDirUsed, _ret):
        try:
            fileList = os.listdir(_currentDirUsed)
            for fileName in fileList:
                de_path = os.path.join(_currentDirUsed, fileName)
                if os.path.isfile(de_path):
                    if de_path.endswith(".apk"):
                        _ret.append(de_path)
                else:
                    FileToolKit.findApk(de_path, _ret)
        except Exception, e:
            print 'findApk fail , error msg : \t' + str(e)

    # copy apk file
    @staticmethod
    def copyApk(_resApkPath, _disFolder):
        pass

    # 删除一个文件或者目录
    @staticmethod
    def deleteFile(_targetPath):
        try:
            # 如果_targetPath是文件时则调用unlink()否则调用rmdir()
            os.remove(_targetPath)
            return True
        except Exception, e:
            print 'deleteFile fail , error msg : \t' + str(e)
            return False

    # 重命名文件或文件夹
    @staticmethod
    def renameFile(_resFilePath, _newFileName):
        try:
            os.renames(_resFilePath, _newFileName)
            return True
        except Exception, e:
            print 'renameFile fail , error msg : \t' + str(e)
            return False

    # 判断一个文件是否存在 存在返回True
    @staticmethod
    def isExist(_filePath):
        try:
            return os.path.exists(_filePath)
        except Exception, e:
            print 'isExist fail error msg : \t' + str(e)
            return False

    # 创建目录
    @staticmethod
    def createDir(_disDirName):
        try:
            os.makedirs(_disDirName)
            return True
        except Exception, e:
            print 'createDir fail error msg : \t' + str(e)
            return False

    # read txt file
    @staticmethod
    def readTxtFile(_fileName):
        try:
            with open(_fileName, 'r') as f:
                return f.read()
        except Exception, e:
            print 'readTxtFile fail , error msg : ' + str(e)
            return None

    # write txt file
    @staticmethod
    def writeTxtFile(_fileName, _newStr):
        try:
            with open(_fileName, 'w')as f:
                f.write(_newStr)
                return True
        except Exception, e:
            print 'writeTxtFile fail , error msg : ' + str(e)
            return False
