---
title: 并发
index_img: /img/cover34.png
date: 2023-10-20 20:50:13
categories: 
- Go进阶
tags:
- Go进阶


---

# 1.  并发

## 1.1  并发和并行的区别

并发和并行是两个不同的概念：

- 并行意味着程序在**任意时刻**都是同时运行的；
- 并发意味着程序在**单位时间内**是同时运行的

### 1.1.1  并行

**并行**就是在任一粒度时间内都具备同时执行的能力：简单来说并行就是多机或多台机器并行处理； SMP（SMP 是对称多处理器（Symmetric MultiProcessing）的简称。在这样的系统中包含多个处理器，同时，处理器间共享了内存和 I/O 总线。"对称"是指所有的处理器在功能和位置上地位相同，不存在主处理器或者被处理器较多的 "主机"） 表面上看是并行的，但由于是共享内存，以及线程间的同步等，不可能完全做
到并行。

### 1.1.2   并发

**并发**是在规定的时间内多个请求都得到执行和处理，强调的是给外界的感觉，实际上内部可能是分时操作的。并发重在避免阻塞，使程序不会因为一个阻塞而停止处理。并发典型的应用场景：分时操作系统就是一种并发设计（忽略多核 CPU）。

## 1.2  goroutine

`goroutine`是 Go 语言中处理并发执行的一个主要工具，是 Go 运行时层面的轻量级线程，与 OS 线程相比，它的开销更小。操作系统可以进行线程和进程的调度，本身具备并发处理能力，但进程切换代价还是过高，当操作系统在系统进程之间切换时，它需要保存当前正在运行进程的状态，以便在再次切换回该进程时恢复执行。这通常涉及保存进程的 "上下文"，即使该进程能够从中断点继续执行的所有信息（**处理器的寄存器**、**内存管理信息**、**进程状态**、**输入和输出状态**、**资源使用情况**等）。如果应用可以在用户态进行调度，应该可以更大限度地提升程序运行效率，goroutine就是基于这个思想实现的。

- goroutine 示例，代码如下：

```go
var wg sync.WaitGroup // 第一步：定义一个计数器

func routine1() {
   for i := 0; i < 10; i++ {
      fmt.Println("routine1 你好golang-", i) // routine1 你好golang-0, ...9
      time.Sleep(time.Millisecond * 100)
   }
   wg.Done() //协程计数器-1    // 第三步：协程执行完毕，计数器-1
}

func routine2() {
   for i := 0; i < 2; i++ {
      fmt.Println("routine2 你好golang-", i) // routine2 你好golang-0, routine2 你好golang-1
      time.Sleep(time.Millisecond * 100)
   }
   wg.Done() //协程计数器-1
}

func main() {
   wg.Add(1)  //协程计数器+1       第二步：开启一个协程计数器+1
   go routine1() //表示开启一个协程
   wg.Add(1)  //协程计数器+1
   go routine2() //表示开启一个协程

   wg.Wait() //等待协程执行完毕...   第四步：计数器为0时推出
   fmt.Println("主线程退出...")
}
```

goroutine 有如下特性：

- go 的执行是非阻塞的，不会等待；
- go 后面函数的返回值会被忽略；
- 调度器不能保证多个 goroutine 的执行次序；
- 没有父子 goroutine 的概念，所有 goroutine 是平等地被调度和执行的；
- go 程序运行时会在 main 函数先创建一个 goroutine，其他 go 关键字创建的 goroutine 会另外创建；
- go 没有暴露 goroutine id 给用户，所以不能在一个 goroutine 里面显式地操作另一个 goroutine ，不过 runtime 包提供了一些函数访问和设置 goroutine 的相关信息；

### 1.2.1  GOMAXPROCS

GOMAXPROCS( n int ) 用来设置或查询可以并发执行的 goroutine 数目，n 大于 1 表示设置 GOMAXPROCS 值，否则表示查询当前 GOMAXPROCS 的值。

### 1.2.2   Goexit

Goexit() 是结束当前 goroutine 的运行， Goexit 在结束当前 goroutine 运行之前会调用当前 goroutine 已经注册的 defer 。 Goexit 并不会产生 panic ，所以该 goroutine defer 里面的 recover 调用都返回 nil 。

