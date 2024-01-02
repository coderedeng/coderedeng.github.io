---
title: Golang常犯错误
index_img: /img/cover20.png
date: 2022-04-20 22:35:42
categories: 
- Go进阶
tags:
- Go进阶

---

# 1.Golang常犯错误

## 01.01~10

### 01.nil的slice和map

- 允许对值为 nil 的 slice 添加元素，但对值为 nil 的 map 添加元素，则会造成运行时 panic。

```go
// map 错误示例
func main() {
    var m map[string]int
    m["one"] = 1  // error: panic: assignment to entry in nil map
    // m := make(map[string]int)// map 的正确声明，分配了实际的内存
}    

// slice 正确示例
func main() {
     var s []int
     s = append(s, 1)
}
```

### 02.判断map中key是否存在

- 当访问 map 中不存在的 key 时，Go 则会返回元素对应数据类型的零值，比如 nil、’’ 、false 和 0
- 取值操作总有值返回，故不能通过取出来的值，来判断 key 是不是在 map 中。
- 检查 key 是否存在可以用 map 直接访问，检查返回的第二个参数即可。

```go
// 错误的 key 检测方式
func main() {
	x := map[string]string{"one": "2", "two": "", "three": "3"}
	if v := x["two"]; v == "" {
		fmt.Println("key two is no entry") // 键 two 存不存在都会返回的空字符串
	}
}

// 正确示例
func main() {
	x := map[string]string{"one": "2", "two": "", "three": "3"}
	if _, ok := x["two"]; !ok {
		fmt.Println("key two is no entry")
	}
}
```

### 03.string值修改

- 不能，尝试使用索引遍历字符串，来更新字符串中的个别字符，是不允许的。
- string 类型的值是只读的二进制 byte slice，如果真要修改字符串中的字符
- `将 string 转为 []byte 修改后，再转为 string 即可`。

```go
// 修改字符串的错误示例
func main() {
	x := "text"
	x[0] = "T"  // error: cannot assign to x[0]
	fmt.Println(x)
}


// 修改示例
func main() {
	x := "text"
	xBytes := []byte(x)
	xBytes[0] = 'T' // 注意此时的 T 是 rune 类型
	x = string(xBytes)
	fmt.Println(x) // Text
}
```

### 04.解析JSON数字转成float64

- 在 encode/decode JSON 数据时，Go 默认会将数值当做 float64 处理。

```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
)

func main() {
     var data = []byte(`{"status": 200}`)
     var result map[string]interface{}

     if err := json.Unmarshal(data, &result); err != nil {
     	log.Fatalln(err)
     }
     fmt.Printf("%v--%T",result["status"],result["status"])  // 200--float64
}
```

- 解析出来的 200 是 float 类型。

### 05.如何从 panic 中恢复

- 在一个 defer 延迟执行的函数中调用 recover ，它便能捕捉/中断 panic。

```go
// 错误的 recover 调用示例
func main() {
	recover() // 什么都不会捕捉
	panic("not good") // 发生 panic，主程序退出
	recover() // 不会被执行
	println("ok")
}

// 正确的 recover 调用示例
func main() {
	defer func() {
		fmt.Println("recovered: ", recover())
	}()
	panic("not good")
}
```

### 06.避免Goroutine泄露

- 可以通过 context 包来避免内存泄漏。

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())

    ch := func(ctx context.Context) <-chan int {
        ch := make(chan int)
        go func() {
            for i := 0; ; i++ {
                select {
                case <- ctx.Done():
                    return
                case ch <- i:
                }
            }
        } ()
        return ch
    }(ctx)

    for v := range ch {
        fmt.Println(v)
        if v == 5 {
            cancel()
            break
        }
    }
}
```

- 下面的 for 循环停止取数据时，就用 cancel 函数，让另一个协程停止写数据。
- 如果下面 for 已停止读取数据，上面 for 循环还在写入，就会造成内存泄漏。

### 07.跳出for select 循环

- 通常在for循环中，使用break可以跳出循环
- 但是注意在go语言中，for select配合时，break 并不能跳出循环。

```go
func testSelectFor2(chExit chan bool){
 EXIT:
    for  {
        select {
        case v, ok := <-chExit:
            if !ok {
                fmt.Println("close channel 2", v)
                break EXIT//goto EXIT2
            }
            fmt.Println("ch2 val =", v)
        }
    }

    //EXIT2:
    fmt.Println("exit testSelectFor2")
}
```

### 08.嵌套结构初始化

- go 的哲学是组合优于继承，使用 struct 嵌套即可完成组合，内嵌的结构体属性就像外层结构的属性即可，可以直接调用。
- 注意初始化外层结构体时，必须指定内嵌结构体名称的结构体初始化，如下看到 s1方式报错，s2 方式正确。

```go
type stPeople struct {
    Gender bool
    Name string
}

