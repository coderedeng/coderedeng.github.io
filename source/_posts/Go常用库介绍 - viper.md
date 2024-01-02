---
title: viper配置管理
index_img: /img/cover2-12.png
date: 2022-06-09 21:24:37
categories: 
- Go常用库
tags:
- Go常用库
---

# 12.viper配置管理

## 01.viper介绍

- [参考博客(opens new window)](https://www.liwenzhou.com/posts/Go/viper_tutorial/)

### 1.1 viper是什么？

- [Viper (opens new window)](https://github.com/spf13/viper)是适用于Go应用程序的完整配置解决方案。
- 它被设计用于在应用程序中工作，并且可以处理所有类型的配置需求和格式
- viper功能
  - 设置默认值
  - 从`JSON`、`TOML`、`YAML`、`HCL`、`envfile`和`Java properties`格式的配置文件读取配置信息
  - 实时监控和重新读取配置文件（可选）
  - 从环境变量中读取
  - 从远程配置系统（etcd或Consul）读取并监控配置变化
  - 从命令行参数读取配置
  - 从buffer读取配置
  - 显式配置值

### 1.2 为什么选择Viper?

- 在构建现代应用程序时，你无需担心配置文件格式；
- Viper能够为你执行下列操作：
  - 查找、加载和反序列化JSON、TOML、YAML、HCL、INI、envfile和Java properties格式的配置文件。
  - 提供一种机制为你的不同配置选项设置默认值。
  - 提供一种机制来通过命令行参数覆盖指定选项的值。
  - 提供别名系统，以便在不破坏现有代码的情况下轻松重命名参数。
  - 当用户提供了与默认值相同的命令行或配置文件时，可以很容易地分辨出它们之间的区别。
- `Viper会按照下面的优先，每个项目的优先级都高于它下面的项目`
  - 显示调用`Set`设置值
  - 命令行参数（flag）
  - 环境变量
  - 配置文件
  - key/value存储
  - 默认值
- **重要：** 目前Viper配置的键（Key）是`大小写不敏感的`

### 1.3 viper安装

```go
go get github.com/spf13/viper
```

## 02.viper设置配置

### 2.1 建立默认值

- 一个好的配置系统应该支持默认值。
- 键不需要默认值，但如果没有通过配置文件、环境变量、远程配置或命令行标志（flag）设置键，则默认值非常有用。
- 例如：

```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```

### 2.2 读取配置文件

- Viper需要最少知道在哪里查找配置文件的配置。
- Viper支持`JSON`、`TOML`、`YAML`、`HCL`、`envfile`和`Java properties`格式的配置文件。
- Viper可以搜索多个路径，但目前单个Viper实例只支持单个配置文件。

```go
viper.SetConfigFile("./config.yaml") // 指定配置文件路径
viper.SetConfigName("config") // 配置文件名称(无扩展名)
viper.SetConfigType("yaml") // 如果配置文件的名称中没有扩展名，则需要配置此项
viper.AddConfigPath("/etc/appname/")   // 查找配置文件所在的路径
viper.AddConfigPath("$HOME/.appname")  // 多次调用以添加多个搜索路径
viper.AddConfigPath(".")               // 还可以在工作目录中查找配置
err := viper.ReadInConfig() // 查找并读取配置文件
if err != nil { // 处理读取配置文件的错误
	panic(fmt.Errorf("Fatal error config file: %s \n", err))
}
```

### 2.3 写入配置文件

- 从配置文件中读取配置文件是有用的，但是有时你想要存储在运行时所做的所有修改。
- 为此，可以使用下面一组命令，每个命令都有自己的用途

```go
viper.WriteConfig() // 将当前配置写入“viper.AddConfigPath()”和“viper.SetConfigName”设置的预定义路径
viper.SafeWriteConfig()
viper.WriteConfigAs("/path/to/my/.config")
viper.SafeWriteConfigAs("/path/to/my/.config") // 因为该配置文件写入过，所以会报错
viper.SafeWriteConfigAs("/path/to/my/.other_config")
```

### 2.4 监控并重新读取配置文件

- 确保在调用`WatchConfig()`之前添加了所有的配置路径。

```go
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) {
  // 配置文件发生变更之后会调用的回调函数
	fmt.Println("Config file changed:", e.Name)
})
```

### 2.4 覆盖设置

- 这些可能来自命令行标志，也可能来自你自己的应用程序逻辑。

```go
viper.Set("Verbose", true)
viper.Set("LogFile", LogFile)
```

## 03.viper读取配置

### 3.1 几种访问值的方法

- 在Viper中，有几种方法可以根据值的类型获取值
- `Get(key string) : interface{}`
- `GetBool(key string) : bool`
- `GetFloat64(key string) : float64`
- `GetInt(key string) : int`
- `GetIntSlice(key string) : []int`
- `GetString(key string) : string`
- `GetStringMap(key string) : map[string]interface{}`
- `GetStringMapString(key string) : map[string]string`
- `GetStringSlice(key string) : []string`
- `GetTime(key string) : time.Time`
- `GetDuration(key string) : time.Duration`
- `IsSet(key string) : bool`
- `AllSettings() : map[string]interface{}`

例如：

```go
viper.GetString("logfile") // 不区分大小写的设置和获取
if viper.GetBool("verbose") {
    fmt.Println("verbose enabled")
}
```

### 3.2 访问嵌套的键

- 问器方法也接受深度嵌套键的格式化路径
- 例如，如果加载下面的JSON文件

```json
{
    "host": {
        "address": "localhost",
        "port": 5799
    },
    "datastore": {
        "metric": {
            "host": "127.0.0.1",
            "port": 3099
        },
        "warehouse": {
            "host": "198.0.0.1",
            "port": 2112
        }
    }
}
```

- Viper可以通过传入`.`分隔的路径来访问嵌套字段：

```go
GetString("datastore.metric.host") // (返回 "127.0.0.1")
```

### 3.3 提取子树

- 例如，`viper`实例现在代表了以下配置：

```yaml
app:
  cache1:
    max-items: 100
    item-size: 64
  cache2:
    max-items: 200
    item-size: 80
```

- 执行后：

```go
subv := viper.Sub("app.cache1")
```

- `subv`现在就代表：

```yaml
max-items: 100
item-size: 64
```

- 假设我们现在有这么一个函数：

```go
func NewCache(cfg *Viper) *Cache {...}
```

- 它基于`subv`格式的配置信息创建缓存。现在，可以轻松地分别创建这两个缓存，如下所示：

```go
cfg1 := viper.Sub("app.cache1")
cache1 := NewCache(cfg1)

cfg2 := viper.Sub("app.cache2")
cache2 := NewCache(cfg2)
```

### 3.4 反序列化

你还可以选择将所有或特定的值解析到结构体、map等。

有两种方法可以做到这一点：

- `Unmarshal(rawVal interface{}) : error`
- `UnmarshalKey(key string, rawVal interface{}) : error`

![](/img/image-20210609094655146.46d6e697.png)

- `main.go`

```go
package main

import (
	"fmt"
	"github.com/spf13/viper"
)

type Config struct {
	Port        int    `mapstructure:"port"`
	Version     string `mapstructure:"version"`
	MySQLConfig `mapstructure:"mysql"`
}

type MySQLConfig struct {
	Host   string `mapstructure:"host"`
	DbName string `mapstructure:"dbname"`
	Port   int    `mapstructure:"port"`
}

func main() {
	// 读取配置文件
	viper.SetConfigFile("./config.yaml") // 指定配置文件路径

	err := viper.ReadInConfig() // 查找并读取配置文件
	if err != nil {             // 处理读取配置文件的错误
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}

	var c Config

	if err := viper.Unmarshal(&c); err != nil {
		fmt.Printf("viper.Unmarshal failed, err:%v\n", err)
		return
	}
	fmt.Printf("c:%#v\n", c)
}
```

- config.yaml

```yaml
port: 8081
version: "v0.0.2"

mysql:
  host: "127.0.0.1"
  port: 13306
  dbname: "sql_demo"
```

## 04.使用Viper示例

- 目录结构

![img](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATIAAAClCAYAAADf0nGKAAAgAElEQVR4nO2de1Bc95XnP7cRCMSzuyX0tCMQMIptybIaeQxrxxkTawxRElkR+JHE8sxmmsxW7dbCOrVTW1bKFWd3djYOpGpSKdMzdqzYlcSgTOREBgcFPyJHnVhCfuDEuBtoWbb14v0SCETf/aMf3G4aaOhuuhvOp6qr4N7f4/SF/vY55/e79ygtLS2qTqcjOTmZm2++mYGRCQRBEGKd/u5PAZicnEQXZVsEQRBCRoRMEIS4R4RMEIS4R4RMEIS4R4RMEOIAT2JbCIwImSAIcY8ImSAIcc+qaBsgxD9Op5PRkSGujg4zNXUdgISEVaxJTSc1LQOdLrzfl39ue5f3295ZVN9bduzi5h23htWeeGRs7CoAKSlromxJeAhJyLp7+xmfuBaSAclJq1ln1Ic0hhAdVFVloK+bvp4rOJ1TM84PDfSh0yVgWJtNlmEdiqKEZd7BwQE+Pv/RovrecOPWsNigZXx8jLdbT6OqasDziqJwm2kPyckpYZ97MdT/4nnOn3MAcOPWHCoe/EaULQqdkITscm8vQyMjIRmQkZYmQhaHOJ1TXPj4HGNXR1AUHRlZBhITk+jtvgSAcd0GJicnGB4coOfKRUZHhtl0w1Z0uoSQ587MzOKGGz+z6L7hJjk5hfSMDH7b+JsZYqYoCn9b9qWYETGAkeHhgD/HMys+tFTVLp75yu18l+/xxkuV5ITJa1jOqKrqFbGk1cls2pJDYlISV0env9SSU1IxrF2PwbieC584GLs6woWPz7H5xtyQPbObd9wac+HhLTt2AfiImUfEPOeiwdWrVxkZHiJ7/QaczinefecsQ4MD3vNDgwO8ffY0t+7ajU6XwJXLl0hLz2DNmvgKOWNeyByWUu5+4rTvwUIRnWgy0NftFbEbtubPmQNLTErihq35fHzOztjVEQb6utEbsyNil9Pp5PWWZgA+X7I37Lm5+dCKGRB1EVNVlVdefomuTjs3bs1h/OpVrly57NPm+vXrtDQ30fbOWZLXrOH8OQe52/K5/+CDYUsFLAUhC1m20UC20bCovld6+xi/FsRN6hrh8nhQd3+FsIiZouTyzV/38M2QRpmJqrbwT5sfgBe6+Zd74ucfYj6cU1P09VxBUXRs2pITlFjodK62H3V9SF/PFTKzjOgSQg8xtUxMTHD817+kq8MOwMBgP/u+/FWSkpLCOs98aIUrmiIG4OjqoKvTdT08ObHZ0ApcV6cdR1cHudvyI2pfOAlZyFYnJaFLXkPHaOBE52zkpSqsThoJTsg0KEou//mH3+PlOx/n6dcq+Zd7FtRdCJHR0SGczikyMg0k+olEUlIShrXrvT9rSUxKIj0ji6HBPkZHh0jPCF9edGRkmP+o/5nvh7HDzi9e+AkHKh4mLS09bHMFQ7QFzMOlixcCHt+x8zZ23HobAG3vvk3be28H7LuihAxgeArODk0uqM/65BC+KXPyKdD8+vq31/LIh9/jp/te4pEnTvt6cF1Pc+DOx2nVtH/Iz0vy9Nd6eDP6BQhnPV7Xz/3a8G9l0+Hw19fxc8D0xFv8ypwb1Nu7fOkinR22oNpuyytg/YaNQbUNB2NXRwFm5MSSkpJYlZiEcd0G77HrkxNMTEx/UXmEb+zqaNiE7Nr4OL9/7XesTk4OuADw+9d+R8m9paxOTg7LfB6GBgcYHBxcVN/MzEwyIrDo4E/xnXeTkZnJiVdeZmrKtaq8Y+dt/G3Zl7xtNm3eAuAVs4SEBO6974thEeOlvEYxnyMLiMOOjT18UbuSfuZxHvmrFzl/ocR7SH21ms98/ac89EI3v7pHK1DruH8OYXH1+4DvvNnNr3IDh7OesU1PvMV59zhq19M88xp809zER/+w+NByXfZ6/nDyNbo6O+Zsl7stjzuK71rQ2KFyfdL1heVZnfRgWLveR8QABgf66OvxzcloxwgHq5OTKfvS/WEbL1jeb3uXU2++sai+xXfeTfGdd4fZosDcsmMXr554ZVrIdt02o82OXbf5CFm4PMqlvEZxt7NfVVv4pzsfp/Vrj/HNXK1APMJP/989vu3cQqMVEiX3W9Q8sYfWJ37E6wH2/ahqF8/88Kc89EKjd3xPOGs68xItjuk2fO1FHzFUcr/FN8OQD9PpdHxpfzkbN22etc3GTZv50v7yJU9oC0IsEh8e2ZnHuXvz495ftV6Ql8ICfAILhx0bUJCXM2O4rXmfBT6gwwGf93fKHM28fAZa3SGhPwXnAFxtHvrvkUvQJSYmcqD8IX7+/E/o6+v1OWcwGDlQ/hCJiYkRm382VrnnNK7bQHJKqvd4oKR6ZpaBlDVp3t/Hx0bp7b7kHSMcXBsfp+VEE8PDQwHPp6dnRCS0vGXHrYveXJuZmRlWW+bi/bZ3vN4YQNs7b7Np0xafNm3vTOfIpqameL/tnbB4ZUt5jeJDyKKw3cI/j6ZF7VoaG1JS1nDwga/xs+d/wsiIa+NiWlo6Bx/4WtRuLUlZk8pgfy+TExPexL6H65MTDA70AS4RW5Xoypt5GB7s944RLlYnJ/O5v/nCjGQ/QHb2er745QNhFzGAjMysJclzhcKpN9+YEdp5QsjZkv1TU1O88vKvGRocDDn8XcprtHzjEveCgK1j5rLzuY4PgM8SwFmbs9+C2oSJjMwsDlQ8zOrkZFYnJ3Og4uGofoBSUzPQ6RIYHhpgcsJ3xXliYoK+nsv09Vz2SfIDTE5MMDw0gE6XQGpqRlhtSktL58Gv/x25edOrbLl5+Tz49b9b8hVLcHlBi70XNJxs2Lgp4PG2997mZ88/y8+efzbgiuVcfWOVZStkilLCt57YQ+sTt/M/X53OhamvVnP3E6d56IUf8PkAHt6s/bqe5v5vt8w7tvZ3CI/YZWevZ/+BB9h/4AGys9fP3yGC6BJc906qqpMLnzhwOp3z9nE6XW1V1YlhbXbY95CBK7Tdf+ABdptuZ7fpdvYfeGDJ95CBS8R+2/gbftv4m6iLWU5unncLxY1bc+b838nOXs+NW13f7Lnb8snJzVsSG8NFfISWiyTH3MRHedV8xifftYfvvNntt1Aws98blHK3tl/h93jjpXt82swY+2svcv77ngWCEv7vC4/wma/fzo1PLGz7RSAWe29hJMgyrGN0ZJixqyN8fM7uvUUpEJMTE1z4xMHEtXFS1qSRZVgXMbt0Oh333HtfxMafD4+IeW5R8uzwj9a+MkVRuO+LX5lxi9Ibr57g+nXXU0pWrVrF3ffcO+MWpXja1Q+ghFIO7n1bB5npaaxfv4Heyfm/mbUYE3VcvnyJweERbimIrvq//u21PMKLnP9+yfyNBWDmTePpmVmz3jSuqk5S1qSF7abxWHyMj7+IeQjX/Zb93Z+iXzf7KvZCePbffkxfbw8ABuNa/v4f/ktYxl1qtOXgQvbIBodHgEvztvPnsrdvdFHVLjo+BNO+QAkzYTZ0ugQ235jrfYzPkDvJ78EjaDpdAsZ1G5f9Y3yGh4Yo+k+fC3h+eGiI8fGxmHkCRlp6ulfI0tKXPocYCUISsrQ1KYxcHQtJkNLWRPmP+9qP+O6ZPXznhyJkC0VRFPTGbDL1a5f0wYqx+Bif2UQsFql48BvyYEUtW7eEx9WNBtqnajz0wtw5M2FudDod6RlZpGcszWpqLD7GJ95YLgLmYVkn++cix9zEeXO0rRAEIRws2+0XgiCsHETIBCEOCNeK5XJFhEwQhLhHhEwQhLhHhEwQhLhnxqqlZ7esIAhCvOAjZOnp6ezcuTNatgiCIATNe++95/1ZQktBEOIeETJBEOIeETJBEOIeETJBEOKemLrX8vyFy4yOjfkcS1q1ivXrjNF/SoYgCDFLTHlkH316ifbOj3xe733YScsfTmM/93FkJ7fXUqwoKEoxtfbIThUSTZUoioKiVNIUbVuEGTha6qg72kp/tA2Zk35aj9ZR1xL5mhNLRUx5ZLPhVFXet3XhdDr5q9zYeeSzsBgctNQ106l5yOK2e82UzHgcnKsdeysDnIu8fYubt5++2FawZUtcCJmHv3Sc4y8d5+Zss1afxV17FvGsqvwqTqlVi7RMCIb+1qM0tPaxbW8lZo1IOFqO0pp1EJNe2zqH3Dxobm1ld44Jvf9gESOUefWYDlZiipBlwuwsOLS8ePEiTz/9NP39s3/12Gw2nnnmGcb88l3CCsbRQv0ZMJXP9L5ySvxFzH18dyHGXgddS+zlRGteYfEs2CMbGRmhp6eH5557jkcffRS93vc/0GazUV9fT2pqKuPj46SkRD9J31SpUGYBMNOo1lEKgJ3a4gKqrYC5EfWxdooLqrFSRI3tFFX5TVQqZViAohobRzhEQbXVPaJ2HO8kKK5JXBTVYDtVhasY1/RY5sZGKCvD4p1nbtvttcW+8zbO+iaDmn/GezE3otaV+vUP4v25xzo13xsAoJ/W1g6MhRUBBcun3dF6zlBIxUETen0uOcYzOLr6Mc3o6Grb2ucKUVV1G3srS8gJx/lZ5nW01NHc77ZNY4n2+IBfG++5EmipP0OfO6RWt91Lpb+i97dyVNvGYPKZyzPW3hwHJ1r7ZpyfFUcLlhOd3l/VbSYKA7ULZn72UpHVSkNrn08b3N524Gs9c2yYLaWwOBYsZPn5+VRUVFBfXz9DzLQiFkjkokXpYzUUWaqxYuFYUx2lpYD9OA1WgCJqHisF2mftb60uoMDniIWy4u1eofAVG28nCorRiIm7Z1lZ0HZPC7Bm3gDdFzI/DYcosGraWsoobivCqj0WzPvDdV2UdrcQzkV/F45e0M+tYgHQYzLlcab5LA6T7wejv/UslFRi1oNHlJqPZnk/eKGdDzxvTm4eNDvo6jdNC3J/K60dkLfXNe5AgHeh9LVS32KiorLSJQr9rRytb6aOvdNi5mihrrmfwopKDmpsqj+Kj5gofa006++l0hykArhFTCsajpY6TvQp+KlxcPN3nqDFVI7ZrPeKU4Ol1SXM5hw8Ocbmllyf92Y50cm2vZUc9Jjd38rR+jqOFlZwcMH/FzNZ1KplQUEBFRUVjI6O8txzz9Hf3x+zIgZA/j7Ki1w/trW7liTtxxtw6Vg5++ZzKopqsKkqqqpiq3EPZG3guB2giafcH3Jzo6uNqtqoKQKs1Tzlv7ToHWseb8xey5NeB6nRd1wfFja/lXL3/I14nvRttUKNzdW30XuwnQ63HYe03pv/dbA8GeQqr5GseR/p78oxVWq9jJxc8uigy2+BTW8q0Xh3LuGhd8ArJKGeDzhvzm4Kjb04NDFnf5eDXvLInUNXVHUbe7XvSW+ipNAIHV24hnd5rHl7D/raVDIzxFXVbewN2o1x0NLcgcFU7uP55JRUYDJoy9YtYH6DiRJPI70JU56/Ta4cI/197pXbwDZ4rkHvmbOEY+100cl+j5jV19fz7LPPMjY2FpsiBkA++8qLqLZasTYcx15VRUe768NZVL6P+XTMfHjaq8mvOoy5ugwLVto7gI5jePTGUqZg8evb1m5HG6Npx5qTjnbcFro9Rtf7qDpsplrrpjUtbP7p91vKfjNYLPiIean34Fx2+F6HhuN2qoIKMReDO/ne5aAkx/cD7Gip40SntmjMtjCeDzSvntwcI2ccXfSbTOjpp8vRi7HQL4zyx5iFv4brDXo8q5w5uDzWvhMWOv37KqAfYNp7CjDWrLjFxDXXXO0WML/eMDOU9bMpK8uId//JHDb4XIMQJSOkVUutmMWuiLnI31dOUbUVq7WB4/bttFsAiiif1x3zw95OWyQMjGN2bJ/nGuoN6Jkt1zU/ObsLMda30ro7x+0xuMKXDvKmczGOFuqaPT1CPT/bvKDPzcF45gxnHSZKsrpw9BrJKQnP/3w4c0bxOH8ohLwhtqCggAcffDCmRQzQhJdWGg496fJczIfnTbYDWJ6sxRM9NT1V7fVQtucBedvxRHvTod30K7hkeAC847o8Hhd2ap+0zNIuzPMHsKNaE6faa93X0HMd5sTl3Sw6jNDnkqMN6RxddGCksGLaE+rXbuAK9fxs84I3nOrocrjCyjzTPAsY+IasXhM6wJhDrh6vlxPQhlCYddwBBnqDaRdJGzzH9MznMAZDWHb25+XlxbaIAZ7wEvAmts3750lSe7BWU6AoKIom+e4RwfwqDrvzSpYyxb3r3v0qnhbAhZs7ndezVhe4x3Svsvq0i9D8AcbHUuYde3rVM7gvg5ySCgqNHTTXHaXV53+6n9ajnmPuHeczdsa7QrpeR5f3uKL0MeBRh/5WWs70+vQI9fxs84I76d/RSoujl7y5kmPeuTpp1u6id7RwolMhz+TJm+Wwu9BIX2sDPpvt+1s5GtLue88XSIvPNXe0+G5Ijtz8c4ztaKGhtY+8vfOE5UESVxtiQ2U6rwNgJlgdK6pppLyhbFpEzL4rdaV1KrbtAVb2dmwPLh8W2FqqTtmguMBnXtv2J2fME5n5fcdX98/cfmFuVJlvwXIaVyI/t/UoDQ0WWt1HVdVAYUXgfWQ+vU0m8s40u0K6nBLKTf00uHM6qsFExd486j2hYajnZ53X0z+XPJrpoDCoUEw1mNib1YrFcsJ7zD+M05sOUs5Rr02efhUHQ/uY55RUspc6Tmiu+bZ7KzD113NG0y5S83vGNhtasGjHVg0UVpjn92aDRGlpaVF1Oh3Jycnccccd4Rl1kZw8/S49/YEWsINn0Tv7Z+C79yrkEE0IGc8+phn7r2J43tn2ngmh43lC7OTkZGx5ZDu35zF5fTKkMRJXJYbJGiHWCJR8X87zCsETU0KWmZ4abROEWEZv4mBlFO5kjNa8QtDElJCtLKZD1xn43F4kCLMx80kiHoK+fWmZEFM5MkEQhGDR5shi6sGKgiAIi2HZhJZ9N0ggJiwew8ex/FhgYT7EIxMEIe4RIRMEIe5ZNqGlFgkThGCQdMTyQTwyQRDiHhEyQRDinmUZWvojhX8FYXmzIoTso08vBbwZXWfr4qb8HPK33hAFq0LAXusulCI3tAsCrBAhm434LPzbRGVBNdTYUEXABAFY4ULmIaKFf8ONvZ22xTyiWxCWMTGT7JfCv0HiLQYiCIKHmBEybeHfQGLmKTc3NDTE+Ph4FCycjyYq53rMtL2WYsX3UdSVPqXa7NQWKyiVTdhrizXtKvE0a6pU3E9ptVJdoKAoxUGWYhOE5U3MCJmn8K+2VqaHmK6ZCa4q3EoZbTW26cIfR+B4k+Z8QTU7tMVBbDW0lSkU+yuRpYxDHHG3a8SMhTK34pXWqaiNZqDIXYdy/krlgrASiBkhgzgs/At4KxuZG31XD/OrqCoFaKKyzEJRjc33+fb5VRypKcJa/RQ+jllRDUe845TyWE0RWI7hX+dXEIRpYkrIwFfMnn322RgXMcB+nAbrHBWZ3HUwA9V+zN++A2ijXeuUhalgiCCsJGJOyGBazGK7erkgCLFCzG6/8BT+NRqNsS1i+dvZAbS126E0gC81x3l7exuwg/kKdQuCMDcx6ZF5iI/Cv648lrW6wHcVsqnS/fvs5wuqrZgb6wi6NKQgCAGJWY8snsivOoW6vRKlTJkuJmJuRK2b47x75VFWHQUhdJZN8RHts6X8n0cWW4V/hVhhrv8ZIfaJ2QK9kUIK/wrC8mZFCJkU/hWE5U1MJ/sFQRCCQYRMEIS4R4RMEIS4R4RMEIS4R4RMEIS4R4RMEIS4R4RMEIS4R4RMEIS4Z9WePXvQ6XR0dnZG25Zlx+WePtavNXDy9LsBz+/cniebdQUhDKyInf3R4IPOc/T0DbJ+rWHW+zxDvW1KEAQXElpGgA86z9He+VG0zVg4mgIpxbV2V7ET/yIqcUS82y8EjwhZmIlbEdMW/lVVTlVBe1u0bRKE4JDQMozEr4gRoPBvPlWnVKqiapQgBIcIWZhwOp2sM2SxzpDlPRZXj/5xF/4tj7YdgrAIJLQME2PXJujuG/B5XbjSzQed50IcOXqFfwPmmJoqfeYqrm3yjh/Q+lnyVL7H3TYGsM3b1t9+d9/Z3pOwshAhCxNj4+O0d34U8LVoYqzwr722GKXMglkz3+H2Mqqts7+F0v1msDZw3FcNOWYB8+Eq8gF77VNwxDOmjZoiC2X+4qe131ZDkbWaAkWhoP1wwPckrCxEyGKWWCv828RT1dYZ85XW2agpmqNb6WPUFFlp0CpZ0zEsmPGUAs2vqtMIZz5Vh81gbadjNvvzqzhsBjDT6DWmlP1moK1dVilXIJIjCxNr9Vncv/fu8A3oKfx7OLTCv94KdKEW/p1jvrnJZ195EdUNx7FXVZHvFuiiGptP9aimSoUyi7af2XeYQPYXbSdP82ve9iKQldYViQhZiDjbbKgDw2EZK+EuU1jGiTXy95VTVN3AcXsVVRynwVpE+RGPLDVRqZRhwUyj6i6N11SJUhZFg4W4Q4QsRN47+zajV7r567ztAEw5nZx47yzpa1KZmLzG39y8y9v2rc4PmZpyUlTwWY6f/RNFBTdhTEsPPHCsFf6ddb4O2q3Ajrn67qO8qJqG43b20YC1qJxpHTuGhSJqbNP1PT32C0KwSI4sRDYY1/KLP7xO15VLAPyu7Sytjg56hwept57kRNvbALRf+JjnXm/mj/YPAHj57Fv0jgzNMXKsFf515aCs1YfQriM0VZbhExF6Vll9jHLlvawNT/FUg9Wb5J/GSrsnIWav5dBcqweCEAARshBZl5nFlwvv4Ke//x0f93bzyjtneORzJegUhTVJq3np9ClaHXaefe23pCSuXtDY+VWnUBvNWMo0WxOO7fcm2wOeL2ujxqb6LgCEidI6lUazZ4uG63Vsv3+yP4/tgZL/pfsxWy1YrNNJfveg2GqKpt/DITjSaA4wgCDMjjI0NKR6nn6xc+fOaNuzaKJVbHXqZCvOnj5+cPyXfNLTwxd23sa+3X/N8bN/wn7xU3LXb+SVd85QsHEzues30nX5IlVfPMA//vu/UrXvAAUbNnvHWnX/F5bM7vBhp7a4gOodjahzqmew7ZYOKdAb32gL9IpHFgYUFMp27eHa9Unu21Xoc+7LhXdwzy27MH+hjATdMrzcntXV/fOIk92V5K95LDZETFheSLI/TKxa5bqUq3QJPscVFMrvuCtgnz/aPsB24RMAbv1MLjmRNTFk7LXFHOKIZl+b60Zza1ENR+bRp6anqrGaGzkVzgUIQXAjQhYmUhKTKNg4HSYa0zIYM074tNEeK9i4md7hIXqHXQn/3OwNS2fsIsmvOsXhSgVF0Rw0zx0q2muLKai2QlENtlPijQmRQXJkITJ1shW1pz8sY8Vnjix+kRxZfKPNkYlHFiLLdROrIMQTyzD7LAjCSkOETBCEuEeETBCEuEeETBCEuGdZJvu1q1GCICx/xCMTBCHuESETBCHuicnQ8uLFi4yMjJCfH3yIuNANjZ7SbWv1Wdy151Z+1fxGwHZ37bmVtfqsgOeWN7F3k7cgzEbMeWSqqvLSSy/x4osvYrPZIjJHXNefFARhBjEnZIqi8MADD5Camkp9fX3YxUxETBCWHzEZWur1eh599FGee+456uvrqaiooKCgIORx476IriAIAYk5j8yDR8zC6ZlFroguwReunbegbqChQyhQG+x8fvYrlccXfy0EYYmJWSGDaTFLSUmhvr6ejo6O+TvNgbaI7qk/nea1k3/wvi5e+MT76uu5sqBxgy5cu5CCuv4spkBtsPM1Vc6wv5HqOQvvCkIsEdNCBtDd3c3Y2BipqakYjcawjfvWyTd45T8aAr7eOhl4BTMwwRauXWBBXX8WXKA22PkCt5u38K4gxBAxmSPzYLPZqK+vJzU1lUcffRS9Xh+2se+7vzw8AwVbuHahBXX9WWiB2mDnY7GFdwUhdohZIYukiAG89eYb9HUHDiEN67K5/c4wVg0XBCGixGRoGWkRAzCsXcf6LTcEfBnWrgt+IG3hWh/chWvnbbcEBXXnmi9Y+wUhhok5IVNVlZMnT0ZUxAAMa9eyYfMWn9ctO2/jtj13kLf9pgWMFGzh2mAL6gYqcLsYgp0vWPsFIXaJudBSURQefvhhrl27RlZW5G4NeuvkG1z89BOfY/cdKGfjpi0LHqu0TqURhbIChWr3MXOjjZq2Au/v4C6ou70SpUzRiEQRNTYVb2Gi2QrcLoLg5gvefkGIVZZN8ZFg6Okf4OTpdxfUZ/H3Wsq9ioIQSaRA71IQbOFaQRBCRoQsDNhri/02tE4XrpXC2oIQeWIuRxZJElclLjhMDOZezMUUrhUEIXysqByZIAjLh2VXoFee0R8/SEVvIRJIjkwQhLhHhEwQhLhnWYSWWiR0iT0k9BcijXhkgiDEPSJkgiDEPcsutFwI5wau0XZljO7RSQCyUxO5JTuFrVmro2yZIAgLYcUJ2dVJJzqg4YM+/nxlzOecrXecN88Pc3N2CuWfNeAE1iSK0yoIsc6KErKB8Sl+cOoiqYkJDFy7Pmu7P18Z49PBy4xOTvE/ijeSlZywhFZO01SpUNZWg+1U1cynwwqC4GVFCZlOAQUYuHadGzKTuDc3k+7RSX5jGyAxQWHPplQATl8YZeDadZJ0Cjpl7jEjh532tvlbCYKwwpL9GasT+OpNBpJ0Ov6xcD2nX/klyidtPLzDSPlNBtb1tTN0+mXKbzIA8NWbDGSsjo43BvlUnVJRxRsThHlZUUIGkJqkIzttFToFDh8+zNNPP83m9CS2ZCRRV1fH448/zpaMJEDyY4IQL6y4T2pqYgKfDE0wfG2KkydP8uMf/5hf/fHP/Pqtdv71Rz/i5JtvYv14BIC0pOC8scUX0LW7ivjOcr6pcnocb1v/eQIV5Z1pYMSKBwtCLLDihGz1KlfS659PXuD3fcnUne3F9ovv8+HPvk/d2V5+/lECJ88PAwv0yBZRQNde+xQc8RTFtVFTZKHMK1xBzBOoKK8fS1I8WBCizIoSMtXpZMjxFxScOIF3L1+le0LHff/tf/OF//pdeiZ09I25VjMVnAw4/ozqdAY3+IIL6EJ+VZ3m2fn5VB02g7WdOeupa5rfYNYAAAISSURBVOdxFxjBcmwWr2yJigcLQpRZUUI2NjzAh68dI3ly1Od48yUdJy75XorkyVHaXz3G2PBAcIMHW0DXj6ZKTShXFkTdokDzzEaYiwcLQqyyooRsTaaBwkceYywxfd62Y4npmL7xGGsyDRGyxlX2rcxiptETyjWaIzSXICxvVpSQAVxbwNa58Uhus2s6hoUiamye+pKewrlhJFaLBwtCmFlxQjY8EWTOCxiZmIqgJQBW2j0JMXsth2Zk4BeKf3HfcBcPFoTYZMUJ2ZRTDbrtApounNI6bDVFWMrc+bFDcCTk0HJmcd/SOpVGs5Xqgulc3LH9/sl+dzHfRvO0PYqCUtZGjU1FaqgIsc6yKD6ifXDffA9WHJmY4v+cvDCvSOkU+F93bQp6L1l8sbTFgxfy9xGEYFnRBXrTkhL4/NaMedt9fmvGMhUxpHiwsOxYcUIGkPLH5ylZc5lVAe4IX6VTKFlzmZQ/Ph8Fy8KPFA8WVgIr6ukXHnJ334lhy1aKV2fQ3jtG/5grqa9PSWC7MQXdtTT69Mvj0kjxYGElsDw+rQtk82d3eX82bUyd2SApy6dNvFNap6LWRdsKQYgcKzK0FARhebHsPDIpPSYIKw/xyARBiHtEyARBiHuWRWgpmywFYWUjHpkgCHFP3Hhkg8OjvOe+w3rn9jwy0wNsmxAEYUUSN0I2eX2Snv4B78+CIAge/j8UQ8AdT/eHsAAAAABJRU5ErkJggg==)

### 4.1 ./conf/config.yaml

```yaml
port: 8123
version: "v1.2.3"
```

### 4.2 gin中使用viper案例

- 这里用一个demo演示如何在gin框架搭建的web项目中使用`viper`，使用viper加载配置文件中的信息
- 并在代码中直接使用`viper.GetXXX()`方法获取对应的配置值。

```go
package main
import (
	"fmt"
	"github.com/fsnotify/fsnotify"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
)

func main() {
	// 第一：viper配置
	viper.AddConfigPath(".")       // 还可以在工作目录中查找配置
	viper.SetConfigName("config")  // 配置文件名称(无扩展名)
	viper.SetConfigType("yaml")    // 如果配置文件的名称中没有扩展名，则需要配置此项
	viper.AddConfigPath("./conf/") // 指定查找配置文件的路径

	err := viper.ReadInConfig() // 读取配置信息
	if err != nil {             // 读取配置信息失败
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}

	// 第二：实时监控配置文件的变化
	viper.WatchConfig()
	viper.OnConfigChange(func(e fsnotify.Event) {
		// 配置文件发生变更之后会调用的回调函数
		fmt.Println("Config file changed:", e.Name)
	})

	// 第三：读取配置
	r := gin.Default()
	r.GET("/version", func(c *gin.Context) {
		c.String(http.StatusOK, viper.GetString("version"))
	})
	r.Run()
}
```

### 4.3 结构体变量保存配置

```go
package main

import (
	"fmt"
	"github.com/spf13/viper"
)

type Config struct {
	Port    int    `mapstructure:"port"`
	Version string `mapstructure:"version"`
}

var Conf = new(Config)

func main() {
	// 第一：viper配置
	viper.AddConfigPath(".")       // 还可以在工作目录中查找配置
	viper.SetConfigName("config")  // 配置文件名称(无扩展名)
	viper.SetConfigType("yaml")    // 如果配置文件的名称中没有扩展名，则需要配置此项
	viper.AddConfigPath("./conf/") // 指定查找配置文件的路径

	err := viper.ReadInConfig() // 读取配置信息
	if err != nil {             // 读取配置信息失败
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}

	// 第二：将读取的配置信息保存至全局变量Conf
	if err := viper.Unmarshal(Conf); err != nil {
		panic(fmt.Errorf("unmarshal conf failed, err:%s \n", err))
	}
	fmt.Printf("Conf:%#v\n", Conf) // 打印
}
/*
Conf:&main.Config{Port:8123, Version:"v1.2.3"}
 */
```

