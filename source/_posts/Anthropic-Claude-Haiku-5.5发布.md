---
title: Anthropic 发布 Claude Haiku 5.5：首个可调"思考档位"的小模型，价格直逼 GPT-6 Luna
cover: /img/cover42.png
date: 2026-10-10 10:00:00
categories:
- Tech前沿
tags:
- AI前沿
- Anthropic
- Claude Haiku
---

## 补齐 Claude 5.5 全家桶的最后一块

Anthropic 于 2026 年 10 月 7 日正式发布 **Claude Haiku 5.5**，这是继 Opus 5.5、Sonnet 5.5 之后 Claude 5.5 系列的最后一个成员——也是最小、最快、最便宜的一个。官方定位很明确：面向高频、成本敏感的重复性任务，如摘要、压缩（compaction）、分类、数据库查询和子代理（subagent）工作。

在 Anthropic"先大后小"的发布节奏里，Haiku 一直是那个扛量活的"打工人"。这一次，它补齐了 Claude 5.5 全家桶，也把整个小模型市场的价格锚点直接拉到了与 OpenAI GPT-6 Luna 齐平的位置。

## 定价：90% 降价，与 GPT-6 Luna 正面相遇

Haiku 5.5 的定价是本次发布最锋利的武器：

```
Claude Haiku 5.5 定价（每百万 token）
├─ ≤100K tokens: 输入 $0.10 / 输出 $0.50   ← 比 Haiku 4.5 便宜约 90%
└─ >100K tokens: 输入 $0.50 / 输出 $2.50   ← 涨价 5 倍
```

在 10 万 token 以内，Haiku 5.5 与 GPT-6 Luna 完全同价；超过之后价格翻 5 倍——而 Luna 的涨价要更晚（到 27.2 万 token）。值得注意的是 Anthropic 换上了一个"更小气"的分词器：Simon Willison 的实测显示，同一篇长 prompt 用 Haiku 5.5 会比 Haiku 4.5 多消耗约 1.25 倍 token——这意味着在长文本场景下存在"隐性涨价"。

## 首个可调 effort 的小模型：OSWorld 从 15.7% 跳到 72.4%

Haiku 5.5 是**首款支持可调节思考档位（adjustable effort）**的 Haiku 模型，用户可在成本与智能之间自行权衡。这一改变直接体现在基准成绩上——最亮眼的是计算机使用（computer use） benchmark **OSWorld 2.1**：

| 模型 | OSWorld 2.1 (离线子集) 准确率 |
|------|------------------------------|
| Haiku 4.5 | 15.7% |
| **Haiku 5.5** | **72.4%** |

近 5 倍的增长说明，小模型的能力短板此前很大程度被"固定低档位"锁死；一旦放开 effort 旋钮，其在需要多步推理的任务上立刻脱胎换骨。此外，Sonnet 5.5 的缓存读取价格也被砍半（$0.20→$0.10），使大多数 agentic 工作负载的成本再降约 20%。

## 来自真实生产环境的验证

Anthropic 展示了多家企业的早期使用数据：Asana 报告任务完成延迟降低 30%+、单 agent 轮次推理快达 2.5 倍；HubSpot 在 CRM 审计评测中取得 92.8% 的历史最高分；AlphaSense 的"Ask in Document"场景（每周约 800 万次调用）从 Haiku 4.5 的 0.76 提升到 0.84。这些数字共同指向一个结论：**Haiku 5.5 的价值不在"全能"，而在"便宜又能扛量"**。

同时，Anthropic 为 Max 和 Team 订阅用户推出每月 API credit（Max 5x 得 $100、Max 20x 得 $200、Team 最高 $500），并更新了 Python/TypeScript SDK 以 beta 形式支持 computer use 与 browser use。

## 影响与展望

Haiku 5.5 的意义在于把"可调 effort + 极低价格"带入了小模型阵营，让高频子代理、摘要和分类这类过去因成本而却步的规模化场景变得经济可行。对开发者而言，一个务实的建议是：**短任务（≤10 万 token）优先 Haiku 5.5 或 Luna，长文本则需权衡分词器涨价后再做选择**。

不过 Anthropic 也坦承，复杂 agentic 编码任务（如 Terminal-Bench 4.0 所衡量）仍应选用 Opus 5.5 与 Sonnet 5.5——Haiku 5.5 是"量活担当"而非"全能选手"。在开源权重模型与 GPT-6 Luna 双重夹击下，Anthropic 用价格战守住小模型市场的策略能否持续赢得份额，值得继续观察。

> 参考来源：Anthropic 官方公告《Introducing Claude Haiku 5.5》、Claude Platform Models Overview 文档、Simon Willison's Weblog（2026-10-07）及 VentureBeat 等媒体报道。
