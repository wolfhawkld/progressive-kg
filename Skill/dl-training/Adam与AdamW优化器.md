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
updated: 2026-08-10
verified: 2026-08-10
review_due: '2026-11-08'
sources:
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

**关键参数：**
- `β₁ = 0.9`：一阶矩衰减率，控制动量记忆长度
- `β₂ = 0.999`：二阶矩衰减率，控制自适应率记忆长度
- `ε = 1e-8`：数值稳定性常数
- `η`：全局学习率，默认 1e-3

**偏差校正**是 Adam 的关键设计：初始时刻 m₀=0、v₀=0 导致估计偏向零，除以 `(1-β^t)` 校正。训练早期校正幅度大，t 增大后趋近 1。

### 几何直觉

Adam 将每个参数的更新步长调整为 `η / √v̂_t`。梯度大的方向（v̂_t 大）步长变小，梯度小的方向步长变大。这等价于对每个参数做了一种近似对角化预处理——不是使用固定的学习率，而是根据梯度历史自适应调整。

- 对比标准 SGD：SGD 对所有参数用同一学习率，在稀疏梯度场景下效率低
- 对比动量：动量只使用一阶矩（方向平滑），Adam 额外使用二阶矩（尺度自适应）

## AdamW：解耦权重衰减

AdamW 由 Loshchilov & Hutter 于 2017 年提出，修改了 Adam 中权重衰减的实现方式。

**问题：** 原版 Adam 的 L2 正则化（权重衰减）通过 `g_t += λ·θ_t` 实现，但 Adam 的自适应学习率会破坏权重衰减的语义——不同参数的衰减量被 `√v̂_t` 不等比例缩放，导致衰减不再均匀。

**AdamW 修正：** 将权重衰减从梯度更新中解耦，在 Adam 更新之后直接对参数做衰减：

```text
# Adam 部分与标准 Adam 完全一致
m_t = β₁·m_{t-1} + (1-β₁)·g_t
v_t = β₂·v_{t-1} + (1-β₂)·g_t²

m̂_t = m_t / (1 - β₁^t)
v̂_t = v_t / (1 - β₂^t)

# 唯一区别：先做 Adam 更新，然后单独做权重衰减
θ_t = θ_{t-1} - η · m̂_t / (√v̂_t + ε) - η·λ·θ_{t-1}
```

**实际影响：** AdamW 在多数任务上效果等于或优于 Adam + L2 正则化，已成为 PyTorch、HuggingFace、Transformers 等框架的默认选择。LLM 训练几乎全部使用 AdamW 而非原版 Adam。

### 工程检查

1. 确认框架中 AdamW 的 weight_decay 参数是否真的实现了解耦版本（PyTorch `torch.optim.AdamW` 是，`torch.optim.Adam` 加 weight_decay 不是）
2. AdamW 的权重衰减通常只作用于可训练权重，不对 bias、norm scale 做衰减（与 Muon 的分组策略一致）
3. 学习率预热期可以考虑禁用或降低 weight_decay，避免早期梯度噪声放大衰减影响

## 实用建议

| 场景 | 推荐配置 |
|---|---|
| 通用 CV/NLP 任务 | AdamW, lr=1e-3~3e-4, β=(0.9, 0.999), wd=0.01~0.1 |
| LLM 训练 | AdamW, lr=3e-4~1e-4, β=(0.9, 0.95), wd=0.1 |
| 小批量/高噪声 | 增大 β₂ 到 0.9999，或启用 decoupled Adam 变体 |
| 对比 Muon | Muon 替换 hidden 二维权重，其余参数仍用 AdamW |

**限制：** Adam/AdamW 的内存开销是 SGD 的两倍（额外存储 m 和 v）。对 LLM 训练，优化器状态可占模型参数内存的 2-3 倍（FP32 m 和 v + FP32 参数）。LOMO、Adafactor 等内存高效变体在资源受限时值得考虑。

## 关系网络

- 基于 [[梯度下降优化]] — Adam 是梯度下降的自适应变体
- 使用 [[动量]] — Adam 的一阶矩本质上就是带偏差校正的动量
- 对比 [[Muon优化器|Muon 优化器]] — Muon 对二维隐藏层参数做矩阵正交化后处理，其余参数仍用 AdamW；两者不是简单的替代关系
- 使用 [[正交]] — Adam 的分参数自适应可视为一种对角近似预处理，与 Muon 的矩阵级正交化形成对比

## 参考资料

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — 原始论文，Kingma & Ba, ICLR 2015
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) — AdamW 论文，Loshchilov & Hutter, 2017

- [[raw/human_ai_knowledge/deep-learning-metaphors.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/deep-learning-metaphors.html) - Adam 作为灵活变通年轻匠人的类比