### 1.2.3   Gosched

Gosched() 是放弃当前调度执行机会，将当前 goroutine 放到队列中等待下次被调度。只有 goroutine 还是不够的，多个 goroutine 之间还需要通信、同步、协同等。

## 1.3  Chan

chan 是 Go 语言里面的一个关键宇，是 channel 的简写，翻译为中文就是通道。  goroutine 是 Go 语言里面的并发执行体，通道是 goroutine 之间通信和同步的重要组件。 Go 的哲学是“不要通过共享内存来通信，而是通过通信来共享内存”（CSP（Communicating Sequential Processes）是一种用于设计并发系统的模型，它强调通过在独立的并发实体或“进程”之间传递消息来进行通信），通道是 Go 通过通信来共享内存的载体。例如：

```go
／／创建一个无缓冲的通道，通道存放元素的类型为 datatype 
make(chan datatype ) 
／／创建一个有 10 个缓冲的远远，遥远存放元素的类型为 datatype 
make(chan datatype,  10)
```

通道分为无缓冲的通道和有缓冲的通道， Go 提供内置函数 len 和 cap ，**无缓冲的通道的 len** **和 cap 都是 0**，**有缓冲的通道的 len 代表没有被读取的元素数， cap 代表整个通道的容量**。无缓冲的通道既可以用于通信，也可以用于两个 goroutine 的同步，有缓冲的通道主要用于通信。有缓冲通道示例：

```go
var m sync.Mutex

func main(){
	m.Lock() // 互斥锁
	c := make(chan int ,100)
	go func() {
		defer m.Unlock() // 解锁
		for i := 0; i < 100; i++{
			c <- i // 向 c 通道传递数据
		}
		close(c)
	}()
	m.Lock() // 等到互斥锁解锁，然后再次锁定用来阻塞主程序。

	for v := range c { // 向已关闭的通道遍历读取数据
		fmt.Println(v)
	}
}
```

写到缓冲通道中的数据不会消失，它还可以缓冲和适配两个 goroutine 处理速率不一致的情况，缓冲通道和消息队列类似，有削峰和增大吞吐量的功能。

操作不同状态的 chan 会引发三种行为：

1. panic
   - 向已经关闭的通道写数据会导致 panic ；最佳实践是由写入者关闭通道，能最大程度地避免向已经关闭的通道写数据而导致的 panic；
   - 重复关闭的通道会导致 panic；
2. 阻塞
   - 向未初始化的通道写数据或读数据都会导致当前 goroutine 的永久阻塞；
   - 向缓冲区己满的通道写入数据会导致 goroutine 阻塞；
   - 通道中没有数据，读取该通道会导致 goroutine 阻塞；
3. 非阻塞
   - 读取己经关闭的通道不会引发阻塞，而是立即返回通道元素类型的零值，可以使用 comrna , ok 语法判断通道是否己经关闭；
   - 向有缓冲且没有满的通道读／写不会引发阻塞；

## 1.4  WaitGroup 

goroutine 和 chan 一个用于并发，另一个用于通信。没有缓冲的通道具有同步的功能，除此之外， sync 包也提供了多个 goroutine 同步的机制，主要是通过 WaitGroup 实现的。

主要数据结构和操作如下：

```go
type WaitGroup struct  { 
 // contains filtered or unexported fields
}
// 添加等待信号
func (wg *WaitGroup) Add(delta int) 
// 释放等待信号
func (wg *WaitGroup) Done() 
// 等待
func (wg *WaitGroup) Wait() 
```

WaitGroup 用来等待多个 goroutine 完成， main goroutine 调用 Add 设置需要等待 goroutine 的数目，每一个 goroutine 结束时调用 Done(), Wait() 被 main 用来等待所有的 goroutine 完成。

## 1.5  select 

select 是类 UNIX 系统提供的一个多路复用系统 API, Go 语言借用多路复用的概念，提供了 select 关键字，用于多路监昕多个通道。当监听的通道没有状态是可读或可写的， select 是阻塞的；只要监听的通道中有一个状态是可读或可写的，则 select 就不会阻塞，而是进入处理就绪通道的分支流程。如果监听的通道有多个可读或可写的状态， 则 select 随机选取一个处理。

