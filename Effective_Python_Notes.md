# Effective Python Notes

<!-- GFM-TOC -->
* [一、Pythonic](#Pythonic)
* [二、并发与并行](#并发与并行)
<!-- GFM-TOC -->

## Pythonic

### （1）弄清你的python版本

``` python
# in terminal
python --version 
# or 
python3 --version
# in code
import sys
print(sys.version_info)
# or
print(sys.version)
```

这条建议的目的是：**确保机器执行程序的python版本和你预期的为同一版本。** 可以在程序中加层保障，比如该程序需要python3.6及以上版本才可以执行，那么可在程序开头加上以下代码：

``` python
import sys
assert sys.version_info >= (3, 6)

```

这样，当机器执行的python版本小于3.6时就会报``AssertionError``异常。此时，你可能需要做的就是安装合适版本的python解释器。

### （2）PEP8规范

代码风格请遵循PEP8规范，这样可以写出更好看以及更易懂的代码。具体内容请参阅 [官方文档](https://www.python.org/dev/peps/pep-0008/) 。

### （3）弄清楚bytes和str的区别

- bytes存的是8位无符号值，str存的是Unicode码位。str是给人看的，bytes是给机器看的。
- 把码位转换为字节序列的过程是编码，把字节序列转换为码位的过程是解码。
- Unicode三明治：尽早将bytes解码为Unicode，尽晚将Unicode编码为bytes。在程序中只使用Unicode字符。
- 不对外部数据编码做任何假设，读/写文件时请显式指定编码。

代码示例：

``` python
In [18]: a = b'hello world'
# a为ASCII编码的字节序列
In [19]: list(a)
Out[19]: [104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]

In [20]: b = 'hello world'
# b为Unicode码位
In [21]: list(b)
Out[21]: ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

# 字节序列 --> 码位（解码，显式指定编码）
In [22]: list(a.decode(encoding='utf-8'))
Out[22]: ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

# 码位 --> 字节序列（编码，显式指定编码）
In [23]: list(b.encode(encoding='utf-8'))
Out[23]: [104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]
```
读写文件示例：
``` python
with open(filename, 'r', encoding='utf-8') as f:
    # deal with f

with open(filename, 'w', encoding='utf-8') as f:
    f.write('some Unicode string')
```
如果要直接读写二进制文件，则将'r', 'w' 相应换为 'rb', wb'即可。

### （4）字符串格式化（F-string）

python提供了四种格式化字符串方法。

1. C 风格的 % 格式
2. format函数
3. str.format()方法
4. F-string

有人喜欢用第一种，有人喜欢用第三种（比如我），而作者推荐用第四种。我的建议是选择一种用熟练就行，推荐第四种F-string。
因为F-string可以少打很多字。
示例：
``` python
In [1]: key = 'my_val'

In [2]: value = 1.2345

# C 风格 % 格式
In [3]: s1 = '%-10s = %.2f' % (key, value)

In [4]: s1
Out[4]: 'my_val     = 1.23'

# str.format()函数
In [5]: s2 = '{:<10} = {:.2f}'.format(key, value)

In [6]: s2
Out[6]: 'my_val     = 1.23'

# F-string格式
In [7]: s3 = f'{key:<10} = {value:.2f}'

In [8]: s3
Out[8]: 'my_val     = 1.23'
```
可以看出F-string和前两种方法最大的区别就是前两种方法对变量没有直接访问权，需要在格式化字符串中设置占位符，然后通过位置参数（也支持键值对参数）将变量值传递进去。而F-string对同作用域的变量有直接访问权。

以下示例可能更能说明这一点。
``` python
# 自定义字符串处理函数，大小写相间。
In [24]: def personality(s):
    ...:     new_s = ''
    ...:     for i in range(len(s)):
    ...:         if i % 2:
    ...:             new_s += s[i].upper()
    ...:         else:
    ...:             new_s += s[i].lower()
    ...:     return new_s
    
In [25]: s = 'hello'

In [26]: s1 = '%s world' % personality(s)

In [27]: s1
Out[27]: 'hElLo world'

In [28]: s2 = '{} world'.format(personality(s))

In [29]: s2
Out[29]: 'hElLo world'

In [32]: s3 = f'{personality(s)} world'
    
In [33]: s3
Out[33]: 'hElLo world'
```
F-string可以直接在格式化字符串中执行我的自定义函数。

另外，如果你最终在三种方法中选择了F-string，千万别忘了F-string的 ``f``前缀。

### （5）使用辅助函数代替复杂的表达式

如果发现某条表达式变得复杂难懂或者重复多次时（DRY：Don't repeat youself），就应该将该处逻辑分离出来编写为小函数。这样做的好处有：

1. 代码更清晰易懂。
2. 代码可复用。

### （6）使用序列解包完成多变量赋值

先看一下python实现的冒泡排序。
``` python
def bubble_sort(lst):
    for _ in range(len(lst)):
        for i in range(1, len(lst)):
            if lst[i] < lst[i-1]:
                # 数据交换
                lst[i], lst[i-1] = lst[i-1], lst[i]
```
如果采用C风格方式编写，则是如下代码：
``` python
def bubble_sort(lst):
    for _ in range(len(lst)):
        for i in range(1, len(lst)):
            if lst[i] < lst[i-1]:
                # 数据交换
                tmp = lst[i]
                lst[i] = lst[i-1]
                lst[i-1] = tmp
```
它们的区别就在于数据交换部分。C语言风格的语法需要一个临时变量``tmp``来保存中间结果以完成交换。而python则使用 **序列解包** 省掉了这个临时变量。使代码量更少且可读性高。

原理： **其实序列解包也用到了临时变量，具体说是临时元组。序列解包先计算赋值号右侧，将计算结果保存到一个临时元组中，然后将这个临时元组再赋值给赋值号左侧。这就是``a, b = b, a``能正常工作的原因。**

序列解包除了用于多变量赋值，也常用于``for``循环中。例：
``` python
persons = [('taylor', 29), ('hans', 25), ('bob', 12)]

# 序列解包
for name, age in persons:
    print(f'{name} is {age} years old')
```
直接对列表``persons``里的元素进行解包，赋予它们更有意义的变量名，可以让程序更易读。避免写成下面这样：
``` python
for item in persons:
    name = item[0]
    age = item[1]
    print(f'{name} is {age} years old')
```

### （7）多使用 enumerate 而不是 range

如果你同时需要可迭代序列（如list）的索引和元素值，那么可以用``enumerate``代替``range``来提高可读性。
``` python
# 使用range
for i in range(len(lst)):
    print(f'{i + 1} item is {lst[i]}')
    
# 使用enumerate
for i, item in enumerate(lst, start=1):
    print(f'{i} item is {item}')
```
``enumerate``可以指定索引的起始值（``start``参数，默认为0），如果需要从1开始计数，后续就省掉了加1的操作。

### （8）使用zip同步处理多个可迭代序列（如list）

对于两个（或多个）有相关性的可迭代序列（它们的序列长度是相同的）。我们可以用某一个序列的长度来做``for``循环的``range``参数，这样不会出错，但可读性差。使用``zip``函数可以提高可读性。如下例所示：

``` python
In [5]: names = ['Cecilia', 'Lise', 'Marie']

In [6]: counts = [len(item) for item in name]

In [7]: for i in range(len(names)):
   ...:     print(f'{names[i]}: {counts[i]}')
   ...:
Cecilia: 7
Lise: 4
Marie: 5

In [8]: for name, count in zip(names, counts):
   ...:     print(f'{name}: {count}')
   ...:
Cecilia: 7
Lise: 4
Marie: 5
```
``zip``函数以两个或多个可迭代对象作为参数，返回一个生成器，该生成器每次生成以参数中每一个可迭代对象的下一个值组成的元组。

值得注意的是，如果``zip``函数的参数序列长度不相同，则``zip``函数返回元组项的个数和参数中最短的序列元素个数相同。如果需要元组项个数和参数中最长的序列元素个数相同，则可以使用``itertools.zip_longest``函数。如下例所示：
```python
In [33]: names.append('Taylor swift')
    
In [34]: for name, count in zip(names, counts):
    ...:     print(f'{name}: {count}')
    ...:
Cecilia: 7
Lise: 4
Marie: 5
# 输出没有 Taylor swift

In [35]: import itertools

In [36]: for name, count in itertools.zip_longest(names, counts):
    ...:     print(f'{name}: {count}')
    ...:
Cecilia: 7
Lise: 4
Marie: 5
Taylor swift: None
```
当参数中较短的可迭代对象耗尽时，将使用``fillvalue``关键字参数的提供的值（默认为``None``）作为它们的填充值。

### （9）避免在``for/while``循环后直接使用``else``代码块

先说一句，这个语法我还是蛮常用的。并不觉得会产生什么歧义。当循环正常结束时会执行``else``代码块，否则不执行（比如循环中途``break``出来）。

当你需要在循环中寻找某个东西，只有当整个循环都没有找到时才执行某些操作。就很符合这个应用场景。这种场景下一般``for``循环里会有``if``代码块，``if``代码块里会有``break``语句，当执行了``if``代码块（``if``的条件为真）程序就会``break``出循环。和普通的``if/else``语法一样，当执行了``if``块，就不会执行``else``块。只不过这块是多个``if``对应一个``else``，只有当所有循环都没有执行``if``块时，才会执行``else``块。举个简单的例子，假如你想在姓名列表中找到第一个姓名长度大于5的姓名并打印输出，如果找不到则打印``Not found``。你可以这样写：
```python
for name in names:
    if len(name) > 5:
        print(name)
        break
else:
    print('Not Found')
```
作者提供了两种替换写法。

第一种：（作者在这里耍了小心机，替换了需求，把打印输出改成了直接作为返回值返回。）
```python
for name in names:
    if len(name) > 5:
        return name
return 'Not Found'
```

第二种还是可以接受的，在``for``循环之前为变量设置默认值来省掉``else``子句：
```python
rst_output = 'Not found'
for name in names:
    if len(name) > 5:
        rst_output = name
        break
print(rst_output)
```
你可以根据自己喜好选择``for/else``或作者提供的第二种替代写法。

### （10）海象运算符（:=）的使用场景

这是我想要很久的语法了！终于在python3.8加了进来！它可以减少很多重复代码或重复计算。话不多说，先看第一个应用场景。
```python
# 最接近的三数之和 leetcode 16.
# 题目中需要维护一个所有三元组之和与target值的最小距离（绝对值最小），最后返回这个距离最小的三元组之和
# diff是维护的最小距离

# 方法一（重复计算）
if abs(three_sum - target) < diff:
    diff = abs(three_sum - target)
    
# 方法二（可读性差，distance只会在if代码块中用到，定义在if代码块上面感觉是个更大作用域的变量）
distance = abs(three_sum - target)
if distance < diff:
    diff = distance
    
# 海象运算符（:=）
if (distance := abs(three_sum - target)) < diff:
    diff = distance
```
一般大家写代码的时候都会直接把计算写进条件语句，而不是提前想到之后可能会用到计算结果，然后先计算把结果保留，再用结果做条件判断（大多数人是懒得做这个预判的）。而且能这样写就说明有很大可能计算结果除了做条件判断在其他地方不会用到。所以我一般是先写成普通条件语句，后面发现会用到计算结果再把其改为海象运算符格式。

海象运算符（:=）先执行赋值操作，把右侧表达式计算结果赋值给左侧变量，然后以左侧变量计算条件语句真假。因为海象运算符的优先级低于比较运算符，所以如果左侧变量是条件语句的一部分，则需要给海象运算符的操作加上括号以得到预期的结果。

海象运算符还可用于实现C语言中``do/while``功能。这也是它的第二个应用场景。直接贴作者的例子吧。
```python
fresh_fruit = pick_fruit() 
while fresh_fruit: 
    for fruit, count in fresh_fruit.items(): 
        batch = make_juice(fruit, count) 
    fresh_fruit = pick_fruit()
```
上面的代码在进入循环之前需要先进行一次计算。使用海象运算符可以这样写：
```python
while fresh_fruit := pick_fruit(): 
    for fruit, count in fresh_fruit.items(): 
        batch = make_juice(fruit, count)
```
把计算本身放到条件语句中，而不是只把计算结果放到条件语句中。

## 并发与并行

### （52）使用``subprocess``模块管理子进程

如果需要在python脚本中执行系统命令，可以用``os``模块，比如执行``os.system('cd /; ls')``。现在推荐使用``subprocess``模块来完成这些功能。
```python
In [35]: import subprocess

In [36]: result = subprocess.run(['echo',  'hello word'], capture_output=True, encoding='utf-8')

In [37]: print(result.stdout)
hello word

```
等有需求再来具体学习这个模块吧。

