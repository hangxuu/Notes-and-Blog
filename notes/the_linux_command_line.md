# The Linux Command Line

<!-- GFM-TOC -->

* [一、learning the shell](#learning-the-shell)


<!-- GFM-TOC -->

## learning the shell

### exploring the system
- df：查看磁盘使用情况。
- pwd：打印当前工作目录。
- cd：修改工作目录。``cd``回到个人主目录，``cd -``回到上一个工作目录，``cd ~usrename``切到 username 的个人主目录。
- file：``file filename`` determine a file’s type.
- less：``less filename`` Viewing File Contents, ``q`` to exit.
- ls: ``ls -a`` 列出所有文件，包括隐藏文件。 ``ls -d`` 列出目录。 ``ls -lh`` 组合长格式，human-readable。``ls --reverse``输出逆序显式。
- cp: copy files and dictionaries
- mv: move/rename files and dictionaries
- mkdir: Create directories 
- rm: Remove files and directories 
- ln: Create hard and symbolic links

软链接和硬链接的区别：软链接可以链接目录和文件，硬链接只能链接文件；硬链接相当于引用计数，每创建一个硬链接，对该文件的引用加一，之后无论是删除硬链接还是删除原文件，对该文件（内存块）的引用减一，当引用为0时系统删除该文件。软链接则相当于指针（独立于原文件的特殊文件），当原文件删除后，软链接就会失效。

### commands
command有四种不同的类型：（1）一个可执行程序，（2）shell builtins，（3）shell function，（4）an alias 别名。
- type: Display a Command’s Type, 上述四种之一。
- which
- help
- man
- apropos
- info
- whatis: Display one-line manual page descriptions.
- alias: Create an alias for a command. for example, ``alias foo='cd /home; ls'``.

### redirection
- cat: Concatenate files. ``cat filename1 filename2 > filename``, ``&>, &>>``.
- sort: Sort lines of text. 用于管道
- uniq: Report or omit repeated lines. 用于管道
- grep: Print lines matching a pattern. ``grep 0*.jpg`` 打印所有以0开头，.jpg结尾的文件名。``-i 忽略大小写``
- wc: Print newline, word, and byte counts for each file. ``-l 只打印行数``
- head: Output the first part of a file. ``-n 打印前 n 行``
- tail: Output the last part of a file. ``-n 打印后 n 行， -f 实时查看日志文件时使用``.
- tee: Read from standard input and write to standard output and files. 用于把管道中间的结果保存到文件。

