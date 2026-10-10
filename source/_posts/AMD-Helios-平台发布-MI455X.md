---
title: AMD Helios 平台正式发布：MI455X 72 卡成箱，正面硬刚 NVIDIA Rubin
cover: /img/cover42.png
date: 2026-10-10 10:00:00
categories:
- Tech前沿
tags:
- AI芯片
- AMD
- MI455X
---

## 不再"卖单卡"，AMD 把整个机架变成武器

在 Advancing AI 2026（2026 年 7 月 23 日）上，AMD 一口气推出第六代 EPYC CPU、Instinct MI400 系列 GPU，以及其首款机架级 AI 方案 **Helios**——号称"全球性能最强的 AI 机架"。其中旗舰芯片 **MI455X** 是 AMD 迄今最具野心的数据中心 GPU：它从设计之初就不是为了做一张独立显卡，而是作为 72 卡机架中的一块拼图——这与 NVIDIA NVL72 的思路如出一辙。

Helios 将于 2026 下半年开始出货，直接对标 NVIDIA 的 GB300 NVL72 与下一代 Rubin 平台。对长期被 NVIDIA CUDA 生态压制的 AI 基础设施市场来说，这是 AMD 第一次在"机架级"维度上正面叫板。

## MI455X：432GB HBM4、3200 亿晶体管

单看芯片，MI455X 的规格相当激进：

```
AMD Instinct MI455X（Helios 核心 GPU）
├─ 架构        → 第 5 代 CDNA（CDNA 5），异构 chiplet
├─ 工艺        → 计算 die: TSMC 2nm / I/O die: TSMC 3nm
├─ 晶体管      → ~3200 亿（跨整个封装）
├─ 显存        → 432 GB HBM4
├─ 带宽        → ~19.6 TB/s
└─ FP4 算力    → 40 PFLOPS / 卡
```

相比上一代 MI355X，MI455X 在 4-bit 与 8-bit 矩阵运算上性能最高提升 **4 倍**——这也是它主打低精度推理/微调的原因。432GB HBM4 的显存容量甚至超过单颗 NVIDIA Rubin（288GB），为更大模型的原地加载提供了可能。

## Helios 机架：2.9 ExaFLOPS 的"成箱算力"

真正拉开差距的是整机柜表现。**Helios** 将 72 颗 MI455X 与 18 块第六代 EPYC CPU 整合为一台统一机柜：

| 指标 | Helios（72 卡） |
|------|-----------------|
| FP4 算力 | 2.9 ExaFLOPS |
| FP8 算力 | 1.4 ExaFLOPS |
| HBM4 总量 | 最高 31 TB |
| 内存带宽 | 最高 ~1.67 PB/s（聚合） |

作为对比，NVIDIA 的 GB300 NVL72 机架约 1.08 ExaFLOPS FP4；而 Rubin NVL72 则达到 3.6 ExaFLOPS。Helios 在纸面参数上介于两者之间——以略低于 Rubin 的算力，换取了**更高的单机柜 HBM4 总容量**（31TB vs 20.7TB），这对长上下文、大 batch 推理是实打实的优势。

## ROCm：AMD 真正的胜负手

硬件规格容易追赶，生态才是护城河。MI455X 与 Helios 建立在 **ROCm** 开源软件栈之上，主打"开放、标准一致、可虚拟化分区"——从超大规模部署到主权云（sovereign cloud）与研究环境，模型、工具与运维保持一致性。AMD 的策略很明确：不硬碰 CUDA 的成熟度，而是用开放标准和 TCO（总拥有成本）来争取那些受 GPU 供应紧张和高昂算力成本困扰的企业客户。

对国内开发者而言，ROCm 对 PyTorch/JAX 的支持已相当完善，迁移成本正在降低——这与 ROCm 一贯"让代码在 AMD 上跑起来"的定位一脉相承。

## 影响与展望

Helios 的意义在于：AMD 承认了前沿 AI 训练必须在"机架级"思考，而非单卡内卷。它给市场带来了 NVIDIA 之外真正可规模化的第二选择，尤其在 HBM4 容量、开放生态和成本三个维度上形成差异化竞争力。

不过，理论跑分能否转化为真实世界的吞吐与运营成本，仍是出货后的大问号——CUDA 的生态黏性、第三方 ISV 适配、以及大规模集群的工程稳定性，都是 AMD 必须跨越的坎。但对整个行业而言，一个真正多极化的 AI 算力市场，对厂商和开发者都绝非坏事。

> 参考来源：AMD 官方新闻稿《AAI 2026: AMD Delivers Full-Stack Compute for the Agentic AI Era》、AMD Instinct MI455X 产品页与宣传册、ServeTheHome「Hot Chips 2026」技术详解及多家硬件媒体规格分析。
