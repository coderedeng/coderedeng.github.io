---
title: jwt-go
index_img: /img/cover2-14.png
date: 2022-06-13 21:01:24
categories: 
- Go常用库
tags:
- Go常用库
---

# 14.jwt-go

## 01.JWT介绍

### 1.1 什么是JWT？

- JWT全称JSON Web Token是一种跨域认证解决方案，属于一个开放的标准，它规定了一种Token实现方式
- 目前多用于前后端分离项目和OAuth2.0业务场景下。

### 1.2 jwt三部分

- 基于JWT技术及RSA非对称加密实现真正无状态的单点登录

![](/img/image-20210614161501680.e267e765.png)

## 02.JWT基本用法

### 2.1 定义需求

- 我们需要定制自己的需求来决定JWT中保存哪些数据
- 比如我们规定在JWT中要存储`username`信息
- 那么我们就定义一个`MyClaims`结构体如下

```go
// MyClaims 自定义声明结构体并内嵌jwt.StandardClaims
// jwt包自带的jwt.StandardClaims只包含了官方字段
// 我们这里需要额外记录一个username字段，所以要自定义结构体
// 如果想要保存更多信息，都可以添加到这个结构体中
type MyClaims struct {
	Username string `json:"username"`
	jwt.StandardClaims
}
```

- 然后我们定义JWT的过期时间，这里以2小时为例：

```go
const TokenExpireDuration = time.Hour * 2
```

- 接下来还需要定义Secret：

```go
var MySecret = []byte("夏天夏天悄悄过去")
```

### 2.2 生成JWT

```go
// GenToken 生成JWT
func GenToken(username string) (string, error) {
	// 创建一个我们自己的声明
	c := MyClaims{
		username, // 自定义字段
		jwt.StandardClaims{
			ExpiresAt: time.Now().Add(TokenExpireDuration).Unix(), // 过期时间
			Issuer:    "my-project",                               // 签发人
		},
	}
	// 使用指定的签名方法创建签名对象
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	// 使用指定的secret签名并获得完整的编码后的字符串token
	return token.SignedString(MySecret)
}
```

### 2.3 解析JWT

```go
// ParseToken 解析JWT
func ParseToken(tokenString string) (*MyClaims, error) {
	// 解析token
	token, err := jwt.ParseWithClaims(tokenString, &MyClaims{}, func(token *jwt.Token) (i interface{}, err error) {
		return MySecret, nil
	})
	if err != nil {
		return nil, err
	}
	if claims, ok := token.Claims.(*MyClaims); ok && token.Valid { // 校验token
		return claims, nil
	}
	return nil, errors.New("invalid token")
}
```

## 03.gin使用JWT

### 3.0 demo结构

![](/img/image-20210614170143996.08fc999d.png)

### 3.1 main.go

```go
package main

import (
	"github.com/gin-gonic/gin"
	"jwt-test/controllers"
	"jwt-test/middlewares"
)

func main() {
	r := gin.Default()
	r.POST("/auth", controllers.AuthHandler)
	r.GET("/home", middlewares.JWTAuthMiddleware(), controllers.HomeHandler)
	r.Run(":8000")
}
```

### 3.2 controllers/user.go

```go
package controllers

import (
	"github.com/gin-gonic/gin"
	"jwt-test/pkg/jwt"
	"net/http"
)

// ParamSignUp 注册请求参数
type UserInfo struct {
	Username   string `json:"username" binding:"required"`
	Password   string `json:"password" binding:"required"`
	RePassword string `json:"confirm_password" binding:"required,eqfield=Password"`
	//RePassword string `json:"re_password" binding:"required,eqfield=Password"`
}

func AuthHandler(c *gin.Context) {
	// 用户发送用户名和密码过来
	var user UserInfo
	err := c.ShouldBind(&user)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"code": 2001,
			"msg":  "无效的参数",
		})
		return
	}
	// 校验用户名和密码是否正确
	if user.Username == "zhangsan" && user.Password == "123456" {
		// 生成Token
		tokenString, _ := jwt.GenToken(user.Username)
		c.JSON(http.StatusOK, gin.H{
			"code": 2000,
			"msg":  "success",
			"data": gin.H{"token": tokenString},
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"code": 2002,
		"msg":  "鉴权失败",
	})
	return
}

func HomeHandler(c *gin.Context) {
	username := c.MustGet("username").(string)
	c.JSON(http.StatusOK, gin.H{
		"code": 2000,
		"msg":  "success",
		"data": gin.H{"username": username},
	})
}
```

