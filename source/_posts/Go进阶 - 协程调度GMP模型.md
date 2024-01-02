---
title: 协程调度GMP模型
index_img: /img/cover16.png
date: 2021-02-20 22:15:12
categories: 
- Go进阶
tags:
- Go进阶

---

# 1.协程调度GMP模型

## 01.线程调度

### 1.1 早期单线程操作系统

- 一切的软件都是跑在操作系统上，真正用来干活(计算)的是CPU。
- 早期的操作系统每个程序就是一个进程，知道一个程序运行完，才能进行下一个进程，就是“单进程时代”
- 一切的程序只能串行发生。

![img](/img/image-20210604144028156.d6b2864c.png)

### 1.2 多进程/线程时代

- 在多进程/多线程的操作系统中，就解决了阻塞的问题，因为一个进程阻塞cpu可以立刻切换到其他进程中去执行
- 而且调度cpu的算法可以保证在运行的进程都可以被分配到cpu的运行时间片
- 这样从宏观来看，似乎多个进程是在同时被运行。
- 但新的问题就又出现了，进程拥有太多的资源，进程的创建、切换、销毁，都会占用很长的时间
- CPU虽然利用起来了，但如果`进程过多，CPU有很大的一部分都被用来进行进程调度了`
- 大量的进程/线程出现了新的问题
  - 高内存占用
  - 调度的高消耗CPU
  - 进程虚拟内存会占用4GB[32位操作系统], 而线程也要大约4MB

![img](/img/image-20210604144407556.878340a6.png)

### 1.3 Go协程goroutine

- Go中，协程被称为goroutine，它非常轻量，一个goroutine只占几KB，并且这几KB就足够goroutine运行完
- 这就能在有限的内存空间内支持大量goroutine，支持了更多的并发
- 虽然一个goroutine的栈只占几KB，但实际是可伸缩的，如果需要更多内容，`runtime`会自动为goroutine分配。
- Goroutine特点：
  - 占用内存更小（几kb）
  - 调度更灵活(runtime调度)

### 1.4 协程与线程区别

- 协程跟线程是有区别的，线程由CPU调度是抢占式的
- **协程由用户态调度是协作式的**，一个协程让出CPU后，才执行下一个协程

![img](/img/image-20210604151113883.31ff129f.png)

## 02.调度器GMP模型

- G：goroutine（协程）
- M：thread（内核线程，不是用户态线程）
- P：processer（调度器）

### 2.1 GM模型

- `G（协程）`，通常在代码里用 `go` 关键字执行一个方法，那么就等于起了一个`G`。
- `M（内核线程）`，操作系统内核其实看不见`G`和`P`，只知道自己在执行一个线程。
- `G`和`P`都是在**用户层**上的实现。
- 并发量小的时候还好，当并发量大了，这把大锁，就成为了**性能瓶颈**。

![img](/img/640.adc59e89.gif)

- GPM由来
  - 基于没有什么是加一个中间层不能解决的思路，`golang`在原有的`GM`模型的基础上加入了一个调度器`P`
  - 可以简单理解为是在`G`和`M`中间加了个中间层
  - 于是就有了现在的`GMP`模型里的P

### 2.2 GMP模型

![img](/img/image-20210604153340855.3a3ed056.png)

## 03.GPM流程分析

- 我们通过 go func()来创建一个goroutine；

### 3.1 P本地队列获取G

- M`想要运行`G`，就得先获取`P`，然后从`P`的本地队列获取`G

![img](/img/641.ac98dab0.gif)

### 3.2 本地队列中G移动到全局队列

- 新建 `G` 时，新`G`会优先加入到 `P` 的本地队列；
- 如果本地队列满了，则会把本地队列中一半的 `G` 移动到全局队列

![img](/img/646.61ce03be.gif)

### 3.3 从其他P本地队列的G放到自己P队列

- 如果全局队列为空时，`M` 会从其他 `P` 的本地队列**偷（stealing）一半G**放到自己 `P` 的本地队列。

![img](/img/888.ab33d3d0.gif)

### 3.4 M从P获取下一个G，不断重复

