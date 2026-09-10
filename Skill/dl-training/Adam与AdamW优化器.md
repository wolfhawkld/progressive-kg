---
schema_version: '1.1'
title: Adam与AdamW优化器
aliases:
- Adam
- AdamW
- Adaptive Moment Estimation
- Adam with Decoupled Weight Decay
summary: 用梯度的一阶矩和二阶矩的指数滑动平均自适应调整每个参数的学习率，AdamW将权重衰减从梯度更新中解耦
type: concept
maturity: growing
confidence: medium
tags:
- 优化器
- 自适应学习率
created: '2026-07-27'
updated: '2026-09-11'
verified: 2026-08-10
review_due: '2026-11-08'
sources:
- https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html
- https://arxiv.org/abs/1412.6980
- https://arxiv.org/abs/1711.05101
---

# Adam与AdamW优化器

> 用梯度的一阶矩和二阶矩的指数滑动平均自适应调整每个参数的学习率，AdamW将权重衰减从梯度更新中解耦。

## Adam 算法

Adam（Adaptive Moment Estimation）由 Kingma & Ba 于 ICLR 2015 提出。它对每个参数维护两个状态量——梯度的一阶矩估计（动量）和二阶矩估计（自适应学习率），并用指数滑动平均更新。

**算法更新规则（逐元素）：**

```text
g_t = ∇_θ L_t(θ_{t-1})              # 当前梯度

m_t = β₁·m_{t-1} + (1-β₁)·g_t       # 一阶矩（动量）
v_t = β₂·v_{t-1} + (1-β₂)·g_t²      # 二阶矩（自适应率）

m̂_t = m_t / (1 - β₁^t)              # 偏差校正
v̂_t = v_t / (1 - β₂^t)

θ_t = θ_{t-1} - η · m̂_t / (√v̂_t + ε)
```

**原论文常用默认值（不是跨任务推荐）：**
- `β₁ = 0.9`：一阶矩衰减率，控制动量记忆长度
- `β₂ = 0.999`：二阶矩衰减率，控制自适应率记忆长度
- `ε = 1e-8`：数值稳定性常数
- `η`：全局学习率，默认 1e-3

**偏差校正**是 Adam 的关键设计：初始时刻 m₀=0、v₀=0 导致估计偏向零，除以 `(1-β^t)` 校正。训练早期校正幅度大，t 增大后趋近 1。

### 几何直觉

Adam 的逐坐标缩放系数为 `η / (√v̂_t + ε)`，实际更新还乘以一阶矩 `m̂_t`。二阶矩大时缩放较小，但不能仅凭当前梯度大小判断最终更新幅度。这是一种依赖历史状态的对角预条件，并不对参数矩阵执行正交化。

- 对比标准 SGD：普通SGD通常使用共享学习率，自适应方法在某些稀疏梯度问题上有优势，但不构成普遍效率排序
- 对比动量：动量只使用一阶矩（方向平滑），Adam 额外使用二阶矩（尺度自适应）

## AdamW：解耦权重衰减

AdamW 由 Loshchilov & Hutter 于 2017 年提出，修改了 Adam 中权重衰减的实现方式。

**问题：** 在Adam梯度中加入L2惩罚时，可写为 `g_t += λ·θ_{t-1}`，但 Adam 的自适应学习率会破坏权重衰减的语义——不同参数的衰减量被 `√v̂_t` 不等比例缩放，导致衰减不再均匀。

**AdamW 修正：** 将衰减从梯度及矩估计中解耦，衰减项作用于更新前的参数：

```text
# Adam 部分与标准 Adam 完全一致
m_t = β₁·m_{t-1} + (1-β₁)·g_t
v_t = β₂·v_{t-1} + (1-β₂)·g_t²

m̂_t = m_t / (1 - β₁^t)
v̂_t = v_t / (1 - β₂^t)

# 解耦衰减作用于旧参数；不对刚算出的Adam更新再乘衰减因子
θ_t = θ_{t-1} - η · m̂_t / (√v̂_t + ε) - η·λ·θ_{t-1}
```

**实际影响：** 解耦后，衰减项不进入一阶和二阶矩状态。若先执行Adam梯度更新，再把整个新参数乘以衰减系数，还会额外缩放梯度更新项，与上式不同。泛化效果仍需在同任务和预算下比较。

### 工程检查

1. 检查实际优化器配置；当前PyTorch的Adam也提供 `decoupled_weight_decay=True` 选项，不能仅凭类名判断是否解耦。项目应记录安装版本。
2. bias、norm scale是否衰减由参数分组决定，AdamW不会自动排除这些参数。
3. 学习率、衰减、矩系数和epsilon需联合验证；增大二阶矩记忆时间不保证改善噪声问题。

## 显存核算与适用边界

优化器状态应与参数、梯度、主权重副本和临时工作区分别核算。

| 状态（普通密集实现） | 每参数常驻元素 |
|---|---|
| 无动量SGD | 通常无额外持久矩状态 |
| SGD动量 | 一个速度/动量状态 |
| Adam/AdamW | 一阶矩和二阶矩两个状态 |

若两个矩都存为FP32，仅这两项就是每参数8字节；相对于FP32参数为2倍，相对于FP16参数为4倍。这不是整个训练显存的倍数。AMSGrad、量化状态、分片和实现工作区都会改变占用。

## 关系网络

- 基于 [[梯度下降优化]] — Adam 是梯度下降的自适应变体
- 使用 [[动量]] — Adam 的一阶矩本质上就是带偏差校正的动量
- 对比 [[Muon优化器|Muon 优化器]] — Muon 对二维隐藏层参数做矩阵正交化后处理，其余参数仍用 AdamW；两者不是简单的替代关系
- 对比 [[正交]] — Adam的对角预条件不等于Muon式矩阵正交化

## 参考资料

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — 原始论文，Kingma & Ba, ICLR 2015
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) — AdamW 论文，Loshchilov & Hutter, 2017

- [[raw/human_ai_knowledge/deep-learning-metaphors.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/deep-learning-metaphors.html) - Adam 作为灵活变通年轻匠人的类比

- [官方依据](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html) — 纠正衰减顺序、PyTorch解耦选项和显存计数，去除通用超参数与胜率保证；2026-09-11核验

## 变更记录
- 2026-09-11：纠正衰减顺序、PyTorch解耦选项和显存计数，去除通用超参数与胜率保证；局部修正，保留原 verified。
