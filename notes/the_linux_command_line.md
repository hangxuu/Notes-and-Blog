# The Linux Command Line

由于本书每章节内容较少，就不按章节记录，而是按照系统各模块进行记录。

<!-- GFM-TOC -->

* [一、文件系统](#文件系统)

<!-- GFM-TOC -->

## 文件系统
- df：查看磁盘使用情况。
- pwd：打印当前工作目录。
- ls
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