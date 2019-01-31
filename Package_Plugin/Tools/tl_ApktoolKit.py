# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-19.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of Apktool
import subprocess


class ApktoolKit:
    __APKTOOL_JAR_PATH__ = './local/bin'

    def __init__(self):
        pass

    @staticmethod
    def decompileApk(_apkPath, _apkOutPath, _apkJarPath=None):
        if _apkJarPath is None:
            _apkJarPath += ApktoolKit.__APKTOOL_JAR_PATH__
        print 'doing decompileApk'

        bashScript = 'java -jar ' + _apkJarPath + ' d -f ' + _apkPath + ' -o ' + _apkOutPath

        if ApktoolKit.execCmdLine(bashScript):
            return True
        else:
            return False

    @staticmethod
    def compileApk(_apkFolderPath, _apkOutPath, _apkJarPath=None):
        if _apkJarPath is None:
            _apkJarPath = ApktoolKit.__APKTOOL_JAR_PATH__

        print 'doing compileApk'

        bashScript = 'java -jar ' + _apkJarPath + ' b ' + _apkFolderPath + ' -o ' + _apkOutPath

        if ApktoolKit.execCmdLine(bashScript):
            return True
        else:
            return False

    @staticmethod
    def signedApk(_signApkPath, _signedApkPath, _keyStorePath, _keyStorePwd, _keyStoreAlias):
        # jarsigner  -digestalg SHA1 -sigalg MD5withRSA -keystore cbzj_3k.keystore
        # -storepass cbzj_3k2019 -signedjar abc_signed.apk abc.apk alias.cbzj_3k2019
        print 'doing signedApk'
        bashScript = 'jarsigner -digestalg SHA1 -sigalg MD5withRSA -keystore ' + _keyStorePath + ' -storepass ' + _keyStorePwd + ' -signedjar ' + _signApkPath + ' ' + _signedApkPath + ' ' + _keyStoreAlias
        if ApktoolKit.execCmdLine(bashScript):
            return True
        else:
            return False

    @staticmethod
    def execCmdLine(_bashScript):
        p = subprocess.Popen(_bashScript, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
        status = p.wait()
        for line in p.stdout.readlines():
            print line
        return status
