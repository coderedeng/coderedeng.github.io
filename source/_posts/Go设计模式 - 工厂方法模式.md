---
title: Go设计模式 - 工厂方法模式
index_img: /img/cover32.png
date: 2022-05-15 21:28:35
categories: 
- Go设计模式
tags:
- Go设计模式

---

# 5. 工厂方法模式

##  5.1  工厂方法模式中的角色和职责

**抽象工厂（Abstract Factory）角色**：工厂方法模式的核心，任何工厂类都必须实现这个接口。

**工厂（Concrete Factory）角色**：具体工厂类是抽象工厂的一个实现，负责实例化产品对象。

**抽象产品（Abstract Product）角色**：工厂方法模式所创建的所有对象的父类，它负责描述所有实例所共有的公共接口。	

**具体产品（Concrete Product）角色**：工厂方法模式所创建的具体实例对象。

## 5.2 工厂方法模式的实现 

工厂方法模式的实现代码如下：

```go
package main

import "fmt"

// TODO 工厂模式
// ----抽象层----
// 文具类
type AbstractStationery interface {
	Show()
}

// 工厂类
type AbstractFactory interface {
	CreateStationery() AbstractStationery // 生产文具的（抽象）类方法
}

// ----实现层----
type ActualPencil struct {
	AbstractStationery // 实际的铅笔继承抽象的文具
}

func (stationery *ActualPencil) Show() {
	fmt.Println("生产铅笔")
}

type ActualPen struct {
	AbstractStationery // 实际的钢笔继承抽象的文具
}

func (stationery *ActualPen) Show() {
	fmt.Println("生产钢笔")
}

// ----工厂模块----
// 铅笔工厂
type PencilFactory struct {
	AbstractFactory // 实际的铅笔工厂继承抽象的工厂
}

func (pencil *PencilFactory) CreateStationery() AbstractStationery {
	return &ActualPencil{} // 返回实际的铅笔
}

// 钢笔工厂
type PenFactory struct {
	AbstractFactory // 实际的钢笔工厂继承抽象的工厂
}

func (pen *PenFactory) CreateStationery() AbstractStationery {
	return &ActualPen{} // 返回实际的钢笔
}

func main() {
	// 生产铅笔
	pencilFactory := new(PencilFactory)
	pencil := pencilFactory.CreateStationery()
	pencil.Show()

	// 生产钢笔
	penFactory := new(PenFactory)
	pen := penFactory.CreateStationery()
	pen.Show()

}
```

上述代码是通过面向抽象层开发，业务逻辑层的main()函数逻辑，依然是只与工厂耦合，且只与抽象的工厂和抽象的水果类耦合，这样就遵循了面向抽象层接口编程的原则。

## 5.3 工厂方法模式的优缺点 

优点：

1. 不需要记住具体类名，甚至连具体参数都不用记忆。
2. 实现了对象创建和使用的分离。
3. 系统的可扩展性也就变得非常好，无需修改接口和原类。
4. 对于新产品的创建，符合开闭原则。

缺点：

1. 增加系统中类的个数，复杂度和理解度增加。
2. 增加了系统的抽象性和理解难度。

适用场景：

1. 客户端不知道它所需要的对象的类。
2. 抽象工厂类通过其子类来指定创建哪个对象。

