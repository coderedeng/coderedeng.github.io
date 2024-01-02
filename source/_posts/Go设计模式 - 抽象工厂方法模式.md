---
title: Go设计模式 - 抽象工厂方法模式
index_img: /img/cover33.png
date: 2022-05-17 22:15:10
categories: 
- Go设计模式
tags:
- Go设计模式

---

# 6. 抽象工厂方法模式

##  6.1  抽象工厂方法模式中的角色和职责

**抽象工厂（Abstract Factory）角色：**它声明了一组用于创建一族产品的方法，每一个方法对应一种产品。

**具体工厂（Concrete Factory）角色：**它实现了在抽象工厂中声明的创建产品的方法，生成一组具体产品，这些产品构成了一个产品族，每一个产品都位于某个产品等级结构中。

**抽象产品（Abstract Product）角色：**它为每种产品声明接口，在抽象产品中声明了产品所具有的业务方法。

**具体产品（Concrete Product）角色：**它定义具体工厂生产的具体产品对象，实现抽象产品接口中声明的业务方法。

## 6.2 抽象工厂方法模式的实现 

抽象工厂方法模式的实现代码如下：

```go
package main

import "fmt"

/*
练习：

设计一个电脑主板架构，电脑包括（显卡，内存，CPU）3个固定的插口，
显卡具有显示功能（display，功能实现只要打印出意义即可），内存
具有存储功能（storage），cpu具有计算功能（calculate）。

现有Intel厂商，nvidia厂商，Kingston厂商，均会生产以上三种硬件。
要求组装两台电脑，
            1台（Intel的CPU，Intel的显卡，Intel的内存）
            1台（Intel的CPU， nvidia的显卡，Kingston的内存）
用抽象工厂模式实现。
*/

// ======= 抽象层 =========
type AbstractCPU interface {
	Calculate()
}
type AbstractGraphics interface {
	Display()
}
type AbstractMemory interface {
	Storage()
}

// 抽象工厂
type AbstractFactoryFn interface {
	CreateCPU() AbstractCPU
	CreateGraphics() AbstractGraphics
	CreateMemory() AbstractMemory
}

// ======= 实现层 =========
/* Inter 产品族 */
type InterCPU struct{}

func (ic *InterCPU) Calculate() {
	fmt.Println("Inter's CPU calculation")
}

type InterGraphics struct{}

func (ig *InterGraphics) Display() {
	fmt.Println("Inter's graphics display")
}

type InterMemory struct{}

func (im *InterMemory) Storage() {
	fmt.Println("Inter's memory storage")
}

type InterFactory struct {
	AbstractFactoryFn
}

func (f *InterFactory) CreateCPU() AbstractCPU {
	var cpu *InterCPU
	cpu = new(InterCPU)
	return cpu
}
func (f *InterFactory) CreateGraphics() AbstractGraphics {
	var graphics *InterGraphics
	graphics = new(InterGraphics)
	return graphics
}
func (f *InterFactory) CreateMemory() AbstractMemory {
	var memory *InterMemory
	memory = new(InterMemory)
	return memory
}

/* Nvidia 产品族 */
type NvidiaCPU struct{}

func (nc *NvidiaCPU) Calculate() {
	fmt.Println("Nvidia's CPU calculation")
}

type NvidiaGraphics struct{}

func (ng *NvidiaGraphics) Display() {
	fmt.Println("Nvidia's graphics display")
}

type NvidiaMemory struct{}

func (nm *NvidiaMemory) Storage() {
	fmt.Println("Nvidia's memory storage")
}

type NvidiaFactory struct {
	AbstractFactoryFn
}

func (f *NvidiaFactory) CreateCPU() AbstractCPU {
	var cpu *NvidiaCPU
	cpu = new(NvidiaCPU)
	return cpu
}
func (f *NvidiaFactory) CreateGraphics() AbstractGraphics {
	var graphics *NvidiaGraphics
	graphics = new(NvidiaGraphics)
	return graphics
}
func (f *NvidiaFactory) CreateMemory() AbstractMemory {
	var memory *NvidiaMemory
	memory = new(NvidiaMemory)
	return memory
}

/* Kingston 产品族 */
type KingstonCPU struct{}

func (ic *KingstonCPU) Calculate() {
	fmt.Println("Kingston's CPU calculation")
}

type KingstonGraphics struct{}

func (ig *KingstonGraphics) Display() {
	fmt.Println("Kingston's graphics display")
}

type KingstonMemory struct{}

func (im *KingstonMemory) Storage() {
	fmt.Println("Kingston's memory storage")
}

type KingstonFactory struct {
	AbstractFactoryFn
}

func (f *KingstonFactory) CreateCPU() AbstractCPU {
	var cpu *KingstonCPU
	cpu = new(KingstonCPU)
	return cpu
}
func (f *KingstonFactory) CreateGraphics() AbstractGraphics {
	var graphics *KingstonGraphics
	graphics = new(KingstonGraphics)
	return graphics
}
func (f *KingstonFactory) CreateMemory() AbstractMemory {
	var memory *KingstonMemory
	memory = new(KingstonMemory)
	return memory
}

// ======= 业务逻辑层 =========
func main() {
	// 要求组装两台电脑，
	// 1台（Intel的CPU，Intel的显卡，Intel的内存）
	fmt.Println("第1台：（Intel的CPU，Intel的显卡，Intel的内存）")
	iFac := new(InterFactory)
	iCpu := iFac.CreateCPU()
	iCpu.Calculate()
	iGraphics := iFac.CreateGraphics()
	iGraphics.Display()
	iMemory := iFac.CreateMemory()
	iMemory.Storage()

	// 1台（Intel的CPU， nvidia的显卡，Kingston的内存）
	fmt.Println("第2台：（Intel的CPU，nvidia的显卡，Kingston的内存）")
	inFac := new(InterFactory)
	inCpu := inFac.CreateCPU()
	inCpu.Calculate()
	nGraphics := new(NvidiaFactory).CreateGraphics()
	nGraphics.Display()
	kMemory := new(KingstonFactory).CreateMemory()
	kMemory.Storage()
}

```

