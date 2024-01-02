---
title: Flag
index_img: /img/cover2-4.png
date: 2022-05-26 22:01:24
categories: 
- Go常用库
tags:
- Go常用库
---

# 04.Flag

## 01.Flag

- Go语言内置的flag包实现了命令行参数的解析，flag包使得开发命令行工具更为简单。

### 1.1 os.Args

- 如果你只是简单的想要获取命令行参数，可以像下面的代码示例一样使用os.Args来获取命令行参数
- os.Args是一个存储命令行参数的字符串切片，它的第一个元素是执行文件的名称。

```go
package main
import (
	"fmt"
	"os"
)

//os.Args demo
func main() {
	//os.Args是一个[]string
	if len(os.Args) > 0 {
		for index, arg := range os.Args {
			fmt.Printf("args[%d]=%v\n", index, arg)
		}
	}
}
/* 
C:\aaa\gin_demo> go run main.go a b c
args[1]=a
args[2]=b
args[3]=c
 */
```

### 1.2 flag.Parse()

通过以上两种方法定义好命令行flag参数后，需要通过调用flag.Parse()来对命令行参数进行解析。

支持的命令行参数格式有以下几种：

- -flag xxx （使用空格，一个-符号）
- --flag xxx （使用空格，两个-符号）
- -flag=xxx （使用等号，一个-符号）
- --flag=xxx （使用等号，两个-符号）

其中，布尔类型的参数必须使用等号的方式指定。

Flag解析在第一个非flag参数（单个”-“不是flag参数）之前停止，或者在终止符”–“之后停止。

### 1.3 其他函数

- flag.Args() ////返回命令行参数后的其他参数，以[]string类型
- flag.NArg() //返回命令行参数后的其他参数个数
- flag.NFlag() //返回使用的命令行参数个数

## 02.完整示例

### 2.1 main.go

```go
package main
import (
	"flag"
	"fmt"
	"time"
)

func main() {
	//定义命令行参数方式1
	var name string
	var age int
	var married bool
	var delay time.Duration
	flag.StringVar(&name, "name", "张三", "姓名")
	flag.IntVar(&age, "age", 18, "年龄")
	flag.BoolVar(&married, "married", false, "婚否")
	flag.DurationVar(&delay, "d", 0, "延迟的时间间隔")

	//解析命令行参数
	flag.Parse()
	fmt.Println(name, age, married, delay)
	//返回命令行参数后的其他参数
	fmt.Println(flag.Args())
	//返回命令行参数后的其他参数个数
	fmt.Println(flag.NArg())
	//返回使用的命令行参数个数
	fmt.Println(flag.NFlag())
}
```

### 2.2 查看帮助

```go
C:\aaa\gin_demo>  go run main.go --help
  -age int
        年龄 (default 18)
  -d duration
        延迟的时间间隔
  -married
        婚否
  -name string
        姓名 (default "张三")
```

### 2.3 flag参数演示

```go
C:\aaa\gin_demo>  go run main.go -name pprof --age 28 -married=false -d=1h30m
pprof 28 false 1h30m0s
[]
0
4
```

### 2.4 非flag命令行参数

```go
C:\aaa\gin_demo>go run main.go a b c
张三 18 false 0s
[a b c]
3
0
```