- `M` 运行 `G`，`G` 执行之后，`M` 会从 `P` 获取下一个 `G`，不断重复下去

![img](/img/999.29c4346c.gif)

## 04.goroutine调度器

- [参考(opens new window)](https://github.com/lifei6671/interview-go/blob/master/base/go-scheduler-base.md)

### 4.1 普通线程与goroutine

#### 1、普通线程缺点

- 1）创建和切换太重

  - 操作系统`线程的创建和切换都需要进入内核`，而进入内核所消耗的`性能代价比较高，开销较大`；

- 2）内存使用太重

  - 一方面，为了尽量避免极端情况下操作系统线程栈的溢出，

    ```
    内核在创建操作系统线程时默认会为其分配一个较大的栈内存
    ```

    - 虚拟地址空间，内核并不会一开始就分配这么多的物理内存
    - 然而在绝大多数情况下，系统线程远远用不了这么多内存，这导致了浪费；

  - 另一方面，栈内存空间一旦创建和初始化完成之后其大小就不能再有变化，这决定了在某些特殊场景下系统线程栈还是有溢出的风险。

#### 2、goroutine为什么轻量

- goroutine是用户态线程，其创`建和切换都在用户代码中完成而无需进入操作系统内核`，所以其开销要远远小于系统线程的创建和切换；
- `goroutine启动时默认栈大小只有2k`，这在多数情况下已经够用了，即使不够用，goroutine的栈也会自动扩大
  - 同时，如果栈太大了过于浪费它还能自动收缩，这样既没有栈溢出的风险，也不会造成栈内存空间的大量浪费。

### 4.2 线程模型与调度器

#### 1、调度器理论

- goroutine建立在操作系统线程基础之上，它与操作系统线程之间实现了一个多对多(M:N)的两级线程模型
- 这里的 M:N 是指M个goroutine运行在N个操作系统线程之上
- `内核负责对这N个操作系统线程进行调度`，而这`N个系统线程又负责对这M个goroutine进行调度和运行`

```
如何调度
```

- 所谓的对goroutine的调度，是指程序代码按照一定的算法在适当的时候挑选出合适的goroutine并放到CPU上去运行的过程
- 这些`负责对goroutine进行调度的程序代码我们称之为goroutine调度器`

#### 2、调度器伪代码理解

- 所谓的对goroutine的调度，`是指程序代码按照一定的算法在适当的时候挑选出合适的goroutine并放到CPU上去运行的过程`
- 这些`负责对goroutine进行调度的程序代码我们称之为goroutine调度器`

```go
// 程序启动时的初始化代码
......
for i := 0; i < N; i++ { // 创建N个操作系统线程执行schedule函数
    create_os_thread(schedule) // 创建一个操作系统线程执行schedule函数
}

//schedule函数实现调度逻辑
func schedule() {
   for {   //调度循环
         // 根据某种算法从M个goroutine中找出一个需要运行的goroutine
         g := find_a_runnable_goroutine_from_M_goroutines()
         run_g(g) // CPU运行该goroutine，直到需要调度其它goroutine才返回
         save_status_of_g(g) // 保存goroutine的状态，主要是寄存器的值
    }
}
```

- `程序运行起来之后创建了N个由内核调度的操作系统线程（工作线程）去执行shedule函数`
- 而schedule函数在一个调度循环中反复从M个goroutine中挑选出一个需要运行的goroutine并跳转到该goroutine去运行
- 直到需要调度其它goroutine时才返回到schedule函数中
  - 通过save_status_of_g保存刚刚正在运行的goroutine的状态然后再次去寻找下一个goroutine

### 4.3 调度器数据结构

```
操作系统线程及其调度
```

- 在执行操作系统代码时，`内核调度器按照一定的算法挑选出一个线程`
- 并把`该线程保存在内存之中的寄存器的值放入CPU对应的寄存器从而恢复该线程的运行`

#### 1、g结构体

```
存放goroutine状态信息：g的结构体
```

- `系统线程对goroutine的调度与内核对系统线程的调度原理是一样的`
- `实质都是通过保存和修改CPU寄存器的值来达到切换线程/goroutine的目的`
- 为了实现对goroutine的调度，需要引入一个数据结构来保存CPU寄存器的值以及goroutine的其它一些状态信息
- 在Go语言调度器源代码中，这个数据结构是一个名叫g的结构体，它保存了goroutine的所有信息
- 该结构体的每一个实例对象都代表了一个goroutine，调度器代码可以通过g对象来对goroutine进行调度
- 当goroutine被调离CPU时，`调度器代码负责把CPU寄存器的值保存在g对象的成员变量之中`
- `当goroutine被调度起来运行时，调度器代码又负责把g对象的成员变量所保存的寄存器的值恢复到CPU的寄存器`

#### 2、全局队列

```
goroutine全局队列：schedt结构体
```

- 要实现对goroutine的调度，仅仅有g结构体对象是不够的，至少还需要`一个存放所有（可运行）goroutine的容器`
- 一方面用来`保存调度器自身的状态信息`，另一方面它还拥有`一个用来保存goroutine的运行队列`
- 在每个Go程序中schedt结构体只有一个实例对象，该实例对象在源代码中被定义成了一个共享的全局变量
- 这样每个工作线程都可以`访问它以及它所拥有的goroutine运行队列，我们称这个运行队列为全局运行队列`

#### 3、局部队列

```
goroutine局部队列：p结构体
```

- 因为全局运行队列是每个工作线程都可以读写的，因此访问它需要加锁，加锁会导致严重的性能问题。
- 于是，调度器又为`每个工作线程引入了一个私有的局部goroutine运行队列`
- `工作线程优先使用自己的局部运行队列，只有必要时才会去访问全局运行队列`，这大大减少了锁冲突，提高了工作线程的并发性
- 在Go调度器源代码中，局部运行队列被包含在p结构体的实例对象之中
- 每一个运行着go代码的工作线程都会与一个p结构体的实例对象关联在一起

#### 4、m结构体

```
属于工作线程的m结构体
```

- Go调度器源代码中还有一个`用来代表工作线程的m结构体`
- `每个工作线程都有唯一的一个m结构体的实例对象与之对应`，m结构体对象除了记录着
  - 1）工作线程的诸如栈的`起止位置`
  - 2）当前`正在执行的goroutine`以及是否空闲等等状态信息之外
  - 3）还通过指针维持着与`p结构体的实例对象之间的绑定关系`
- 于是，`通过m既可以找到与之对应的工作线程正在运行的goroutine，又可以找到工作线程的局部运行队列等资源`

#### 5、全局私有变量

```
全局私有变量 工作线程与工作线程结构体对应关系
```

- 工作线程执行的代码是如何找到属于自己的那个m结构体实例对象的呢？
- 每个`工作线程在刚刚被创建出来`进入调度循环之前就利用线程本地存储机制`为该工作线程实现了一个指向m结构体实例对象的私有全局变量`
- 这样在之后的代码中就使用该全局变量来访问自己的m结构体对象以及与m相关联的p和g对象

### 4.4 重要的结构体

#### 1、g结构体

- g结构体用于代表一个goroutine，该结构体保存了goroutine的所有信息
- 包括`栈，gobuf结构体和其它的一些状态信息`

```go
// 前文所说的g结构体，它代表了一个goroutine
type g struct {
    stack       stack     // 记录该goroutine使用的栈
    m          *m      // 此goroutine正在被哪个工作线程执行
    sched       gobuf    // 保存调度信息，主要是几个寄存器的值

    // schedlink字段指向全局运行队列中的下一个g,所有位于全局运行队列中的g形成一个链表
    schedlink      guintptr
    preempt        bool   // 抢占调度标志，如果需要抢占调度，设置preempt为true
}
```

#### 2、m结构体

- m结构体用来代表`工作线程`，它保存了m自身使用的栈信息
- `当前正在运行的goroutine以及与m绑定的p等信息`

```go
type m struct {
    // g0主要用来记录工作线程使用的栈信息，在执行调度代码时需要使用这个栈
    // 执行用户goroutine代码时，使用用户goroutine自己的栈，调度时会发生栈的切换
    g0      *g

    // 通过TLS实现m结构体对象与工作线程之间的绑定
    tls           [6]uintptr   // thread-local storage (for x86 extern register)
    curg          *g         // 指向工作线程正在运行的goroutine的g结构体对象

    p            puintptr     // 记录与当前工作线程绑定的p结构体对象
    nextp         puintptr
    oldp          puintptr     // the p that was attached before executing a syscall
   
    // spinning状态：表示当前工作线程正在试图从其它工作线程的本地运行队列偷取goroutine
    spinning      bool // m is out of work and is actively looking for work
    blocked       bool // m is blocked on a note
   
    // 没有goroutine需要运行时，工作线程睡眠在这个park成员上，
    // 其它线程通过这个park唤醒该工作线程
    park          note
    // 记录所有工作线程的一个链表
    alllink       *m // on allm
    schedlink     muintptr

    // Linux平台thread的值就是操作系统线程ID
    thread        uintptr // thread handle
    freelink      *m      // on sched.freem
}
```

#### 3、p结构体

- p结构体用于`保存工作线程执行go代码时所必需的资源`，比如goroutine的运行队列，内存分配用到的缓存等等

```go
type p struct {
    lock mutex
    status       uint32 // one of pidle/prunning/...
    link            puintptr
    schedtick   uint32     // incremented on every scheduler call
    syscalltick  uint32     // incremented on every system call
    sysmontick  sysmontick // last tick observed by sysmon
    m                muintptr   // back-link to associated m (nil if idle)
    //本地goroutine运行队列
    runqhead uint32  // 队列头
    runqtail uint32     // 队列尾
    runq     [256]guintptr  //使用数组实现的循环队列
    runnext guintptr
    gFree struct {
        gList
        n int32
    }
}
```

#### 4、schedt结构体

- schedt结构体用来保存调度器的状态信息和goroutine的全局运行队列：

```go
type schedt struct {
    // accessed atomically. keep at top to ensure alignment on 32-bit systems.
    goidgen  uint64
    lastpoll uint64

    lock mutex

    // When increasing nmidle, nmidlelocked, nmsys, or nmfreed, be
    // sure to call checkdead().

    // 由空闲的工作线程组成链表
    midle        muintptr // idle m's waiting for work
    // 空闲的工作线程的数量
    nmidle       int32    // number of idle m's waiting for work
    nmidlelocked int32    // number of locked m's waiting for work
    mnext        int64    // number of m's that have been created and next M ID
    // 最多只能创建maxmcount个工作线程
    maxmcount    int32    // maximum number of m's allowed (or die)
    nmsys        int32    // number of system m's not counted for deadlock
    nmfreed      int64    // cumulative number of freed m's

    ngsys uint32 // number of system goroutines; updated atomically

    // 由空闲的p结构体对象组成的链表
    pidle      puintptr // idle p's
    // 空闲的p结构体对象的数量
    npidle     uint32
    nmspinning uint32 // See "Worker thread parking/unparking" comment in proc.go.

    // Global runnable queue.
    // goroutine全局运行队列
    runq     gQueue
    runqsize int32

    ......

    // Global cache of dead G's.
    // gFree是所有已经退出的goroutine对应的g结构体对象组成的链表
    // 用于缓存g结构体对象，避免每次创建goroutine时都重新分配内存
    gFree struct {
        lock          mutex
        stack        gList // Gs with stacks
        noStack   gList // Gs without stacks
        n              int32
    }
 
    ......
}
```

#### 5、重要的全局变量

```go
allgs     []*g     // 保存所有的g
allm       *m    // 所有的m构成的一个链表，包括下面的m0
allp       []*p    // 保存所有的p，len(allp) == gomaxprocs

ncpu             int32   // 系统中cpu核的数量，程序启动时由runtime代码初始化
gomaxprocs int32   // p的最大值，默认等于ncpu，但可以通过GOMAXPROCS修改

sched      schedt     // 调度器结构体对象，记录了调度器的工作状态

m0  m       // 代表进程的主线程
g0   g        // m0的g0，也就是m0.g0 = &g0
```