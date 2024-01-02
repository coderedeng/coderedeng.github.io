---
title: Time
index_img: /img/cover2-2.png
date: 2022-05-22 21:22:12
categories: 
- Go常用库
tags:
- Go常用库
---

# 02.Time

## 01.时间类型

- 我们可以通过 time.Now()函数获取当前的时间对象，然后获取时间对象的年月日时分秒等信息。
- 注意：**%02d** 中的 2 表示宽度，如果整数不够 2 列就补上 0

```go
package main
import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()   //获取当前时间
	fmt.Printf("current time:%v\n", now)
	
	year := now.Year()     //年
	month := now.Month()   //月
	day := now.Day()       //日
	hour := now.Hour()        //小时
	minute := now.Minute()     //分钟
	second := now.Second()     //秒
	
	// 打印结果为：2021-05-19 09:20:06
	fmt.Printf("%d-%02d-%02d %02d:%02d:%02d\n", year, month, day, hour, minute, second)
}
```

## 02.时间戳

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()            //获取当前时间
	timestamp1 := now.Unix()     //时间戳
	timestamp2 := now.UnixNano() //纳秒时间戳
	fmt.Printf("current timestamp1:%v\n", timestamp1)  // current timestamp1:1623560753
	fmt.Printf("current timestamp2:%v\n", timestamp2)  // current timestamp2:1623560753965606600
}
```

- 使用`time.Unix()`函数可以将时间戳转为时间格式

```go
func timestampDemo2(timestamp int64) {
	timeObj := time.Unix(timestamp, 0) //将时间戳转为时间格式
	fmt.Println(timeObj)
	year := timeObj.Year()     //年
	month := timeObj.Month()   //月
	day := timeObj.Day()       //日
	hour := timeObj.Hour()     //小时
	minute := timeObj.Minute()  //分钟
	second := timeObj.Second()  //秒
	fmt.Printf("%d-%02d-%02d %02d:%02d:%02d\n", year, month, day, hour, minute, second)
}
```

## 03.时间间隔

- `time.Duration`是`time`包定义的一个类型，它代表两个时间点之间经过的时间，以纳秒为单位。
- `time.Duration`表示一段时间间隔，可表示的最长时间段大约290年。
- time包中定义的时间间隔类型的常量如下：

```go
const (
    Nanosecond  Duration = 1
    Microsecond          = 1000 * Nanosecond
    Millisecond          = 1000 * Microsecond
    Second               = 1000 * Millisecond
    Minute               = 60 * Second
    Hour                 = 60 * Minute
)
```

## 04.时间格式化

- 时间类型有一个自带的方法`Format`进行格式化
- 需要注意的是Go语言中格式化时间模板不是常见的`Y-m-d H:M:S`
- 而是使用Go的诞生时间2006年1月2号15点04分（记忆口诀为2006 1 2 3 4）。
- 补充：如果想格式化为12小时方式，需指定`PM`。

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	// 格式化的模板为Go的出生时间2006年1月2号15点04分 Mon Jan
	// 24小时制
	fmt.Println(now.Format("2006-01-02 15:04:05.000 Mon Jan"))   // 2021-06-13 13:10:18.143 Sun Jun
	// 12小时制
	fmt.Println(now.Format("2006-01-02 03:04:05.000 PM Mon Jan"))  // 2021-06-13 01:10:18.143 PM Sun Jun
	fmt.Println(now.Format("2006/01/02 15:04"))  // 2021/06/13 13:10
	fmt.Println(now.Format("15:04 2006/01/02"))  // 13:10 2021/06/13
	fmt.Println(now.Format("2006/01/02"))        // 2021/06/13
}
```

- 解析字符串格式的时间

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	fmt.Println(now)  // 2021-06-13 13:11:29.0679475 +0800 CST m=+0.001573301
	// 加载时区
	loc, err := time.LoadLocation("Asia/Shanghai")
	if err != nil {
		fmt.Println(err)
		return
	}
	// 按照指定时区和指定格式解析字符串时间
	timeObj, err := time.ParseInLocation("2006/01/02 15:04:05", "2019/08/04 14:15:20", loc)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(timeObj)  // 2019-08-04 14:15:20 +0800 CST
	fmt.Println(timeObj.Sub(now))  // -16294h56m9.0679475s
}
```

## 05.时间操作函数

- Add
  - 我们在日常的编码过程中可能会遇到要求时间+时间间隔的需求
  - Go 语言的时间对象有提供Add 方法如下
- Sub
  - 求两个时间之间的差值

```go
package main
import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()   // 获取当前时间
	// 10分钟前
	m, _ := time.ParseDuration("-1m")
	m1 := now.Add(m)
	fmt.Println(m1)
	// 8个小时前
	h, _ := time.ParseDuration("-1h")
	h1 := now.Add(8 * h)
	fmt.Println(h1)
	// 一天前
	d, _ := time.ParseDuration("-24h")
	d1 := now.Add(d)
	fmt.Println(d1)

	// 10分钟后
	mm, _ := time.ParseDuration("1m")
	mm1 := now.Add(mm)
	fmt.Println(mm1)
	// 8小时后
	hh, _ := time.ParseDuration("1h")
	hh1 := now.Add(hh)
	fmt.Println(hh1)
	// 一天后
	dd, _ := time.ParseDuration("24h")
	dd1 := now.Add(dd)
	fmt.Println(dd1)

	// Sub 计算两个时间差
	subM := now.Sub(m1)
	fmt.Println(subM.Minutes(), "分钟")   // 1 分钟
	sumH := now.Sub(h1)
	fmt.Println(sumH.Hours(), "小时")    // 8 小时
	sumD := now.Sub(d1)
	fmt.Printf("%v 天\n", sumD.Hours()/24)   // 1 天
}
```

- Equal
  - 判断两个时间是否相同，会考虑时区的影响，因此不同时区标准的时间也可以正确比较。
  - 本方法和用t==u不同，这种方法还会比较地点和时区信息。
- Before
  - 如果t代表的时间点在u之前，返回真；否则返回假。
- After
  - 如果t代表的时间点在u之后，返回真；否则返回假。

## 06.定时器

- 使用`time.Tick(时间间隔)`来设置定时器，定时器的本质上是一个通道（channel）。

```go
func tickDemo() {
	ticker := time.Tick(time.Second) //定义一个1秒间隔的定时器
	for i := range ticker {
		fmt.Println(i)//每秒都会执行的任务
	}
}
```