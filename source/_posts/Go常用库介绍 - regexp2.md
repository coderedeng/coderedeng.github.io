---
title: regexp2
index_img: /img/cover2-21.png
date: 2022-06-23 22:02:41
categories: 
- Go常用库
tags:
- Go常用库
---

# 21.regexp2

## 01.regexp2

- Regexp2：https://blog.csdn.net/dianxin113/article/details/118769094
- GitHub：https://github.com/dlclark/regexp2

```go
package main

import (
	"fmt"
	"github.com/dlclark/regexp2"
)

func Regexp2GroupMatch(m *regexp2.Match, re *regexp2.Regexp) [][]string {
	var matches [][]string
	for m != nil {
		var ret []string
		gps := m.Groups()
		for index, g := range gps {
			if index == 0 {
				continue
			}
			ret = append(ret, g.Captures[0].String())
		}
		matches = append(matches, ret)
		m, _ = re.FindNextMatch(m)
	}
	return matches
}

func CompileRegexp(regex string) (*regexp2.Regexp, error) {
	msgRegexp, e := regexp2.Compile(regex, 0)
	if e != nil {
		fmt.Println(e)
	}
	return msgRegexp, nil
}

func main() {
	str := "2022-8-12 2023-8-11"
	expr := "(\\d{4})-(\\d{1,2})-(\\d{1,2})" // [[2022 8 12]]
	reg, _ := CompileRegexp(expr)
	m, _ := reg.FindStringMatch(str)
	ret := Regexp2GroupMatch(m, reg)
	fmt.Println(ret) // [[2022 8 12] [2023 8 11]]
}
```
