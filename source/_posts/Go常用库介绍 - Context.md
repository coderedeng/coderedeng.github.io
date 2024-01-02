---
title: Context
index_img: /img/cover2-9.png
date: 2022-06-03 22:42:57
categories: 
categories: 
- Go常用库
tags:
- Go常用库
---

# 09.Context

## 01.context介绍

### 1.1 context由来

- context在Go1.7之后就进入标准库中了，是在于`控制goroutine的生命周期`。
- 由于在Golang severs中，每个request都是在单个goroutine中完成
- 并且在单个goroutine（不妨称之为A）中也会有请求其他服务（启动另一个goroutine（称之为B）去完成）的场景
- 这就会涉及多个Goroutine之间的调用
- 如果某一时刻请求其他服务被取消或者超时，则作为深陷其中的当前goroutine B需要立即退出，然后系统才可回收B所占用的资源。
- 即一个request中通常包含多个goroutine，这些goroutine之间通常会有交互。

![](/img/image-20210616213116924.6104cd92.png)

- 那么，如何有效管理这些goroutine成为一个问题（主要是退出通知和元数据传递问题）
- Google的解决方法是Context机制，相互调用的goroutine之间通过传递context变量保持关联
- 这样在不用暴露各goroutine内部实现细节的前提下，有效地控制各goroutine的运行。

![](/img/image-20210616213314610.60383589.png)

- 如此一来，通过传递Context就可以追踪goroutine调用树，并在这些调用树之间传递通知和元数据。
- 虽然goroutine之间是平行的，没有继承关系，但是Context设计成是包含父子关系的，这样可以更好的描述goroutine调用之间的树型关系。

### 1.2 context常用方法

- `context.Context`是一个接口，该接口定义了四个需要实现的方法

```go
type Context interface {
    Deadline() (deadline time.Time, ok bool)
    Done() <-chan struct{}
    Err() error
    Value(key interface{}) interface{}
}
```

- **Done** 方法
  - 在Context被取消或超时时返回一个close的channel,close的channel可以作为广播通知
  - 告诉给context相关的函数要停止当前工作然后返回。
  - 当一个父operation启动一个goroutine用于子operation，这些子operation不能够取消父operation。
  - 下面描述的WithCancel函数提供一种方式可以取消新创建的Context.
  - 开发者可以把一个Context传递给任意多个goroutine然后cancel这个context的时候就能够通知到所有的goroutine。
- **Err**方法
  - 返回context为什么被取消
- **Deadline**
  - 返回context何时会超时。
- **Value**
  - 返回context相关的数据。

## 02.为什么需要context

- 在 Go http包的Server中，每一个请求在都有一个对应的 goroutine 去处理。
- 请求处理函数通常会启动额外的 goroutine 用来访问后端服务，比如数据库和RPC服务。
- 用来处理一个请求的 goroutine 通常需要访问一些与请求特定的数据，比如终端用户的身份认证信息、验证相关的token、请求的截止时间。
- 当一个请求被取消或超时时，所有用来处理该请求的 goroutine 都应该迅速退出，然后系统才能释放这些 goroutine 占用的资源。

### 2.1 全局变量解决

```go
// 全局变量方式存在的问题：
// 1. 使用全局变量在跨包调用时不容易统一
// 2. 如果worker中再启动goroutine，就不太好控制了。
```

```go
package main
import (
	"fmt"
	"sync"
	"time"
)

var wg sync.WaitGroup
var exit bool

func worker() {
	for {
		fmt.Println("worker")
		time.Sleep(time.Second)
		if exit {
			break
		}
	}
	wg.Done()
}

func main() {
	wg.Add(1)
	go worker()
	time.Sleep(time.Second * 3) // sleep3秒以免程序过快退出
	exit = true                 // 修改全局变量实现子goroutine的退出
	wg.Wait()
	fmt.Println("over")
}
```

### 2.2 通道方式

