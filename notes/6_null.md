# 6.NULL - The Missing Semester of Your CS Education
[课程主页](https://missing.csail.mit.edu/)

## The Shell
注：没按官方题号组织。
### Exercises
2. Create a new directory called missing under /tmp.
```shell
mkdir /tmp/missing
```


3. Use touch to create a new file called semester in missing.
```shell
cd /tmp/missing
touch semester
```


4. write 

```bash
#!/bin/sh
curl --head --silent https://missing.csail.mit.edu
```
into the file and try to execute the file.
```shell
sh semester # ok
./semester # permission denied 需给该文件执行权限
chmod 777 semester # 给了所有权限
./semester # ok
```
shebang 的作用，shell 通过它寻找执行该脚本程序的位置。


5. Use | and > to write the “last modified” date output by semester into a file called last-modified.txt in your home directory.
```shell
./semester | grep --ignore-case last-modified | cut --delimiter=' ' -f2- > /home/last-modified.txt
```


6. Write a command that reads out your laptop battery’s power level or your desktop machine’s CPU temperature from /sys
```shell
# linux on winsows. battery's power
cat /sys/class/power_supply//battery/capacity
# 没找到 CPU 温度
```

## Shell Tools
- In general, in shell scripts the space character will perform argument splitting. 
- trings delimited with ' are literal strings and will not substitute variable values whereas " delimited strings will.
- ``$0``: Name of the script
- ``$1 - $9``: Arguments to the script. ``$1`` is the first argument and so on.
- ``$@``: All the arguments
- ``$#``: Number of arguments
- ``$?``: Return code of the previous command
- ``$$``: Process identification number (PID) for the current script
- ``!!``: Entire last command, including arguments. A common pattern is to execute a command only for it to fail due to missing permissions; you can quickly re-execute the command with sudo by doing sudo !!
- ``$_``: Last argument from the last command. If you are in an interactive shell, you can also quickly get this value by typing Esc followed by .
- The return code or exit status is the way scripts/commands have to communicate how execution went. A value of 0 usually means everything went OK; anything different from 0 means an error occurred.
- command substitution. ``for file in $(ls)``
- process substitution, ``<( CMD )``, This is useful when commands expect values to be passed by file instead of by STDIN. ``diff <(ls foo) <(ls bar)``

### Exercises
1. Read man ls and write an ls command that lists files in the following manner
- Includes all files, including hidden files.
- Sizes are listed in human readable format (e.g. 454M instead of 454279954)
- Files are ordered by recency
- Output is colorized

```shell
ls -lath --color=auto
```

2.  Write bash functions marco and polo that do the following. Whenever you execute marco the current working directory should be saved in some manner, then when you execute polo, no matter what directory you are in, polo should cd you back to the directory where you executed marco. For ease of debugging you can write the code in a file marco.sh and (re)load the definitions to your shell by executing source marco.sh.

```bash

marco(){
    export MARCO=$(pwd)
}

polo(){
    cd "$MARCO"
}

```

3. Say you have a command that fails rarely. In order to debug it you need to capture its output but it can be time consuming to get a failure run. Write a bash script that runs the following script until it fails and captures its standard output and error streams to files and prints everything at the end. Bonus points if you can also report how many runs it took for the script to fail.

```bash
# random.sh
n="$(( RANDOM % 100 ))"
if [[ n -eq 42 ]]; then
        echo "Something went wrong"
        >&2 echo "The error was using magic numbers"
        exit 1
fi
echo "Everything went according to plan"

```
count.sh 为本题答案。

```bash
# count.sh
count=0
while true; do
        ./random.sh &> out.txt
        if [[ "$?" -eq 1 ]]; then
                break
        fi
        #echo "$count"
        count=$(( count + 1))
done
echo "$count runs before it fails"
cat out.txt
```

4. 