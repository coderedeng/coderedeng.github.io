---
title: gRPC
index_img: /img/cover2-13.png
date: 2022-06-11 22:11:19
categories: 
- Go常用库
tags:
- Go常用库
---

# 13.gRPC

## 01.gRPC基础

### 1.1 RPC是什么

- 在分布式计算，远程过程调用（英语：Remote Procedure Call，缩写为 RPC）是一个计算机通信协议。
- 该协议允许运行于一台计算机的程序调用另一个地址空间（通常为一个开放网络的一台计算机）的子程序
- 而程序员就像调用本地程序一样，无需额外地为这个交互作用编程（无需关注细节）。
- RPC是一种服务器-客户端（Client/Server）模式，经典实现是一个通过`发送请求-接受回应`进行信息交互的系统。

### 1.2 gRPC是什么

- `gRPC`是一种现代化开源的高性能RPC框架，能够运行于任意环境之中。
- 最初由谷歌进行开发，它使用HTTP/2作为传输协议。
- 在gRPC里，客户端可以像调用本地方法一样直接调用其他机器上的服务端应用程序的方法，帮助你更容易创建分布式应用程序和服务。
- 与许多RPC系统一样，gRPC是基于定义一个服务，指定一个可以远程调用的带有参数和返回类型的的方法。
- 在服务端程序中实现这个接口并且运行gRPC服务处理客户端调用。
- 在客户端，有一个stub提供和服务端相同的方

### 1.3 为什么要用gRPC

- 使用gRPC， 我们可以一次性的在一个`.proto`文件中定义服务并使用任何支持它的语言去实现客户端和服务端
- 反过来，它们可以应用在各种场景中，从Google的服务器到你自己的平板电脑—— gRPC帮你解决了不同语言及环境间通信的复杂性。
- 使用`protocol buffers`还能获得其他好处，包括高效的序列号，简单的IDL以及容易进行接口更新。
- 总之一句话，使用gRPC能让我们更容易编写跨语言的分布式代码。

## 02.安装gRPC

### 2.1 安装gRPC

```bash
go get -u google.golang.org/grpc
```

### 2.2 安装Protocol Buffers v3

- 安装用于生成gRPC服务代码的协议编译器，最简单的方法是从下面的链接
- https://github.com/google/protobuf/releases
- 下载适合你平台的预编译好的二进制文件（`protoc-<version>-<platform>.zip`）。
- 下载完之后，执行下面的步骤：
  - 1、解压下载好的文件
  - 2、把`protoc`二进制文件的路径加到环境变量中
- 接下来执行下面的命令安装protoc的Go插件

```bash
go get -u github.com/golang/protobuf/protoc-gen-go
```

- 编译插件`protoc-gen-go`将会安装到`$GOBIN`，默认是`$GOPATH/bin`，它必须在你的`$PATH`中以便协议编译器`protoc`能够找到它。





