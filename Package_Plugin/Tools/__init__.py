# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-01-14.
# Copyright (c) 2019 3KWan.
# Description : tools unit test

if __name__ == '__main__':
    with open('/Users/suyghur/Android/permission.xml', 'r') as f:
        permission = f.read()
    with open('/Users/suyghur/Android/test.xml', 'r') as f:
        test = f.read()
    with open('/Users/suyghur/Android/test.xml', 'w') as f:
        test = test.replace('<kkkwan>kkkwan_special_permission</kkkwan>', permission)

    print test