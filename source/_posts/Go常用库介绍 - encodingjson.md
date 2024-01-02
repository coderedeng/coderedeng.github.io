---
title: encodingjson
index_img: /img/cover2-3.png
date: 2022-05-24 21:11:52
categories: 
- Go常用库
tags:
- Go常用库
---

# 03.encoding/json包

## 01.struct与json

- 比如我们 Golang 要给 App 或者小程序提供 Api 接口数据，这个时候就需要涉及到结构体和Json 之间的相互转换
- **GolangJSON** 序列化是指把结构体数据转化成 JSON 格式的字符串
- **Golang** **JSON** 的反序列化是指把 JSON 数据转化成 Golang 中的结构体对象
- Golang 中 的 序 列 化 和 反 序 列 化 主 要 通 过 "encoding/json" 包 中 的 json.Marshal() 和json.Unmarshal()方法实现

### 1.1 struct转Json字符串

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {
	ID int
	Gender string
	name string     //私有属性不能被 json 包访问
	Sno string
}
func main() {
	var s1 = Student{
		ID: 1,
		Gender: "男",
		name: "李四",
		Sno: "s0001",
	}
	fmt.Printf("%#v\n", s1)  // main.Student{ID:1, Gender:"男", name:"李四", Sno:"s0001"}
	var s, _ = json.Marshal(s1)
	jsonStr := string(s)
	fmt.Println(jsonStr)   // {"ID":1,"Gender":"男","Sno":"s0001"}
}
```

### 1.2 Json字符串转struct

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {
	ID int
	Gender string
	Name string
	Sno string
}
func main() {
	var jsonStr = `{"ID":1,"Gender":"男","Name":"李四","Sno":"s0001"}`
	var student Student   //定义一个 Monster 实例
	err := json.Unmarshal([]byte(jsonStr), &student)
	if err != nil {
		fmt.Printf("unmarshal err=%v\n", err)
	}
	// 反序列化后 student=main.Student{ID:1, Gender:"男", Name:"李四", Sno:"s0001"} student.Name=李四 
	fmt.Printf("反序列化后 student=%#v student.Name=%v \n", student, student.Name)
}
```

## 02. struct tag

### 2.1 Tag标签说明

- Tag 是结构体的元信息，可以在运行的时候通过反射的机制读取出来。
- Tag 在结构体字段的后方定义，由一对反引号包裹起来
- 具体的格式如下：

```go
key1:"value1" key2:"value2"
```

1

- 结构体 tag 由一个或多个键值对组成。键与值使用冒号分隔，值用双引号括起来。
- 同一个结构体字段可以设置多个键值对 tag，不同的键值对之间使用空格分隔。
- 注意事项：
  - 为结构体编写 Tag 时，必须严格遵守键值对的规则。
  - 结构体标签的解析代码的容错能力很差，一旦格式写错，编译和运行时都不会提示任何错误，通过反射也无法正确取值。
  - 例如不要在 key 和 value 之间添加空格。

### 2.2 Tag结构体转化Json字符串

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {
	ID int `json:"id"`       //通过指定 tag 实现 json 序列化该字段时的 key
	Gender string `json:"gender"`
	Name string
	Sno string
}
func main() {
	var s1 = Student{
		ID: 1,
		Gender: "男",
		Name: "李四",
		Sno: "s0001",
	}
	// main.Student{ID:1, Gender:"男", Name:"李四", Sno:"s0001"}
	fmt.Printf("%#v\n", s1) 
	var s, _ = json.Marshal(s1)
	jsonStr := string(s)
	fmt.Println(jsonStr)  // {"id":1,"gender":"男","Name":"李四","Sno":"s0001"}
}
```

### 2.3 Json字符串转成Tag结构体

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {
	ID int `json:"id"` //通过指定 tag 实现 json 序列化该字段时的 key
	Gender string `json:"gender"`
	Name string
	Sno string
}
func main() {
	var s2 Student
	var str = `{"id":1,"gender":"男","Name":"李四","Sno":"s0001"}`
	err := json.Unmarshal([]byte(str), &s2)
	if err != nil {
		fmt.Println(err)
	}
	// main.Student{ID:1, Gender:"男", Name:"李四", Sno:"s0001"}
	fmt.Printf("%#v", s2)
}
```

