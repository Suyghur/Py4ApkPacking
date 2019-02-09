# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-19.
# Copyright (c) 2019 3KWan.
# Description : the toolkit of Apk
from Package_Plugin.Tools.tl_CmdToolKit import CmdToolKit
from Package_Plugin.mod_GlobalStaticVars import GlobalStaticVars


class ApkToolKit:

    def __init__(self):
        pass

    @staticmethod
    def decompileApk(_apkPath, _apkOutPath, _apkJarPath=None):
        if _apkJarPath is None:
            _apkJarPath += GlobalStaticVars.__TOOLS_APKTOOL_JAR_PATH__
        print 'doing decompileApk'

        bashScript = 'java -jar ' + _apkJarPath + ' d -f ' + _apkPath + ' -o ' + _apkOutPath

        if CmdToolKit.execCmdLine(bashScript):
            return True
        else:
            return False

    @staticmethod
    def compileApk(_apkFolderPath, _apkOutPath, _apkJarPath=None):
        if _apkJarPath is None:
            _apkJarPath = GlobalStaticVars.__TOOLS_APKTOOL_JAR_PATH__

        print 'doing compileApk'

        bashScript = 'java -jar ' + _apkJarPath + ' b ' + _apkFolderPath + ' -o ' + _apkOutPath

        if CmdToolKit.execCmdLine(bashScript):
            return True
        else:
            return False

    @staticmethod
    def signedApk(_signApkPath, _signedApkPath, _keyStorePath, _keyStorePwd, _keyStoreAlias):
        # jarsigner  -digestalg SHA1 -sigalg MD5withRSA -keystore cbzj_3k.keystore
        # -storepass cbzj_3k2019 -signedjar abc_signed.apk abc.apk alias.cbzj_3k2019
        print 'doing signedApk'
        bashScript = 'jarsigner -digestalg SHA1 -sigalg MD5withRSA -keystore ' + _keyStorePath + ' -storepass ' + _keyStorePwd + ' -signedjar ' + _signApkPath + ' ' + _signedApkPath + ' ' + _keyStoreAlias
        if CmdToolKit.execCmdLine(bashScript):
            return True
        else:
            return False
