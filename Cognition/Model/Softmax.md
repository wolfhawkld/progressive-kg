---
schema_version: '1.1'
title: Softmax
aliases:
- Softmax Function
- 指数归一化
summary: 将有限实数 logits 指数归一化为各项非负且总和为1的概率向量
type: concept
maturity: growing
confidence: high
tags:
- 注意力机制
- 概率归一化
- 多分类
- Transformer
created: '2026-07-13'
updated: '2026-07-17'
verified: '2026-07-17'
review_due: '2027-07-17'
sources:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html
- https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/1503.02531
---

# Softmax

> 将有限实数 logits 指数归一化为各项非负且总和为1的概率向量。

## 定义与性质

对实数向量 $z=[z_1,\ldots,z_n]$，Softmax 定义为：

$$
p_i=\operatorname{softmax}(z)_i
=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

对有限实数输入，每项 $p_i>0$ 且 $\sum_i p_i=1$。在有限精度实现中，极小概率仍可能下溢为零。

- **平移不变**：对任意常数 $c$，$\operatorname{softmax}(z+c)=\operatorname{softmax}(z)$。
- **保持排序**：logit 较大者概率较大，但集中程度由所有相对差值共同决定。
- **非逐元素映射**：一个分量变化会通过分母影响全部输出，因此不能把 Softmax 当成普通隐藏层逐元素激活。

## 数值稳定性

直接计算大 logit 的指数可能溢出。令 $m=\max_i z_i$，利用平移不变性计算：

$$
p_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}
$$

此时所有指数的输入都不大于零。对应的 log-softmax 可写成：

$$
\log p_i=z_i-\operatorname{LSE}(z)
$$

其中 [[Log-Sum-Exp]] 应使用同样的减最大值技巧。若一整行都被掩码成 $-\infty$，简单相减会出现未定义结果；注意力实现需要单独约定这种边界。

## 在注意力中的应用

缩放点积 [[注意力机制]] 使用：

$$
\operatorname{Attention}(Q,K,V)
=\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}+M\right)V
$$

- $QK^T$ 通过 [[内积]] 形成匹配 logits。
- $1/\sqrt{d_k}$ 在常见独立同尺度近似下控制点积方差，降低 Softmax 过早饱和的风险，但不是通用梯度保证。
- 掩码 $M$ 先限制可见位置，Softmax 再在允许位置上归一化。
- [[flash-attention|FlashAttention]] 用在线 Softmax 状态避免物化完整注意力概率矩阵，数学结果仍对应标准注意力。

## 与交叉熵

互斥多类分类常把 logits 与 [[交叉熵]] 联合计算。对真实类别 $y$：

$$
\ell(z,y)=-z_y+\operatorname{LSE}(z)
$$

未加额外权重时，其梯度为 $\partial\ell/\partial z_i=p_i-y_i$。PyTorch `CrossEntropyLoss` 直接接收 logits；手工先做 Softmax 再传入会重复参数化，并放弃融合 log-softmax 的数值优势。

## 温度参数

温度 $\tau>0$ 调节概率集中程度：

$$
p_i(\tau)=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}}
$$

| 温度 | 分布变化 | 常见用途 |
|---|---|---|
| $0<\tau<1$ | 相对更尖锐 | 降低随机采样多样性 |
| $\tau=1$ | 标准 Softmax | 默认训练或推理 |
| $\tau>1$ | 相对更平滑 | 蒸馏软目标、提高采样多样性 |

在 [[知识蒸馏]] 中，教师与学生使用一致温度比较软分布；具体实现还可能按 $\tau^2$ 缩放蒸馏项以补偿梯度尺度。温度会改变概率，不应在未重新校准和评估时随意改动。

## 关系网络

- 应用 [[注意力机制]] — 把匹配 logits 归一化为 Value 的聚合权重
- 数值基础 [[Log-Sum-Exp]] — log-softmax 与稳定归一化的核心算子
- 组合 [[交叉熵]] — 多类分类中常融合为稳定的 logits 损失
- 关联 [[激活函数]] — Softmax 常用于互斥多类输出，但不是逐元素隐藏激活
- 求导 [[反向传播]] — Jacobian 耦合所有输出分量
- 优化 [[flash-attention|FlashAttention]] — 以分块在线状态重排 Softmax 的执行过程

## 参考资料

- [SciPy：softmax](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html) — 定义、稳定实现及其与 LSE 的关系
- [PyTorch：CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) — logits 与交叉熵的融合语义
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — 缩放点积注意力中的 Softmax
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) — 蒸馏温度与软目标
