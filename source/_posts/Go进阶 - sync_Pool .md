---
title: sync_Pool
index_img: /img/cover26.png
date: 2021-02-21 21:19:10
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.sync.Pool

## 01.sync.Pool介绍

### 1.1 是什么

- `sync.Pool` 是 sync 包下的一个组件，可以作为保存临时取还对象的一个“池子”。
- 个人觉得它的名字有一定的误导性，因为 Pool 里装的对象可以被无通知地被回收，可能 `sync.Cache` 是一个更合适的名字。
- `Pool` 结构体的定义为：
  - `Pool` 中有两个定义的公共方法，分别是 `Put` - 向池中添加元素；
  - `Get` 从池中获取元素，如果没有，则调用 `New` 生成元素，如果 `New` 未设置，则返回 `nil`。

```text
type Pool struct {
   noCopy noCopy

   local     unsafe.Pointer // 本地P缓存池指针
   localSize uintptr        // 本地P缓存池大小

   // 当池中没有可能对象时
   // 会调用 New 函数构造构造一个对象
   New func() interface{}
}
```

### 1.2 有什么用

- 对于很多需要重复分配、回收内存的地方，`sync.Pool` 是一个很好的选择。
- 频繁地分配、回收内存会给 GC 带来一定的负担，严重的时候会引起 CPU 的毛刺
- 而 `sync.Pool` 可以将暂时不用的对象缓存起来，待下次需要的时候直接使用，不用再次经过内存分配
- 复用对象的内存，减轻 GC 的压力，提升系统的性能。

### 1.3 怎么用

- 首先，`sync.Pool` 是协程安全的，这对于使用者来说是极其方便的。
- 使用前，设置好对象的 `New` 函数，用于在 `Pool` 里没有缓存的对象时，创建一个。
- 之后，在程序的任何地方、任何时候仅通过 `Get()`、`Put()` 方法就可以取、还对象了。

```go
package main
import (
	"fmt"
	"sync"
)

var pool *sync.Pool

type Person struct {
	Name string
}

func initPool() {
	pool = &sync.Pool {
		New: func() interface{} {
			fmt.Println("Creating a new Person")
			return new(Person)
		},
	}
}

func main() {
	initPool()

	p := pool.Get().(*Person)   // get获取不到就会调用方法，创建一个
	p.Name = "first"

	pool.Put(p)  // 使用 Put方法将对象放回 pool池子中

	fmt.Println("Pool 里已有一个对象：&{first}，调用 Get: ", pool.Get().(*Person))
	fmt.Println("Pool 没有对象了，调用 Get: ", pool.Get().(*Person))  // 获取后再次获取就没有了,会再次创建
}
/*
Creating a new Person
Pool 里已有一个对象：&{first}，调用 Get:  &{first}
Creating a new Person
Pool 没有对象了，调用 Get:  &{}
 */
```

### 1.4 Get

- `Pool` 会为每个 `P` 维护一个本地池，`P` 的本地池分为 私有池 `private` 和共享池 `shared`。
- 私有池中的元素只能本地 `P` 使用，共享池中的元素可能会被其他 `P` 偷走
- 所以使用私有池 `private` 时不用加锁，而使用共享池 `shared` 时需加锁。
- `Get` 会优先查找本地 `private`，再查找本地 `shared`，最后查找其他 `P` 的 `shared`
- 如果以上全部没有可用元素，最后会调用 `New` 函数获取新元素。

### 1.5 PUT

- `Put` 优先把元素放在 `private` 池中；
- 如果 `private` 不为空，则放在 `shared` 池中
- 有趣的是，在入池之前，该元素有 1/4 可能被丢掉。

## 02.gin中的Context pool

- 在 `web` 应用中，后台在处理用户的每条请求时都会为当前请求创建一个上下文环境 `Context`，用于存储请求信息及相应信息等。
- `Context` 满足长生命周期的特点，且用户请求也是属于并发环境，所以对于线程安全的 `Pool` 非常适合用来维护 `Context` 的临时对象池。
- `Gin` 在结构体 `Engine` 中定义了一个 `pool`:

```go
type Engine struct {
   // ... 省略了其他字段
   pool             sync.Pool
}
```

- 初始化 `engine` 时定义了 `pool` 的 `New` 函数：

```go
engine.pool.New = func() interface{} {
   return engine.allocateContext()
}

// allocateContext
func (engine *Engine) allocateContext() *Context {
   // 构造新的上下文对象
   return &Context{engine: engine}
}
```

- ServeHttp

```go
// 从 pool 中获取，并转化为 *Context
c := engine.pool.Get().(*Context)
c.writermem.reset(w)
c.Request = req
c.reset()  // reset

engine.handleHTTPRequest(c)

// 再扔回 pool 中
engine.pool.Put(c)
```