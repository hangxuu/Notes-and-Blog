### （1）多用 assert

``` python
assert expression [, arguments]
# 等价于
if not expression:
    raise AssertionError(arguments)
```
让程序在自己控制的条件下运行，arguments 输出一些错误原因。