type stStudent struct {
    stPeople
    Class int
}

//尝试4 嵌套结构的初始化表达式
//var s1 = stStudent{false, "JimWen", 3}
var s2 = stStudent{stPeople{false, "JimWen"}, 3}
fmt.Println(s2.Gender, s2.Name, s2.Class)
```

### 09.defer触发顺序

```go
func main() {
     defer_call()
}

func defer_call() {
    defer func() { fmt.Println("打印前") }()
    defer func() { fmt.Println("打印中") }()
    defer func() { fmt.Println("打印后") }()
    panic("触发异常")
}
```

- 看下答案，输出：

```text
打印后
打印中
打印前
panic: 触发异常
```

- 参考解析：defer 的执行顺序是后进先出。当出现 panic 语句的时候，会先按照 defer 的后进先出的顺序执行，最后才会执行panic

### 10.for循环&val取值错误

```go
func main() {
     slice := []int{0,1,2,3}
     m := make(map[int]*int)
     for key,val := range slice {
         m[key] = &val
     }
    for k,v := range m {
        fmt.Println(k,"->",*v)
    }
}
```

- 直接给答案：

```text
0 -> 3
1 -> 3
2 -> 3
3 -> 3
```

- 参考解析：
  - 这是新手常会犯的错误写法，for range 循环的时候会创建每个元素的副本，而不是元素的引用
  - 所以 m[key] = &val 取的都是变量 val 的地址，所以最后 map 中的所有元素的值都是变量 val 的地址
  - 因为最后 val 被赋值为3，所有输出都是3
- 正确的写法:

```go
func main() {
     slice := []int{0,1,2,3}
     m := make(map[int]*int)
    
     for key,val := range slice {
         value := val
         m[key] = &value
     }

    for k,v := range m {
        fmt.Println(k,"===>",*v)
    }
}
```

### 11.切片append错误

```go
// 1.
 func main() {
     s := make([]int, 5)
     s = append(s, 1, 2, 3)
     fmt.Println(s)
 }

// 2.
 func main() {
    s := make([]int,0)
    s = append(s,1,2,3,4)
    fmt.Println(s)
}
```

- 两段代码分别输出：

```text
[0 0 0 0 0 1 2 3]
[1 2 3 4]
```

- 参考解析：这道题考的是使用 append 向 slice 添加元素，第一段代码常见的错误是 [1 2 3]，需要注意。

## 02.11~20

### 12.new()返回指针

```go
func main() {
    list := new([]int)
    list = append(list, 1)
    fmt.Println(list)
}
```

- 参考答案及解析：
  - 不能通过编译，new([]int) 之后的 list 是一个 `*[]int` 类型的指针，不能对指针执行 append 操作。
  - 可以使用 make() 初始化之后再用。
  - 同样的，map 和 channel 建议使用 make() 或字面量的方式初始化，不要用 new() 。

### 13. :=赋值只能在函数内部使用

```go
package main
// myvar := 1   // error
var myvar = 1   // ok

func main() {  
}
```

- :=赋值不会影响外层函数值

```go
package main
import "fmt"
func main() {
	x := 1
	fmt.Println(x)       //prints 1
	{
		fmt.Println(x)   //prints 1
		x := 2           // 不会影响到外部x变量的值
		fmt.Println(x)   //prints 2
		//x = 5         // 要想修改x的值，必须使用这种语法赋值
	}
	fmt.Println(x)      //prints 1
}
```

### 14.数组用于函数传参时是值复制

- 注意：方法或函数调用时，传入参数都是值复制（跟赋值一致）
- 除非是`map、slice、channel、指针类型` 这些特殊类型是引用传递

```go
package main
import "fmt"
func main()  {
	x := [3]int{1,2,3}
	test01(x)
	fmt.Println(x)     // [1 2 3]
}

// 数组在函数中传参是值复制
func test01(arr [3]int) {
	arr[0] = 7
	fmt.Println(arr)    //prints [7 2 3]
}
```

### 15.defer打印顺序

```go
package main

 import (
     "fmt"
 )

 func main() {
     defer_call()
 }

func defer_call() {
    defer func() { fmt.Println("打印前") }()
    defer func() { fmt.Println("打印中") }()
    defer func() { fmt.Println("打印后") }()
    panic("触发异常")
}
/*
    打印后
    打印中
    打印前
    panic: 触发异常
*/
```

- 当出现 panic 语句的时候，会先按照 defer 的后进先出的顺序执行，最后才会执行panic