```go
func  main()   { 
ch  : =  make(chan int ,  1) 
go  func(chan  int)  { 
for  { 
    select  { 
        //0 或 1 的写入是随机的
        case  ch  < - 0 : 
        case  ch  <- 1 : 
        }
    }
} (ch) 
for  i : =  0;  i   <  10;i++ { 
    println(<-ch)
    }
}
// 运行结果
0 0 1 0 0 1 0 1 1 0
```

## 1.6  扇入（ Fan in ）和扇出（ Fan out ) 

编程中经常遇到 “扇入和扇出” 两个概念，所谓的扇入是指将多路通道聚合到一条通道中处理，Go 语言最简单的扇入就是使用 sel ect 聚合多条通道服务；所谓的扇出是指将一条通道发散到多条通道中处理，在 Go 语言里面具体实现就是使用 go 关键字启动多个 goroutine 并发处理。

中国有句经典的哲学名句叫 “分久必合，合久必分” 软件的设计和开发也遵循同样的哲学思想，扇入就是合，扇出就是分。当生产者的速度很慢时，需要使用扇入技术聚合多个生产者满足消费者， 比如恨耗时的加密／解密服务；当消费者的速度很慢时，需要使用扇出技术，比如Web 服务器并发请求处理。扇入和扇出是 Go 并发编程中常用的技术。

### 1.6.1   扇入（Fan-In）：

```go
func fanIn(input1, input2 <-chan string) <-chan string {
    c := make(chan string)
    go func() {
        for {
            select {
            case s := <-input1:
                c <- s
            case s := <-input2:
                c <- s
            }
        }
    }()
    return c
}
```

扇入指的是将多个输入 channel 合并到一个 channel 中，扇出是将一个输入 channel 分散给多个 worker 进行处理。

### 1.6.2  扇出（Fan-Out）：

```go
func fanOut(input <-chan string, workerCount int) []<-chan string {
    var outputs []<-chan string
    for i := 0; i < workerCount; i++ {
        outputs = append(outputs, createWorker(input))
    }
    return outputs
}

func createWorker(input <-chan string) <-chan string {
    c := make(chan string)
    go func() {
        for n := range input {
            c <- doWork(n)
        }
        close(c)
    }()
    return c
}

func doWork(n string) string {
    //...执行一些操作...
    return n
}
```

在以上扇出的例子中，`input`是输入channel，在`fanOut`函数中，我们根据`workerCount`创建相同数量的Worker来处理输入信息。每个Worker处理的任务是从输入channel读取信息，然后进行一些工作（在`doWork`函数中定义），然后将信息写入自己的输出channel中。Workers的输出channel会被添加到`outputs`切片中，并从`fanOut`函数返回。

### 1.6.3  扇入扇出分别对应的应用场景

扇入和扇出的概念常用在处理并发和流处理系统中，它们各自有一些常见的应用场景：

**（1）扇入（Fan-In）**
扇入是将来自多个源的数据聚合到一个通道中，这种方式常用于多个并行或异步任务完成时集中处理结果，如：

1. 对来自多个源的日志或状态更新聚合到一个处理者，以实现统一的日志记录、分析或监控。
2. 在分布式计算的上下文中，多个节点可能正在并行处理任务，并在完成时将结果发送回中央节点以进行聚合和处理。

**（2）扇出（Fan-Out）**
扇出是将数据从一个源分发到多个接收者的过程，每个接收者都会得到完整的数据拷贝，扇出可以提高处理或任务的吞吐量。具体应用可能包括：

1. 在负载均衡的上下文中，扇出通常用作一种将任务分发到多个工作节点的手段以提高整体处理速度，每个节点处理部分工作负载。
2. 在自然语言处理或图像处理等领域，可以使用扇出来并行训练或运行多个模型，然后比较各自的输出以确定最优解。
3. 扇出模式还可以用于数据备份和冗余存储的场景。比如，我们可以将一个流量的数据同时发送到多个存储节点，以此达到数据的备份和冗余保障。

## 1.7  通知推出机制

读取己经关闭的通道不会引 起阻塞，也不会导致 panic ，而是立即返回该通道存储类型的零值。关闭 select 监听的某个通道能使 select 立即感知这种通知，然后进行相应的处理，  这就是所谓的退出通知机制（close channel to broadcast ）。下面通过一个随机数生成器的示例演示退出通知机制，下游的消费者不需要随机数时，显式地通知生产者停止生产。