```go
package main

import (
	"fmt"
	"sync"

	"time"
)

var wg sync.WaitGroup

// 管道方式存在的问题：
// 1. 使用全局变量在跨包调用时不容易实现规范和统一，需要维护一个共用的channel

func worker(exitChan chan struct{}) {
LOOP:
	for {
		fmt.Println("worker")
		time.Sleep(time.Second)
		select {
		case <-exitChan: // 等待接收上级通知
			break LOOP
		default:
		}
	}
	wg.Done()
}

func main() {
	var exitChan = make(chan struct{})
	wg.Add(1)
	go worker(exitChan)
	time.Sleep(time.Second * 3)   // sleep3秒以免程序过快退出
    
	exitChan <- struct{}{}      // 给子goroutine发送退出信号
	close(exitChan)
	wg.Wait()
	fmt.Println("over")
}
```

### 2.3 官方版的方案

```go
package main
import (
	"context"
	"fmt"
	"sync"
	"time"
)

var wg sync.WaitGroup

func worker(ctx context.Context) {
LOOP:
	for {
		fmt.Println("worker")
		time.Sleep(time.Second)
		select {
		case <-ctx.Done(): // 等待上级通知
			break LOOP
		default:
		}
	}
	wg.Done()
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	wg.Add(1)
	go worker(ctx)
	time.Sleep(time.Second * 3)
	cancel() // 通知子goroutine结束
	wg.Wait()
	fmt.Println("over")
}
```

## 03.With系列函数

此外，`context`包中还定义了四个With系列函数。

### 3.1 WithCancel

- `WithCancel`返回带有新Done通道的父节点的副本。
- 当调用返回的cancel函数或当关闭父上下文的Done通道时，将关闭返回上下文的Done通道，无论先发生什么情况。
- 取消此上下文将释放与其关联的资源，因此代码应该在此上下文中运行的操作完成后立即调用cancel。
- 示例
  - 上面的示例代码中，`gen`函数在单独的goroutine中生成整数并将它们发送到返回的通道。
  - gen的调用者在使用生成的整数之后需要取消上下文，以免`gen`启动的内部goroutine发生泄漏。

```go
package main

import (
	"context"
	"fmt"
)

func gen(ctx context.Context) <-chan int {
	dst := make(chan int)
	n := 1
	go func() {
		for {
			select {
			case <-ctx.Done():
				return // return结束该goroutine，防止泄露
			case dst <- n:
				n++
			}
		}
	}()
	return dst
}
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel() // 当我们取完需要的整数后调用cancel

	for n := range gen(ctx) {
		fmt.Println(n)
		if n == 5 {
			break
		}
	}
}
/*
1
2
3
4
5
 */
```

### 3.2 WithDeadline

- 下面的代码中，定义了一个50毫秒之后过期的deadline
- 然后我们调用`context.WithDeadline(context.Background(), d)`得到一个上下文（ctx）和一个取消函数（cancel）
- 然后使用一个select让主程序陷入等待：等待1秒后打印`overslept`退出或者等待ctx过期后退出。
- 因为ctx50秒后就过期，所以`ctx.Done()`会先接收到值，上面的代码会打印ctx.Err()取消原因。

```go
package main
import (
	"context"
	"fmt"
	"time"
)

func main() {
	d := time.Now().Add(50 * time.Millisecond)
	ctx, cancel := context.WithDeadline(context.Background(), d)

	// 尽管ctx会过期，但在任何情况下调用它的cancel函数都是很好的实践。
	// 如果不这样做，可能会使上下文及其父类存活的时间超过必要的时间。
	defer cancel()

	select {
	case <-time.After(1 * time.Second):
		fmt.Println("overslept")
	case <-ctx.Done():
		fmt.Println(ctx.Err())
	}
}
```

### 3.3WithTimeout

- 取消此上下文将释放与其相关的资源，因此代码应该在此上下文中运行的操作完成后立即调用cancel
- 通常用于数据库或者网络连接的超时控制

```go
package main

import (
	"context"
	"fmt"
	"sync"

	"time"
)

// context.WithTimeout

var wg sync.WaitGroup

func worker(ctx context.Context) {
LOOP:
	for {
		fmt.Println("db connecting ...")
		time.Sleep(time.Millisecond * 10) // 假设正常连接数据库耗时10毫秒
		select {
		case <-ctx.Done(): // 50毫秒后自动调用
			break LOOP
		default:
		}
	}
	fmt.Println("worker done!")
	wg.Done()
}

func main() {
	// 设置一个50毫秒的超时
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond*50)
	wg.Add(1)
	go worker(ctx)
	time.Sleep(time.Second * 5)
	cancel() // 通知子goroutine结束
	wg.Wait()
	fmt.Println("over")
}
```

