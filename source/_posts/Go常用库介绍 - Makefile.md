---
title: Makefile
index_img: /img/cover2-16.png
date: 2022-06-17 22:21:58
categories: 
- Go常用库
tags:
- Go常用库
---

# 16.Makefile

## 01.介绍

### 1.1 make介绍

- `make`是一个构建自动化工具，会在当前目录下寻找`Makefile`或`makefile`文件
- 如果存在相应的文件，它就会依据其中定义好的规则完成构建任务。

### 1.2 Makefile介绍

- 借助`Makefile`我们在编译过程中不再需要每次手动输入编译的命令和编译的参数，可以极大简化项目编译过程。
- 我们可以把`Makefile`简单理解为它定义了一个项目文件的编译规则。
- 借助`Makefile`我们在编译过程中不再需要每次手动输入编译的命令和编译的参数，可以极大简化项目编译过程。
- 同时使用`Makefile`也可以在项目中确定具体的编译规则和流程，很多开源项目中都会定义`Makefile`文件。

### 1.3 win10安装make

- MinGW下载网页：http://sourceforge.net/projects/mingw/files/latest/download?source=files
- 右击计算机->属性->高级系统设置->环境变量，在系统变量中找到PATH
- 将MinGW安装目录里的bin文件夹的地址添加到PATH里面。
- 打开MinGW的安装目录，打开bin文件夹，将mingw32-make.exe重命名为make.exe。
- 经过以上步骤后，控制台可以输入make。

### 1.4 规则介绍

- `Makefile`由多条规则组成，每条规则主要由两个部分组成，分别是依赖的关系和执行的命令。
- 其结构如下所示：

```makefile
[target] ... : [prerequisites] ...
<tab>[command]
    ...
    ...
```

- 其中：
  - targets：规则的目标
  - prerequisites：可选的要生成 targets 需要的文件或者是目标。
  - command：make 需要执行的命令（任意的 shell 命令）。可以有多条命令，每一条命令占一行。
- 举个例子：

```makefile
build:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o xx
```

## 02.makefile基本使用

### 2.1 main.go

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", hello)
	server := &http.Server{
		Addr: ":8888",
	}
	fmt.Println("server startup...")
	if err := server.ListenAndServe(); err != nil {
		fmt.Printf("server startup failed, err:%v\n", err)
	}
}

func hello(w http.ResponseWriter, _ *http.Request) {
	w.Write([]byte("hello v5blog.cn!"))
}
```

### 2.2 示例

- `BINARY="xxx"`是定义变量
- `.PHONY`用来定义伪目标，不创建目标文件，而是去执行这个目标下面的命令

```makefile
.PHONY: all build run gotool clean help
# 编译后的项目名
BINARY="xxx"
# 如果make后面不加任何参数，默认执行all
all: gotool build

build:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o ${BINARY}

run:
	@go run ./main.go
	#@go run ./main.go conf/config.yaml

gotool:
	go fmt ./
	go vet ./

clean:
	@if [ -f ${BINARY} ] ; then rm ${BINARY} ; fi

help:
	@echo "make - 格式化 Go 代码, 并编译生成二进制文件"
	@echo "make build - 编译 Go 代码, 生成二进制文件"
	@echo "make run - 直接运行 Go 代码"
	@echo "make clean - 移除二进制文件和 vim swap files"
	@echo "make gotool - 运行 Go 工具 'fmt' and 'vet'"
```

### 2.3 使用

![](/img/image-20210615203624174.c01717f8.png)

## 03.完整

```go
.PHONY: all build run gotool clean help

BINARY="bluebell"

all: gotool build

build:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o ./bin/${BINARY}

run:
	@go run ./main.go conf/config.yaml

gotool:
	go fmt ./
	go vet ./

clean:
	@if [ -f ${BINARY} ] ; then rm ${BINARY} ; fi

help:
	@echo "make - 格式化 Go 代码, 并编译生成二进制文件"
	@echo "make build - 编译 Go 代码, 生成二进制文件"
	@echo "make run - 直接运行 Go 代码"
	@echo "make clean - 移除二进制文件和 vim swap files"
	@echo "make gotool - 运行 Go 工具 'fmt' and 'vet'"
```
