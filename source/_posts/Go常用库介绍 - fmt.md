---
title: fmt
index_img: /img/cover2-1.png
date: 2022-05-20 20:31:14
categories: 
- Go常用库
tags:
- Go常用库
---

# 01.fmt

## 01.常用占位符

| 动词  | 功能                                       |
| ----- | ------------------------------------------ |
| `%v`  | 按值的本来值输出                           |
| %+v   | 在 %v 的基础上，对结构体字段名和值进行展开 |
| `%#v` | 输出 Go 语言语法格式的值                   |
| `%T`  | 输出 Go 语言语法格式的类型和值             |
| %%    | 输出 %% 本体                               |
| %b    | 整型以二进制方式显示                       |
| %o    | 整型以八进制方式显示                       |
| `%d`  | 整型以十进制方式显示                       |
| %x    | 整型以 十六进制显示                        |
| %X    | 整型以十六进制、字母大写方式显示           |
| %U    | Unicode 字符                               |
| %f    | 浮点数                                     |
| %p    | 指针，十六进制方式显示                     |

## 02. Print

- Println：
  - 一次输入多个值的时候 Println 中间有空格
  - Println 会自动换行，Print 不会
- Print：
  - 一次输入多个值的时候 Print 没有 中间有空格
  - Print 不会自动换行
- Printf
  - Printf 是格式化输出，在很多场景下比 Println 更方便

```go
package main
import "fmt"

func main() {
	fmt.Print("zhangsan", "lisi", "wangwu")   // zhangsanlisiwangwu
	fmt.Println("zhangsan", "lisi", "wangwu") // zhangsan lisi wangwu

	name := "zhangsan"
	age := 20
	fmt.Printf("%s 今年 %d 岁\n", name, age)     // zhangsan 今年 20 岁
	fmt.Printf("值：%v --> 类型: %T", name, name) // 值：zhangsan --> 类型: string
}
```

## 03.Sprint

- Sprint系列函数会把传入的数据生成并返回一个字符串。

```go
package main
import "fmt"

func main() {
	s1 := fmt.Sprint("枯藤")
	fmt.Println(s1) // 枯藤
	name := "枯藤"
	age := 18
	s2 := fmt.Sprintf("name:%s,age:%d", name, age) // name:枯藤,age:18
	fmt.Println(s2)
	s3 := fmt.Sprintln("枯藤") // 枯藤 有空格
	fmt.Println(s3)
}
```

## 04. Fprint

- Fprint系列函数会将内容输出到一个io.Writer接口类型的变量w中
- 我们通常用这个函数往文件中写入内容。

```go
package main
import (
	"fmt"
	"os"
)

func main() {
	// 方法1：输出到控制台
	fmt.Fprintln(os.Stdout, "向标准输出写入内容")

	// 方法2：将文件写入到 xx.txt 文件中
	fileObj, err := os.OpenFile("./xx.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		fmt.Println("打开文件出错，err:", err)
		return
	}
	name := "枯藤"
	// 向打开的文件句柄中写入内容
	fmt.Fprintf(fileObj, "往文件中写如信息：%s", name)
}
```