---
title: 使用 net/http 实现并发爬取多个 url 标题
index_img: /img/cover37.png
date: 2024-04-30 21:26:38
categories: 
- Go爬虫
tags:
- Go爬虫
---

# 1. net/http 包相关方法

## 1.1 `http.NewRequestWithContext`

```go
req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
```

- 这个方法用于创建一个新的 HTTP 请求。
- 它接受一个 `context.Context` 对象，可以用来设置请求的超时、取消等操作。
- 第一个参数是 HTTP 方法，这里是 "GET"。
- 第二个参数是要请求的 URL。
- 第三个参数是请求体，这里传入 `nil` 表示没有请求体。
- 返回一个 `*http.Request` 对象和错误对象。

## 1.2 `Request` 结构体类型

```go
type Request struct {
   Method string // 指定HTTP方法（GET，POST，PUT等）。
   URL *url.URL
   ......
}
```

## 1.3 `http.DefaultClient.Do`

```go
resp, err := http.DefaultClient.Do(req)
```

- `http.DefaultClient` 是一个全局的 `*http.Client` 对象，它提供了默认的 HTTP 客户端实现。
- `Do` 方法用于发送 HTTP 请求并返回响应。
- 它接受一个 `*http.Request` 对象作为参数，表示要发送的请求。
- 返回一个 `*http.Response` 对象和一个错误对象。

## 1.4 `Response` 结构体类型

```go
type Response struct {
  Status   string // e.g. "200 OK"
  StatusCode int   // e.g. 200
  Proto    string // e.g. "HTTP/1.0"
  ProtoMajor int   // e.g. 1
  ProtoMinor int   // e.g. 0
  ......
}
```

## 1.5 `http.Response`

- `http.Response` 结构表示 HTTP 响应。
- 它包含响应状态码、响应头和响应体等信息。
- 在代码中，我们使用 `resp.StatusCode` 来检查响应的状态码是否为200，以确定请求是否成功。

## 1.6 `http.Response.Body`

```go
defer resp.Body.Close()
```

- `Body` 字段是一个 `io.ReadCloser` 接口，代表响应体。
- 在读取完响应体后，我们应该关闭响应体以释放资源。通常使用 `defer` 关键字来确保在函数退出时关闭响应体。

# 2. ` golang.org/x/net/html` 包相关方法

## 2.1 `html.Parse`

- `func Parse(r io.Reader) (*Node, error)`
- 此函数接受一个实现了 `io.Reader` 接口的对象作为参数，通常是一个 `http.Response.Body` 或文件等。
- 返回一个 `*html.Node` 对象和一个 `error`，表示解析的根节点以及可能发生的错误。

## 2.2 `html.Render`

- `func Render(w io.Writer, n *Node) error`
- 此函数接受一个实现了 `io.Writer` 接口的对象以及一个 `*html.Node` 对象作为参数，将HTML节点 n 以HTML格式写入 w。
- 返回一个 `error`，表示可能发生的写入错误。

## 2.3 `html.ParseFragment`

- `func ParseFragment(r io.Reader, context *Node) ([]*Node, error)`
- 此函数接受一个实现了 `io.Reader` 接口的对象以及一个上下文节点 `*html.Node` 对象作为参数。
- 返回解析的HTML片段中的节点切片和一个 `error`。

## 2.4 `html.EscapeString`

- `func EscapeString(s string) string`
- 此函数接受一个HTML字符串作为参数，返回其在HTML中的转义形式。

## 2.5 `html.UnescapeString`

- `func UnescapeString(s string) string`
- 此函数接受一个转义过的HTML字符串作为参数，返回其原始形式。

## 2.6 `html.Node`

- HTML文档中的节点表示。
- 每个节点都有一个类型、一系列属性和子节点。
- 可以通过 `Type` 字段来判断节点的类型，如 `ElementNode`、`TextNode` 等。
- 可以通过 `Data` 字段获取节点的数据，如元素节点的标签名或文本节点的内容。
- 可以通过 `Attr` 字段获取节点的属性。

# 3. 具体实现代码

```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"

	"golang.org/x/net/html"
)

// fetchTitle 使用给定的URL获取网站的标题。
func fetchTitle(ctx context.Context, url string) (string, error) {
	startTime := time.Now()
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return "", err
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("bad status: %s", resp.Status)
	}

	doc, err := html.Parse(resp.Body)
	if err != nil {
		return "", err
	}

	var title string
	var f func(*html.Node)
	f = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "title" && n.FirstChild != nil {
			title = n.FirstChild.Data
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			f(c)
		}
	}
	f(doc)

	elapsedTime := time.Since(startTime).Round(time.Millisecond)
	return title + " (" + elapsedTime.String() + ")", nil
}

// crawlURLs 并发地爬取一系列URL的标题。
func crawlURLs(ctx context.Context, urls []string) ([]string, error) {
	// 使用WaitGroup等待所有的goroutine完成
	var wg sync.WaitGroup
	wg.Add(len(urls))

	// 使用通道来收集结果(防止结果竟态)
	titles := make(chan string, len(urls))
    
	for _, url := range urls {
        // 每一个url创建一个goroutine
		go func(url string) {
			defer wg.Done()
			title, err := fetchTitle(ctx, url)
			if err != nil {
				fmt.Printf("Error fetching %s: %v\n", url, err)
				titles <- "Error: " + err.Error()
				return
			}
			// 将标题发送到通道
			titles <- title
		}(url)
	}

	// 等待所有的goroutine完成
	wg.Wait()
	close(titles)

	// 将通道的结果收集到数组中
	resultTitles := make([]string, 0, len(urls))
	for title := range titles {
		resultTitles = append(resultTitles, title)
	}

	return resultTitles, nil
}

func main() {
	urls := []string{
		"https://www.baidu.com",
		"https://www.36kr.com",
		"https://www.sina.com.cn",
		"https://www.jd.com",
		"https://www.taobao.com",
		"https://www.pinduoduo.com",
		"https://www.tmall.com",
		"https://www.zhihu.com",
		"http://www.juejin.cn",
		"https://www.aliyun.com",
	}

	// 创建一个上下文，例如，用于设置超时
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	titles, err := crawlURLs(ctx, urls)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	for i, title := range titles {
		fmt.Printf("%d: %s\n", i+1, title)
	}
}

```

