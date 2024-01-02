---
title: sync.Map
index_img: /img/cover27.png
date: 2021-02-22 21:54:21
categories: 
- Go进阶
tags:
- Go进阶
---

# 1.sync.map

## 01.sync.Map介绍

### 1.1 sync.Map介绍

- 简单说：空间换时间+读写分离+原子操作(快路径)

- sync.Map 的主要思想就是读写分离，空间换时间

  。

  - sync.Map底层使用了两个原生**map**，一个叫read，仅用于读；
  - 一个叫dirty，用于在特定情况下存储最新写入的key-value数据

### 1.2 sync.Map特点

- 1、空间换时间：通过冗余的两个Map数据结构(read、dirty)，实现加锁对性能的影响。
- 2、使用只读数据(read)，避免读写冲突。
- 3、动态调整，miss次数多了之后，将dirty数据迁移到read中。
- 4、double-checking。
- 5、迟删除。 删除一个键值只是打标记，只有在迁移dirty数据的时候才清理删除的数据。
- 6、优先从read读取、更新、删除，因为对read的读取不需要锁。

### 1.3 sync.Map结构体

```go
type Map struct {
    // 当涉及到脏数据(dirty)操作时候，需要使用这个锁
    mu Mutex

    // 后面是readOnly结构体，依靠map实现，仅仅只用来读
    read atomic.Value // readOnly

    // 这个map主要用来写的，部分时候也承担读的能力
    dirty map[interface{}]*entry

    // 记录自从上次更新了read之后，从read读取key失败的次数
    misses int
}
```

- readOnly

```go
// readOnly is an immutable struct stored atomically in the Map.read field.
type readOnly struct {
    // m包含所有只读数据，不会进行任何的数据增加和删除操作 
    // 但是可以修改entry的指针因为这个不会导致map的元素移动
    m       map[interface{}]*entry
    
    // 标志位，如果为true则表明当前read只读map的数据不完整，dirty map中包含部分数据
    amended bool // true if the dirty map contains some key not in m.
}
```

## 02.sync.Map操作

![img](/img/image-20220331102352849.979847b4.png)

### 2.1 新增数据

- 1、key原先就存在于read中，获取key所对应内存地址，原子性修改
- 2、key存在，但是key所对应的值被标记为 expunged，解锁，解除标记，并更新dirty中的key，与read中进行同步，然后修改key对应的值
- 3、read中没有key，但是dirty中存在这个key，直接修改dirty中key的值
- 4、read和dirty中都没有值，先判断自从read上次同步dirty的内容后有没有再修改过dirty的内容，没有的话，先同步read和dirty的值，然后添加新的key value到dirty上面

### 2.2 删除数据

- 1、read中没有，且Map存在修改，则尝试删除dirty中的map中的key
- 2、read中没有，且Map不存在修改，那就是没有这个key，无需操作
- 3、read中有，尝试将key对应的值设置为nil，后面读取的时候就知道被删了，
  - `因为dirty中map的值跟read的map中的值指向的都是同一个地址空间，所以，修改了read也就是修改了dirty`

### 2.3 遍历（Range）

- 遍历的逻辑就比较简单了，Map只有两种状态，被修改过和没有修改过
- 修改过：将dirty的指针交给read，read就是最新的数据了，然后遍历read的map
- 没有修改过：遍历read的map就好了