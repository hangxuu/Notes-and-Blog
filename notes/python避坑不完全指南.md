### （1）尽量避免多分支返回，特别是多层if（两层以上）嵌套的情况
先来看个例子。下面函数的功能是完善省市信息，如果 ``utype`` 是 ``c``，说明 ``city_or_prov`` 是城市，如果为 ``p``，则为省份。如果不传 ``utype`` ，则直接返回 ``city_or_prov`` 参数。
```python
def add_suffix(city_or_prov, utype=None):
    if utype == 'c':
        if city_or_prov[-1] != '市':
            return city_or_prov + '市'
    elif utype == 'p':
        if city_or_prov[-1] != '省':
            return city_or_prov + '省'
    else:
        return city_or_prov
```
大家能看出上面函数有什么问题吗？如果传入 ``('上海', 'c')``，那么返回 ``上海市`` 。没有问题。传入 ``('陕西', 'p')`` 也不会有问题。可是如果传入 ``('上海市', 'c')``，这时程序会返回``None``！！因为程序进入第一个``if``后不满足第二个``if``条件，而后续也没有相应代码，所以程序直接返回默认值``None``。python不要求返回值类型必须一致，甚至可以不返回值，但我们在享受这种灵活性的同时要警惕不要制造隐含的bug。

修改的方法是使用单一``return``语句。上例修改如下：
```python
def add_suffix(city_or_prov, utype):
    if utype == 'c':
        if city_or_prov[-1] != '市':
            city_or_prov = city_or_prov + '市'
    elif utype == 'p':
        if city_or_prov[-1] != '省':
            city_or_prov = city_or_prov + '省'

    return city_or_prov
```
**if语句中修改变量后不要直接返回，而是统一赋给一个变量，在函数末尾进行返回。**

提出这个建议的原因是，一层``if``的话，我们往往能够记得写相应的``else``，可一旦``if``嵌套超过一层，我们就很容易忽略写对应的``else``子句。此时应该使用单一``return``语句，而不要在各个分支内分别``return``。

### （2）不要滥用``try/except``块
我看过很多人写的代码，一进函数体就``try``，然后在函数末尾``except``，或者稍微好点，只把一大部分而不是全部代码包到``try/except``块里。
大概类似这样：
```python
def run(example_list):
    try:
        item = example_list[0]
        item += 1
        # code to process item and other codes
        ...
        ...
    except Exception as e:
        logger.error(e)
```
这样程序跑起来基本上不会崩，但同时也失去了异常处理的意义。很多人只要程序正常结束了，就不会去看日志。更何况多进程的程序一旦跑起来日志基本上就乱的不能看了，所以即使去看日志，想找到``error``也是难上加难。

那么应该怎么做呢？

**“尽早暴露错误”** 原则，如果程序要崩溃，那就让它尽早崩溃，然后修改bug，提高质量。具体到代码中，还是以上面例子为例：
```python
def run(example_list):
    try:
        item = example_list[0]
    except Exception as e:
        logger.error(e)
    else:
        item += 1
        # code to process item and other codes
        ...
        ...
```
把确定不会出错的代码转移至``else``子句。``try``中只放可能会引发异常的语句。这样，当错误发生时，就能更快的定位到错误的位置。特别是``try``里面有多条可能会引发异常的语句时（上例只写了一条），应该把它们分开，使每个``try``中只含一条可能会引发异常的语句。

### （3）不要在程序中使用文件相对路径
这个例子可能不是很好帖，先说结论。**在函数调用的过程中，当前路径.代表的是被执行的脚本文件的所在路径**。也就是说，执行不同的脚本文件，对同一相对路径的解析会出现不同的结果！！

项目的目录树如下图，同级目录已用相同颜色标出。

![目录树](https://github.com/hangxuu/blog/blob/master/images/path_1.png)

``E:\test_dir\test_path\codes\read_file.py`` 文件如下：
``` python
import os

file_path = '../data/hello.txt'
print(os.path.abspath(file_path))
with open(file_path, 'r') as f:
    for line in f:
        print(line)
```
我在这个脚本中使用了文件相对路径。

直接运行这个脚本，``print(os.path.abspath(file_path))`` 的输出是 ``E:\test_dir\test_path\data\hello.txt``。

运行 ``E:\test_dir\a_test_file.py``文件（该文件只有一句``from test_path.codes import read_file``），``print(os.path.abspath(file_path))`` 的输出是 ``E:\data\hello.txt``。

可见，相对路径的解析会根据执行脚本的不同而不同。如上例，程序自然会报 ``FileNotFoundError``，但如果你的项目所有使用这个相对路径的脚本都在同一目录下，或者运气好目录的深度相同，那就不会报错，而会成为一个隐形的bug。

解决方法：
修改 ``E:\test_dir\test_path\codes\read_file.py`` 文件如下：
``` python
import os

file_abs_path = os.path.abspath(__file__)
file_path = os.path.join(os.path.dirname(os.path.dirname(file_abs_path)), 'data', 'hello.txt')
print(file_path)
with open(file_path, 'r') as f:
    for line in f:
        print(line)
```
``file_abs_path = os.path.abspath(__file__)`` 会得到当前脚本（该行程序所在脚本）的绝对路径，然后用 ``os`` 模块提供的方法一步步去寻找所需文件。这样虽然写起来是麻烦了一些。但可以解决路径解析问题，而且还做到了跨平台兼容。