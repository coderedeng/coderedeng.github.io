---
title: NVIDIA发布Vera Rubin NVL72：336B晶体管与20.7TB HBM4的AI工厂革命
cover: /img/cover42.png
date: 2026-09-05 10:00:00
categories:
- Tech前沿
tags:
- AI芯片
- NVIDIA Vera Rubin
- NVL72
---

# NVIDIA发布Vera Rubin NVL72：336B晶体管与20.7TB HBM4的AI工厂革命

## 一、从"卖芯片"到"造工厂"：NVIDIA的战略跃迁

当AMD MI400用432GB HBM4正面硬刚、Intel Gaudi4押注18A制程试图成为"第三极"时，NVIDIA没有选择在同一维度上缠斗。CES 2026上，黄仁勋发布了被称为"AI超级计算机"的Vera Rubin平台——它不是单颗GPU，而是由六颗协同设计的芯片组成的机架级系统。

这一转变的核心逻辑在于：现代推理模型的成本瓶颈已从"算力"转移到"数据搬运"。万亿参数模型的预填充（prefill）和解码（decode）阶段需要跨越数百块GPU移动海量激活值，网络带宽和显存容量才是真正卡脖子的一环。Vera Rubin正是围绕"内存墙"问题重构的产物。

## 二、六芯协同：Vera Rubin平台的完整架构

Vera Rubin平台由六颗芯片组成，形成完整的计算-互联-存储闭环：

| 芯片 | 角色 | 关键规格 |
|------|------|----------|
| Rubin GPU | AI算力核心 | 336B晶体管、TSMC N3P、288GB HBM4、50 PFLOPS NVFP4推理 |
| Vera CPU | 主机CPU/数据编排 | 88颗Olympus Arm核心、176线程、227B晶体管 |
| NVLink 6 Switch | 机架内scale-up互联 | 单芯片28 TB/s带宽 |
| Spectrum-6 Ethernet | 机架间scale-out网络 | 共封装光学（CPO） |
| Vera Memory Accelerator | CPU扩展显存 | 最高1.5TB SOCAMM LPDDR5X、1.2 TB/s带宽 |
| Rubin CPX | 推理预填充专用芯片 | NVL144 CPX机架达8 exaFLOPS |

其中Rubin GPU采用与Blackwell B200类似的双reticle die设计（两块巨型计算die + I/O die），通过TSMC CoWoS-L先进封装集成。这是全球首颗晶体管数量突破3360亿的商用芯片，单包即配备8层HBM4、288GB容量和22 TB/s带宽。

## 三、NVL72机架：重新定义"AI工厂"的技术细节

Vera Rubin NVL72将72块Rubin GPU与36块Vera CPU整合进一台液冷机柜，形成完整的算力单元：

```
┌─────────────────────── Vera Rubin NVL72 ──────────────────────┐
│                                                                │
│   [NVLink 6 Switch ×9]  ←→  260 TB/s scale-up 带宽             │
│         ↑                                                      │
│   72× Rubin GPU (288GB HBM4 each)                              │
│        = 20.7TB 总HBM4 · 1.6 PB/s 显存带宽                      │
│                                                                │
│   36× Vera CPU (Olympus Arm, 54TB LPDDR5X)                     │
│        ↑                                                       │
│   NVLink C2C: 1.8 TB/s (CPU↔GPU相干互联，翻倍自NVLink 5)       │
│                                                                │
│   scale-out: Spectrum-6 + 共封装光学 → DGX SuperPod（8机架）    │
└────────────────────────────────────────────────────────────────┘
```

关键性能指标全面碾压上一代Blackwell：

- **推理算力**：3.6 exaFLOPS NVFP4，单GPU 50 PFLOPS，是GB200的5倍
- **训练算力**：2.5 exaFLOPS NVFP4，为Blackwell的3.5倍
- **成本效率**：每百万token推理成本最高降低10倍，所需GPU数量减少至1/4
- **部署速度**：免线缆模块化托盘设计，单机架安装约5分钟（Blackwell时代需约2小时）

## 四、Rubin CPX：破解"长上下文"推理的结构性创新

Vera Rubin平台最具结构意义的创新是独立的Rubin CPX芯片。它专门处理推理的预填充阶段——即模型摄入超长prompt时的计算密集环节。这一阶段是FLOPS-bound（算力受限），而解码阶段则是内存带宽受限，两者需要不同的优化策略。

将144块Rubin CPX与144块标准Rubin GPU、36块Vera CPU组合成NVL144 CPX机架后，系统可达8 exaFLOPS NVFP4算力、100TB高速内存和1.7 PB/s聚合带宽。NVIDIA称其AI性能是GB300 NVL72机架的7.5倍，代价是约370kW的功耗（标准NVL72约为120-130kW）。

## 五、影响与未来展望：AI芯片竞争进入"系统级"时代

Vera Rubin的发布标志着AI芯片竞争从"单卡性能"全面升级为"机架级系统工程"。当AMD和Intel仍在GPU单点技术上追赶时，NVIDIA已经用"极端协同设计"（extreme co-design）构建起一道由封装、内存、互联共同组成的护城河。

对行业而言，三个趋势值得关注：

1. **HBM4成为标配**：SK海力士、三星、美光三家供应商在2026年6月获得NVIDIA认证，HBM4产能竞赛正式开启
2. **"AI工厂"概念落地**：免线缆模块化托盘和零宕机维护设计，让数据中心运维从"小时级"压缩到"分钟级"
3. **推理成本重构**：10倍token成本下降意味着大模型部署的经济门槛被大幅拉低，有望加速Agent和长上下文应用的普及

随着Vera Rubin NVL72在2026年下半年进入量产，AI算力市场的三足鼎立格局（NVIDIA Rubin / AMD MI400 / Intel Gaudi4）已初步形成。而真正决定胜负的，或许不再是谁的晶体管更多，而是谁能把每一瓦电力、每一块钱成本都转化为可用的推理算力。