以上是一个使用抽象工厂模式实现的电脑主板架构代码。这个系统可以组装不同厂商生产的CPU、显卡和内存来创建电脑。 该代码中定义了抽象层的接口，包括`AbstractCPU`、`AbstractGraphics`和`AbstractMemory`，以及抽象工厂接口`AbstractFactory`。然后通过实现这些接口来创建具体产品族的硬件和工厂。 在实现层中，有三个产品族的具体实现：`Inter`、`Nvidia`和`Kingston`。每个产品族都有对应的CPU、显卡和内存，并实现了抽象层的接口。 在业务逻辑层的`main`函数中，创建了两台电脑并进行组装。第一台电脑使用Intel的CPU、显卡和内存，第二台电脑使用Intel的CPU、Nvidia的显卡和Kingston的内存。组装过程通过抽象工厂来创建对应的硬件，并调用其相应的功能。 运行该代码将输出每个硬件的功能实现结果，例如CPU的计算、显卡的显示和内存的存储。 请注意，这只是一个示例代码，具体的电脑主板架构根据实际需求可能会有所不同。

## 6.3 抽象工厂方法模式的优缺点 

优点：

1. 拥有工厂方法模式的优点
2. 当一个产品族中的多个对象被设计成一起工作时，它能够保证客户端始终只使用同一个产品族中的对象。
3. 增加新的产品族很方便，无须修改已有系统，符合“开闭原则”。
4. 对于新产品的创建，符合开闭原则。

缺点：

1. 增加新的产品等级结构麻烦，需要对原有系统进行较大的修改，甚至需要修改抽象层代码，这显然会带来较大的不便，违背了“开闭原则”。

适用场景：

1. 系统中有多于一个的产品族。而每次只使用其中某一产品族。可以通过配置文件等方式来使得用户可以动态改变产品族，也可以很方便地增加新的产品族。
2. 产品等级结构稳定。设计完成之后，不会向系统中增加新的产品等级结构或者删除已有的产品等级结构。

