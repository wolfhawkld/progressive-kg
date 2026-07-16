---
schema_version: '1.1'
title: Flash Attention
aliases:
- FlashAttention
- Flash-Attention
summary: 通过分块和在线 Softmax 减少显存读写、且不物化完整注意力矩阵的精确注意力算法
type: concept
maturity: growing
confidence: high
tags:
- 注意力机制
- GPU
- 推理优化
created: '2026-07-08'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2026-10-16'
sources:
- https://arxiv.org/abs/2205.14135
- https://arxiv.org/abs/2307.08691
- https://arxiv.org/abs/2407.08608
---

# Flash Attention

> 通过分块和在线 Softmax 减少显存读写、且不物化完整注意力矩阵的精确注意力算法。

## 核心定义

FlashAttention 是一种 IO-aware 的精确注意力算法。它把 Q、K、V 分块搬入片上 SRAM，在块内计算，并以在线 Softmax 状态逐步合并结果，从而避免把完整的 $N\times N$ 注意力分数和概率矩阵写回高带宽显存（HBM）。

这里的“精确”指它计算的是标准注意力，而不是稀疏或低秩近似；由于浮点运算重排，数值末位仍可能与朴素实现不同。

## 为什么能加速

标准注意力为：

$$
O=\operatorname{softmax}\left(\frac{QK^T}{\sqrt d}\right)V
$$

朴素实现往往把 $QK^T$、Softmax 概率等 $O(N^2)$ 中间结果写入 HBM，再为后续操作读回。GPU 上这些数据搬运可能比矩阵乘本身更限制速度。

FlashAttention 的关键不是减少标准注意力的算术量，而是让中间结果尽量停留在更快但更小的片上存储中，并减少 HBM 往返。

## 在线 Softmax

对一行分数分块处理时，维护有限维状态：

- $m$：目前见过的最大值
- $\ell$：以 $m$ 为基准缩放后的指数和
- $o$：对应的未归一化输出累加器

读入新块并得到局部最大值 $m_b$ 后，先令 $m'=\max(m,m_b)$，再把旧状态按 $e^{m-m'}$ 缩放，把新块贡献按 $e^{m_b-m'}$ 合并。这样无需预先看到整行，也能得到数值稳定的 Softmax 归一化结果。

这个有限状态使得每个 Query 块可以依次扫描 K/V 块，而不必保存完整注意力矩阵。

## 分块执行

典型前向过程是：

1. 从 HBM 载入一个 Q 块。
2. 依次载入 K/V 块，在 SRAM 中计算局部分数与局部输出。
3. 用运行中的最大值、归一化因子和输出累加器合并各块。
4. 只把最终输出和反向传播所需的少量统计量写回 HBM。

片上工作集由块大小控制，但总计算仍随序列长度增长：每个 Q 块仍需扫描相关 K/V 块。因此它没有与序列长度“完全解耦”。

## 复杂度与边界

| 指标 | 朴素标准 Attention | FlashAttention |
|---|---:|---:|
| 算术复杂度 | $O(N^2d)$ | $O(N^2d)$ |
| 额外注意力矩阵内存 | $O(N^2)$ | $O(N)$ 级行统计与输出状态 |
| HBM 交互 | 反复物化、读写中间矩阵 | 通过 tiling 显著减少中间读写 |
| 数学算子 | 标准精确注意力 | 标准精确注意力 |

实际加速取决于序列长度、head dimension、掩码、数据类型、GPU 架构和 kernel 实现；不能概括成固定倍数，也不能保证所有形状都从 memory-bound 变为 compute-bound。

## 版本脉络

| 工作 | 主要贡献 |
|---|---|
| FlashAttention | 提出 IO-aware tiling 与精确注意力 kernel |
| FlashAttention-2 | 改进工作划分和并行化，减少非矩阵乘开销 |
| FlashAttention-3 | 面向 Hopper 异步执行与低精度能力进一步优化 |

这张表描述论文脉络，不表示所有框架、硬件或算子组合都自动使用相同实现。

## 可迁移的模式

FlashAttention 体现的是“分块 + 可合并的流式状态”：如果全局归约可以由固定大小状态递推，就可能避免物化大中间张量。在线 Softmax、Welford 方差计算等都具有这种结构；但具体能否加速仍取决于数据复用和硬件内存层次。

- 先证明局部状态能够无损合并。
- 再设计块大小，使工作集适配片上存储。
- 最后用真实 shape 测量 IO、占用率和重算开销。

## 关系网络

- 前置 [[注意力机制]] — 保持标准注意力定义，只改变执行方式
- 应用 [[Transformer架构]] — 用于 Transformer 训练、prefill 和部分解码 kernel
- 对比 [[kv-cache]] — KV Cache 复用跨解码步状态，FlashAttention 优化单次注意力执行

## 参考资料

- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608)
