# 1.概要说明

由于Python源码部署的特性、实际业务中需要隔离两端的代码、客户端打包逻辑变动频率高等原因，Web版的Android批量打包工具整体设计如下：

1)采用“插件式”开发模式，提供宿主和插件package。

2)线上服务端php调用宿主端完成一整套打包流程，无需关注内部具体逻辑实现。宿主端是一个“壳”程序，内部打包流程定型，无特殊原因不会修改。

3)插件端是具体打包逻辑的实现，更新频繁

4)原理实现：利用Python的反射机制，预加载和运行时加载相应包的模块中的类。其中运用到了`__import__()`和`importlib`模块中的`import_module()`方法。

动态装载

```python
# 动态装载
# @param _moduleName : 模块名
# @param _clzName : 类名
# @param _packageName : 包名
# @return 类对象
def dynamicLoadingPlugin(self, _moduleName, _clzName, _packageName=Package_Plugin):
    mod = importlib.import_module('.' + _moduleName, _packageName)
    return getattr(mod, _clzName)
```

静态装载

```python
# 静态装载
# @param _moduleName : 模块名
# @param _clzName : 类名
# @param _packName : 包名
# @return 类对象
def preLoadingPlugin(self, _moduleName, _clzName, _packageName='Module_Plugin'):
    mod = __import__(_packageName + "." + _moduleName, fromlist=[_clzName])
    return getattr(mod, _clzName)
```

# 2.Demo

1)工程目录

python4apkpacking

​	--Module_Host

​		--main.py

​		--PluginHelper.py

​	--Module_Plugin

​		--Plugin1.py

​		--Plugin2.py



2)main.py

```python
from PluginsHelper import PluginsManager

if __name__ == '__main__':
    # ----- 启动时加载 ------
    # no params
    # mod1=__import__('Module_Plugin.Plugin1',fromlist=('Plugin1'))
    # clz1=getattr(mod1,'Plugin1')
    # clz1().PluginPrint()

    # ------ 使用时加载 ------
    # no params
    # mod3 = importlib.import_module('.Plugin1', 'Module_Plugin')
    # clz3=getattr(mod3,'Plugin1')
    # clz3().PluginPrint()

    # have params
    # mod4 = importlib.import_module('.Plugin2', 'Module_Plugin')
    # mod4.PluginPrintWithParam('123')

    # ------ 使用时加载 ------
    manager = PluginsManager()
    mod1 = manager.DynamicLoadingPlugin('Plugin1', 'Plugin1')
    mod1().PluginPrint()

    # ------ 启动时加载 ------
    mod2 = manager.PreLoadingPlugin('Plugin2', 'Plugin2')
    mod2().PluginPrintWithParam('123')
```



3)PluginHelper.py

```python
import importlib


class PluginsManager():

    # 动态装载
    # @param _moduleName : 模块名
    # @param _clzName : 类名
    # @param _packageName : 包名
    # @return 类对象
    def DynamicLoadingPlugin(self, _moduleName, _clzName, _packageName='Module_Plugin'):
        mod = importlib.import_module('.' + _moduleName, _packageName)
        return getattr(mod, _clzName)

    # 静态装载
    # @param _moduleName : 模块名
    # @param _clzName : 类名
    # @param _packName : 包名
    # @return 类对象
    def PreLoadingPlugin(self, _moduleName, _clzName, _packageName='Module_Plugin'):
        mod = __import__(_packageName + "." + _moduleName, fromlist=[_clzName])
        return getattr(mod, _clzName)
```



4)Plugin1.py

```python
class Plugin1:

    def PluginPrint(self):
        print 'i am plugin1'
```



5)Plugin2.py

```python
class Plugin2:

    def PluginPrintWithParam(self,param):
        print 'i am plugin , the param is ' + param
```

