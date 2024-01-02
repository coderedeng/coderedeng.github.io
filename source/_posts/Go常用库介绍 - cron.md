---
title: cron
index_img: /img/cover2-19.png
date: 2022-06-21 21:24:57
categories: 
- Go常用库
tags:
- Go常用库
---

# 19.cron定时

## 01.cron基本使用

### 1.1 使用举例

```go
package main

import (
	"fmt"
	"github.com/robfig/cron"
)

//主函数
func main() {
	cron2 := cron.New() //创建一个cron实例

	//执行定时任务（每5秒执行一次）
	err:= cron2.AddFunc("*/5 * * * * *", print5)
	if err!=nil{
	   fmt.Println(err)
	}

	//启动/关闭
	cron2.Start()
	defer cron2.Stop()
	select {
	  //查询语句，保持程序运行，在这里等同于for{}
	}
}

//执行函数
func print5()  {
     fmt.Println("每5s执行一次cron")
}
```

### 1.2 配置

```go
┌─────────────second 范围 (0 - 60)
│ ┌───────────── min (0 - 59)
│ │ ┌────────────── hour (0 - 23)
│ │ │ ┌─────────────── day of month (1 - 31)
│ │ │ │ ┌──────────────── month (1 - 12)
│ │ │ │ │ ┌───────────────── day of week (0 - 6)
│ │ │ │ │ │
│ │ │ │ │ │
*  *  *  *  *  *  
```

### 1.3 多个crontab任务

```go
package main

import (
	"fmt"

	"github.com/robfig/cron"
)

type TestJob struct {
}

func (this TestJob) Run() {
	fmt.Println("testJob1...")
}

type Test2Job struct {
}

func (this Test2Job) Run() {
	fmt.Println("testJob2...")
}

//启动多个任务
func main() {
	c := cron.New()
	spec := "*/5 * * * * ?"
	//AddJob方法
	c.AddJob(spec, TestJob{})
	c.AddJob(spec, Test2Job{})
	//启动计划任务
	c.Start()
	//关闭着计划任务, 但是不能关闭已经在执行中的任务.
	defer c.Stop()

	select {}
}

/*
testJob1...
testJob2...
testJob1...
testJob2...
*/
```

## 02.gin框架cron应用

- 目录结构

```go
.
├── main.go
└── pkg
    └── jobs
        ├── job_cron.go    // 分布式任务配置
        └── test_task.go   // 具体任务实例
```

### 2.1 main.go

```go
package main

import (
	"go_cron_demo/pkg/jobs"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	jobs.InitJobs()
	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "hello World!")
	})
	r.Run(":8000")
}
```

### 2.2 pkg/jobs/job_cron.go

```go
package jobs

import (
	"github.com/robfig/cron"
)

var mainCron *cron.Cron

func init() {
	mainCron = cron.New()
	mainCron.Start()
}

func InitJobs() {
	// 每5s钟调度一次，并传参
	mainCron.AddJob(
		"*/5 * * * * ?",
		TestJob{Id: 1, Name: "zhangsan"},
	)
}

/*  运行结果
1 zhangsan
testJob1...
1 zhangsan
testJob1...
*/
```

### 2.3 pkg/jobs/test_task.go

```go
package jobs

import "fmt"

type TestJob struct {
	Id   int
	Name string
}

func (this TestJob) Run() {
	fmt.Println(this.Id, this.Name)
	fmt.Println("testJob1...")
}
```
