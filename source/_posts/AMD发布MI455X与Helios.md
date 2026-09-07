---
title: AMD发布MI455X与Helios：用72卡机架正面硬刚NVIDIA Vera Rubin
cover: /img/cover42.png
date: 2026-09-07 10:00:00
categories:
- Tech前沿
tags:
- AI芯片
- AMD MI455X
- Helios
---

# AMD发布MI455X与Helios：用72卡机架正面硬刚NVIDIA Vera Rubin

## 一、从"单卡对标"到"机架级对抗"：AMD的第二次豪赌

在 NVIDIA 于 CES 2026 抛出被称为"AI超级计算机"的 Vera Rubin NVL72 后，整个行业的目光都聚焦于这家绿色巨头如何用六颗协同芯片构建机架级护城河。彼时，AMD 和 Intel 仍被普遍认为停留在"单卡参数追赶"的阶段——直到 AMD 在 Advancing AI 2026 活动上正式推出 **Instinct MI455X** 与配套的 **Helios** 机架方案，才真正让竞争回到同一张牌桌。

MI455X 是 AMD MI400 系列的旗舰成员，基于全新的 **CDNA 5 架构**、采用 TSMC N2（N3P）先进制程制造。但真正让业界侧目的是它背后的 Helios：这不是一张孤立的加速卡，而是一套以机架为单位的完整 AI 计算系统。AMD 的战略意图很明确——既然在单颗 GPU 的绝对算力上难以瞬间超越 Rubin，那就用"内存容量 + 带宽 + 机架级互联"的组合拳，把竞争拉到自己熟悉的赛道。

## 二、核心规格：432GB HBM4 与 1.7 PB/s 的带宽暴力美学

MI455X 最引人注目的参数是显存。每块 GPU 配备 **432GB HBM4**，相比 NVIDIA GB200 所用的方案高出约 50%，内存带宽达到 **23.3 TB/s**。作为对照，NVIDIA Vera Rubin 单卡为 288GB HBM4、22 TB/s——AMD 在"显存容量"这一维度上明确领先。

算力方面，MI455X 支持 NVIDIA 力推的 Open Compute **MXFP4 / MXFP8** 低精度格式（而非 CUDA 生态独占的 NVFP4），峰值性能可达 **40.26 PFLOPS（MXFP4）** 与 **22.6 PFLOPS（FP32 密集）**。

而 Helios 机架才是 AMD 的真正底牌。整套系统由 **72 块 MI455X** 组成，提供：

- **总显存 31TB HBM4**
- **聚合内存带宽约 1.7 PB/s**（即 1,677,600 GB/s）
- **约 2.9 FP4 exaFLOPS 推理算力**（OCP MXFP8 下约 1.4 exaFLOPS）

这套数字直接对标 NVIDIA 的 NVL72 机架。在长上下文推理时代，模型预填充阶段本质是"带宽受限"而非"算力受限"——31TB 高速显存 + 1.7 PB/s 带宽的组合，意味着 Helios 能够把整个大模型的激活值尽量留在片上，减少跨 GPU 的数据搬运。这正是 AMD 试图绕开 NVIDIA CUDA 算力优势、在"内存墙"问题上正面突破的思路。

## 三、技术解析：机架即产品，CDNA 5 的协同设计

Helios 与 Rubin NVL72 最大的结构差异在于**互联方式**。NVIDIA 用 NVLink C2C 构建 CPU↔GPU 的缓存一致性互联；AMD 则采用 **UALink 与 Ultra Ethernet（超以太网）** 作为机架级 scale-out 的骨干，通过两块扩展板卡连接各计算节点。这种开放互联标准的意义在于：它降低了 AMD 对 proprietary 私有协议的依赖，也为多供应商生态留出了空间。

在软件层面，Helios 深度绑定 **ROCm** 平台与 AMD 自研的 **MIVisionX / MIOpen** 库，并针对 MXFP4/MXFP8 做了算子优化。AMD 反复强调其 ROCm 对开放精度格式的原生支持——这是它向 NVIDIA CUDA 生态发起挑战的核心软件抓手。

Helios 还引入了灵活的**分区与多租户能力**：一个 72-GPU 机架可被切分为从 4 块 GPU（共享同一计算托盘内的 CPU）到整柜不等的虚拟 pod，兼顾专用部署与资源共享。对云厂商而言，这意味着更高的机柜利用率和更精细的成本核算。

```
┌─────────────────────── AMD Helios Rackscale ─────────────────────┐
│  72 × Instinct MI455X (CDNA 5, 432GB HBM4 each)                   │
│   ├─ 总显存：31TB HBM4                                            │
│   ├─ 聚合带宽：~1.7 PB/s (UALink + Ultra Ethernet)                │
│   └─ 推理算力：~2.9 FP4 exaFLOPS                                  │
│                                                                   │
│  Host: AMD EPYC Gen6 CPU（提供 PCIe/协处理支持）                   │
└───────────────────────────────────────────────────────────────────┘
```

## 四、影响与未来展望：AI 芯片进入"三足鼎立"的机架时代

MI455X 与 Helios 的意义，不在于它是否立刻在跑分上击败 Rubin，而在于它**验证了"机架级开放方案"的商业可行性**。当 NVIDIA 用"极端协同设计"封装出由六颗芯片组成的系统时，AMD 选择了另一条路：用成熟制程（N3P）、开放互联标准（UALink/Ultra Ethernet）和超大显存，把"内存墙"问题转化为自身的护城河。

至此，AI 算力市场的三足鼎立格局已清晰成形：**NVIDIA Vera Rubin / AMD MI455X-Helios / Intel Gaudi4**。NVIDIA 胜在 CUDA 生态与 NVFP4 的极致优化；Intel 押注 18A 制程试图成为"第三极"；而 AMD 则用 432GB HBM4 和机架级带宽，证明了自己不再是跟随者。

对开发者而言，真正的看点在于 ROCm 能否真正接住 MXFP4/MXFP8 的开放生态——如果 AMD 的软件栈能在推理场景做到与 CUDA 相近的开发体验，那么"第二供应商"将不再是一句空话。黄仁勋用"AI工厂"重新定义了 GPU，而 AMD 正在证明：这座工厂，未必只能由一家公司建造。
