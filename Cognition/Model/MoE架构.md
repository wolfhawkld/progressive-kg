---
schema_version: '1.1'
title: MoE架构 (Mixture of Experts)
aliases:
- MoE
- Mixture of Experts
- 混合专家模型
summary: 用路由器为每个 token 选择少量专家，在不激活全部参数的情况下扩展模型容量
type: concept
maturity: growing
confidence: high
tags:
- 模型架构
- 稀疏模型
- LLM
created: '2026-07-08'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2027-01-16'
sources:
- https://arxiv.org/abs/2101.03961
- https://arxiv.org/abs/2006.16668
- https://arxiv.org/abs/2401.04088
---

# MoE架构 (Mixture of Experts)

> 用路由器为每个 token 选择少量专家，在不激活全部参数的情况下扩展模型容量。

稀疏 MoE（Mixture of Experts）通常用多个专家替换 Transformer 的 FFN，并让路由器只为每个 token 选择少量专家。这样总参数量可以远大于每 token 激活参数量，但权重存储、路由和跨设备通信仍可能成为训练与推理瓶颈。

核心思想

```
y = Σ_{i=1}^{n} G(x)_i * E_i(x)
```

- **专家 (Experts)**: 多个独立的子网络（通常是FFN）
- **门控网络 (Router/Gate)**: 决定每个输入激活哪些专家
- **稀疏激活**: 每个输入只激活Top-k个专家（通常k=1或2）

## 关键组件

MoE 层需要同时定义专家计算、token 路由和容量约束；只描述专家 FFN 还不足以确定系统行为。

### 专家层

```
每个专家是一个FFN:
E_i(x) = W_2 * activation(W_1 * x)
```

- 专家数量、结构和大小由模型设计决定；同层专家常同构，但不是定义要求

### 门控网络 (Router)

```
logits = x W_g
S = TopK(logits, k)
G_S(x) = Softmax(logits_S)
```

- 计算每个专家的得分
- 只保留Top-k个专家
- Softmax归一化选中的专家得分

### 辅助损失 (Auxiliary Loss)

**问题**: 专家负载不均衡，部分专家过载/闲置

**常见方案**: 添加负载均衡损失、限制容量、调整路由噪声，或采用不依赖辅助损失的均衡策略

```
L_aux = α · N · Σ_i f_i p_i   （Switch Transformer 示例）
```

- $f_i$ 表示实际路由到专家 $i$ 的 token 比例，$p_i$ 表示平均路由概率
- 公式因路由算法而异，不能把“变异系数平方”当成所有 MoE 的统一定义

## 训练技巧

训练稳定性主要取决于容量分配、路由均衡和跨设备通信，三者需要联合调试。

### 容量因子 (Capacity Factor)

```
expert_capacity ≈ ceil(tokens * k / num_experts * capacity_factor)
```

- 控制每个专家处理的最大token数
- 超额 token 可被丢弃、转给备选专家或由无丢弃实现动态处理，策略取决于系统

### 专家并行 (Expert Parallelism)

- 不同专家分布在不同设备
- 需要All-to-All通信
- 与数据并行结合

### 路由策略

- **Top-k路由**: 选择得分最高的k个专家
- **Expert Choice**: 专家选择token（非token选专家）
- **BASE**: 最优传输理论的路由

## 代表设计

| 工作 | 路由特征 | 说明 |
|---|---|---|
| Switch Transformer | Top-1 | 简化路由，并系统研究容量与负载均衡 |
| GShard | Top-2 | 展示超大规模条件计算与专家并行 |
| Mixtral 8x7B | 每 token 选择 8 个专家中的 2 个 | 开放权重稀疏 MoE 的代表实现 |

## 优势与挑战

稀疏激活降低每 token 的专家计算，但总权重、路由和通信成本仍由整个系统承担。

### 优势
- **条件计算**: 每 token 的专家计算量小于激活全部专家
- **扩展性**: 可持续增加专家数量
- **潜在专业化**: 专家可能形成一定分工，但路由模式不一定对应人类可解释领域

### 挑战
- **训练不稳定**: 路由收敛问题
- **负载均衡**: 需要辅助损失
- **通信开销**: 分布式训练的All-to-All通信
- **内存占用**: 总参数量大，需要更多显存

## 与稠密模型对比

| 特性 | MoE | 稠密模型 |
|-----|-----|---------|
| 每 token 激活参数 | 可远小于总参数 | 等于所用层的全部参数 |
| 路由与通信 | 有额外路由、容量和 All-to-All 问题 | 无专家路由开销 |
| 推理速度 | 激活 FLOPs 可较低，但权重读取、批量和通信可能抵消收益 | 更容易使用规则、成熟的 dense kernels |
| 权重内存 | 必须容纳或分片全部专家权重 | 容纳稠密权重 |
| 训练/微调 | 需处理负载、专家退化和并行布局 | 通常更直接，但成本取决于模型规模 |

## 关系网络
- [[Transformer架构]] - MoE通常替换FFN层
- [[分布式训练]] - 专家并行策略
- [[参数高效微调]] - MoE的微调挑战

## 参考资料

- [Switch Transformers](https://arxiv.org/abs/2101.03961) — Top-1 路由、容量与辅助损失
- [GShard](https://arxiv.org/abs/2006.16668) — 条件计算与专家并行
- [Mixtral of Experts](https://arxiv.org/abs/2401.04088) — Top-2 of 8 的开放 MoE 架构
