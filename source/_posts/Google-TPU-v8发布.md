---
title: Google TPU v8发布：一分为二，为"智能体时代"量身定制的AI芯片
cover: /img/cover42.png
date: 2026-09-22 10:00:00
categories:
- Tech前沿
tags:
- AI芯片
- Google TPU v8
---

# Google TPU v8发布：一分为二，为"智能体时代"量身定制的AI芯片

过去十年，Google 的张量处理器（TPU）一直遵循一个朴素理念：**一颗芯片同时兼顾训练与推理**。从第一代到第七代 Ironwood，无论模型规模如何膨胀、负载如何分化，Google 都试图用同一块硅片把预训练、微调和在线服务串起来。

但到了第八代，这个信念动摇了。2026年4月22日的 Google Cloud Next 大会上，Google 首次把 TPU 线拆成**两颗独立芯片**——专为训练打造的 **TPU 8t** 和为推理而生、面向"智能体时代"的 **TPU 8i**。这不是简单的迭代，而是对 AI 算力需求分化的正式承认：当 Agent 开始连续调用工具、检索、多轮推理时，"一颗通吃"的时代结束了。

## 一、为什么必须拆分？"智能体"改变了负载画像

要理解这次拆分的意义，先要看现代工作负载发生了什么变化。

传统大模型部署是"一问一答"的同步模式：训练阶段追求峰值算力（FLOPS-bound），推理阶段则越来越**受内存带宽和通信延迟主导**。而 Agent 系统的出现让这个问题进一步恶化——它们需要在一次请求中完成数十次工具调用、跨多个专家模块（MoE）的路由、以及长上下文的 KV cache 管理。这种"all-to-all"的通信模式，让传统拓扑结构的网络直径成为新的瓶颈。

Google 的应对是**彻底放弃通用化**：训练和推理不再是同一颗芯片的两个模式，而是两种截然不同的硅片。

## 二、两颗芯片的技术拆解

### TPU 8t：预训练的吞吐怪兽

TPU 8t 面向大规模预训练和 embedding 密集型负载，关键规格如下：

| 参数 | TPU 8t |
|------|--------|
| 主要负载 | 大规模预训练 |
| 网络拓扑 | 3D Torus（可扩展至单 superpod 9,600 颗芯片） |
| HBM 容量 | 216 GB，带宽 6,528 GB/s |
| 片上 SRAM (Vmem) | 128 MB |
| FP4 峰值算力 | 12.6 PFLOPS |
| 专用单元 | SparseCore（Embeddings）+ LLM Decoder Engine |

TPU 8t 引入了两个关键机制：**SparseCore** 专门卸载 embedding 查找中不规则的内存访问，避免矩阵乘法单元在数据依赖的 collectives 上空转；**LLM Decoder Engine** 则加速自回归路径。此外，它首次支持 **TPUDirect RDMA** 和 **TPU Direct Storage**，让芯片直接通过 NIC 与 HBM、以及高速存储（如 10T Lustre）通信，绕过 CPU host 瓶颈——训练数据得以"线速"喂入，保证硅片始终满负载。

### TPU 8i：为推理和 Agent 而生

TPU 8i 面向采样、服务和并发推理，规格与 8t 形成鲜明对比：

| 参数 | TPU 8i |
|------|--------|
| 主要负载 | 采样、服务、推理 |
| 网络拓扑 | Boardfly（单 pod 1,152 颗芯片） |
| HBM 容量 | 288 GB，带宽 8,601 GB/s（约为 8t 的 1.3 倍） |
| 片上 SRAM (Vmem) | 384 MB（前三代的三倍） |
| FP4 峰值算力 | 10.1 PFLOPS |
| 专用单元 | CAE（Collectives Acceleration Engine） |

TPU 8i 最聪明的设计在于**超大 SRAM**。在长上下文解码中，KV cache 可以直接留在片上而非溢出到 HBM——384MB 的容量正是为推理模型的生产级 KV cache 足迹量身定制。配合新的 **Boardfly 拓扑**（网络直径缩小约 56%、collective 延迟降低 5 倍）和 **CAE** 加速跨芯片同步，TPU 8i 专门应对 MoE 路由中那种密集的全对全通信。

## 三、系统级协同：Arm Axion 成为新的"粘合剂"

第八代 TPU 的另一大变化是**首次统一采用 Google 自研的 Arm Axion CPU 作为 host**。Axion 基于 Neoverse N3（Armv9.2）核心架构，为两颗芯片提供统一的编排底座。

对推理密集的 TPU 8i，Google 将 Axion host 与 TPU 的比例提升到 **2:1**——每服务器物理 CPU 主机数量翻倍，配合严格的 NUMA 架构做工作负载隔离，彻底消除数据预处理的瓶颈。这意味着过去"CPU host 拖慢超快 TPU 硅片"的老问题，在第八代基本被根治。

```
# 对开发者而言：迁移成本几乎为零
# JAX / PyTorch / Keras 代码无需改写即可跨芯片运行
import jax
from jax.experimental.pjit import pjit

# 同一份代码，TPU 8t 负责训练分片，TPU 8i 负责推理服务
model = train_on(tpu_8t_cluster, dataset)
serve(model, on=tpu_8i_pod)   # Boardfly 拓扑自动优化 all-to-all
```

## 四、性能数字与行业意义

Google 给出的官方对比（相对第七代 Ironwood）：

- **TPU 8t**：训练价格提升 **2.7 倍**
- **TPU 8i**：推理价格提升 **80%**
- 两颗芯片均实现最高 **2 倍**的每瓦性能提升
- 单集群可支持 **100 万+ TPU** 协同工作

这些数字背后的战略信号更值得玩味。Google 并未将 TPU 视为 NVIDIA 的正面替代品——相反，它承诺今年晚些时候将在自家云提供 NVIDIA Vera Rubin，并与 NVIDIA 合作优化开源网络栈 **Falcon**。这揭示了一个现实：**超大规模厂商正在构建"自研芯片 + NVIDIA 补充"的混合架构**，而非彻底二选一。

对开发者来说，真正的看点在于：当训练与推理被拆成两种专门优化的硅片，AI 基础设施正式从"堆通用算力"迈向"**按负载定制硅片**"的时代。这既是 Google 对 Agent 时代的最强回应，也预示着通用 AI 加速器的黄昏正在到来。
