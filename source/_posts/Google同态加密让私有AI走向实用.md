---
title: Google让私有AI走向实用：同态加密与HEIR编译器让AI在密文上推理成真
cover: /img/cover42.png
date: 2026-08-15 15:30:00
last_modified_at: 2026-08-15 15:30:00
sticky: false
categories:
- Tech前沿
tags:
- AI前沿
- 隐私计算
- 同态加密
---

当我们在云端调用大模型或推荐系统时，一个绕不开的问题是：服务器到底"看"到了多少你的数据？上周，Google 在官方安全博客发文《How Google is making private AI practical with homomorphic encryption》，宣布其在同态加密（Fully Homomorphic Encryption, FHE）隐私 AI 推理上的最新进展——AI 可以直接在密文上完成推理，服务端从头到尾看不到你的明文数据。这篇文章迅速冲上 Hacker News 首页并收获 441 个赞，引发了密码学社区与 AI 社区的激烈讨论。

## 背景：云 AI 的"信任困境"

隐私计算领域有一个经典难题：数据的价值在于被计算，但一旦交给云端计算，就必须信任云厂商。传统的 TLS 只保护传输过程，数据到了服务器就变成明文；差分隐私又损失精度。而同态加密给出了第三条路——**直接在加密数据上做运算，解密后的结果等同于对明文计算的结果**。

这一概念自 2009 年 Gentry 的奠基性工作以来，长期停留在"理论优美、实践极慢"的阶段：密文膨胀上万倍、一次乘法运算的开销是明文的数千到数百万倍，业界普遍认为只能跑玩具模型。Google 此番高调宣布"走向实用"，靠的是一套编译器加算法的组合拳。

## HEIR：同态加密界的 LLVM

Google 开源的核心武器是 [HEIR](https://heir.dev/)（Homomorphic Encryption Intermediate Representation），一个基于 MLIR 的 FHE 编译器工具链，目标是成为"同态加密行业的标准编译器"。目前在 GitHub 上获得 810 星、153 fork，采用 Apache 2.0 协议开源，且代码库至今保持高频更新。

它的设计思路对应用户相当友好：

```python
# HEIR 的开发者视角：只需标注哪些类型是"秘密"，其余交给编译器
def recommend(user_features: secret.Vector, item_table: secret.Table):
    # 开发者按普通 Python 写逻辑
    scores = dot(user_features, item_table)
    return argmax(scores)
# HEIR 自动完成：明文程序 → FHE 中间表示 → 优化 → 目标后端代码
```

HEIR 的技术目标包括：支持 BGV、CKKS、TFHE 等所有主流 FHE 方案；生成面向 OpenFHE、Lattigo 等标准密码库的代码；为 GPU、TPU、FPGA 乃至专用 ASIC 加速器提供代码生成。对密码学研究者而言，它还是一个标准化的优化与基准测试平台——类似 LLVM 之于传统编译器。

## HE-LRM：加密推荐模型的 56 倍加速

算法层面的突破来自 Google 的论文《HE-LRM: Encrypted Deep Learning Recommendation Models using Fully Homomorphic Encryption》（arXiv:2506.18150）。推荐模型（DLRM）与 CNN 不同，其输入是稀疏的类别特征，需要在庞大的嵌入表（Embedding Table）中做私有查找，而 FHE 只支持加法和乘法，没有原生"查表"操作。

HE-LRM 给出了两个关键创新：

- **客户端数字分解压缩**：客户端对嵌入表索引做数字分解，大幅降低通信与内存开销，比此前的 SOTA 方案快 **56 倍**；
- **多嵌入打包策略**：将多张嵌入表打包进同一密文，利用 SIMD 通道并行查找。

在开源 Orion FHE 框架上的端到端实测：UCI 健康预测任务推理延迟 24 秒，Criteo 点击预测任务 228~489 秒（单线程 CPU）——听起来仍不快，但论文进一步展示，配合 GPU 和 ASIC 的 FHE 加速器，延迟可以压缩到秒级甚至亚秒级。这正是 Google 所说的："同态加密的成本开销是客观存在的，但它把隐私与能力的权衡问题，变成了一个纯粹的成本问题。"

## 技术分析：从 10⁶ 到 10 倍的开销压缩

HN 讨论中有从业者指出，FHE 推理的传统开销在 10³~10⁶ 倍之间，而 HEIR 这类编译器的参数自动选择与 SIMD 优化，可以把惩罚压缩到 10~100 倍——这是"能用"与"不能用"的分水岭。

几个值得注意的技术细节：

1. **方案选择**：Google 的路线偏向 CKKS 系（适合实数近似运算，天然契合神经网络），而非 Zama 主推的 TFHE。多位从业者认为 CKKS 在加密 AI 负载上已占据优势。
2. **保密 ≠ 可验证**：FHE 保证服务器看不到你的输入和输出，但不保证服务器"诚实地执行了你想要的计算"。计算完整性需要零知识证明等可验证计算技术补足，两者经常被混淆。
3. **算法-硬件协同**：密文运算本质是大规模多项式环运算，天然适合 GPU/TPU 并行。FHE 专用芯片（如 DARPA DPRIVE 项目推动的方向）可能才是终局。

## 影响与展望

这一方向的想象空间远超推荐系统：医疗诊断（论文中的 UCI 任务就是健康预测）、金融风控、跨境联合建模——所有"数据不能出域但又需要强大模型"的场景，都可能是 FHE 推理的落地土壤。Google 也并非孤军，Zama、Belfort 等创业公司正在同一赛道竞争。

个人观点上，我认为需要保持两点清醒：其一，Google 在隐私产品上的历史记录（如密码管理器未默认端到端加密）让部分用户对其动机存疑，但 HEIR 的开源与 Apache 2.0 协议确实给了社区审视和复用的机会；其二，10~100 倍的开销意味着短期内 FHE 推理只会出现在少数高价值、强合规的场景，而非通用大模型调用。

但方向本身几乎无可争议：当 AI 深入最敏感的数据领域，"不信任服务器也能获得服务"的密码学基础设施，会像当年的 TLS 一样，从学术奇观变成互联网的默认底座。HEIR 和 HE-LRM 让我们看到，这条路正在以超出预期的速度被铺平。

## 来源

- [Google 官方博客：How Google is making private AI practical with homomorphic encryption](https://blog.google/security/how-google-is-making-private-ai-practical-with-homomorphic-encryption/)
- [HEIR 项目官网](https://heir.dev/) / [GitHub: google/heir](https://github.com/google/heir)（Apache 2.0，810 stars）
- [HE-LRM 论文：arXiv:2506.18150](https://arxiv.org/abs/2506.18150)
- [Hacker News 讨论（441 分）](https://news.ycombinator.com/item?id=49300314)