```go
// GenerateintA 是一个随机数生成器
func GenerateintA(done chan struct{}) chan int {
	ch := make(chan int)
	go func() {
	Label:
		for {
			select {
			case ch <- rand.Int():
			case <-done:
				break Label
			}
		}
		close(ch)
	}()
	return ch
}

func main() {
	done := make(chan struct{})
	ch := GenerateintA(done)
	fmt.Println(<-ch)
	fmt.Println(<-ch)

	close(done)

	fmt.Println(<-ch)
	fmt.Println(<-ch)

	println("NumGoroutine=", runtime.NumGoroutine())
}

// 输出结果
146870834388028874
7216694335601338127
0
0
NumGoroutine= 1

```

## 1.8  并发范式

通过具体的程序示例来演示 Go 语言强大的并发处理能力，每个示例代表一个并发处理范式，这些范式具有典型的特征，在真实的程序中稍加改造就能使用。

### 1.8.1   生成器

在应用系统编程中，常见的应用场景就是调用一个统一的全局的生成器服务， 用于生成全局事务号、订单号、序列号和随机数等。 Go 对这种场景的支持非常简单，下面以一个随机数生成器为例来说明。

1. 最简单的带缓冲的生成器。  例如：

```go
// RandomNumber 是一个随机数生成器
func RandomNumber() chan int {
	ch := make(chan int, 10)
	// 启动一个 go routine 用于生成随机数，函数返回一个通道用于获取随机数
	go func() {
		for {
			ch <- rand.Int()
		}
	}()
	return ch
}

func main() {
	ch := RandomNumber()
	fmt.Println(<-ch)
	fmt.Println(<-ch)
}

// 输出结果
8442295699646266936
6343099628820528177

```

2. 多个 goroutine 增强型生成器。  例如：

```go

// RandomNumber1 是一个随机数生成器
func RandomNumber1() chan int {
	ch := make(chan int)
	// 启动一个 go routine 用于生成随机数，函数返回一个通道用于获取随机数
	go func() {
		for {
			ch <- rand.Int()
		}
	}()
	return ch
}

// RandomNumber2 是一个随机数生成器
func RandomNumber2() chan int {
	ch := make(chan int)
	// 启动一个 go routine 用于生成随机数，函数返回一个通道用于获取随机数
	go func() {
		for {
			ch <- rand.Int()
		}
	}()
	return ch
}

func GenerateInt() chan int {
	ch := make(chan int, 20)
	go func() {
		for {
			select {
			case ch <- <-RandomNumber1():
			case ch <- <-RandomNumber2():
			}
		}
	}()
	return ch
}

func main() {
	ch := GenerateInt()

	for i := 0; i < 100; i++ {
		fmt.Println(<-ch)
	}
}

// 输出结果
4732711589376798349
5980361011433472918
8507484322095864034
......
```

### 1.8.2   管道

通道可以分为两个方向，一个是读，另一个是写，假如一个函数的输入参数和输出参数都是相同的 chan 类型， 则该函数可以调用自己，最终形成一个调用链。当然多个具有相同参数类型的函数也能组成一个调用链，这很像 UNIX 系统的管道，是一个有类型的管道。

下面通过具体的示例演示 Go 程序这种链式处理能力：

```go
package  main 

import ( 
"fmt"
)

// chain 函数的输入参数和输出参数类型相同，都是 chan int 类型
// chain 函数的功能是将 chan 内的数据统一加1
func chain(in chan int) chan int { 
    out := make(chan int)
    go func(){
        for v := range in{
            out <- 1 + v
        }
        close(out)
    }()
    return out
}

func main() {
    in := make(chan int)
    go func() {
        for i := 0; i < 10; i++ { 
        	in <- i
        } 
        close(in)
    }()
    // 连续调用 3 次 chan，相当于把 in 中的每个元素都加 3
    out := chain(chain(chain(in)))
    for v := range out {
        fmt.Println(v)
    }
}
```

### 1.8.3   每个请求一个  goroutine

下面以计算 100 个自然数的和来举例，将计算任务拆分为多个 task，每个 task 启动一个 goroutine 进行处理，程序示例代码如下：

