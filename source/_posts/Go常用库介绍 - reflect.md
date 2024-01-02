---
title: reflect
index_img: /img/cover2-11.png
date: 2022-06-05 22:14:35
categories: 
- Go常用库
tags:
- Go常用库
---

# 10.reflect

## 01.反射

- `反射是指在程序运行期对程序本身进行访问和修改的能力`

### 1.1 变量的内在机制

- 变量包含类型信息和值信息 var arr [10]int arr[0] = 10
- 类型信息：是静态的元信息，是预先定义好的
- 值信息：是程序运行过程中动态改变的

### 1.2 反射的使用

- 反射是指`在程序运行期对程序本身进行访问和修改的能力`。
- 程序在编译时，变量被转换为内存地址，变量名不会被编译器写入到可执行部分。
- 在运行程序时，程序无法获取自身的信息。
- 支持反射的语言可以在程序编译期将变量的反射信息，如字段名称、类型信息、结构体信息等整合到可执行文件中
- 并给程序提供接口访问反射信息，这样就可以在程序运行期获取类型的反射信息，并且有能力修改它们。
- Go程序在运行期使用reflect包访问程序的反射信息。

## 02.反射方法

- `反射可以在运行时动态获取程序的各种详细信息`

### 2.1 TypeOf

- `reflect.TypeOf()`获取`类型信息`

```go
package main
import (
"fmt"
"reflect"
)

func reflectType(x interface{}) {
	v := reflect.TypeOf(x)
	fmt.Printf("type:%v\n", v)
}
func main() {
	var a float32 = 3.14
	reflectType(a) // type:float32
	var b int64 = 100
	reflectType(b) // type:int64
}
```

### 2.2 ValueOf

- `reflect.Value`获取值
- `reflect.Value`类型提供的获取原始值的方法如下

|           方法           |                             说明                             |
| :----------------------: | :----------------------------------------------------------: |
| Interface() interface {} | 将值以 interface{} 类型返回，可以通过类型断言转换为指定类型  |
|       Int() int64        |     将值以 int 类型返回，所有有符号整型均可以此方式返回      |
|      Uint() uint64       |     将值以 uint 类型返回，所有无符号整型均可以此方式返回     |
|     Float() float64      | 将值以双精度（float64）类型返回，所有浮点数（float32、float64）均可以此方式返回 |
|       Bool() bool        |                     将值以 bool 类型返回                     |
|     Bytes() []bytes      |               将值以字节数组 []bytes 类型返回                |
|     String() string      |                     将值以字符串类型返回                     |

```go
package main
import (
    "fmt"
    "reflect"
)

func reflectValue(x interface{}) {
	v := reflect.ValueOf(x)
	k := v.Kind()
	switch k {
	case reflect.Int64:
		// v.Int()从反射中获取整型的原始值，然后通过int64()强制类型转换
		fmt.Printf("type is int64, value is %d\n", int64(v.Int()))
	case reflect.Float32:
		// v.Float()从反射中获取浮点型的原始值，然后通过float32()强制类型转换
		fmt.Printf("type is float32, value is %f\n", float32(v.Float()))
	case reflect.Float64:
		// v.Float()从反射中获取浮点型的原始值，然后通过float64()强制类型转换
		fmt.Printf("type is float64, value is %f\n", float64(v.Float()))
	}
}
func main() {
	var a float32 = 3.14
	var b int64 = 100
	reflectValue(a) // type is float32, value is 3.140000
	reflectValue(b) // type is int64, value is 100
	// 将int类型的原始值转换为reflect.Value类型
	c := reflect.ValueOf(10)
	fmt.Printf("type c :%T\n", c) // type c :reflect.Value
}
```

### 2.3 修改值

- 想要在函数中通过反射修改变量的值，需要注意函数参数传递的是值拷贝，必须传递变量地址才能修改变量值。
- 而反射中使用专有的`Elem()`方法来获取指针对应的值。

```go
package main
import (
	"fmt"
	"reflect"
)

func reflectSetValue1(x interface{}) {
	v := reflect.ValueOf(x)
	if v.Kind() == reflect.Int64 {
		v.SetInt(200) //修改的是副本，reflect包会引发panic
	}
}
func reflectSetValue2(x interface{}) {
	v := reflect.ValueOf(x)
	// 反射中使用 Elem()方法获取指针对应的值
	if v.Elem().Kind() == reflect.Int64 {
		v.Elem().SetInt(200)
	}
}
func main() {
	var a int64 = 100
	// reflectSetValue1(a) //panic: reflect: reflect.Value.SetInt using unaddressable value
	reflectSetValue2(&a)
	fmt.Println(a)
}
```

### 2.4 isNil()和isValid()

- isNil()

  - `IsNil()`报告v持有的值是否为nil。
  - v持有的值的分类必须是通道、函数、接口、映射、指针、切片之一；
  - 否则IsNil函数会导致panic。

- isValid()

  - `IsValid()`返回v是否持有一个值。
  - 如果v是Value零值会返回假，此时v除了IsValid、String、Kind之外的方法都会导致panic。

