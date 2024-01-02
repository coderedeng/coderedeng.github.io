---
title: Go设计模式 - 面向对象设计原则
index_img: /img/cover29.png
date: 2022-05-03 21:15:11
categories: 
- Go设计模式
tags:
- Go设计模式

---

# 2. 面向对象设计原则

对于面向对象软件系统的设计而言，在支持可维护性的同时，提高系统的可复用性是一个至关重要的问题，**如何同时提高一个软件系统的可维护性和可复用性是面向对象设计需要解决的核心问题之一。**在面向对象设计中，可维护性的复用是以设计原则为基础的。每一个原则都蕴含一些面向对象设计的思想，可以从不同的角度提升一个软件结构的设计水平。

**面向对象设计原则为支持可维护性复用而诞生，这些原则蕴含在很多设计模式中，它们是从许多设计方案中总结出的指导性原则。**面向对象设计原则也是我们用于评价一个设计模式的使用效果的重要指标之一。

原则的目的： 高内聚，低耦合

## 2.1 面向对象设计原则表

| **名称**                                                     | **定义**                                                     |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| **单一职责原则<br />(Single Responsibility Principle, SRP)**<br />**★★★★☆** | 类的职责单一，对外只提供一种功能，而引起类变化的原因都应该只有一个。 |
| **开闭原则<br />(Open-Closed Principle, OCP)<br />★★★★★**    | 类的改动是通过增加代码进行的，而不是修改源代码。             |
| **里氏代换原则**<br />**(Liskov Substitution Principle, LSP)**<br />**★★★★★** | 任何抽象类（interface接口）出现的地方都可以用他的实现类进行替换，实际就是虚拟机制，语言级别实现面向对象功能。 |
| **依赖倒转原则**<br />**(Dependence  Inversion Principle, DIP)**<br />**★★★★★** | 依赖于抽象(接口)，不要依赖具体的实现(类)，也就是针对接口编程。 |
| **接口隔离原则**<br />**(Interface Segregation Principle, ISP)**<br />**★★☆☆☆** | 不应该强迫用户的程序依赖他们不需要的接口方法。一个接口应该只提供一种对外功能，不应该把所有操作都封装到一个接口中去。 |
| **合成复用原则<br />(Composite Reuse Principle,CRP)<br />★★★★☆** | 如果使用继承，会导致父类的任何变换都可能影响到子类的行为。如果使用对象组合，就降低了这种依赖关系。对于继承和组合，优先使用组合。 |
| **迪米特法则<br />(Law of Demeter,LoD)**<br />**★★★☆☆**      | 一个对象应当对其他对象尽可能少的了解，从而降低各个对象之间的耦合，提高系统的可维护性。例如在一个程序中，各个模块之间相互调用时，通常会提供一个统一的接口来实现。这样其他模块不需要了解另外一个模块的内部实现细节，这样当一个模块内部的实现发生改变时，不会影响其他模块的使用。（黑盒原理） |

## 2.2 单一职责原则

类的职责单一，对外只提供一种功能，而引起类变化的原因都应该只有一个。

```go
package main

import "fmt"

type ClothesShop struct {}

func (cs *ClothesShop) OnShop() {
	fmt.Println("休闲的装扮")
}

type ClothesWork struct {}

func (cw *ClothesWork) OnWork() {
	fmt.Println("工作的装扮")
}

func main() {
	//工作的时候
	cw := new(ClothesWork)
	cw.OnWork()

	//shopping的时候
	cs := new(ClothesShop)
	cs.OnShop()
}
```

在面向对象编程的过程中，设计一个类，建议对外提供的功能单一，接口单一，影响一个类的范围就只限定在这一个接口上，一个类的一个接口具备这个类的功能含义，职责单一不复杂。

## 2.3 开闭原则

类的改动是通过增加代码实现的，而不是修改源码。

