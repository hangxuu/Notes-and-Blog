### Getting Started

当我们接触一门新语言，第一件事就是写出相应版本的**Hello world**。那么，让我们开始吧！
```haskell
-- hello.hs my first haskell file
main = do
    putStrLn "Hello world"
```

想要运行这个简单的程序，你需要一个编译器。去 [官方网站](https://www.haskell.org/platform/) 下载**haskell-platform**，安装。现在，你已经完全准备就绪了！
```haskell
$ ghc hello.hs
[ 1 of 1 ] Compiling Main
Linking hello ...
```
如果编译成功，GHC会创建以下三个文件：

- hello (windows 上为hello.exe)
- hello.hi
- hello.o

学过C++的对这个过程应该不会感到陌生，编译然后链接，这是编译型语言生成机器可执行文件的一般过程。如果不太明白也没有关系，现在只需要知道**hello**就是最后生成的可执行文件就行。你可以执行这个文件。

```haskell
$ ./hello
Hello world
```

每一个编译的Haskell程序都需要有一个``main``，就和C++中的``int main()``是一个作用。是程序开始运行的切入点。

### GHCi

神奇的是，haskell还为我们提供了一个GHC的交互接口，用起来就和python等解释型语言一样。你可以这样打开它：

```haskell
$  ghci
 Prelude> 
```

你可以把它当作计算器用。

```haskell
Prelude> 1 + 1
2
Prelude> x = 2 + 2
Prelude> x
4
Prelude> f x = x * 2
Prelude> f 4
8

-- GHCi的早期版本定义变量和函数可能需要使用let关键字

Prelude> let x = 2 + 2
Prelude> x
4
Prelude> let f x = x * 2
Prelude> f 4
8
```

Prelude是GHCi预先加载的一个文件，里面包含常用的函数和变量。你也可以把你自己的文件加载进去以进行交互。有两种方法可以做到：

- ``$ ghci hello.hs``    终端提示符下操作
- ``Prelude> :l hello.hs``    Prelude提示符下操作。

导入成功后，你就可以调用你文件里的函数了。（需要说明的是，作为导入GHCi的文件不需要必须包含**main**，编译文件时才作此要求。）

```haskell 
Prelude> :l hello.hs
Ok, one module loaded.
Main> main
Hello world
```

以后当你修改文件需要重新导入的时候只需要在Prelude提示符下``:r``就可以了，即**reload**的意思。``:q``退出GHCi。
