---
title: interface
index_img: /img/cover21.png
date: 2021-02-05 22:15:27
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.interface

## 01.interface

### 1.1 interface作用

- 接口是 Go 语言的重要组成部分，它在 Go 语言中通过一组方法指定了一个对象的行为

- 接口 interface 的引入能够让我们在 Go 语言更好地组织并写出易于测试的代码

- golang中的接口分为

  ```
  带方法的接口和空接口
  ```

  - iface：表示带方法的接口
  - eface：表示空接口

### 1.2 eface空接口

- 空接口eface结构比较简单，由两个属性构成
- 一个是`类型信息_type`，一个是`数据信息`
- 其数据结构声明如下：

```go
type eface struct {
  _type *_type
  data  unsafe.Pointer
}
```

![img](/img/image-20210602153422706.ccbddf01.png)

- 其中_type是GO语言中所有类型的公共描述，Go语言几乎所有的数据结构都可以抽象成 _type，是所有类型的公共描述
- **type负责决定data应该如何解释和操作**
- type的结构代码如下:

```go
type _type struct {
  size       uintptr 
  ptrdata    uintptr    // size of memory prefix holding all pointers
  hash       uint32     // 类型哈希
  tflag      tflag
  align      uint8      // _type作为整体变量存放时的对齐字节数
  fieldalign uint8
  kind       uint8
  alg        *typeAlg
  // gcdata stores the GC type data for the garbage collector.
  // If the KindGCProg bit is set in kind, gcdata is a GC program.
  // Otherwise it is a ptrmask bitmap. See mbitmap.go for details.
  gcdata    *byte
  str       nameOff
  ptrToThis typeOff  // type for pointer to this type, may be zero
}
```

- data表示指向具体的实例数据，由于Go的参数传递规则为值传递
- 如果希望可以通过interface对实例数据修改，则需要传入指针
- 此时data指向的是指针的副本，但指针指向的实例地址不变，仍然可以对实例数据产生修改。

### 1.3 iface带方法的接口

- iface 表示带方法的数据结构，非空接口初始化的过程就是初始化一个iface类型的结构
- 其中data的作用同eface的相同，这里不再多加描述。

```go
type iface struct {
  tab  *itab
  data unsafe.Pointer
}
```

![img](/img/image-20210602155153963.8ea13138.png)

- iface结构中最重要的是itab结构（结构如下），每一个 `itab` 都占 32 字节的空间
- itab可以理解为pair<interface type, concrete type>
- itab里面包含了interface的一些关键信息，比如method的具体实现

```go
type itab struct {
  inter  *interfacetype      // 接口自身的元信息
  _type  *_type           // 具体类型的元信息
  link   *itab
  bad    int32
  hash   int32           // _type里也有一个同样的hash，此处多放一个是为了方便运行接口断言
  fun    [1]uintptr        // 函数指针，指向具体类型所实现的方法
}

// interface type包含了一些关于interface本身的信息，比如package path，包含的method
type interfacetype struct {
  typ     _type
  pkgpath name
  mhdr    []imethod
}

type imethod struct {      //这里的 method 只是一种函数声明的抽象，比如  func Print() error
  name nameOff
  ityp typeOff
}
```

### 1.4 interface设计的优缺点

- 优点，非侵入式设计，写起来更自由，无需显式实现，只要实现了与 interface 所包含的所有函数签名相同的方法即可。
- 缺点，duck-typing风格并不关注接口的规则和含义，也没法检查，不确定某个struct具体实现了哪些interface。
- 只能通过goru工具查看。