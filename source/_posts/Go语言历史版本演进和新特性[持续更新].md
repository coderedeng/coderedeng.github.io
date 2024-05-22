---
title: Go语言历史版本演进和新特性[持续更新]
index_img: /img/cover35.png
date: 2024-04-10 21:34:11
sticky: true
categories: 
- Go基础
tags:
- Go基础
---

发布总览：[Release History - The Go Programming Language](https://go.dev/doc/devel/release)

## GO 1.22 新特性

发布时间：2024-02-06

官方说明：[Go 1.22 Release Notes - The Go Programming Language](https://go.dev/doc/go1.22)

- 循环变量改进：Go 1.22解决了for循环中循环变量在迭代之间意外共享的问题。在新的版本中，for循环中的循环变量（如for range语句中的变量）将不再在整个循环中共享，而是在每次迭代中都有自己的变量。这意味着在goroutine中使用循环变量时，每个goroutine将捕获其迭代的变量，而不是共享同一个变量。这一变化可能会对现有代码的行为产生影响，因此Go团队提供了一个工具来检测代码中可能因此特性变化而产生问题的地方。

- range支持整型表达式：在Go 1.22中，for range循环的range表达式除了支持传统的数组、切片、map、channel等类型外，还支持整型表达式。这意味着你可以在for range循环中使用整型值，循环将基于该整型值进行迭代。

- 性能提升：Go 1.22在运行时进行了内存优化，提高了CPU性能（约1-3%），并减少了大多数Go程序的内存开销（约1%）。此外，Go 1.21引入的profile-guided optimization（PGO）功能在1.22版本中得到了进一步改进，包括改进的devirtualization，允许更多的接口方法调用进行静态调度，从而提高了程序性能。

- 标准库新增内容：

  - 引入了一个新的`math/rand/v2`包，提供更清晰、更一致的API，并使用更高质量、更快的伪随机生成算法。
  - `net/http.ServeMux`的 patterns 现在接受方法和通配符，例如可以匹配仅限GET请求的`GET /task/{id}/`模式。
  - `database/sql`包中新增了一个`Null[T]`类型，用于扫描可为空的列。
  - 在`slices`包中添加了一个`Concat`函数，用于连接任意类型的多个切片。

- 工具链：

  在Go工具链改善方面，首当其冲的要数go module相关工具了。

  在Go 1.22中，go work增加了一个与go mod一致的特性：支持vendor。通过go work vendor，可以将workspace中的依赖放到vendor目录下，同时在构建时，如果module root下有vendor目录，那么默认的构建是go build -mod=vendor，即基于vendor的构建。

  go mod init在Go 1.22中将不再考虑GOPATH时代的包依赖工具的配置文件了，比如Gopkg.lock。在Go 1.22版本之前，如果go module之前使用的是类似[dep这样的工具来管理包依赖](https://tonybai.com/2017/06/08/first-glimpse-of-dep/)，go mod init会尝试读取dep配置文件来生成go.mod。

  go vet工具取消了对loop变量引用的警告，增加了对空append的行为的警告(比如：slice = append(slice))、增加了deferring time.Since的警告以及在log/slog包的方法调用时key-value pair不匹配的警告。

## GO 1.21 新特性

发布时间：2023.08.08

官方说明：[Go 1.21 Release Notes - The Go Programming Language](https://go.dev/doc/go1.21)

特性：

go1.21.1（发布于 2023 年 9 月 6 日）包括对`cmd/go`、`crypto/tls`和`html/template`包的四个安全修复，以及对编译器、`go`命令、链接器、运行时和`context`、`crypto/tls`、`encoding/gob`、`encoding/xml`、`go/types`、`net/http`、`os`和 的错误修复`path/filepath`包。

go1.21.2（2023 年 10 月 5 日发布）包括对包的一项安全修复`cmd/go`，以及对编译器、`go`命令、链接器、运行时和包的错误修复`runtime/metrics`。 

go1.21.3（2023 年 10 月 10 日发布）包含对该`net/http`软件包的安全修复。



## GO 1.20 新特性

发布时间：2023.02.01

官方说明：[Go 1.20 Release Notes - The Go Programming Language](https://go.dev/doc/go1.20)



特性：

- 支持将slice直接转为数组
- Comparable类型可比较
- unsafe包添加`Slice`，`SliceData`，`String`，`StringData 4个函数`
- 可移植性：Go 1.20将会成为支持macOS 10.13 High Sierra和10.14 Mojave的最后一个版本。
- Go 1.20增加了对于RISC-V架构在FreeBSD操作系统的实验性支持
- PGO引入
- 标准库加强
  - 新增了几个 时间转换格式常量
  - 新包 crypto/ecdh 支持通过 NIST 曲线和 Curve25519 椭圆曲线 Diffie-Hellman 密钥交换
  - 新类型 http.ResponseController 访问 http.ResponseWriter 接口未处理的扩展请求
  - httputil.ReverseProxy 包含一个新的 Rewrite 钩子函数，取代了之前的 Director 钩子
  - 新方法 context.WithCancelCause 提供了一种方法来取消具有给定错误的上下文
  - os/exec.Cmd 结构体中的新字段 Cancel 和 WaitDelay, 指定 Cmd 在其关联的 Context 被取消或其进程退出时的回调
- 工具链
  - cover 工具可以收集整个程序的覆盖率，不仅仅是单元测试
  - go build、go install 和其他与构建相关的命令可以接收一个 -pgo 标志，启用配置文件引导优化，以及一个 -cover 标志，用于整个程序覆盖率分析
  - go test -json 的实现已得到改进，可以处理复杂多样的 Stdout 输出
  - vet 在并行运行的测试中可能会发生更多循环变量引用错误
  - 在没有 C 工具链 的系统上默认禁用 CGO
- 性能提升
  - [编译器](https://so.csdn.net/so/search?q=编译器&spm=1001.2101.3001.7020)和 GC 的优化减少了内存开销，并将 CPU 性能整体提高了 2%
  - 针对编译时间进行了优化，提升了 10%。使得构建速度与 Go 1.17 保持一致 (恢复到了泛型之前的速度)
  - Go 发行版瘦身，新版本起，Go 的 $GOROOT/pkg 目录将不再存储标准库的预编译包存档，Go 发行版的将迎来一轮瘦身

## GO 1.19 新特性

时间：2022.05

官方说明：[Go 1.19 Release Notes - The Go Programming Language](https://go.dev/doc/go1.19)

主要特性：

- 泛型问题fix
- 修订Go memory model:对Go memory model做了更正式的整体描述，增加了对multiword竞态、runtime.SetFinalizer、更多sync类型、atomic操作以及编译器优化方面的描述。
- 修订go doc comment格式：增加了对超链、列表、标题、标准库API引用等格式支持
- 新增runtime.SetMemoryLimit和GOMEMLIMIT环境变量：避免Go程序因分配heap过多，超出系统内存资源限制而被kill，默认memory limit是math.MaxInt64，limit限制的是go runtime掌控的内存总量，对于开发者自行从os申请的内存(比如通过mmap)则不予考虑。
- 启动时将默认提高打开文件的限值：对于导入os包的go程序，Go将在1.19中默认提高这些限制值到hard limit。
- race detector将升级到v3版thread sanitizer：race detector性能相对于上一版将提升1.5倍-2倍，内存开销减半，并且没有对goroutine的数量的上限限制
- 增加"unix" build tag：//go:build unix
- 标准库net包使用EDNS
- 标准库flag包增加TextVar函数
- 正式支持64位龙芯cpu架构 (GOOS=linux, GOARCH=loong64)
- 当Go程序空闲时，Go GC进入到周期性的GC循环的情况下(2分钟一次)，Go运行时现在会在idle的操作系统线程上安排更少的GC worker goroutine，减少空闲时Go应用对os资源的占用。
- Go行时将根据goroutine的历史平均栈使用率来分配初始goroutine栈，避免了一些goroutine的最多2倍的goroutine栈空间浪费。
- sync/atomic包增加了新的高级原子类型Bool, Int32, Int64, Uint32, Uint64, Uintptr和Pointer，提升了使用体验。
- Go编译器使用jump table重新实现了针对大整型数和string类型的switch语句，平均性能提升20%左右。
- 等

## Go 1.18 新特性

时间：2022.03

官方说明：[Go 1.18 Release Notes - The Go Programming Language](https://go.dev/doc/go1.18)

主要特性：

- 泛型支持
- Workspaces 工作区
- Go编译器与Go module变化：修正的语法bug，在AMD64平台上引入architectural level，为ARM64架构带来高达 20% 的 CPU 性能改进：但由于编译器中与支持泛型有关的变化，Go 1.18 的编译速度可能比Go 1.17的编译速度大约慢15%。编译后的代码的执行时间不受影响。打算在Go 1.19中提高编译器的速度。Go 1.18明确了能修改go.mod、go.sum的命令只有三个：go get、go mod tidy和go mod download。
- go fuzzing test：将fuzz testing纳入了go test工具链，与单元测试、性能基准测试等一起成为了Go原生测试工具链中的重要成员，单元测试函数名样式：FuzzXxx
- go get 不再执行编译和安装工作
- gofmt支持并发
- 内置函数Append对切片的扩容算法发生变化：和Go 1.17以1024作为大小分界不同，Go 1.18使用256作为threshold
- 新增net/netip包
- tls client默认将使用TLS 1.2版本
- crypto/x509包默认将拒绝使用SHA-1哈希函数签名的证书（自签发的除外）
- strings包和bytes包新增Cut函数
- runtime/pprof精确性提升
- sync包新增Mutex.TryLock、RWMutex.TryLock和RWMutex.TryRLock
- 等

## Go 1.17 新特性

时间：2021.08

官方说明：[Go 1.17 Release Notes - The Go Programming Language](https://go.dev/doc/go1.17)

主要特性：

- 从切片到数组指针的转换： []T 类型的表达式 s 现在可以转换为数组指针类型 *[N]T
- go modules 支持“修剪模块图”（Pruned module graphs）：go mod tidy -go=1.17
- 编译器带来了额外的改进：即一种传递函数参数和结果的新方法，程序性能提高了约 5%，amd64 平台的二进制大小减少了约 2%。
- unsafe包新增了`unsafe.Add`和`unsafe.Slice`
- `go.mod 中添加 // Deprecated: 注释来弃用模块`
- net包：

1. url参数解析增加对“;”的支持变化（原先 example?a=1;b=2&c=3 会解析成 `map[a:[1] b:[2] c:[3]]`, 现在解析成`map[c:[3]]`）
2. 增加 IP.IsPrivate 判断私有 IP
3. a.b.c.d 格式的 ip v4 地址不允许每段有前缀 0（因为某些系统会认为前缀 0 表示 8进制）
4. 等

## Go 1.16 新特性

时间：2021.02

官方说明：[Go 1.16 Release Notes - The Go Programming Language](https://go.dev/doc/go1.17)

主要特性：

- GO111MODULE 默认为 on
- 支持编译阶段将静态资源文件打包进编译好的程序中，并提供访问这些文件的能力：//go:embed

## Go 1.15 新特性

时间：2020.08

官方说明：[Go 1.15 Release Notes - The Go Programming Language](https://go.dev/doc/go1.16)

主要特性：

- 改进了对高核心数的小对象的分配
- 编译器/汇编器/链接器的优化:二进制大小减少了约 5%，减少了链接器资源的使用（时间和内存）并提高了代码的稳健性/可维护性。
- 内置了time/tzdata包：允许将时区数据库嵌入到程序中
- 等

## Go 1.14 新特性

时间：2020.02

官方说明：[Go 1.14 Release Notes - The Go Programming Language](https://go.dev/doc/go1.15)

主要特性：

- Go Module已可用于生产使用
- 嵌入具有重叠方法集的接口
- 改进了defer的性能
- goroutines 异步可抢占
- 页面分配器更高效
- 内部定时器更高效
- 等

## Go 1.13 新特性

时间：2019.09

官方说明：[Go 1.13 Release Notes - The Go Programming Language](https://go.dev/doc/go1.14)

主要特性：

- 优化sync.Pool

sync 包的 Pool 组件得到改进，得其中的资源不会在垃圾回收时被清除(通过新机制里引入的缓存，两次垃圾回收之间没有被使用过的实例才会被清除)

- 重了逃逸分析逻辑，使得 Go 程序减少了堆上的分配次数
- go 命令默认使用 Go module mirror and Go checksum database下载和验证模块
- 对数字文字的改进
- 错误换行
- 默认开启 TLS 1.3
- 等

## Go 1.12 新特性

时间：2019.02

官方说明：[Go 1.12 Release Notes - The Go Programming Language](https://go.dev/doc/go1.13)

主要特性：

- 改进了Go modules
- 在[analysis包](https://link.juejin.cn/?target=https%3A%2F%2Fpkg.go.dev%2Fgolang.org%2Fx%2Ftools%2Fgo%2Fanalysis)基础上重写了 go vet 命令
- 等

## Go 1.11 新特性

时间：2018.08

官方说明：[Go 1.11 Release Notes - The Go Programming Language](https://go.dev/doc/go1.12)

主要特性：

- Go modules

## Go 1.10 新特性

时间：2018.02

官方说明：[Go 1.10 Release Notes - The Go Programming Language](https://go.dev/doc/go1.12)

主要特性：

- go test with cache：go test命令可以缓存测试结果
- go build 命令会缓存最近构建过的包，从而加快了构建过程
- 明确预声明类型(predeclared type)是defined type还是alias type
- 移除spec中对method expression: T.m中T的类型的限制
- 默认的GOROOT
- 增加GOTMPDIR变量
- 通过cache实现增量构建，提高go tools性能
- go tool pprof做了一个较大的改变：增加了Web UI
- 标准库新增strings.Builder
- 标准库bytes包的几个方法Fields, FieldsFunc, Split和SplitAfter在底层实现上有变化，使得外部展现的行为有所变化
- 等

## Go 1.9 新特性

时间：2017.08

官方说明：[Go 1.9 Release Notes - The Go Programming Language](https://go.dev/doc/go1.10)

主要特性：

- 提升了垃圾收集器和编译器
- 增加了类型别名
- 新增了sync.Map
- time包更加安全
- testing包新增helper方法
- 支持渐进式代码重构
- 引入了类型别名并提升了运行时和工具支持

## Go 1.8 新特性

时间：2017.02

官方说明：[Go 1.8 Release Notes - The Go Programming Language](https://go.dev/doc/go1.9)

主要特性：

- 优化编译

CPU 时间在 32 位 ARM 系统上减少了 20-30%, 还针对 64 位 x86 系统进行了一些适度的性能改进。编译器和[链接器](https://so.csdn.net/so/search?q=链接器&spm=1001.2101.3001.7020)变得更快。

编译时间应该比 Go 1.7 改进了大约 15%



Go 1.7中进入标准库的context，提供了取消和超时机制。

Go 1.8 让标准库中更多package使用(支持)context，包括 database/sql，net 包， net/http 包中的 Server.Shutdown等



- 对垃圾回收器改进，使两次垃圾回收的暂停时间减小到了毫秒级
- 同时识别了剩余仍未解决的暂停模式，并在下一个版本中得到修复。修复后，通常情况下暂停时间能控制在 100 微秒左右,甚至能低至 10 微秒。
- 改进了 defer 函数
- 部分标准库使用context包来改造
- sort 包中新添加的 Slice 函数，对切片进行排序变得比之前简单得多

## Go 1.7 新特性

时间：2016.08

官方说明：[Go 1.7 Release Notes - The Go Programming Language](https://go.dev/doc/go1.8)

主要特性：

- context包转正
- 编译时间显着加快：二进制文件大小减少了 20-30%, CPU 时间减少了 5-35%
- 垃圾收集器的加速和标准库的优化
- go tool trace改进

## Go 1.6 新特性

时间：2016.02

官方说明：[Go 1.6 Release Notes - The Go Programming Language](https://go.dev/doc/go1.7)

主要特性：

- 增加对于 HTTP/2 协议的默认支持
- 再一次降低了垃圾回收器的延迟
- runtime改变了打印程序结束恐慌的方式。现在只打印发生panic的 goroutine 的堆栈，而不是所有现有的 goroutine
- 默认启用vendor目录
- sort.Sort 内部的算法进行了改进，运行速度提高了约 10%

## Go 1.5 新特性

时间：2015.08

官方说明：[Go 1.5 Release Notes - The Go Programming Language](https://go.dev/doc/go1.6)

主要特性：

- [垃圾回收器](https://link.juejin.cn/?target=https%3A%2F%2Fgo.dev%2Fdoc%2Fgo1.5%23gc)被完全重新设计实现： 基于并发的回收期，GC延迟显著降低，来自Twitter生产案例从300ms下降到30ms
- 调度程序的相关改进允许将默认的 GOMAXPROCS 值（并发执行的 goroutine 的数量）从 1 更改为逻辑 CPU 的数量。在以前的版本中，默认值为 1
- go tool trace：可以在运行时可视化跟踪程序，追踪信息可在测试或运行期间生成，展示在浏览器窗口中
- map语法的更改：由于疏忽，允许从slice literals中省略元素类型的规则未应用于map。在1.5版本得到了修正，以下两种定义map的方式从1.5及之后都可以（即可以省略Point的类型）



## Go 1.4 新特性

时间：2014.02

官方说明：[Go 1.4 Release Notes - The Go Programming Language](https://go.dev/doc/go1.5)

主要特性：

- For-range loops支持新语法

  1234567891011121314151617

  package mainimport “fmt”func main() { sli := []string{“shandong”, “zhejiang”, “guangdong”, “jiangsu”} for k, v := range sli { fmt.Println(“k-v:”, k, v) //go 1.3及之前的For-range loops } for range sli { fmt.Println(“从1.4开始这种写法是可以通过编译的”) }}

- Android 的官方支持包[golang.org/x/mobile](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fgolang%2Fmobile)随该版本一同发布，使开发者可以仅用 Go 代码编写简单的 Android 应用。

- 之前用 C 和汇编语言编写的大多数运行时已转换为用 Go 语言实现 && 使用了更精准的垃圾收集器，堆栈大小减少了 10~30%

- 发布 go generate 命令，此命令会扫描//go:generate 指令提供的信息生成代码，简化了代码生成的方式。 [Generating code](https://link.juejin.cn/?target=https%3A%2F%2Fgo.dev%2Fblog%2Fgenerate)

- 引入了Internal包

Go 的项目代码管理工具从 Mercurial 切换为 Git，与此同时，项目也从 Google Code 迁移到了 Github 上

## Go 1.3 新特性

时间：2014.06

官方说明：[Go 1.3 Release Notes - The Go Programming Language](https://go.dev/doc/go1.4)

主要特性：

- 堆栈管理得到了重要改善
- 发布了 sync 包的 Pool 组件
- 改进了[channel的实现](https://link.juejin.cn/?target=https%3A%2F%2Fdocs.google.com%2Fdocument%2Fd%2F1yIAYmbvL3JxOKOjuCyon7JhW4cSv1wy5hC0ApeGMV9s%2Fpub)，提升了性能

## Go 1.2 新特性

时间：2013.12

官方说明：[Go 1.2 Release Notes - The Go Programming Language](https://go.dev/doc/go1.3)

主要特性：

- [Three-index slices](https://link.juejin.cn/?target=https%3A%2F%2Fgo.dev%2Fdoc%2Fgo1.2%23three_index)
- go test 命令支持代码覆盖率报告，并提供新的 `go tool cover` 命令输出代码测试覆盖率的统计信息. [The cover story](https://link.juejin.cn/?target=https%3A%2F%2Fgo.dev%2Fblog%2Fcover)

## Go 1.1 新特性

时间：2013.05

官方说明：[Go 1.1 Release Notes - The Go Programming Language](https://go.dev/doc/go1.2)

主要特性：

-  增强语言特性（编译器、垃圾回收机制、映射、goroutine 调度器）与性能。

## Go 1.0 新特性

时间：2012.03

官方说明：[Go 1 Release Notes - The Go Programming Language](https://go.dev/doc/go1)

主要特性：

-  承诺兼容性，确保向后兼容 [Go 1 and the Future of Go Programs - The Go Programming Language](https://go.dev/doc/go1compat)

本文转自 https://blog.csdn.net/mdpets/article/details/127663206，如有侵权，请联系删除。