---
title: Cobor
index_img: /img/cover2-17.png
date: 2022-06-19 22:26:53
categories: 
- Go常用库
tags:
- Go常用库
---

# 17.cobor

## 01.cobra使用

- GitHub地址： https://github.com/spf13/cobra/blob/master/user_guide.md
- 参考博客：https://www.qikqiak.com/post/create-cli-app-with-cobra/
- 安装

```bash
go get -u github.com/spf13/cobra 
```

### 1.1 基本使用

- 初始项目

```bash
$  mkdir cobra-demo && cd cobra-demo
$  go mod init cobra-demo
```

- 2）下载cobra

```bash
# 强烈推荐配置该环境变量
$  export GOPROXY=https://goproxy.cn
$  go get -u github.com/spf13/cobra/cobra
```

- 3）`cobra init` 命令来初始化 CLI 应用的脚手架

```bash
$ cobra init
```

### 1.2 初始化结构说明

- 目录结构

```text
├── cmd
│   └── root.go
└── main.go
```

- main.go

```go
package main

import "cobra-demo/cmd"

func main() {
	cmd.Execute()
}
```

- cmd/root.go

```go
package cmd

import (
	"os"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "cobra-demo",
	Short: "A brief description of your application",
	Long: 
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello Cobra CLI")
  },
}

// 然后再执行 execute 方法
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

// 每当执行或者调用命令的时候，它都会先执行 init 函数中的所有函数
func init() {
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
```

- `rootCmd` 根命令就会首先运行 `initConfig` 函数，当所有的初始化函数执行完成后，才会执行 `rootCmd` 的 `RUN: func` 执行函数
- 我们可以在 `initConfig` 函数里面添加一些 Debug 信息

```go
func initConfig() {
    fmt.Println("I'm inside initConfig function in cmd/root.go")
}
```

## 02.cobra项目使用

### 2.0 目录结构

- 目录结构

```bash
cobra-demo
├── cmd
│   ├── root.go
│   └── serve.go
└── main.go
```

### 2.1 main.go

```go
package main

import "cobra-demo/cmd"

func main() {
	cmd.Execute()
}
```

### 2.2 cmd/root.go

```go
package cmd

import (
	"errors"
	"github.com/spf13/cobra"
	"log"
	"os"
)

var rootCmd = &cobra.Command{
	Use:               "demo",  // 命令行时关键字
	Short:             "cobra demo example",  // 命令简单描述
	Long:              `cobra demo example ....`,  // 命令详细描述
	Args: func(cmd *cobra.Command, args []string) error {
		if len(args) < 1 {
			return errors.New("requires at least one arg")
		}
		return nil
	},
	PersistentPreRunE:      func(*cobra.Command, []string) error { return nil },
	Run: func(cmd *cobra.Command, args []string) {   // 钩子函数
		usageStr := `可以使用 -h 查看命令`
		log.Printf("%s\n", usageStr)
	},
}

// 第二步：然后再执行 execute 方法
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

// 第一步：每当执行或者调用命令的时候，它都会先执行 init 函数中的所有函数
func init() {
	rootCmd.AddCommand(StartCmd)
}
```

### 2.3 cmd/serve.go

```go
package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"log"
)

var (
	config   string  // 启动配置文件位置
	port     string  // 启动端口号
	mode     string  // 启动模式
	StartCmd = &cobra.Command{
		// go run main.go server -c=config/settings.dev.yml
		Use:     "server",  // 启动时要添加 server关键字
		Short:   "Start API server",  // 对命令简单描述
		Example: "ferry server config/settings.yml",  // 运行命令例子
		PreRun: func(cmd *cobra.Command, args []string) {  // 钩子函数，在RunE前执行
			usage()
			setup()
		},
		RunE: func(cmd *cobra.Command, args []string) error {  // 钩子函数
			return run()
		},
	}
)

func init() {
	// 为 Command 添加选项(flags)
	StartCmd.PersistentFlags().StringVarP(&config, "config", "c", "config/settings.yml", "Start server with provided configuration file")
	StartCmd.PersistentFlags().StringVarP(&port, "port", "p", "8002", "Tcp port server listening on")
	StartCmd.PersistentFlags().StringVarP(&mode, "mode", "m", "dev", "server mode ; eg:dev,test,prod")
}

// 记录日志
func usage() {
	usageStr := `starting api server`
	log.Printf("%s\n", usageStr)
}

// 初始化项目
func setup() {
	// 1. 读取配置
	fmt.Println("启动命令配置文件：",config)
	// 2. 初始化数据库链接
	// 3. 启动异步任务队列
}

func run() error {
	// 1.获取当前启动模式
	fmt.Println("启动命令当前模式：", mode)
	// 2.获取当前启动端口
	fmt.Println("启动命令当前端口", port)
	return nil
}
```

### 2.4 运行测试

- 我们可以根据当前命令行传入的 `配置文件位置、端口号、启动模式` 来启动项目

```bash
xiaonaiqiang1@ZBMac-C02CW08SM cobra-demo %  go run main.go server -c=config/settings.dev.yml -p=8888 -m=release
2021/12/23 11:09:12 starting api server
启动命令配置文件： config/settings.dev.yml
启动命令当前模式： release
启动命令当前端口 8888
```
