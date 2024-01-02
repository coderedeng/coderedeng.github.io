---
title: machinery
index_img: /img/cover2-20.png
date: 2022-06-22 22:52:21
categories: 
- Go常用库
tags:
- Go常用库
---

# 20.machinery

## 01.异步框架machinery

- [github地址(opens new window)](https://github.com/RichardKnop/machinery)

### 1.1 machinery介绍

- go machinery框架类似python中常用celery框架，主要用于 异步任务和定时任务，有一下特性
  - 任务重试机制
  - 延迟任务支持
  - 任务回调机制
  - 任务结果记录
  - 支持Workflow模式：Chain，Group，Chord
  - 多Brokers支持：Redis, AMQP, [AWS SQS(opens new window)](https://link.segmentfault.com/?enc=DHe3inPV2HBq6uxnZ2CEOg%3D%3D.XhC%2BOAXOeJgqueAZ3HrM4nnCWizYNVCgbJcSKS7%2BsPE%3D)
  - 多Backends支持：Redis, Memcache, AMQP, [MongoDB(opens new window)](https://link.segmentfault.com/?enc=s1hIwqlq%2BqzLK6uutFwrfg%3D%3D.LOQSm2d600WNtAuHuxnSX%2B%2B%2F1hm1iNUspqC1IcqZPCrXnAQ23jRJTDMUunMDFawu2mQXughrPBtdSeR7f1l45w%3D%3D)

### 1.2 架构

- 任务队列，简而言之就是一个放大的生产者消费者模型
- 用户请求会生成任务，队列的处理器程序充当消费者不断的消费任务。
- 基于这种框架设计思想，我们来看下machinery的简单设计结构图例
  - Sender：业务推送模块，生成具体任务，可根据业务逻辑中，按交互进行拆分；
  - Broker：存储具体序列化后的任务，machinery中目前支持到Redis, AMQP,和SQS；
  - Worker：工作进程，负责消费者功能，处理具体的任务；
  - Backend：后端存储，用于存储任务执行状态的数据；

![](/img/image-20220206111846252.6cdeba77.png)

## 02.machinery使用

### 2.1 异步和定时任务

```go
package main

import (
	"fmt"
	redisbackend "github.com/RichardKnop/machinery/v2/backends/redis"
	redisbroker "github.com/RichardKnop/machinery/v2/brokers/redis"
	eagerlock "github.com/RichardKnop/machinery/v2/locks/eager"
	"github.com/RichardKnop/machinery/v2"
	"github.com/RichardKnop/machinery/v2/config"
	"github.com/RichardKnop/machinery/v2/tasks"
	"os"
	"time"
)

func main()  {
	if len(os.Args) == 2 && os.Args[1] == "worker" {  // 启动worker
		if err := worker(); err != nil {
			panic(err)
		}
	}
	TestPeriodicTask()  // 触发一个定时任务（定时任务由客户端控制，客户端退出定时就会结束）
	TestAdd()           // 触发一个异步任务
	time.Sleep(time.Second * 1000)
}

/* 触发执行Add异步任务 */
func TestAdd()  {
	server, _ := startServer()	// 调用异步任务 Add 函数，执行 1+4=5这个逻辑
	signature := &tasks.Signature{
		Name: "add",
		Args: []tasks.Arg{
			{
				Type:  "int64",
				Value: 4,
			},
			{
				Type:  "int64",
				Value: 1,
			},
		},
	}
	asyncResult, _ := server.SendTask(signature)	        // 任务可以通过将Signature的实例传递给Server实例来调用
	results,_ := asyncResult.Get(time.Millisecond * 5)  	// 您还可以执行同步阻塞调用来等待任务结果
	for _, result := range results {
		fmt.Println(result.Interface())
	}
}

/* 触发执行periodicTask异步任务 */
func TestPeriodicTask()  {
	server, _ := startServer()
	signature := &tasks.Signature{
		Name: "periodicTask",
		Args: []tasks.Arg{

		},
	}
	// 每分钟执行一次periodicTask函数，验证发现不支持秒级别定时任务
	err := server.RegisterPeriodicTask("*/1 * * * ?", "periodic-task", signature)
	if err != nil {
	    fmt.Println(err)
	}
	asyncResult, _ := server.SendTask(signature)
	fmt.Println(asyncResult)
}

// 第一：配置Server并注册任务
func startServer() (*machinery.Server, error) {
	cnf := &config.Config{
		DefaultQueue:    "machinery_tasks",
		ResultsExpireIn: 3600,
		Redis: &config.RedisConfig{
			MaxIdle:                3,
			IdleTimeout:            240,
			ReadTimeout:            15,
			WriteTimeout:           15,
			ConnectTimeout:         15,
			NormalTasksPollPeriod:  1000,
			DelayedTasksPollPeriod: 500,
		},
	}

	// 创建服务器实例
	broker := redisbroker.NewGR(cnf, []string{"localhost:6379"}, 0)
	backend := redisbackend.NewGR(cnf, []string{"localhost:6379"}, 0)
	lock := eagerlock.New()
	server := machinery.NewServer(cnf, broker, backend, lock)

	// 注册异步任务
	tasksMap := map[string]interface{}{
		"add":               Add,
		"periodicTask":      PeriodicTask,
	}
	return server, server.RegisterTasks(tasksMap)
}

// 第二步：启动Worker
func worker() error {
	//消费者的标记
	consumerTag := "machinery_worker"

	server, err := startServer()
	if err != nil {
		return err
	}

	//第二个参数并发数, 0表示不限制
	worker := server.NewWorker(consumerTag, 0)

	//钩子函数
	errorhandler := func(err error) {}
	pretaskhandler := func(signature *tasks.Signature) {}
	posttaskhandler := func(signature *tasks.Signature) {}

	worker.SetPostTaskHandler(posttaskhandler)
	worker.SetErrorHandler(errorhandler)
	worker.SetPreTaskHandler(pretaskhandler)
	return worker.Launch()
}

// 第三步：添加异步执行函数
func Add(args ...int64) (int64, error) {
	println("############# 执行Add方法 #############")
	sum := int64(0)
	for _, arg := range args {
		sum += arg
	}
	return sum, nil
}

// 第四步：添加一个周期性任务
func PeriodicTask() error {
	fmt.Println("################ 执行周期任务PeriodicTask #################")
	return nil
}
```

### 2.2 启动服务并发送任务

> - go run main.go worker // 启动worker服务
> - go run main.go // 发送任务到worker

![](/img/image-20220206111935400.8a7a4509.png)

## 03.gin+machinery

### 3.0 项目结构

> go run main.go // 直接执行即可测试

```go
xiaonaiqiang1@ZBMac-C02CW08SM work % tree ginWorker 
ginWorker
├── main.go   // 项目入库
└── pkg
    └── task
        ├── server.go     // machinery服务初始化
        ├── start.go      // 启动异步任务入口
        ├── cronJobs.go   // 触发周期性任务
        ├── sendJobs.go   // 触发异任务
        └── workers
            └── tasks.go   // 定义执行任务函数
```

### 3.1 main.go

```go
package main

import (
	"fmt"
	"ginWorker/pkg/task"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main()  {
	go task.Start()  // 启动异步任务worker
	go task.StartCron()  // 启动定时任务

	r := gin.Default()
	r.GET("/add", func(c *gin.Context) {
		task.TaskAdd(4,5)   // 测试执行异步任务
		c.String(http.StatusOK, "hello word")
	})
	fmt.Println("http://127.0.0.1:8000")	//监听端口默认为8080
	r.Run(":8000")
}
```

### 3.2 pkg/task/server.go

```go
package task

import (
	"ginWorker/pkg/task/workers"
	"github.com/RichardKnop/machinery/v2"
	redisbackend "github.com/RichardKnop/machinery/v2/backends/redis"
	redisbroker "github.com/RichardKnop/machinery/v2/brokers/redis"
	"github.com/RichardKnop/machinery/v2/config"
	eagerlock "github.com/RichardKnop/machinery/v2/locks/eager"
	"github.com/RichardKnop/machinery/v2/tasks"
)

var AsyncTaskCenter *machinery.Server

// 第一：配置Server并注册任务
func startServer() (*machinery.Server, error) {
	cnf := &config.Config{
		DefaultQueue:    "machinery_tasks",
		ResultsExpireIn: 3600,
		Redis: &config.RedisConfig{
			MaxIdle:                3,
			IdleTimeout:            240,
			ReadTimeout:            15,
			WriteTimeout:           15,
			ConnectTimeout:         15,
			NormalTasksPollPeriod:  1000,
			DelayedTasksPollPeriod: 500,
		},
	}

	// 创建服务器实例
	broker := redisbroker.NewGR(cnf, []string{"localhost:6379"}, 0)
	backend := redisbackend.NewGR(cnf, []string{"localhost:6379"}, 0)
	lock := eagerlock.New()
	server := machinery.NewServer(cnf, broker, backend, lock)

	tasksMap := initAsyncTaskMap()
	AsyncTaskCenter = server
	return server, server.RegisterTasks(tasksMap)
}

// 第二步：启动Worker
func worker() error {
	consumerTag := "machinery_worker"	//消费者的标记
	server, err := startServer()
	if err != nil {
		return err
	}
	worker := server.NewWorker(consumerTag, 0)	//第二个参数并发数, 0表示不限制

	//钩子函数
	errorhandler := func(err error) {}
	pretaskhandler := func(signature *tasks.Signature) {}
	posttaskhandler := func(signature *tasks.Signature) {}

	worker.SetPostTaskHandler(posttaskhandler)
	worker.SetErrorHandler(errorhandler)
	worker.SetPreTaskHandler(pretaskhandler)
	return worker.Launch()
}

// 第三步：注册函数
func initAsyncTaskMap() map[string]interface{} {
	tasksMap := map[string]interface{}{
		"add":               workers.Add,
		"periodicTask":      workers.PeriodicTask,
	}
	return tasksMap
}
```

### 3.3 pkg/task/start.go

```go
package task

func Start() {
	// 启动worker
	if err := worker(); err != nil {
		panic(err)
	}
}

// 启动周期性任务
func StartCron()  {
	TestPeriodicTask()
}
```

### 3.4 pkg/task/cronJobs.go

```go
package task

import (
	"fmt"
	"github.com/RichardKnop/machinery/v2/tasks"
)

/* 触发执行periodicTask异步任务 */
func TestPeriodicTask()  {
	server, _ := startServer()
	signature := &tasks.Signature{
		Name: "periodicTask",
		Args: []tasks.Arg{

		},
	}
	// 每分钟执行一次periodicTask函数，验证发现不支持秒级别定时任务
	err := server.RegisterPeriodicTask("*/1 * * * ?", "periodic-task", signature)
	if err != nil {
		fmt.Println(err)
	}
	asyncResult, _ := server.SendTask(signature)
	fmt.Println(asyncResult)
}
```

### 3.5 pkg/task/sendJobs.go

```go
package task

import (
	"fmt"
	"github.com/RichardKnop/machinery/v2/tasks"
)

/* 触发执行Add异步任务 */
func TaskAdd(a,b int64)  {
	signature := &tasks.Signature{
		Name: "add",
		Args: []tasks.Arg{
			{
				Type:  "int64",
				Value: a,
			},
			{
				Type:  "int64",
				Value: b,
			},
		},
	}
	_, err := AsyncTaskCenter.SendTask(signature) // 任务可以通过将Signature的实例传递给Server实例来调用
	if err != nil {
		fmt.Println(err)
	}
}
```

### 3.6 pkg/task/workers/tasks.go

```go
package workers

import (
	"fmt"
	"time"
)

// 添加异步执行函数
func Add(args ...int64) (int64, error) {
	println("############# 执行Add方法 #############")
	time.Sleep(10 * time.Second)  // 模拟执行耗时任务
	sum := int64(0)
	for _, arg := range args {
		sum += arg
	}
	println("############# Add方法Done #############")
	return sum, nil
}

// 添加一个周期性任务
func PeriodicTask() error {
	fmt.Println("################ 执行周期任务PeriodicTask #################")
	return nil
}
```

### 3.7 运行结果

- `执行周期任务：每秒执行一次`

![](/img/image-20220206112020324.6a282832.png)

- ```
  通过接口触发异步任务
  ```

  - http://127.0.0.1:8000/add

![](/img/image-20220206112110293.6b3d47fc.png)
