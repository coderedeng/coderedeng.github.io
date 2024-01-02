---
title: logrus
index_img: /img/cover2-18.png
date: 2022-06-20 21:54:53
categories: 
- Go常用库
tags:
- Go常用库
---

# 18.logrus

## 01.logrus基础

- [参考GitHub(opens new window)](https://github.com/sirupsen/logrus)
- [参考博客1(opens new window)](https://blog.51cto.com/u_15183360/2737283)
- [参考博客2(opens new window)](https://www.liwenzhou.com/posts/Go/go_logrus/)
- 安装

```bash
go get github.com/sirupsen/logrus
```

### 1.1 简介

> Logrus是Go（golang）的结构化logger，与标准库logger完全API兼容，它有以下特点

- 完全兼容标准日志库，拥有七种日志级别：`Trace`, `Debug`, `Info`, `Warning`, `Error`, `Fatal`and `Panic`。
- 可扩展的Hook机制，允许使用者通过Hook的方式将日志分发到任意地方
  - 如本地文件系统，logstash，elasticsearch或者mq等，或者通过Hook定义日志内容和格式等
- 可选的日志输出格式，内置了两种日志格式JSONFormater和TextFormatter，还可以自定义日志格式
- Field机制，通过Filed机制进行结构化的日志记录
- 线程安全

### 1.2 简单导报使用

```go
package main
import (
	log "github.com/sirupsen/logrus"
)

func main() {
	log.WithFields(log.Fields{
		"animal": "dog",
	}).Info("测试info日志")
}
// INFO[0000] 测试info日志      animal=dog
```

### 1.3 日志级别

```go
package main

import (
	"github.com/sirupsen/logrus"
)

// 创建一个新的logger实例。可以创建任意多个。
var log = logrus.New()

func main() {
	log.Trace("Something very low level.")
	log.Debug("Useful debugging information.")
	log.Info("Something noteworthy happened!")
	log.Warn("You should probably take a look at this.")
	log.Error("Something failed but I'm not quitting.")
	// 记完日志后会调用os.Exit(1)
	log.Fatal("Bye.")
	// 记完日志后会调用 panic()
	log.Panic("I'm bailing.")
}
/*
INFO[0000] Something noteworthy happened!
WARN[0000] You should probably take a look at this.
ERRO[0000] Something failed but I'm not quitting.
FATA[0000] Bye.
*/
```

### 1.4 设置日志级别

```go
// 会记录info及以上级别 (warn, error, fatal, panic)
log.SetLevel(log.InfoLevel)
```

### 1.5 字段

- Logrus鼓励通过日志字段进行谨慎的结构化日志记录，而不是冗长的、不可解析的错误消息。
- 例如，区别于使用`log.Fatalf("Failed to send event %s to topic %s with key %d")`
- 你应该使用如下方式记录更容易发现的内容

```go
package main

import (
	log "github.com/sirupsen/logrus"
)

func main() {
	log.WithFields(log.Fields{
		"event": "event",
		"topic": "topic",
		"key": "key",
	}).Fatal("Failed to send event")
}
// FATA[0000] Failed to send event   event=event key=key topic=topic
```

### 1.6 默认字段

- 通常，将一些字段始终附加到应用程序的全部或部分的日志语句中会很有帮助。
- 例如，你可能希望始终在请求的上下文中记录`request_id`和`user_ip`。
- 区别于在每一行日志中写上`log.WithFields(log.Fields{"request_id": request_id, "user_ip": user_ip})`
- 你可以向下面的示例代码一样创建一个`logrus.Entry`去传递这些字段。

```go
package main

import log "github.com/sirupsen/logrus"

func main() {
	requestLogger := log.WithFields(log.Fields{"request_id": "request_id", "user_ip": "user_ip"})
	requestLogger.Info("something happened on that request") // will log request_id and user_ip
	requestLogger.Warn("something not great happened")
}
/*
INFO[0000] something happened on that request            request_id=request_id user_ip=user_ip
WARN[0000] something not great happened                  request_id=request_id user_ip=user_ip
 */
```

### 1.7 Hooks

- 你可以添加日志级别的钩子（Hook）。
- 例如，向异常跟踪服务发送`Error`、`Fatal`和`Panic`、信息到StatsD或同时将日志发送到多个位置，例如syslog。
- Logrus配有内置钩子，在`init`中添加这些内置钩子或你自定义的钩子
- [GitHub参考(opens new window)](https://github.com/sirupsen/logrus/blob/master/hooks/syslog/README.md)

```go
package main
import (
	log "github.com/sirupsen/logrus"
	"gopkg.in/gemnasium/logrus-airbrake-hook.v2" // the package is named "airbrake"
	logrus_syslog "github.com/sirupsen/logrus/hooks/syslog"
	"log/syslog"
)

func init() {

	// Use the Airbrake hook to report errors that have Error severity or above to
	// an exception tracker. You can create custom hooks, see the Hooks section.
	log.AddHook(airbrake.NewHook(123, "xyz", "production"))

	hook, err := logrus_syslog.NewSyslogHook("udp", "localhost:514", syslog.LOG_INFO, "")
	if err != nil {
		log.Error("Unable to connect to local syslog daemon")
	} else {
		log.AddHook(hook)
	}
}
```

### 1.8 格式化

```go
package main
import (
	"github.com/sirupsen/logrus"
)

var log = logrus.New()
func main() {
	log.Formatter = &logrus.JSONFormatter{}
  //log.SetReportCaller(true)  // 可以开启记录函数名，但是会消耗性能
	log.WithFields(logrus.Fields{
		"event": "event",
		"topic": "topic",
		"key": "key",
	}).Info("Failed to send event")
}

/*
{
    "event":"event",
    "key":"key",
    "level":"info",
    "msg":"Failed to send event",
    "time":"2021-12-23T12:21:55+08:00",
    "topic":"topic"
}
 */
```

### 1.9 gin中使用logrus

```go
package main

import (
	"fmt"
	"github.com/sirupsen/logrus"
	"os"
	"github.com/gin-gonic/gin"
)

var log = logrus.New()

func init() {
	// Log as JSON instead of the default ASCII formatter.
	log.Formatter = &logrus.JSONFormatter{}
	// Output to stdout instead of the default stderr
	// Can be any io.Writer, see below for File example
	f, _ := os.Create("./gin.log")
	log.Out = f
	gin.SetMode(gin.ReleaseMode)

	gin.DefaultWriter = log.Out
	// Only log the warning severity or above.
	log.Level = logrus.InfoLevel
}

func main() {
	// 创建一个默认的路由引擎
	r := gin.Default()
	// GET：请求方式；/hello：请求的路径
	// 当客户端以GET方法请求/hello路径时，会执行后面的匿名函数
	r.GET("/hello", func(c *gin.Context) {
		log.WithFields(logrus.Fields{
			"animal": "walrus",
			"size":   10,
		}).Warn("A group of walrus emerges from the ocean")
		// c.JSON：返回JSON格式的数据
		c.JSON(200, gin.H{
			"message": "Hello world!",
		})
	})
	// 启动HTTP服务，默认在0.0.0.0:8080启动服务
	fmt.Println(`http://127.0.0.1:8080/hello`)
	r.Run(":8080")
}
```

- 记录日志

```text
{"animal":"walrus","level":"warning","msg":"A group of walrus emerges from the ocean","size":10,"time":"2021-12-23T12:37:21+08:00"}
[GIN] 2021/12/23 - 12:37:21 | 200 |     705.823µs |       127.0.0.1 | GET      "/hello"
```

## 02.在gin中封装使用

### 2.0 目录结构

```go
logrus-demo
├── main.go
└── middleware
    └── logger.go
```

### 2.1 main.go

```go
package main

import (
	"cobra-demo/middleware"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func helloWorld(c *gin.Context) {
	// 测试写入日志
	middleware.Logger.WithFields(logrus.Fields{
		"data"  : "访问/hello",
	}).Info("测试写入info")

	// c.JSON：返回JSON格式的数据
	c.JSON(200, gin.H{
		"message": "Hello world!",
	})
}

func main() {
	r := gin.Default()
	r.Use(middleware.LoggerMiddleware())
	r.GET("/hello", helloWorld)
	// 启动HTTP服务，默认在0.0.0.0:8080启动服务
	fmt.Println(`http://127.0.0.1:8080/hello`)
	r.Run(":8080")
}
```

### 2.2 middleware/logger.ge

```go
package middleware

import (
	"fmt"
	"github.com/gin-gonic/gin"
	rotatelogs "github.com/lestrrat-go/file-rotatelogs"
	"github.com/rifflock/lfshook"
	"github.com/sirupsen/logrus"
	"os"
	"path"
	"time"
)

var (
	logFilePath = "./"
	logFileName = "system.log"
)

func LoggerMiddleware() gin.HandlerFunc {
	// 日志文件
	fileName := path.Join(logFilePath, logFileName)
	// 写入文件
	src, err := os.OpenFile(fileName, os.O_APPEND|os.O_WRONLY, os.ModeAppend)
	if err != nil {
		fmt.Println("err", err)
	}
	// 实例化
	logger := logrus.New()
	//设置日志级别
	logger.SetLevel(logrus.DebugLevel)
	//设置输出
	logger.Out = src

	// 设置 rotatelogs
	logWriter, err := rotatelogs.New(
		// 分割后的文件名称
		fileName+".%Y%m%d.log",

		// 生成软链，指向最新日志文件
		rotatelogs.WithLinkName(fileName),

		// 设置最大保存时间(7天)
		rotatelogs.WithMaxAge(7*24*time.Hour),

		// 设置日志切割时间间隔(1天)
		rotatelogs.WithRotationTime(24*time.Hour),
	)

	writeMap := lfshook.WriterMap{
		logrus.InfoLevel:  logWriter,
		logrus.FatalLevel: logWriter,
		logrus.DebugLevel: logWriter,
		logrus.WarnLevel:  logWriter,
		logrus.ErrorLevel: logWriter,
		logrus.PanicLevel: logWriter,
	}

	logger.AddHook(lfshook.NewHook(writeMap, &logrus.JSONFormatter{
		TimestampFormat: "2006-01-02 15:04:05",
	}))

	return func(c *gin.Context) {
		//开始时间
		startTime := time.Now()
		//处理请求
		c.Next()
		//结束时间
		endTime := time.Now()
		// 执行时间
		latencyTime := endTime.Sub(startTime)
		//请求方式
		reqMethod := c.Request.Method
		//请求路由
		reqUrl := c.Request.RequestURI
		//状态码
		statusCode := c.Writer.Status()
		//请求ip
		clientIP := c.ClientIP()

		// 日志格式
		logger.WithFields(logrus.Fields{
			"status_code":  statusCode,
			"latency_time": latencyTime,
			"client_ip":    clientIP,
			"req_method":   reqMethod,
			"req_uri":      reqUrl,
		}).Info()

	}
}
```

### 2.3 logging/logger.go

```go
package logging

import (
	setting "bamboo.com/pipeline/Go-assault-squad/config"
	"fmt"
	"github.com/sirupsen/logrus"
	"os"
)

var WebLog *logrus.Logger

func Init() {
	initWebLog()
}

func initWebLog() {
	WebLog = initLog(setting.Conf.LogConfig.WebLogName)
}

// 初始化日志句柄
func initLog(logFileName string) *logrus.Logger{
	log := logrus.New()
	log.Formatter = &logrus.JSONFormatter{
		TimestampFormat: "2006-01-02 15:04:05",
	}
	logFilePath := setting.Conf.LogFilePath
	logName := logFilePath + logFileName
	var f *os.File
	var err error
	//判断日志文件夹是否存在，不存在则创建
	if _, err := os.Stat(logFilePath); os.IsNotExist(err) {
		os.MkdirAll(logFilePath, os.ModePerm)
	}
	//判断日志文件是否存在，不存在则创建，否则就直接打开
	if _, err := os.Stat(logName); os.IsNotExist(err) {
		f, err = os.Create(logName)
	} else {
		f, err = os.OpenFile(logName,os.O_APPEND|os.O_WRONLY, os.ModeAppend)
	}

	if err != nil {
		fmt.Println("open log file failed")
	}

	log.Out = f
	log.Level = logrus.InfoLevel
	return log
}

/*
---- 日志写入测试 ----
WebLog.WithFields(logrus.Fields{
	"data"  : "访问/hello",
}).Info("测试写入info")
---- 写入结构如下 ----
{"data":"访问/hello","level":"info","msg":"测试写入info","time":"2021-12-29 18:15:54"}
 */
```

### 2.4 访问测试

> go run main.go

- http://127.0.0.1:8080/hello
- 写入日志格式

```json
{"data":"访问/hello","level":"info","msg":"测试写入info","time":"2021-12-23 15:27:37"}
{"client_ip":"127.0.0.1","latency_time":418116,"level":"info","msg":"","req_method":"GET","req_uri":"/hello","status_code":200,"time":"2021-12-23 15:27:37"}
```
