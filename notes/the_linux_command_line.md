# The Linux Command Line

由于本书每章节内容较少，就不按章节记录，而是按照系统各模块进行记录。

<!-- GFM-TOC -->

* [一、文件系统](#文件系统)

<!-- GFM-TOC -->

## 文件系统
- df：查看磁盘使用情况。
- pwd：打印当前工作目录。
- cd：修改工作目录。``cd``回到个人主目录，``cd -``回到上一个工作目录，``cd ~usrename``切到 username 的个人主目录。
- file：``file filename`` determine a file’s type.
- less：``less filename`` Viewing File Contents, ``q`` to exit.

### ls
```
// command -options arguments
ls -a：列出所有文件，包括隐藏文件。
ls -d：列出目录。
ls -lh：组合长格式，human-readable。
ls --reverse：输出逆序显式。
```

- cp: copy files and dictionaries
- mv: move/rename files and dictionaries
- mkdir: Create directories 
- rm: Remove files and directories 
- ln: Create hard and symbolic links

软链接和硬链接的区别：软链接可以链接目录和文件，硬链接只能链接文件；硬链接相当于引用计数，每创建一个硬链接，对该文件的引用加一，之后无论是删除硬链接还是删除原文件，对该文件（内存块）的引用减一，当引用为0时系统删除该文件。软链接则相当于指针（独立于原文件的特殊文件），当原文件删除后，软链接就会失效。