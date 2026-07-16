---
schema_version: '1.1'
title: KV Cache
aliases:
- KV-Cache
- KV缓存
summary: 自回归推理中复用历史注意力层的 K/V 状态，减少重复投影计算并降低解码延迟
type: concept
maturity: growing
confidence: high
tags:
- 注意力机制
- LLM推理
- 缓存
created: '2026-07-08'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2026-10-16'
sources:
- https://huggingface.co/docs/transformers/cache_explanation
- https://arxiv.org/abs/2309.06180
---

# KV Cache

> 自回归推理中复用历史注意力层的 K/V 状态，减少重复投影计算并降低解码延迟。

## 核心定义

KV Cache（Key–Value Cache）保存每层注意力中历史 token 已计算出的 Key 和 Value。生成下一个 token 时，只需为新 token 计算 Q/K/V，再让新 Query 与缓存中的全部 K/V 做注意力计算。

它减少的是对历史 token 的重复投影和重复前向计算，不会消除新 Query 对全部历史位置的扫描。

## 推理流程

自回归推理通常分为两个阶段：

| 阶段 | 输入方式 | KV 处理 |
|---|---|---|
| Prefill | 并行处理完整 prompt | 计算并保存 prompt 的 K/V |
| Decode | 每次加入一个新 token | 只追加新 token 的 K/V |

### 单步解码

在第 $t$ 个解码位置：

1. 为新 token 计算 $Q_t,K_t,V_t$。
2. 把 $K_t,V_t$ 追加到各层缓存。
3. 用 $Q_t$ 与位置 $1\ldots t$ 的全部缓存 K 做打分，并对对应 V 加权求和。

因此，忽略隐藏维度和层数等常数后，有缓存时第 $t$ 步的注意力工作量仍为 $O(t)$。

### 复杂度边界

| 情况 | 单个后期解码步 | 生成长度为 $n$ 时的累计注意力工作量 |
|---|---:|---:|
| 无缓存，反复重算整个前缀 | $O(n^2)$ | $O(n^3)$ |
| 使用 KV Cache | $O(n)$ | $O(n^2)$ |

这是只观察序列长度的简化量级。实际延迟还受模型宽度、层数、批大小、内存带宽和所用 kernel 影响。KV Cache 的核心收益是避免重复计算历史 K/V，而不是把注意力本身变成线性累计复杂度。

## 显存占用

若不考虑对齐、分页和运行时开销，每个 token 的理论 KV 容量为：

$$
2 \times L_{\text{layers}} \times H_{KV} \times D_{head} \times B_{dtype}
$$

其中 2 分别代表 K 和 V。批大小、并行序列数和序列长度还要继续相乘；使用 GQA/MQA 时，$H_{KV}$ 小于 Query 头数，因此缓存更小。

### 示例

假设模型有 32 层、8 个 KV 头、head dimension 为 128，并用 2-byte 数据类型保存缓存：

$$
2 \times 32 \times 8 \times 128 \times 2 = 131{,}072\ \text{bytes/token}
$$

即约 128 KiB/token。单序列 2K、16K、128K token 的理论缓存分别约为 256 MiB、2 GiB、16 GiB；真实占用还会受实现和内存对齐影响。

## PagedAttention

传统服务若按最大输出长度为每个请求预留连续缓存，会产生内部碎片和过度预留。PagedAttention 把一条逻辑连续的 KV 序列映射到离散物理块，并按需分配：

- 块表维护逻辑块到物理块的映射；块大小是实现参数，并非固定为 16 token。
- 并行采样或 beam search 可共享 prompt 块，在发生分歧时使用写时复制。
- 请求结束后释放块，使服务端更容易动态组合不同长度的请求。

PagedAttention 论文在其测试模型和工作负载中报告了接近零的 KV 内存浪费，以及相对当时系统约 2–4 倍的吞吐提升；这些是实验结果，不是任意硬件与负载上的固定保证。

## Continuous Batching

连续批处理允许已完成的请求及时离开、等待的请求及时加入，减少静态批处理等待最长序列造成的空闲。它能缓解队头阻塞并提高设备利用率，但仍受 prefill/decode 调度、显存预算和服务级目标约束。

- 调度器需要在吞吐、首 token 延迟和 decode 抖动之间取舍。
- 大 prefill 可能阻塞正在 decode 的请求，因此常需分块或优先级策略。

## 容量规划

可用于 KV Cache 的显存不是“总显存减模型权重”这么简单，还需要预留激活、临时工作区、框架和通信开销。实用估算顺序是：

1. 测量模型加载后的稳定显存基线。
2. 为运行时峰值和安全余量留预算。
3. 用每 token 缓存公式估算总 token 容量。
4. 再按并发数、平均 prompt 和最大生成长度分配。

常见优化包括 KV 量化、GQA/MQA、前缀缓存、分页管理和有条件的 KV 淘汰。它们分别交换精度、模型结构、调度复杂度或可见上下文，不能视为完全无代价。

## 与其他推理优化的区别

| 方法 | 主要减少什么 | 是否改变缓存内容 |
|---|---|---|
| KV Cache | 历史 K/V 的重复计算 | 保存完整历史 K/V |
| FlashAttention | 注意力 kernel 的 HBM 数据搬运和中间矩阵物化 | 不负责跨解码步保存 K/V |
| GQA/MQA | KV 头数和缓存体积 | 改变注意力头结构，通常需对应模型设计或训练 |
| PagedAttention | KV 内存碎片和预留浪费 | 改变缓存的物理管理方式 |
| KV 淘汰/压缩 | 长上下文的缓存容量 | 可能近似化或丢弃部分历史信息 |

## 关系网络

- 前置 [[注意力机制]] — 缓存的是注意力层已经计算出的 K/V
- 应用 [[Transformer架构]] — 主要用于自回归 Transformer 的增量解码
- 对比 [[flash-attention]] — 分别优化跨步重复计算与单次注意力的内存 IO

## 参考资料

- [Hugging Face：Cache explanation](https://huggingface.co/docs/transformers/cache_explanation) — 缓存张量、位置与解码流程
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — PagedAttention 与 vLLM 的原始论文