### 2.4 加tag坑

- 如果变量`首字母小写`，则为`private`。无论如何`不能转`，因为取不到`反射信息`。

- 如果变量`首字母大写`，则为`public`。

- - ```
    不加tag
    ```

    ，可以正常转为

    ```
    json
    ```

    里的字段，

    ```
    json
    ```

    内字段名跟结构体内字段

    ```
    原名一致
    ```

    。

    - `加了tag`，从`struct`转`json`的时候，`json`的字段名就是`tag`里的字段名，原字段名已经没用。

```go
package main
import (
	"encoding/json"
	"fmt"
)
type J struct {
	a string          // 首字母小写，不能转换成json
	b string `json:"B"`  // 首字母小写，不能转换成json
	C string          // 不加`tag`则`json`内的字段跟结构体字段`原名一致`。
	D string `json:"dd"`  // 而`大写的`加了`tag`可以`取别名`
}
func main() {
	j := J {
		a: "1",
		b: "2",
		C: "3",
		D: "4",
	}
	fmt.Printf("转为json前j结构体的内容 = %+v\n", j)      // 转为json前j结构体的内容 = {a:1 b:2 C:3 D:4}
	jsonInfo, _ := json.Marshal(j)
	fmt.Printf("转为json后的内容 = %+v\n", string(jsonInfo))  // 转为json后的内容 = {"C":"3","dd":"4"}
}
```

- 结构体里定义了四个字段，分别对应 `小写无tag`，`小写+tag`，`大写无tag`，`大写+tag`。
- 转为`json`后首字母`小写的`不管加不加tag`都不能`转为`json`里的内容，而`大写的`加了`tag`可以`取别名`，不加`tag`则`json`内的字段跟结构体字段`原名一致`。

## 03.嵌套struct和JSON

### [#](http://v5blog.cn/pages/4c5209/#_3-1-结构化转json字符串)3.1 结构化转Json字符串

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {   //Student 学生
	ID int
	Gender string
	Name string
}
type Class struct {   //Class 班级
	Title string
	Students []Student
}
func main() {
	c := &Class{
		Title:    "001",
		Students: make([]Student, 0, 200),
	}
	for i := 0; i < 10; i++ {
		stu := Student{
			Name:   fmt.Sprintf("stu%02d", i),
			Gender: "男",
			ID:     i,
		}
		c.Students = append(c.Students, stu)
	}
	//JSON 序列化：结构体-->JSON 格式的字符串
	data, err := json.Marshal(c)
	if err != nil {
		fmt.Println("json marshal failed")
		return
	}
	fmt.Printf("json:%s\n", data)
}
/*
{
    "Title":"001",
    "Students":[
        {
            "ID":0,
            "Gender":"男",
            "Name":"stu00"
        },
        {
            "ID":1,
            "Gender":"男",
            "Name":"stu01"
        },
        {
            "ID":2,
            "Gender":"男",
            "Name":"stu02"
        },
		....
    ]
}
 */
```

### 3.2 Json字符串转结构化

```go
package main
import (
	"encoding/json"
	"fmt"
)
type Student struct {   //Student 学生
	ID int
	Gender string
	Name string
}
type Class struct {   //Class 班级
	Title string
	Students []Student
}
func main() {
	str := `{"Title":"001","Students":[{"ID":0,"Gender":"男","Name":"stu00"},{"ID":1,"Gender":"男","Name":"stu01"},{"ID":2,"Gender":"男","Name":"stu02"},{"ID":3,"Gender":"男","Name":"stu03"}]}`
	c1 := &Class{}
	err := json.Unmarshal([]byte(str), c1)
	if err != nil {
		fmt.Println("json unmarshal failed!")
		return
	}
	fmt.Printf("%#v\n", c1)
	// &main.Class{Title:"001", Students:[]main.Student{main.Student{ID:0, Gender:"男", Name:"stu00"}, main.Student{ID:1, Gender:"男", Name:"stu01"}, main.Student{ID:2, Gender:"男", Name:"stu02"}, main.Student{ID:3, Gender:"男", Name:"stu03"}}}
}
```