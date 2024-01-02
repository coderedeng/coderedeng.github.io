---
title: net/http
index_img: /img/cover2-8.png
date: 2022-06-01 21:35:53
categories: 
- Go常用库
tags:
- Go常用库
---

# 08.net/http

## 01.net/http（GET）

- Go语言内置的net/http包十分的优秀，提供了HTTP客户端和服务端的实现。

### 1.1 无参GET

- 使用net/http包编写一个简单的发送HTTP请求的Client端

```go
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	resp, err := http.Get("https://www.baidu.com/")
	if err != nil {
		fmt.Println("get failed, err:", err)
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("read from resp.Body failed,err:", err)
		return
	}
	fmt.Print(string(body))
}
```

### 1.2 带参GET

- 关于GET请求的参数需要使用Go语言内置的net/url这个标准库来处理。

关于GET请求的参数需要使用Go语言内置的net/url这个标准库来处理。

```go
func main() {
    apiUrl := "http://127.0.0.1:9090/get"
    // URL param
    data := url.Values{}
    data.Set("name", "枯藤")
    data.Set("age", "18")
    u, err := url.ParseRequestURI(apiUrl)
    if err != nil {
        fmt.Printf("parse url requestUrl failed,err:%v\n", err)
    }
    u.RawQuery = data.Encode() // URL encode
    fmt.Println(u.String())
    resp, err := http.Get(u.String())
    if err != nil {
        fmt.Println("post failed, err:%v\n", err)
        return
    }
    defer resp.Body.Close()
    b, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("get resp failed,err:%v\n", err)
        return
    }
    fmt.Println(string(b))
}
```

- 对应的Server端HandlerFunc如下：

```go
func getHandler(w http.ResponseWriter, r *http.Request) {
    defer r.Body.Close()
    data := r.URL.Query()
    fmt.Println(data.Get("name"))
    fmt.Println(data.Get("age"))
    answer := `{"status": "ok"}`
    w.Write([]byte(answer))
}
```

### 1.3 自定义Client

- 要管理HTTP客户端的头域、重定向策略和其他设置，创建一个Client：

```go
client := &http.Client{
    CheckRedirect: redirectPolicyFunc,
}
resp, err := client.Get("http://5lmh.com")
// ...
req, err := http.NewRequest("GET", "http://5lmh.com", nil)
// ...
req.Header.Add("If-None-Match", `W/"wyzzy"`)
resp, err := client.Do(req)
// ...
```

### 1.4 自定义Transport

- 要管理代理、TLS配置、keep-alive、压缩和其他设置，创建一个Transport

```go
tr := &http.Transport{
    TLSClientConfig:    &tls.Config{RootCAs: pool},
    DisableCompression: true,
}
client := &http.Client{Transport: tr}
resp, err := client.Get("https://5lmh.com")
```

- Client和Transport类型都可以安全的被多个go程同时使用，出于效率考虑，应该一次建立、尽量重用。

## 02.net/http（POST）

### 2.1 Post请求示例

- 上面演示了使用net/http包发送GET请求的示例，发送POST请求的示例代码如下：

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"
)

// net/http post demo

func main() {
    url := "http://127.0.0.1:9090/post"
    // 表单数据
    //contentType := "application/x-www-form-urlencoded"
    //data := "name=枯藤&age=18"
    // json
    contentType := "application/json"
    data := `{"name":"枯藤","age":18}`
    resp, err := http.Post(url, contentType, strings.NewReader(data))
    if err != nil {
        fmt.Println("post failed, err:%v\n", err)
        return
    }
    defer resp.Body.Close()
    b, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("get resp failed,err:%v\n", err)
        return
    }
    fmt.Println(string(b))
}
```

### 2.2 Server端

- 对应的Server端HandlerFunc如下：

```go
func postHandler(w http.ResponseWriter, r *http.Request) {
    defer r.Body.Close()
    // 1. 请求类型是application/x-www-form-urlencoded时解析form数据
    r.ParseForm()
    fmt.Println(r.PostForm) // 打印form数据
    fmt.Println(r.PostForm.Get("name"), r.PostForm.Get("age"))
    // 2. 请求类型是application/json时从r.Body读取数据
    b, err := ioutil.ReadAll(r.Body)
    if err != nil {
        fmt.Println("read request.Body failed, err:%v\n", err)
        return
    }
    fmt.Println(string(b))
    answer := `{"status": "ok"}`
    w.Write([]byte(answer))
}
```

## 03.服务端

### 3.1 默认的Server

- ListenAndServe使用指定的监听地址和处理器启动一个HTTP服务端。
- 处理器参数通常是nil，这表示采用包变量DefaultServeMux作为处理器。
- Handle和HandleFunc函数可以向DefaultServeMux添加处理器。

```go
http.Handle("/foo", fooHandler)
http.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
})
log.Fatal(http.ListenAndServe(":8080", nil))
```

- 示例

```go
package main
import (
	"fmt"
	"net/http"
)

func sayHello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello World！")
}

func main() {
	http.HandleFunc("/", sayHello)
	err := http.ListenAndServe(":9090", nil)
	if err != nil {
		fmt.Printf("http server failed, err:%v\n", err)
		return
	}
}
```

### 3.2 自定义Server

- 要管理服务端的行为，可以创建一个自定义的Server：

```go
s := &http.Server{
    Addr:           ":8080",
    Handler:         myHandler,
    ReadTimeout:      10 * time.Second,
    WriteTimeout:      10 * time.Second,
    MaxHeaderBytes:    1 << 20,
}
log.Fatal(s.ListenAndServe())
```
