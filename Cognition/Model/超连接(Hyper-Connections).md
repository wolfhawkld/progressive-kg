---
schema_version: '1.1'
title: 超连接（Hyper-Connections）
aliases:
- Hyper-Connections
- HC
- mHC
- Manifold-Constrained Hyper-Connections
summary: 把单一残差流扩展为多个并行流并用可学习映射混合的连接机制，mHC 用双随机矩阵约束保证其稳定
type: concept
maturity: growing
confidence: high
tags:
- 模型架构
- 残差连接
- 梯度
created: '2026-08-11'
updated: '2026-08-11'
verified: '2026-08-11'
review_due: '2027-08-11'
sources:
- https://arxiv.org/abs/2409.19606
- https://arxiv.org/abs/2512.24880
---

# 超连接（Hyper-Connections）

> 把单一残差流扩展为多个并行流并用可学习映射混合的连接机制，mHC 用双随机矩阵约束保证其稳定。

超连接（Hyper-Connections, HC）由 ByteDance 于 2025 年提出，是残差连接（Residual Connection）的推广：把单一残差向量扩展为 n 个并行流（典型 n=4），每层用可学习的 Res-Mapping / Pre-Mapping / Post-Mapping 混合这些流。DeepSeek 的 mHC（Manifold-Constrained Hyper-Connections）在此之上施加双随机矩阵约束，恢复稳定性。

## 为什么需要它：残差连接的瓶颈

残差连接自 2016 年 ResNet 提出后，连接机制本身几乎十年未变——模块内部（注意力、FFN）进化巨大，但"一个残差向量逐层线性累加、不允许内部信息交换"成了表达力上限。

- 标准残差只提供恒等捷径，解决梯度路径问题
- 但它不允许残差流内部的信息重组/混合
- LayerNorm 管的是单层激活的**幅度稳定**，管不了跨层混合的**结构**是否良态

超连接的目标是突破这个表达力瓶颈：让 n 个并行残差流之间自由交换信息，增强表达力而不显著增加每层 FLOPs。

## 核心机制

HC 把残差流从单一向量扩展为 n 个并行组件，每层用三个可学习映射混合：

- **Pre-Mapping**：把 n 个输入流混合成单个流，送入注意力/FFN 模块
- **Post-Mapping**：把模块的单个输出流再分配回 n 个并行流
- **Res-Mapping**：把 n 个输入流重新混合成 n 个输出流（含跨流信息交换）

关键点：**HC 不改变注意力/MoE 模块本身的计算，改变的是这些模块的输入与输出（残差路径）**。

```
标准残差:  x → F(x) → + → 单流
HC:       [x1,x2,x3,x4] → Pre/Res/Post Mapping → [y1,y2,y3,y4]   (n个并行流)
```

## HC 的问题与 mHC 的修复

HC 的无约束混合矩阵在深层模型上会破坏稳定性：

- 混合矩阵无约束 → 残差流偏离恒等映射
- 信号/梯度在深层层叠后爆炸或消失
- HC 在中小模型效果好，但在前沿大模型（如 27B）约 12000 步后 loss 发散、梯度范数失控

### mHC：双随机矩阵约束

mHC 保留 HC 全部表达能力，同时恢复恒等保证。做法是把残差混合矩阵约束到**双随机矩阵流形**（Birkhoff polytope），用 **Sinkhorn-Knopp** 算法硬投影：

| 约束 | 含义 |
|------|------|
| 所有元素非负 | 避免信号抵消 |
| 每行之和 = 1 | 每个输出流收到等量输入信号 |
| 每列之和 = 1 | 每个输入流等量贡献给输出 |

由此获得关键性质：

- **谱范数 ≤ 1**：非扩张映射，信号/梯度不爆炸
- **组合封闭**：双随机矩阵相乘仍双随机，多层相乘仍稳定
- **全局恒等**：全局保留 identity-like 残差，同时信息自由混合

当 n=1 时，约束退化为标量 1，恰好恢复原始恒等残差——**mHC 是残差的严格推广**。

## 与 LayerNorm 的本质区别

| | LayerNorm | HC/mHC |
|---|---|---|
| 层面 | 单层、局部 | 跨层、全局 |
| 控制对象 | 单层激活尺度（幅度） | 残差流混合方式（结构/流形） |
| 解决的问题 | 幅度的梯度爆炸/消失 | 结构坍缩、失稳、表达力 |
| 是否增加表达力 | 否 | 是 |

两者**互补而非替代**：模型越大越深，只靠"每层尺度稳定"不够，还需要"跨层混合结构化、可扩展"。这就是在 norm 之外研究 HC/mHC 的根本原因——把梯度控制的战场从"单层尺度"推进到"跨层流形"。

## 关系网络
- 扩展：[[残差连接]] — HC 是残差连接的多流推广，mHC 是残差的严格推广
- 对比：[[归一化层]] — LayerNorm 管单层幅度，HC/mHC 管跨层结构
- 相关：[[梯度消失与梯度爆炸]] — HC 无约束会加剧，mHC 通过谱范数约束缓解
- 应用：[[Transformer架构]] — 残差路径被替换为 HC/mHC，模块内部不变

## 参考资料

- [Hyper-Connections (ByteDance, arXiv:2409.19606)](https://arxiv.org/abs/2409.19606) — HC 原始论文：多流残差与表达力
- [mHC: Manifold-Constrained Hyper-Connections (arXiv:2512.24880)](https://arxiv.org/abs/2512.24880) — mHC：双随机矩阵约束与 Sinkhorn-Knopp

- [[raw/human_ai_knowledge/add-norm-vs-hc-mhc-residual-connections.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/add-norm-vs-hc-mhc-residual-connections.html) - add+norm 与 HC/mHC 的幅度 vs 结构控制分析
