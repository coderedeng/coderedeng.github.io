---
title: chan读写问题
index_img: /img/cover18.png
date: 2021-02-15 22:38:41
categories: 
- Go进阶
tags:
- Go进阶

---

# 1.chan读写问题

## 01.对关闭chan读写

- golang面试题：对已经关闭的的chan进行读写，会怎么样？为什么？
- 读**已经关闭**的 `chan` 能一直读到东西，但是读到的内容根据通道内`关闭前`是否有元素而不同。
  - 1）读取有元素，且关闭的chan
    - 会正确读到 `chan` 内的值，且返回的第二个 bool 值（是否读成功）为 `true`。
  - 2）读取无元素，且关闭的chan
    - `chan` 内无值，接下来所有接收的值都会非阻塞直接成功
    - 返回 `channel` 元素的**零值**，但是第二个 `bool` 值一直为 `false`。
- 3）写**已经关闭**的 `chan` 会 `panic`

## 02.未初始化的的chan读写

- 对未初始化的的chan进行读写，会怎么样？为什么？

### 2.1 对于写的情况

- 未初始化的 `chan` 此时是等于 `nil`，当它不能阻塞的情况下，直接返回 `false`，表示写 `chan` 失败
- 当 `chan` 能阻塞的情况下，则直接阻塞 `gopark(nil, nil, waitReasonChanSendNilChan, traceEvGoStop, 2)`
- 然后调用 `throw(s string)` 抛出错误，其中 `waitReasonChanSendNilChan` 就是刚刚提到的报错 `"chan send (nil chan)"`

### 2.2 对于读的情况

- 未初始化的 `chan` 此时是等于 `nil`，当它不能阻塞的情况下，直接返回 `false`，表示读 `chan` 失败
- 当 `chan` 能阻塞的情况下，则直接阻塞 `gopark(nil, nil, waitReasonChanReceiveNilChan, traceEvGoStop, 2)`
- 然后调用 `throw(s string)` 抛出错误，其中 `waitReasonChanReceiveNilChan` 就是刚刚提到的报错 `"chan receive (nil chan)"`