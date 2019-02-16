# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-02-14.
# Copyright (c) 2019 3KWan.
# Description :
import json


class JsonToolKit:
    def __init__(self):
        pass

    @staticmethod
    def json2File(_json, _filePath):
        try:
            with open(_filePath, 'w') as f:
                f.write(json.dumps(_json, indent=4))
                return True
        except Exception, e:
            print 'json2File fail , error msg : ' + str(e)
            return False

    @staticmethod
    def file2Json(_filePath):
        try:
            with open(_filePath, 'r') as f:
                return json.dumps(json.loads(f.read()), indent=4)
        except Exception, e:
            print 'file2Json fail , error msg : ' + str(e)
            return None