- `IsNil()`常被用于判断指针是否为空；`IsValid()`常被用于判定返回值是否有效。

  ```go
  func main() {
  	// *int类型空指针
  	var a *int
  	fmt.Println("var a *int IsNil:", reflect.ValueOf(a).IsNil())
  	// nil值
  	fmt.Println("nil IsValid:", reflect.ValueOf(nil).IsValid())
  	// 实例化一个匿名结构体
  	b := struct{}{}
  	// 尝试从结构体中查找"abc"字段
  	fmt.Println("不存在的结构体成员:", reflect.ValueOf(b).FieldByName("abc").IsValid())
  	// 尝试从结构体中查找"abc"方法
  	fmt.Println("不存在的结构体方法:", reflect.ValueOf(b).MethodByName("abc").IsValid())
  	// map
  	c := map[string]int{}
  	// 尝试从map中查找一个不存在的键
  	fmt.Println("map中不存在的键：", reflect.ValueOf(c).MapIndex(reflect.ValueOf("娜扎")).IsValid())
  }
  ```

## 03.结构体与反射

### 3.1 查看类型、字段和方法

```go
package main

import (
    "fmt"
    "reflect"
)

// 定义结构体
type User struct {
    Id   int
    Name string
    Age  int
}

// 绑方法
func (u User) Hello() {
    fmt.Println("Hello")
}

// 传入interface{}
func Poni(o interface{}) {
    t := reflect.TypeOf(o)
    fmt.Println("类型：", t)
    fmt.Println("字符串类型：", t.Name())
    // 获取值
    v := reflect.ValueOf(o)
    fmt.Println(v)
    // 可以获取所有属性
    // 获取结构体字段个数：t.NumField()
    for i := 0; i < t.NumField(); i++ {
        // 取每个字段
        f := t.Field(i)
        fmt.Printf("%s : %v", f.Name, f.Type)
        // 获取字段的值信息
        // Interface()：获取字段对应的值
        val := v.Field(i).Interface()
        fmt.Println("val :", val)
    }
    fmt.Println("=================方法====================")
    for i := 0; i < t.NumMethod(); i++ {
        m := t.Method(i)
        fmt.Println(m.Name)
        fmt.Println(m.Type)
    }

}

func main() {
    u := User{1, "zs", 20}
    Poni(u)
}
```

### 3.2 查看匿名字段

```go
package main

import (
    "fmt"
    "reflect"
)

// 定义结构体
type User struct {
    Id   int
    Name string
    Age  int
}

// 匿名字段
type Boy struct {
    User
    Addr string
}

func main() {
    m := Boy{User{1, "zs", 20}, "bj"}
    t := reflect.TypeOf(m)
    fmt.Println(t)
    // Anonymous：匿名
    fmt.Printf("%#v\n", t.Field(0))
    // 值信息
    fmt.Printf("%#v\n", reflect.ValueOf(m).Field(0))
}
```

### 3.3 修改结构体的值

```go
package main

import (
    "fmt"
    "reflect"
)

// 定义结构体
type User struct {
    Id   int
    Name string
    Age  int
}

// 修改结构体值
func SetValue(o interface{}) {
    v := reflect.ValueOf(o)
    // 获取指针指向的元素
    v = v.Elem()
    // 取字段
    f := v.FieldByName("Name")
    if f.Kind() == reflect.String {
        f.SetString("kuteng")
    }
}

func main() {
    u := User{1, "5lmh.com", 20}
    SetValue(&u)
    fmt.Println(u)
}
```

### 3.4 调用方法

```go
package main

import (
    "fmt"
    "reflect"
)

// 定义结构体
type User struct {
    Id   int
    Name string
    Age  int
}

func (u User) Hello(name string) {
    fmt.Println("Hello：", name)
}

func main() {
    u := User{1, "5lmh.com", 20}
    v := reflect.ValueOf(u)
    // 获取方法
    m := v.MethodByName("Hello")
    // 构建一些参数
    args := []reflect.Value{reflect.ValueOf("6666")}
    // 没参数的情况下：var args2 []reflect.Value
    // 调用方法，需要传入方法的参数
    m.Call(args)
}
```

### 3.5 获取字段的tag

```go
package main

import (
    "fmt"
    "reflect"
)

type Student struct {
    Name string `json:"name1" db:"name2"`
}

func main() {
    var s Student
    v := reflect.ValueOf(&s)
    // 类型
    t := v.Type()
    // 获取字段
    f := t.Elem().Field(0)
    fmt.Println(f.Tag.Get("json"))
    fmt.Println(f.Tag.Get("db"))
}
```

## 04.反射练习

- 任务：解析如下配置文件
  - 序列化：将结构体序列化为配置文件数据并保存到硬盘
  - 反序列化：将配置文件内容反序列化到程序的结构体
- 配置文件有server和mysql相关配置

```text
#this is comment
;this a comment
;[]表示一个section
[server]
ip = 10.238.2.2
port = 8080

[mysql]
username = root
passwd = admin
database = test
host = 192.168.10.10
port = 8000
timeout = 1.2
```