```go
package main

import "fmt"

// TODO 开闭原则
// 类的改动是通过增加代码实现的，而不是修改源码

// AbstractBanker 创建一个抽象业务员接口
type AbstractBanker interface {
   DoBusi()
}

// SaveBanker 通过存款业务实例化业务员接口
type SaveBanker struct {
   AbstractBanker
}

// DoBusi 方法实例化了抽象接口
func (sb *SaveBanker) DoBusi() {
   fmt.Println("进行存款业务")
}

type TranferBanker struct {
   AbstractBanker
}

func (tb *TranferBanker) DoBusi() {
   fmt.Println("进行了转账业务")
}

type SharesBanker struct {
   AbstractBanker
}

func (sb *SharesBanker) DoBusi() {
   fmt.Println("进行了股票业务")
}

// BankBusiness 实现一个架构层（基于抽象层进行业务封装-针对interface接口进行封装）
func BankBusiness(banker AbstractBanker) {
   // 通过接口向下调用（多态现象）
   banker.DoBusi()
}

func main() {
   BankBusiness(&SaveBanker{})
   BankBusiness(&TranferBanker{})
   BankBusiness(&SharesBanker{})
}
```

开闭原则:一个软件实体如类、模块和函数应该对扩展开放，对修改关闭。
简单的说就是在修改需求的时候，应该尽量通过扩展来实现变化，而不是通过修改已有代码来实现变化。

## 2.4 依赖倒转原则

面向抽象层依赖倒转

![依赖倒转设计.png](/img/1651037225156-1b9ba94a-9498-4b72-a42b-c32e6261bbed.png)

如上图所示，如果我们在设计一个系统的时候，将模块分为3个层次，抽象层、实现层、业务逻辑层。那么，我们首先将抽象层的模块和接口定义出来，这里就需要了`interface`接口的设计，然后我们依照抽象层，依次实现每个实现层的模块，在我们写实现层代码的时候，实际上我们只需要参考对应的抽象层实现就好了，实现每个模块，也和其他的实现的模块没有关系，这样也符合了上面介绍的开闭原则。这样实现起来每个模块只依赖对象的接口，而和其他模块没关系，依赖关系单一。系统容易扩展和维护。

我们在指定业务逻辑也是一样，只需要参考抽象层的接口来业务就好了，抽象层暴露出来的接口就是我们业务层可以使用的方法，然后可以通过多态的线下，接口指针指向哪个实现模块，调用了就是具体的实现方法，这样我们业务逻辑层也是依赖抽象成编程。

我们就将这种的设计原则叫做`依赖倒转原则`。

```go
package main

import "fmt"

// TODO 依赖倒转原则
// 依赖于抽象（接口），不要依赖具体的实现（类），针对接口编程

// <---- 抽象层 ---->
type Car interface {
   Run()
}

type Drive interface {
   Drive(car Car)
}

// <---- 实现层 ---->
type Banz struct{}

func (b *Banz) Run() {
   fmt.Println("Banz is running")
}

type BMW struct{}

func (b *BMW) Run() {
   fmt.Println("BMW is running")
}

type Zhangsan struct{}

func (Zs *Zhangsan) Drive(car Car) {
   fmt.Println("zhangsan drive car")
   car.Run()
}

type Lisi struct{}

func (Ls *Lisi) Drive(car Car) {
   fmt.Println("lisi drive car")
   car.Run()
}

// <---- 业务逻辑层 ---->
func main() {
   var banz Car
   banz = new(Banz)

   var bm Car
   bm = new(BMW)

   // 张三开奔驰
   var zs Drive
   zs = new(Zhangsan)
   zs.Drive(banz)

   //李四开宝马
   var ls Drive
   ls = new(Lisi)
   ls.Drive(bm)

}
```

## 2.5 合成复用原则

如果使用继承，会导致父类的任何变换都可能影响到子类的行为。如果使用对象组合，就降低了这种依赖关系。对于继承和组合，优先使用组合。

```go
package main

import "fmt"

type Cat struct {}

func (c *Cat) Eat() {
	fmt.Println("小猫吃饭")
}

//给小猫添加一个 可以睡觉的方法 （使用继承来实现）
type CatB struct {
	Cat
}

func (cb *CatB) Sleep() {
	fmt.Println("小猫睡觉")
}

//给小猫添加一个 可以睡觉的方法 （使用组合的方式）
type CatC struct {
	C *Cat
}

func (cc *CatC) Sleep() {
	fmt.Println("小猫睡觉")
}


func main() {
	//通过继承增加的功能，可以正常使用
	cb := new(CatB)
	cb.Eat()
	cb.Sleep()
	
    //通过组合增加的功能，可以正常使用
    cc := new(CatC)
    cc.C = new(Cat)
    cc.C.Eat()
    cc.Sleep()
}
```