```go
package main

import (
	"fmt"
	"sync"
)

// 工作任务
type task struct {
	begin  int
	end    int
	result chan<- int
}

// 任务执行:计算 begin 到 end 的和
// 执行结果写入到结果 chan result 中
func (t *task) do() {
	sum := 0
	for i := t.begin; i <= t.end; i++ {
		sum += i
	}
	t.result <- sum
}

// 构建 task 并写入到 task 通道
func InitTask(taskchan chan<- task, r chan int, p int) {
	qu := p / 10
	mod := p % 10
	high := qu * 10
	for j := 0; j < qu; j++ {
		b := 10*j + 1
		e := 10 * (j + 1)
		tsk := task{
			begin:  b,
			end:    e,
			result: r,
		}
		taskchan <- tsk
	}
	if mod != 0 {
		tsk := task{
			begin:  high + 1,
			end:    p,
			result: r,
		}
		taskchan <- tsk
	}

	close(taskchan)
}

// 读取 task chan ,每个 task 一个 worker goroutine 处理
// 并等待每个 task 运行完，关闭结果通道
func DistributeTask(taskchan <-chan task, wait *sync.WaitGroup, result chan int) {

	for v := range taskchan {
		wait.Add(1)
		go ProcessTask(v, wait)
	}
	wait.Wait()
	close(result)
}

// 工作 goroutine 处理具体工作，并将处理结构发送到结果通道
func ProcessTask(t task, wait *sync.WaitGroup) {
	t.do()
	wait.Done()
}

// 读取结果通道，汇总结果
func ProcessResult(resultchan chan int) int {
	sum := 0
	for r := range resultchan {
		sum += r
	}
	return sum
}

func main() {
	// 创建任务通道
	taskchan := make(chan task, 10)

	// 创建结果通道
	resultchan := make(chan int, 10)

	// wait 用于同步等待任务的执行
	wait := &sync.WaitGroup{}

	// 初始化 task 的 goroutine,计算 100 个自然数之和
	go InitTask(taskchan, resultchan, 100)

	//每个 task 启动一个 goroutine 处理，
	go DistributeTask(taskchan, wait, resultchan)

	// 通过结果通道获取结果并汇总
	sum := ProcessResult(resultchan)

	fmt.Println("sum=", sum)
}

// 结果
sum=  5050 
```

程序的逻辑分析：
（1）InitTask 函数构建 task 并发送到 task 通道中；
（2）分发任务函数 DistributeTask 为每个 task 启动一个 goroutine 处理任务，   等待其处理完成， 然后关闭结果通道；
（3）ProcessResult 函数读取并统计所有的结果。这几个函数分别在不同的 goroutine 中运行，  它们通过通道和sync.WaitGroup 进行通信和同步；

### 1.8.4   固定 worker 工作池

服务器编程中使用最多的就是通过线程池来提升服务的井发处理能力。在 Go 语言编程中，
一样可以轻松地构建固定数目的 goroutines 作为工作线程池。下面还是以计算多个整数的和为
例来说明这种并发范式。
程序中除了主要的 main goroutine ，还开启了如下几类 goroutine:
（1）初始化任务的 goroutme；
（2）分发任务的 goroutine；
（3）等待所有 worker 结束通知，然后关闭结果通道的 goroutine；
main 函数负责拉起上述 goroutine ，并从结果通道获取最终的结果；
程序采用三个通道，分别是：
（1）传递 task 任务的通道；
（2）传递 task 结果的通道；
（3）接收 worker 处理完任务后所发送通知的通道；
相关的代码如下：

