---
title: Log
index_img: /img/cover2-5.png
date: 2022-05-27 22:17:35
categories: 
- Go常用库
tags:
- Go常用库
---

# 05.Log

## 01.日志模块介绍

- [参考博客(opens new window)](https://www.liwenzhou.com/posts/Go/zap/)

### 1.1 介绍

在许多Go语言项目中，我们需要一个好的日志记录器能够提供下面这些功能

- 能够将事件记录到文件中，而不是应用程序控制台。
- 日志切割-能够根据文件大小、时间或间隔等来切割日志文件。
- 支持不同的日志级别。例如INFO，DEBUG，ERROR等。
- 能够打印基本信息，如调用文件/函数名和行号，日志时间等。

### 1.2 默认的Go Logger

- 实现一个Go语言中的日志记录器非常简单——创建一个新的日志文件，然后设置它为日志的输出位置。

```go
package main
import (
	"log"
	"net/http"
	"os"
)

// 第一：设置Logger
func SetupLogger() {
	logFileLocation, _ := os.OpenFile("./test.log", os.O_CREATE|os.O_APPEND|os.O_RDWR, 0744)
	log.SetOutput(logFileLocation)
}

// 第二：使用Logger
func simpleHttpGet(url string) {
	resp, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching url %s : %s", url, err.Error())
	} else {
		log.Printf("Status Code for %s : %s", url, resp.Status)
		resp.Body.Close()
	}
}

func main()  {
	SetupLogger()
	simpleHttpGet("www.baidu.com")
	simpleHttpGet("http://www.baidu.com")
}
```

### 1.3 Go Logger的优势和劣势

- 优势
  - 它最大的优点是使用非常简单。
  - 我们可以设置任何`io.Writer`作为日志记录输出并向其发送要写入的日志。
- 劣势
  - 仅限基本的日志级别
  - 只有一个`Print`选项。不支持`INFO`/`DEBUG`等多个级别。
  - 缺乏日志格式化的能力——例如记录调用者的函数名和行号，格式化日期和时间格式。等等。
  - 不提供日志切割的能力。

