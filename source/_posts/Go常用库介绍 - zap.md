---
title: reflect
index_img: /img/cover2-11.png
date: 2022-06-07 20:12:28
categories: 
- Go常用库
tags:
- Go常用库
---

# 11.zap日志包

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

## 02.zap基本使用

### 2.1 zap介绍

- Uber-go zap优势
  - 它同时提供了结构化日志记录和printf风格的日志记录
  - 它非常的快
- 安装

```bash
go get -u go.uber.org/zap
```

1

### 2.2 Sugared Logger和Logger

- Zap提供了两种类型的日志记录器—`Sugared Logger`和`Logger`。
- 在性能很好但不是很关键的上下文中，使用`SugaredLogger`。
- 它比其他结构化日志记录包快4-10倍，并且支持结构化和printf风格的日志记录。
- 在每一微秒和每一次内存分配都很重要的上下文中，使用`Logger`。
- 它甚至比`SugaredLogger`更快，内存分配次数也更少，但它只支持强类型的结构化日志记录。

### 2.3 zap日志记录器Logger

- 通过调用`zap.NewProduction()`/`zap.NewDevelopment()`或者`zap.Example()`创建一个Logger。
- 唯一的区别在于它将记录的信息不同
  - 例如production logger默认记录调用函数信息、日期和时间等。
- 通过Logger调用Info/Error等。
- 默认情况下日志都会打印到应用程序的console界面。

```go
package main
import (
	"go.uber.org/zap"
	"net/http"
)

// 第一步：创建一个Logger
var logger *zap.Logger

func InitLogger() {
	logger, _ = zap.NewProduction()
}

// 第二步：通过Logger调用Info/Error等输出日志
func simpleHttpGet(url string) {
	resp, err := http.Get(url)
	if err != nil {
		logger.Error(
			"Error fetching url..",
			zap.String("url", url),
			zap.Error(err))
	} else {
		logger.Info("Success..",
			zap.String("statusCode", resp.Status),
			zap.String("url", url))
		resp.Body.Close()
	}
}

func main() {
	InitLogger()
	defer logger.Sync()
	simpleHttpGet("www.google.com")
	simpleHttpGet("http://www.google.com")
}
/*
在控制台会输出一下日志信息：
{"level":"error","ts":1623143450.9749353,"caller":"gin_demo/main.go:23","msg":"Error fetching url..","url":"www.google.com","error":"Get \"www.google.com\": unsupported protocol scheme \"\"","stacktrace":"main.simpleHttpGet\n\tC:/aaa/gin_demo/main.go:23\nmain.main\n\tC:/aaa/gin_demo/main.go:12\nruntime.main\n\tC:/Go/src/runtime/proc.go:225"}
{"level":"error","ts":1623143472.030105,"caller":"gin_demo/main.go:23","msg":"Error fetching url..","url":"http://www.google.com","error":"Get \"http://www.google.com\": dial tcp 69.171.247.32:80: connectex: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond.","stacktrace":"main.simpleHttpGet\n\tC:/aaa/gin_demo/main.go:23\nmain.main\n\tC:/aaa/gin_demo/main.go:13\nruntime.main\n\tC:/Go/src/runtime/proc.go:225"}
*/
```

### 2.4 zap日志记录器Sugared Logger

现在让我们使用Sugared Logger来实现相同的功能。

- 大部分的实现基本都相同。
- 惟一的区别是，我们通过调用主logger的`. Sugar()`方法来获取一个`SugaredLogger`。
- 然后使用`SugaredLogger`以`printf`格式记录语句

```go
package main
import (
	"go.uber.org/zap"
	"net/http"
)

// 第一步：创建一个Sugared Logger
var sugarLogger *zap.SugaredLogger

func InitLogger() {
	logger, _ := zap.NewProduction()
	sugarLogger = logger.Sugar()
}

// 第二步：通过Logger调用Info/Error等输出日志
func simpleHttpGet(url string) {
	sugarLogger.Debugf("Trying to hit GET request for %s", url)
	resp, err := http.Get(url)
	if err != nil {
		sugarLogger.Errorf("Error fetching URL %s : Error = %s", url, err)
	} else {
		sugarLogger.Infof("Success! statusCode = %s for URL %s", resp.Status, url)
		resp.Body.Close()
	}
}

func main() {
	InitLogger()
	defer sugarLogger.Sync()
	simpleHttpGet("www.google.com")
	simpleHttpGet("http://www.google.com")
}
/*
在控制台会输出一下日志信息：
{"level":"error","ts":1623143450.9749353,......
{"level":"error","ts":1623143450.9749353,......
*/
```

## 03.定制logger

### 3.1 测试定制logger

```go
package main
import (
	"github.com/natefinch/lumberjack"   // Lumberjack进行日志切割归档
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"net/http"
)

// 第一步：创建一个Sugared Logger
var sugarLogger *zap.SugaredLogger

// 第二步：将编码器从JSON Encoder更改为普通Encoder
func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	// 为此，我们需要将NewJSONEncoder()更改为NewConsoleEncoder()
	return zapcore.NewConsoleEncoder(encoderConfig)
}

// 第三步：使用Lumberjack进行日志切割归档
func getLogWriter() zapcore.WriteSyncer {
	lumberJackLogger := &lumberjack.Logger{
		Filename:   "./test.log",  // 指定日志将写到哪里去
		MaxSize:    1,             // 每次满1M进行切割
		MaxBackups: 5,             // 最多报错5个文件
		MaxAge:     30,            // 文件最多保存30天
		Compress:   false,         // 是否压缩/归档旧文件
	}
	return zapcore.AddSync(lumberJackLogger)
}

// 第四步：重写InitLogger()方法
func InitLogger() {
	writeSyncer := getLogWriter()
	encoder := getEncoder()
	// 	zapcore.Core需要三个配置——Encoder，WriteSyncer，LogLevel
	core := zapcore.NewCore(encoder, writeSyncer, zapcore.DebugLevel)
	/*
		Encoder:编码器(如何写入日志),我们将使用开箱即用的NewJSONEncoder()，并使用预先设置的
		WriterSyncer ：指定日志将写到哪里去。我们使用zapcore.AddSync()函数并且将打开的文件句柄传进去
		Log Level：哪种级别的日志将被写入。
	*/
	// 我们将使用zap.New(…)方法来手动传递所有配置，而不是使用像zap.NewProduction()这样的预置方法来创建logger。
	logger := zap.New(core, zap.AddCaller())
	sugarLogger = logger.Sugar()  // 实例化全局变量sugarLogger
}

// 第五步：函数调用全局sugarLogger写入log日志
func simpleHttpGet(url string) {
	sugarLogger.Debugf("Trying to hit GET request for %s", url)
	resp, err := http.Get(url)
	if err != nil {
		sugarLogger.Errorf("Error fetching URL %s : Error = %s", url, err)
	} else {
		sugarLogger.Infof("Success! statusCode = %s for URL %s", resp.Status, url)
		resp.Body.Close()
	}
}

func main() {
	InitLogger()
	defer sugarLogger.Sync()
	simpleHttpGet("www.sogo.com")
	simpleHttpGet("http://www.sogo.com")
}
```



