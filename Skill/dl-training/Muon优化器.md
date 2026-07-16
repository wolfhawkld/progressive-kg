---
schema_version: '1.1'
title: Muon Optimizer（Muon 优化器）
aliases:
- Muon
- Muon Optimizer
summary: 对二维隐藏层参数的动量更新做 Newton–Schulz 后处理，以平衡更新矩阵的奇异方向尺度
type: concept
maturity: growing
confidence: high
tags:
- 优化器
- 矩阵正交化
created: '2026-04-21'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2026-10-16'
sources:
- https://kellerjordan.github.io/posts/muon/
---

# Muon Optimizer（Muon 优化器）

> 对二维隐藏层参数的动量更新做 Newton–Schulz 后处理，以平衡更新矩阵的奇异方向尺度。

## 核心边界

Muon（MomentUm Orthogonalized by Newton–Schulz）面向神经网络隐藏层的二维参数矩阵。它先形成 SGD-momentum 类更新，再用少量矩阵乘法对更新做 Newton–Schulz 后处理。

它不是“把模型权重变成正交矩阵”，也不是对 embedding、输出头、bias 或 normalization 参数统一替代 AdamW。常见配置会把这些参数留给 AdamW。

## 算法骨架

对二维参数 $W$ 和梯度 $G_t$：

```text
B_t = μ B_{t-1} + G_t          # 具体实现可带 Nesterov 形式
O_t = NewtonSchulz5(B_t)       # 近似平衡奇异方向
W_t = W_{t-1} - η · scale · O_t
```

原始实现使用经过缩放的五次多项式迭代，以 BF16 友好的矩阵乘法近似极分解/矩阵“zeroth power”方向。系数和归一化是算法定义的一部分，不能用任意经典 Newton–Schulz 公式替换后仍假设行为一致。

## 几何直觉

若 $B=U\Sigma V^T$，理想化的极因子为 $UV^T$。它保留左右奇异向量，同时压平非零奇异值的尺度。

- Adam 对坐标元素做自适应缩放。
- Muon 利用二维矩阵结构，在奇异方向层面重塑更新。
- 这种几何差异不等于“Adam 把张量展平”或“Muon 一定是最速下降”；最速方向取决于所选范数和局部模型。

## 参数分组

一个安全起点是显式白名单：

| 参数 | 常见优化器 |
|---|---|
| hidden linear/attention/MLP 的二维权重 | Muon 候选 |
| embedding 与 vocabulary/output head | AdamW 或经验证的专门规则 |
| bias、norm scale、其他一维参数 | AdamW |
| 卷积核、高阶张量 | 先定义 reshape 语义并做消融，不应机械套用 |

共享权重、转置权重和分片参数还要保证参数身份与优化器状态一致。

## 工程检查

1. 以作者参考实现核对 NS 系数、迭代次数、矩阵缩放和更新尺度。
2. 分开记录 Muon/AdamW 参数组的学习率与 weight decay。
3. 在分布式分片下确认每次矩阵乘是否拿到算法所需的完整维度，或使用等价分布式实现。
4. 报告端到端 step time，而不是只报 NS FLOPs；通信、矩阵形状和 batch token 数会改变开销。
5. 与调优充分的 AdamW/SGD 基线按相同 token、数据和算力比较。

公开基准中的加速或 loss 改善只对相应模型、训练预算和实现成立，不能写成固定 35% 或 48% 的通用收益。

## 关系网络

- 基于 [[动量]] — 先累积历史梯度，再处理二维更新
- 使用 [[正交]] — 近似极因子，但不把模型权重强制正交
- 使用 [[奇异值]] — 后处理压平更新矩阵的奇异值尺度
- 对比 [[梯度下降优化]] — 属于带特定矩阵几何的优化方法
- 关联 [[分布式训练]] — 参数分片和矩阵通信会影响实现

## 参考资料

- [Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) — 作者定义、参数范围、NewtonSchulz5 与实验边界
