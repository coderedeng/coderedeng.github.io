---
title: 深浅拷贝
index_img: /img/cover14.png
date: 2021-02-12 22:24:10
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.深浅拷贝

## 01.深浅拷贝

### 1.1 深浅拷贝定义

- 浅拷贝就是只拷贝指针的值，指针指向的内容只有一份。
- 而深拷贝是把指针指向的值拷贝一份。
- golang里面也有浅拷贝和深拷贝。
- slice的浅拷贝就是指slice变量的赋值操作。
- slice的深拷贝就是指使用内置的copy函数来拷贝两个slice。

### 1.2 深浅拷贝代码举例

```go
package main
import "fmt"

func main() {
	SliceShallowCopy()
	SliceDeepCopy()
}

func SliceShallowCopy() {
	src := []byte {1,2,3,4,5,6}
	dst := src
	fmt.Println("浅拷贝原始数据",src)   // [1 2 3 4 5 6]
	dst[0]=10
	// 修改拷贝数据，原始数据会以前跟着改变
	fmt.Println("after modify[src]:",src)  // [10 2 3 4 5 6]
}

func SliceDeepCopy() {
	src := []byte {1,2,3,4,5,6}
	var dst = make([]byte, len(src))
	copy(dst[:], src)
	fmt.Println("深拷贝前:",src)   // [1 2 3 4 5 6]
	dst[0]=10
	fmt.Println("深拷贝修改拷贝数据值后:",src)   // [1 2 3 4 5 6]
}
```