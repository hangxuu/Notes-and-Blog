# Effective python notes

## pythonic
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