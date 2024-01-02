---
title: Go设计模式 - 简单工厂模式
index_img: /img/cover31.png
date: 2022-05-10 21:22:57
categories: 
- Go设计模式
tags:
- Go设计模式

---

# 4. 简单工厂模式

##  4.1 简单工厂模式角色和职责 

简单工厂模式并不属于GoF的23种设计模式。他是开发者自发认为的一种非常简易的设计模式，其角色和职责如下：

工厂（Factory）角色：简单工厂模式的核心，它负责实现创建所有实例的内部逻辑。工厂类可以被外界直接调用，创建所需的产品对象。

抽象产品（AbstractProduct）角色：简单工厂模式所创建的所有对象的父类，它负责描述所有实例所共有的公共接口。

具体产品（Concrete Product）角色：简单工厂模式所创建的具体实例对象。

## 4.2 简单工厂模式实现 

简单工厂方法模式的实现代码如下：

```go
package main

import "fmt"

// TODO 简单工厂模式
// ----抽象层----
type Stationery interface {
   Show()
}

// ----实现层----
type Pencil struct {
   Stationery
}

func (stationery *Pencil) Show() {
   fmt.Println("生产铅笔")
}

type Pen struct {
   Stationery
}

func (stationery *Pen) Show() {
   fmt.Println("生产钢笔")
}

// ----工厂模块----
type Factory struct {
}

func (fac *Factory) CreateStationery(kind string) Stationery {
   var sationery Stationery
   if kind == "pencil" {
      sationery = new(Pencil)
   } else if kind == "pen" {
      sationery = new(Pen)
   }
   return sationery
}

func main() {
   factory := Factory{}
   // 生产铅笔
   pencil := factory.CreateStationery("pencil")
   pencil.Show()
   // 生产钢笔
   pen := factory.CreateStationery("pen")
   pen.Show()
}
```

上述代码可以看出，业务逻辑层只会和工厂模块进行依赖，这样业务逻辑层将不再关心Stationery类是具体怎么创建基础对象的。

## 4.3 简单工厂方法模式的优缺点 

优点：

1. 实现了对象创建和使用的分离。 2. 不需要记住具体类名，记住参数即可，减少使用者记忆量。

缺点： 

1. 对工厂类职责过重，一旦不能工作，系统受到影响。 2. 增加系统中类的个数，复杂度和理解度增加。 3. 违反“开闭原则”，添加新产品需要修改工厂逻辑，工厂越来越复杂。

适用场景：

1. 工厂类负责创建的对象比较少，由于创建的对象较少，不会造成工厂方法中的业务逻辑太过复杂。 2. 客户端只知道传入工厂类的参数，对于如何创建对象并不关心。