```go
package main

import (
	"fmt"
)

// 工作池的 goroutine 数目
const (
	NUMBER = 10
)

// 工作任务
type task struct {
	begin  int
	end    int
	result chan<- int
}

// 任务处理:计算 begin 到 end 的和
// 执行结果写入到结果 chan result 中
func (t *task) do() {
	sum := 0
	for i := t.begin; i <= t.end; i++ {
		sum += i
	}
	t.result <- sum
}

// 初始化待处理 task chan
func InitTask(taskchan chan<- task, r chan int, p int) {
	qu := p / 10
	mod := p % 10
	high := qu * 10
	for j := 0; j < qu; j++ {
		b := 10*j + 1
		e := 10 * (j + 1)
		tsk := task{
			begin:  b,
			end:    e,
			result: r,
		}
		taskchan <- tsk
	}
	if mod != 0 {
		tsk := task{
			begin:  high + 1,
			end:    p,
			result: r,
		}
		taskchan <- tsk
	}

	close(taskchan)
}

// 读取 task chan 分发到 worker goroutine 处理，workers 的总的数量是 workers
func DistributeTask(taskchan <-chan task, workers int, done chan struct{}) {

	for i := 0; i < workers; i++ {
		go ProcessTask(taskchan, done)
	}
}

// 工作 goroutine 处理具体工作，并将处理结构发送到结果 chan
func ProcessTask(taskchan <-chan task, done chan struct{}) {
	for t := range taskchan {
		t.do()
	}
	done <- struct{}{}
}

// 通过 done channel 来同步等待所有工作 goroutine 的结束，然后关闭结果 chan
func CloseResult(done chan struct{}, resultchan chan int, workers int) {
	for i := 0; i < workers; i++ {
		<-done
	}
	close(done)
	close(resultchan)
}

// 读取结果通道，汇总结果
func ProcessResult(resultchan chan int) int {
	sum := 0
	for r := range resultchan {
		sum += r
	}
	return sum
}

func main() {
	workers := NUMBER

	// 工作通道
	taskchan := make(chan task, 10)

	// 结果通道
	resultchan := make(chan int, 10)

	// worker 信号通道
	done := make(chan struct{}, 10)

	// 初始化 task 的 goroutine,计算 1000 个自然数之和
	go InitTask(taskchan, resultchan, 1000)

	// 分发任务在 NUMBER 个 goroutine 池
	DistributeTask(taskchan, workers, done)

	// 获取各个 goroutine 处理完任务的通知，并关闭结果通道
	go CloseResult(done, resultchan, workers)

	// 通过结果通道处理结果
	sum := ProcessResult(resultchan)

	fmt.Println("sum=", sum)
}

// 结果
sum=  5050
```

程序的逻辑分析：
（1）构建 task 并发送到 task 通道中；
（2）分别启动 n 个工作线程，不停地从 task 通道中获取任务，然后将结果写入结果通道。如果任务通道被关闭，则负责向收敛结果的 goroutine 发送通知，告诉其当前 worker 已经完成工作；
（3）收敛结果的 goroutine 接收到所有 task 己经处理完毕的信号后，主动关闭结果通道；
（4）main 中的函数 ProcessResult 读取并统计所有的结果；

### 1.8.5  future 模式

编程中经常遇到在一个流程中需要调用多个子调用的情况，这些子调用相互之间没有依赖，如果串行地调用，则耗时会很长，此时可以使用 Go 并发编程中的 future 模式。
future 模式的基本工作原理：
（1）使用 chan 作为函数参数；
（2）启动 goroutine 调用函数；
（3）通过 chan 传入参数；
（4）做其他可以并行处理的事情；
（5）通过 chan 异步获取结果；
下面通过一段抽象的代码来学习该模式：

```go
package main

import (
	"fmt"
	"time"
)

// 一个查询结构体
// 这里的 sql 和 result 是一个简单的抽象，具体的应用，可能是更复杂的数据类型
type query struct {
	// 参数 Channel
	sql chan string

	// 结果 Channel
	result chan string
}

// 执行 Query
func execQuery(q query) {
	// 启动协程
	go func() {
		// 获取输入
		sql := <-q.sql

		// 访问数据库

		// 输出结果通道
		q.result <- "result from " + sql
	}()

}

func main() {

	// 初始化 Query
	q := query{make(chan string, 1), make(chan string, 1)}

	// 执行 Query，注意执行的时候无需准备参数
	go execQuery(q)
	//准备参数
	q.sql <- "select * from table;"

	// do otherthings
	time.Sleep(1 * time.Second)

	//获取结果
	fmt.Println(<-q.result)
}

```

future 最大的好处是将函数的同步调用转换为异步调用，   适用于一个交易需要多个子调用且这些子调用没有依赖的场景。 实际情况可能比上面示例复杂得多，要考虑错误和异常的处理。