### 3.4 WithValue

- `WithValue`函数能够将请求作用域的数据与 Context 对象建立关系
- `WithValue`返回父节点的副本，其中与key关联的值为val。
- 仅对API和进程间传递请求域的数据使用上下文值，而不是使用它来传递可选参数给函数。
- 所提供的键必须是可比较的，并且不应该是`string`类型或任何其他内置类型，以避免使用上下文在包之间发生冲突。
- `WithValue`的用户应该为键定义自己的类型。为了避免在分配给interface{}时进行分配，上下文键通常具有具体类型`struct{}`。
- 或者，导出的上下文关键变量的静态类型应该是指针或接口。

```go
package main

import (
	"context"
	"fmt"
	"sync"

	"time"
)

// context.WithValue

type TraceCode string

var wg sync.WaitGroup

func worker(ctx context.Context) {
	key := TraceCode("TRACE_CODE")
	traceCode, ok := ctx.Value(key).(string) // 在子goroutine中获取trace code
	if !ok {
		fmt.Println("invalid trace code")
	}
LOOP:
	for {
		fmt.Printf("worker, trace code:%s\n", traceCode)
		time.Sleep(time.Millisecond * 10) // 假设正常连接数据库耗时10毫秒
		select {
		case <-ctx.Done(): // 50毫秒后自动调用
			break LOOP
		default:
		}
	}
	fmt.Println("worker done!")
	wg.Done()
}

func main() {
	// 设置一个50毫秒的超时
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond*50)
	// 在系统的入口中设置trace code传递给后续启动的goroutine实现日志数据聚合
	ctx = context.WithValue(ctx, TraceCode("TRACE_CODE"), "12512312234")
	wg.Add(1)
	go worker(ctx)
	time.Sleep(time.Second * 5)
	cancel() // 通知子goroutine结束
	wg.Wait()
	fmt.Println("over")
}
```

## 04.客户端超时取消示例

调用服务端API时如何在客户端实现超时控制？

### 4.1 server端

```go
// context_timeout/server/main.go
package main

import (
	"fmt"
	"math/rand"
	"net/http"

	"time"
)

// server端，随机出现慢响应

func indexHandler(w http.ResponseWriter, r *http.Request) {
	number := rand.Intn(2)
	if number == 0 {
		time.Sleep(time.Second * 10) // 耗时10秒的慢响应
		fmt.Fprintf(w, "slow response")
		return
	}
	fmt.Fprint(w, "quick response")
}

func main() {
	http.HandleFunc("/", indexHandler)
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		panic(err)
	}
}
```

### 4.2 client端

```go
// context_timeout/client/main.go
package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
	"time"
)

// 客户端

type respData struct {
	resp *http.Response
	err  error
}

func doCall(ctx context.Context) {
	transport := http.Transport{
	   // 请求频繁可定义全局的client对象并启用长链接
	   // 请求不频繁使用短链接
	   DisableKeepAlives: true, 	}
	client := http.Client{
		Transport: &transport,
	}

	respChan := make(chan *respData, 1)
	req, err := http.NewRequest("GET", "http://127.0.0.1:8000/", nil)
	if err != nil {
		fmt.Printf("new requestg failed, err:%v\n", err)
		return
	}
	req = req.WithContext(ctx) // 使用带超时的ctx创建一个新的client request
	var wg sync.WaitGroup
	wg.Add(1)
	defer wg.Wait()
	go func() {
		resp, err := client.Do(req)
		fmt.Printf("client.do resp:%v, err:%v\n", resp, err)
		rd := &respData{
			resp: resp,
			err:  err,
		}
		respChan <- rd
		wg.Done()
	}()

	select {
	case <-ctx.Done():
		//transport.CancelRequest(req)
		fmt.Println("call api timeout")
	case result := <-respChan:
		fmt.Println("call server api success")
		if result.err != nil {
			fmt.Printf("call server api failed, err:%v\n", result.err)
			return
		}
		defer result.resp.Body.Close()
		data, _ := ioutil.ReadAll(result.resp.Body)
		fmt.Printf("resp:%v\n", string(data))
	}
}

func main() {
	// 定义一个100毫秒的超时
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond*100)
	defer cancel() // 调用cancel释放子goroutine资源
	doCall(ctx)
}
```