### 3.3 pkg/jwt/jwt.go

```go
package jwt

import (
	"errors"
	"github.com/dgrijalva/jwt-go"
	"time"
)

// MyClaims 自定义声明结构体并内嵌jwt.StandardClaims
// jwt包自带的jwt.StandardClaims只包含了官方字段
// 我们这里需要额外记录一个username字段，所以要自定义结构体
// 如果想要保存更多信息，都可以添加到这个结构体中
type MyClaims struct {
	Username string `json:"username"`
	jwt.StandardClaims
}

const TokenExpireDuration = time.Hour * 2

var MySecret = []byte("夏天夏天悄悄过去")

// GenToken 生成JWT
func GenToken(username string) (string, error) {
	// 创建一个我们自己的声明
	c := MyClaims{
		username, // 自定义字段
		jwt.StandardClaims{
			ExpiresAt: time.Now().Add(TokenExpireDuration).Unix(), // 过期时间
			Issuer:    "my-project",                               // 签发人
		},
	}
	// 使用指定的签名方法创建签名对象
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	// 使用指定的secret签名并获得完整的编码后的字符串token
	return token.SignedString(MySecret)
}

// ParseToken 解析JWT
func ParseToken(tokenString string) (*MyClaims, error) {
	// 解析token
	token, err := jwt.ParseWithClaims(tokenString, &MyClaims{}, func(token *jwt.Token) (i interface{}, err error) {
		return MySecret, nil
	})
	if err != nil {
		return nil, err
	}
	if claims, ok := token.Claims.(*MyClaims); ok && token.Valid { // 校验token
		return claims, nil
	}
	return nil, errors.New("invalid token")
}
```

### 3.4 middlewares/auth.go

```go
package middlewares

import (
	"github.com/gin-gonic/gin"
	"jwt-test/pkg/jwt"
	"net/http"
	"strings"
)

// JWTAuthMiddleware 基于JWT的认证中间件
func JWTAuthMiddleware() func(c *gin.Context) {
	return func(c *gin.Context) {
		// 客户端携带Token有三种方式 1.放在请求头 2.放在请求体 3.放在URI
		// 这里假设Token放在Header的Authorization中，并使用Bearer开头
		// 这里的具体实现方式要依据你的实际业务情况决定
		authHeader := c.Request.Header.Get("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusOK, gin.H{
				"code": 2003,
				"msg":  "请求头中auth为空",
			})
			c.Abort()
			return
		}
		// 按空格分割
		parts := strings.SplitN(authHeader, " ", 2)
		if !(len(parts) == 2 && parts[0] == "Bearer") {
			c.JSON(http.StatusOK, gin.H{
				"code": 2004,
				"msg":  "请求头中auth格式有误",
			})
			c.Abort()
			return
		}
		// parts[1]是获取到的tokenString，我们使用之前定义好的解析JWT的函数来解析它
		mc, err := jwt.ParseToken(parts[1])
		if err != nil {
			c.JSON(http.StatusOK, gin.H{
				"code": 2005,
				"msg":  "无效的Token",
			})
			c.Abort()
			return
		}
		// 将当前请求的username信息保存到请求的上下文c上
		c.Set("username", mc.Username)
		c.Next() // 后续的处理函数可以用过c.Get("username")来获取当前请求的用户信息
	}
}
```

## 04.测试

### 4.1 登录获取token

- http://127.0.0.1:8000/auth

```json
{
    "username":"zhangsan",
    "password": "123456",
    "confirm_password": "123456"
}
```

![](/img/image-20210614165132336.0766e8a7.png)

### 4.2 携带token访问

- http://127.0.0.1:8000/home

```go
Authorization
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InpoYW5nc2FuIiwiZXhwIjoxNjIzNjY3NzUzLCJpc3MiOiJteS1wcm9qZWN0In0.j9SFygMnMq1-ymsDcTLN59svQb4-BTgO3DLaBeUAAVY
```

![img](http://v5blog.cn/assets/img/image-20210614165555199.4798dd56.png)
