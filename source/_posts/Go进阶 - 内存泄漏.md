---
title: 内存泄露
index_img: /img/cover13.png
date: 2021-02-10 21:10:32
categories: 
- Go进阶
tags:
- Go进阶

---

# 1.内存泄漏

## 01.内存泄漏概念

### 1.1 内存泄漏定义

- 定义：由于疏忽或错误造成程序未能释放已经不再使用的内存。

### 1.2 go内存泄漏两种情况

- ```
  情况1：僵尸进程
  ```

  - 有goroutine泄漏，goroutine“飞”了，zombie goroutine没有结束
  - 这个时候在这个goroutine上分配的内存对象将一直被这个僵尸goroutine引用着
  - 进而导致gc无法回收这类对象，内存泄漏

- ```
  情况2：全局数据结构挂住了本该释放的对象
  ```

  - 有一些全局（或者生命周期和程序本身运行周期一样长的）的数据结构意外的挂住了本该释放的对象
  - 虽然goroutine已经退出了，但是这些对象并没有从这类数据结构中删除，导致对象一直被引用，无法被回收。

## 02.内存泄漏排查

### 2.1 排除掉goroutine泄漏

- 首先，我利用压测工具对server进行100个websocket连接，模拟用户浏览行为，然后关闭连接。
- 打开浏览器查看goroutine数量，发现新起的goroutine全部已经销毁，没有观察到有泄漏的goroutine，因此排除此情况。

### 2.2 确定是全局变量无回收

- 再次用压测工具进行压测然后关闭，使用观察内存情况。
- 使用`go tool pprof -inuse_space http://127.0.0.1:9999/debug/pprof/heap`
- 输入`png`导出（在这种情况下，需要等程序gc完再导出，建议等10分钟左右）
- **发现问题所在**
  - 每次都会遗留这么大概0.5M的内存空间出来
  - 就奇怪，明明整个goroutine退出为什么还有会内存占用?相应的全局变量也会删除该地方的引用。
  - 等一下，全局变量，难道是删除的时候没做好配对导致没有真正删除该引用吗？
  - 去查了下代码，果然是没有**删除引用导致**的，至此问题解决。

![img](/img/image-20210604100636742.9939c323.png)

- 这里面有个项目的坑，上报日志的key不是根据这个`len(map)`计算出，导致上报日志的时候以为删除了该key。

## 03.goroutine 泄露的场景

- goroutine泄露一般是因为channel操作阻塞而导致整个routine一直阻塞等待或者 goroutine 里有死循环的时候
- 可以细分为下面五种情况

### 3.1 情况1：从channel里读但没有写

- leak 是一个有 bug 程序。它启动了一个 goroutine 阻塞接收 channel。
- 当 Goroutine 正在等待时，leak 函数会结束返回。
- 此时，程序的其他任何部分都不能通过 channel 发送数据，那个 channel 永远不会关闭
- fmt.Println 调用永远不会发生， 那个 goroutine 会被永远锁死

```go
func leak() {
     ch := make(chan int)

     go func() {
        val := <-ch
        fmt.Println("We received a value:", val)
    }()
}
```

### 3.2 情况2：向已满的 buffered channel 写，但是没有读

### 3.3 情况3： select操作在所有case上阻塞

- 实现一个 fibonacci 数列生成器，并在独立的 goroutine 中运行
- 在读取完需要长度的数列后，如果 用于 退出生成器的 quit 忘了被 close (或写入数据)
- select 将一直被阻塞造成 该 goroutine 泄露。

```go
package main
import "fmt"

func fibonacci(c, quit chan int)  {
	x, y := 0, 1
	for{
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func main() {
	c := make(chan int)
	quit := make(chan int)

	go fibonacci(c, quit)

	for i := 0; i < 10; i++{
		fmt.Println(<- c)
	}

	// close(quit)
}
```

### 3.4 goroutine进入死循环

```go
// 粗暴的示例
func foo() {
  for{
    fmt.Println("fooo")
  }
}
```