---
title: Strconv
index_img: /img/cover2-7.png
date: 2022-05-31 22:24:31
categories: 
- Go常用库
tags:
- Go常用库
---

# 07.Strconv

## 01.string与int类型转换

### 1.0 strconv包介绍

- strconv包实现了基本数据类型与其字符串表示的转换
- 主要有以下常用函数： Atoi()、Itia()、parse系列、format系列、append系列。
- 更多函数请查看[官方文档 (opens new window)](https://golang.org/pkg/strconv/)。

### 1.1 Atoi()转int

- `Atoi()`函数用于将字符串类型的整数转换为int类型，函数签名如下。

```go
package main
import (
	"fmt"
	"strconv"
)

func main() {
    s1 := "100"
    i1, err := strconv.Atoi(s1)
    if err != nil {
        fmt.Println("can't convert to int")
    } else {
        fmt.Printf("type:%T value:%#v\n", i1, i1) //type:int value:100
    }
}
```

### 1.2 Itoa()转str

- `Itoa()`函数用于将int类型数据转换为对应的字符串表示

```go
package main
import (
	"fmt"
	"strconv"
)

func main() {
	i2 := 200
	s2 := strconv.Itoa(i2)
	fmt.Printf("type:%T value:%#v\n", s2, s2) //type:string value:"200"
}
```

### 1.3 string转字符

```go
package main
import (
	"fmt"
)
func main() {
	s := "hello 张三"
	for _, r := range s { //rune
		// 104(h) 101(e) 108(l) 108(l) 111(o) 32( ) 24352(张) 19977(三) 
		fmt.Printf("%v(%c) ", r, r)
	}
	fmt.Println()
}
```

## 02.Parse系列函数

### 1.1 ParseInt()

```go
package main
import (
	"fmt"
	"strconv"
)
func main() {
	var s = "1234"
	i64, _ := strconv.ParseInt(s, 10, 64)
	fmt.Printf("值：%v 类型：%T", i64, i64)  // 值：1234 类型：int64
}
```

### 1.2 ParseFloat()

```go
package main
import (
	"fmt"
	"strconv"
)
func main() {
	str := "3.1415926535"
	v1, _ := strconv.ParseFloat(str, 32)
	v2, _ := strconv.ParseFloat(str, 64)
	fmt.Printf("值：%v 类型：%T\n", v1, v1)  // 值：3.1415927410125732 类型：float64
	fmt.Printf("值：%v 类型：%T", v2, v2)  // 值：3.1415926535 类型：float64
}
```

### 1.3 ParseBool()

```go
package main
import (
	"fmt"
	"strconv"
)
func main() {
	b, _ := strconv.ParseBool("true")   // string 转 bool
	fmt.Printf("值：%v 类型：%T", b, b)  // 值：true 类型：bool
}
```

## 03.Format系列函数

- Format系列函数实现了将给定类型数据格式化为string类型数据的功能

```go
package main
import (
	"fmt"
	"strconv"
)

func main() {
	s1 := strconv.FormatBool(true)
	s2 := strconv.FormatFloat(3.1415, 'E', -1, 64)
	s3 := strconv.FormatInt(-2, 16)
	s4 := strconv.FormatUint(2, 16)
	fmt.Printf("%v --%T \n", s1, s1)  // true --string 
	fmt.Printf("%v --%T \n", s2, s2)  // 3.1415E+00 --string 
	fmt.Printf("%v --%T \n", s3, s3)  // -2 --string
	fmt.Printf("%v --%T \n", s4, s4)  // 2 --string 
}
```
