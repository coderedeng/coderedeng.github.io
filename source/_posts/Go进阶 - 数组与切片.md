---
title: 数组与切片
index_img: /img/cover15.png
date: 2021-01-25 22:10:18
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.数组与切片

## 01.数组

### 1.1 数组

- 数组是一种非常有用的数据结构，因为其占用的内存是连续分配的。
- 由于内存连续，CPU能把正在使用的数据缓存更久的时间。
- 而且内存连续很容易计算索引，可以快速迭代数组里的所有元素。
- golang中声明数组需要告诉数组长度，以及存放数据类型
- 一旦初始化成功，那么存储的数据类型和数组长度就都不能改变了
- xxxxxxxxxx package mainimport "fmt"​func main() {    SliceShallowCopy()    SliceDeepCopy()}​func SliceShallowCopy() {    src := []byte {1,2,3,4,5,6}    dst := src    fmt.Println("浅拷贝原始数据",src)   // [1 2 3 4 5 6]    dst[0]=10    // 修改拷贝数据，原始数据会以前跟着改变    fmt.Println("after modify[src]:",src)  // [10 2 3 4 5 6]}​func SliceDeepCopy() {    src := []byte {1,2,3,4,5,6}    var dst = make([]byte, len(src))    copy(dst[:], src)    fmt.Println("深拷贝前:",src)   // [1 2 3 4 5 6]    dst[0]=10    fmt.Println("深拷贝修改拷贝数据值后:",src)   // [1 2 3 4 5 6]}go

### 1.2 引用类型

- golang 的引用类型包括 slice、map、channel、function、pointer 等.
- 它们在进行赋值时拷贝的是指针值，但拷贝后指针指向的地址是相同的.

## 02.切片的内部实现

- 切片是一种数据结构，这种数据结构便于使用和管理数据集合。
- 切片是围绕动态数组的概念构建的，可以按需自动增长和缩小。
- 切片的动态增长是通过内置函数 append 来实现的，这个函数可以快速且高效地增长切片。
- 还可以通过对切片再次切片来缩小一个切片的大小。
- 因为切片的底层内存也是在连续块中分配的，所以切片还能获得索引、迭代以及为垃圾回收优化的好处。

![img](/img/image-20210601155555698.78a455d2.png)