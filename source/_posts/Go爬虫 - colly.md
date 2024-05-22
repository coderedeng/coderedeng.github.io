---
title: colly
index_img: /img/cover36.png
date: 2024-04-30 20:12:11
categories: 
- Go爬虫
tags:
- Go爬虫


---

Colly 是 Go 语言中一个功能强大的爬虫库，它被设计用于简化 Web 页面的抓取和数据提取过程。下面是关于 Colly 的一些主要特点和用法：

1. **简单易用**：Colly 提供了一个简洁的 API，使得编写爬虫变得非常容易。你可以很容易地定义需要爬取的网站的规则，并提取感兴趣的数据。
2. **灵活的规则定义**：你可以定义多个规则来匹配不同类型的网页，并在每个规则中指定需要采取的操作，例如提取数据或者跟踪链接。
3. **并发支持**：Colly 内置了对并发的支持，可以同时爬取多个页面，从而提高爬取效率。
4. **中间件**：Colly 提供了中间件机制，允许你在请求发送、响应接收等各个阶段添加自定义逻辑，从而灵活地扩展爬虫的功能。
5. **内置的数据提取工具**：Colly 提供了一些方便的工具函数，用于从 HTML 页面中提取数据，例如使用 CSS 选择器或者 XPath。
6. **可扩展性**：Colly 的设计非常灵活，你可以根据自己的需求轻松地扩展和定制功能。

以下是一个爬取微博热搜的示例代码：

```go
package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/gocolly/colly/v2"
	"github.com/gocolly/colly/v2/extensions"
)

// 获取微博热搜榜colly
func main() {
	c := colly.NewCollector()
	extensions.RandomUserAgent(c)

	c.OnRequest(func(r *colly.Request) {
        // 向请求头添加 cookie 防止进入访客模式
		r.Headers.Add("cookie", "SUB=_2AkMRY4uTf8NxqwFRmfsdxWLna410ygHEieKnP3pIJRMxHRl-yT9kqkAvtRB6OuOlexrgRHkeY_A2VqgX2CcV_p0455qS; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhOnHVoAxngUau7LDxX9KO_; _s_tentry=passport.weibo.com; Apache=6010347679488.02.1715406001552; SINAGLOBAL=6010347679488.02.1715406001552; ULV=17154060015601116010347679488.02.1715406001552")
	})
	
    // 解析热搜页面HTML结构，获取相应热搜内容
	c.OnHTML(".data table tbody", func(e *colly.HTMLElement) {
        startTime := time.Now()
		e.ForEach("tr", func(i int, tr *colly.HTMLElement) {
			if i != 0 { // 去除第一个官方宣传内容
				str := tr.Text
				str1 := strings.ReplaceAll(str, " ", "")
				str2 := strings.ReplaceAll(str1, "\n", " ")

				if !strings.Contains(str2, "•") { // 根据•标记去除相应的广告
					fmt.Printf("%+v\n", str2)
				}

			}
		})
         timeConsum := time.Since(startTime) // 计算时间耗时
		fmt.Println("总耗时:", timeConsum)
	})

	err := c.Visit("https://s.weibo.com/top/summary/")
	if err != nil {
		log.Fatalln(err)
		return
	}

}

```

