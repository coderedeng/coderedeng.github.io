---
title: 字符串
index_img: /img/cover17.png
date: 2021-01-20 21:25:14
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.字符串

## 01.字符串底层

### 1.1 字符串底层结构

- 一个字符串是一个不可改变的字节序列，字符串通常是用来包含人类可读的文本数据。
- 和数组不同的是，字符串的元素不可修改，`是一个只读的字节数组`。
- 每个字符串的长度虽然也是固定的，但是字符串的长度并不是字符串类型的一部分。
- Go语言字符串的底层结构在 reflect.StringHeader 中定义

```go
type StringHeader struct {
	Data uintptr
	Len int
}
```

- 字符串结构由两个信息组成
  - 第一个是字符串指向的底层字节数组
  - 第二个是字符串的字节的长度
- 而slice 包含一个数据指针、一个长度和一个容量，当容量不够时会重新申请新的内存，Data 指针将指向新的地址，原来的地址空间将被释放
- 字符串其实是一个结构体，因此字符串的赋值操作也就是 reflect.StringHeader 结构体的复制过程，并不会涉及底层字节数组的复制。
- 我们可以看看字符串“Hello, world”本身对应的内存结构：

![img](/img/image-20210601140428459.2bc7c2a5.png)

- 字符串虽然不是切片，但是支持切片操作，不同位置的切片底层也访问的同一块内存数据
- 因为字符串是只读的，相同的字符串通常是对应同一个字符串常量

### 1.2 reflect.StringHeader

- 字符串和数组类似，内置的 len 函数返回字符串的长度。
- 也可以通过 reflect.StringHeader 结构访问字符串的长度

```go
package main
import (
	"fmt"
	"reflect"
	"unsafe"
)

func main() {
	a :="aaa"
	// 1.unsafe.Pointer(&a)方法可以得到变量a的地址
	fmt.Println(unsafe.Pointer(&a))  // 0xc000054240

	// 2.(*reflect.StringHeader)(unsafe.Pointer(&a)) 可以把字符串a转成底层结构的形式。
	b := (*reflect.StringHeader)(unsafe.Pointer(&a)).Len
	fmt.Println(b)  // 3

	// 3.(*[]byte)(unsafe.Pointer(&ssh)) 可以把ssh底层结构体转成byte的切片的指针
	// 4.再通过 *转为指针指向的实际内容
	ssh := *(*reflect.StringHeader)(unsafe.Pointer(&a))
	c := *(*[]byte)(unsafe.Pointer(&ssh))
	fmt.Printf("%v",c)  // [97 97 97]
}
```

### 1.3 修改字符串

- 要修改字符串，需要先将其转换成[]rune 或[]byte，完成后再转换为 string。
- 无论哪种转换，都会重新分配内存，并复制字节数组。

```go
package main
import "fmt"
func main() {
	s1 := "big"
	// 强制类型转换
	byteS1 := []byte(s1)
	byteS1[0] = 'p'
	fmt.Println(string(byteS1))  // pig

	s2 := "白萝卜"
	runeS2 := []rune(s2)
	runeS2[0] = '红'
	fmt.Println(string(runeS2))  // 红萝卜
}
```

### 1.4 字符串反转

- `rune`关键字，从golang源码中看出，它是int32的别名（-2^31 ~ 2^31-1），比起byte（-128～127），**可表示更多的字符**。
- 由于rune可表示的范围更大，所以能处理一切字符，当然也包括**中文字符**。在平时计算中文字符，可用rune。
- 因此将`字符串`转为`rune的切片`，再进行翻转，完美解决。

```go
package main
import"fmt"

func main() {
	src := "2012年的第一场雪！"
	fmt.Println([]rune(src))   // [50 48 49 50 24180 30340 31532 19968 22330 38634 65281]
	fmt.Println(string([]rune(src)))   // []rune(src)
	
	dst := reverse([]rune(src))
	fmt.Printf("%v\n", string(dst))  // ！雪场一第的年2102
}

func reverse(s []rune) []rune {
	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
	return s
}
```