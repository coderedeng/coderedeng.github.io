---
title: make和new
index_img: /img/cover22.png
date: 2021-02-08 21:21:28
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.make和new

## 01.make和new

### 1.1 make和new比较

- new 和 make 是两个内置函数，主要用来创建并分配类型的内存。
- make和new区别
  - `make` 关键字的作用是创建于 slice、map 和 channel 等内置的数据结构
  - `new` 的作用是为类型申请一片内存空间，并返回指向这片内存的指针

```go
package main
import "fmt"
func main() {
	a := make([]int, 3, 10)       // 切片长度为 1，预留空间长度为 10
	a = append(a,1)
	fmt.Printf("%v--%T \n",a,a)   // [0 0 0]--[]int   值----切片本身
	
	var b = new([]int)
	//b = b.append(b,2)          // 返回的是内存指针，所以不能直接 append
	*b = append(*b, 3)        // 必须通过 * 指针取值，才能进行 append 添加
	fmt.Printf("%v--%T",b,b)    // &[]--*[]string  内存的指针---内存指针
}
```

### 1.2 new函数

- `一：系统默认的数据类型，分配空间`

```go
package main
import "fmt"
func main() {
	// 1.new实例化int
	age := new(int)
	*age = 1

	// 2.new实例化切片
	li := new([]int)
	*li = append(*li, 1)

	// 3.实例化map
	userinfo := new(map[string]string)
	*userinfo = map[string]string{}
	(*userinfo)["username"] = "张三"
	fmt.Println(userinfo)    // &map[username:张三]
}
```

- `二：自定义类型使用 new 函数来分配空间`

```go
package main
import "fmt"

func main() {
	var s *Student
	s = new(Student)      //分配空间
	s.name ="zhangsan"
	fmt.Println(s)        // &{zhangsan 0}
}

type Student struct {
	name string
	age int
}
```

### 1.3 make函数

- make 也是用于内存分配的，但是和 new 不同，它只用于 chan、map 以及 slice 的内存创建
- 而且它返回的类型就是这三个类型本身，而不是他们的指针类型
- 因为这三种类型就是引用类型，所以就没有必要返回他们的指针了

```go
package main
import "fmt"

func main() {
	a := make([]int, 3, 10)       // 切片长度为 1，预留空间长度为 10
	b := make(map[string]string)
	c := make(chan int, 1)
	fmt.Println(a,b,c)          // [0 0 0]  map[]  0xc0000180e0
}
```

- 当我们为slice分配内存的时候，应当尽量预估到slice可能的最大长度
- 通过给make传第三个参数的方式来给slice预留好内存空间
- 这样可以避免二次分配内存带来的开销，大大提高程序的性能。