---
title: Channel
index_img: /img/cover19.png
date: 2021-01-30 21:26:15
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.channel

## 01.channel的整体结构图

### 1.1 channel结构图

- channel本质是一个`hchan`这个结构体

```go
type hchan struct {
    buf      unsafe.Pointer // points to an array of dataqsiz elements
    sendx    uint   // send index
    recvx    uint   // receive index
    recvq    waitq  // list of recv waiters
    sendq    waitq  // list of send waiters
    lock mutex
}
```

- 简单说明：

  - `buf`是有缓冲的channel所特有的结构，用来存储缓存数据，`是个循环链表`

  - ```
    sendx
    ```

    和

    ```
    recvx
    ```

    用于记录

    ```
    buf
    ```

    这个循环链表中的~发送或者接收的~index

    - `recvx`和`sendx`是根据循环链表`buf`的变动而改变的

  - `lock`是个互斥锁，发送或接收前都需要加锁

  - ```
    recvq
    ```

    和

    ```
    sendq
    ```

     

    —>

     

    ```
    是个双向链表
    ```

    - 分别是接收或者发送的goroutine抽象出来的结构体(sudog)的队列

![img](/img/image-20210602090848795.72979bb7.png)

### 1.2 创建channel

- 创建channel实际上就是在内存中实例化了一个`hchan`的结构体，并返回一个ch指针
- 我们使用过程中channel在函数之间的传递都是用的这个指针
- 这就是为什么函数传递中无需使用channel的指针，而直接用channel就行了，因为channel本身就是一个指针

### 1.3 channel中队列如何实现

- channel中有个缓存buf，是用来缓存数据的(假如实例化了带缓存的channel的话)队列。
- 当使用`send (ch <- xx)`或者`recv ( <-ch)`的时候，首先要锁住`hchan`这个结构体
- 然后开始`send (ch <- xx)`数据，这时候满了，队列塞不进去了
- 然后是取`recv ( <-ch)`的过程，是个逆向的操作，也是需要加锁

![img](/img/mebkj3h2za.b21725dd.gif)

### 1.4 channel缓存满发生什么

- 使用的时候，我们都知道，当channel缓存满了，或者没有缓存的时候
- 我们继续send(ch <- xxx)或者recv(<- ch)会阻塞当前goroutine，但是，是如何实现的呢？
- Go的goroutine是用户态的线程(`user-space threads`)，用户态的线程是需要自己去调度的
- Go有运行时的scheduler去帮我们完成调度这件事情