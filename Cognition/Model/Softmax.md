---
title: Softmax
summary: 将实数向量映射为概率分布的指数归一化函数，输出和为1且各项非负
level: concept
category: Cognition/Model
tags: [激活函数, 注意力机制, 概率归一化, 多分类, Transformer]
related:
  - "[[注意力机制]]"
  - "[[激活函数]]"
  - "[[反向传播]]"
  - "[[flash-attention]]"
  - "[[内积]]"
created: 2026-07-13
last_verified: 2026-07-13
confidence: high
status: stable
---

# Softmax

> 将实数向量映射为概率分布的指数归一化函数，输出和为 1 且各项非负。

---

## 定义与公式

Softmax 接收任意实数向量 z = [z₁, ..., zₙ]，输出概率分布 p = [p₁, ..., pₙ]，满足 pᵢ > 0 且 Σ pᵢ = 1。

- **公式**：pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)
- **输入**：任意实数向量（logits，无范围限制）
- **输出**：概率分布（每项 ∈ (0,1)，全体和为 1）
- **单调性**：更大的输入 logit 对应更大的输出概率，但非线性——差异被指数放大

### 完整推导

给定 logits z₁, ..., zₙ，softmax 做了三步：

```
1. 指数化：e^{z₁}, e^{z₂}, ..., e^{zₙ}     （映射到正数域）
2. 求和：S = e^{z₁} + e^{z₂} + ... + e^{zₙ}  （归一化分母）
3. 归一化：pᵢ = e^{zᵢ} / S                    （得概率分布）
```

指数函数保证：
- 即使 logit 为负，概率仍为正（e^{-∞} → 0 但永不为 0）
- logit 之间的差值被指数放大，最大 logit 获得压倒性概率
- 不像 sigmoid（独立处理每个值），softmax 的竞争性质让所有输出互相约束

---

## 数值稳定性与 Log-Sum-Exp 技巧

直接计算 exp(zᵢ) 会在 |zᵢ| 较大时溢出。标准做法是先减最大值，结果不变。

- **朴素计算**：pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ) —— zᵢ 为 1000 时溢出
- **稳定计算**：pᵢ = exp(zᵢ - max(z)) / Σⱼ exp(zⱼ - max(z)) —— 完全等价，`zᵢ - max ≤ 0` 不会溢出
- **log-softmax**：log(pᵢ) = zᵢ - max(z) - log(Σⱼ exp(zⱼ - max(z))) —— 输出 log 概率，用于计算交叉熵时避免 exp/log 重复

### 稳定性的数学证明

两边除分子分母各除 exp(max(z)) 不影响比值：

```
pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ) = [exp(zᵢ) / exp(max)] / [Σⱼ exp(zⱼ) / exp(max)] = exp(zᵢ - max) / Σⱼ exp(zⱼ - max)
```

### 数值示例

```
z = [1000, 2, 1]
朴素 exp(1000) = ∞ → NaN
稳定: z - max = [0, -998, -999]
     exp = [1.0, ~0, ~0]
     p  = [1.0, ~0, ~0]
```

---

## 在注意力机制中的应用

Softmax 是 [[注意力机制]] 的归一化核心。在 Scaled Dot-Product Attention 中：

```
Attention(Q, K, V) = softmax(Q·Kᵀ / √d) × V
```

- **Q·Kᵀ**：Query 和 Key 的 [[内积]] — 计算每个位置"关注"其他位置的程度
- **/√d**：缩放 — 防止大维度导致内积值过大（softmax 梯度在 logits 绝对值大时趋零）
- **softmax**：将注意力分数归一化为概率权重（每行的权重和 = 1）
- **× V**：按权重聚合 Value

### 为什么需要 √d 缩放

| dₖ 太小 | dₖ 很大 |
|---|---|
| Q·Kᵀ 值适中 | Q·Kᵀ 值很大（方差 ~dₖ） |
| softmax 梯度正常 | softmax 趋近于 one-hot（梯度趋零） |
| 注意力分布较均匀 | 注意力集中到单个位置 |

√d 缩放让 softmax 的输入方差保持 ~1，使注意力分布在"太分散"和"太集中"之间保持平衡。

---

## 与交叉熵损失的关系

Softmax 几乎总是和交叉熵损失（Cross-Entropy Loss）配对使用。在 PyTorch 中，`nn.CrossEntropyLoss` 内部已经包含了 softmax——不需要在外面手动加。

```
L = -log(p_correct) = -log(softmax(z)[correct_class])
  = -z_correct + log(Σⱼ exp(zⱼ))
```

### 梯度之美

当 softmax + cross-entropy 联合使用时，反向传播的梯度有极简形式：

```
∂L/∂zᵢ = pᵢ - yᵢ
```

其中 yᵢ 是 one-hot 标签（正确类为 1），pᵢ 是预测概率。梯度 = 预测 - 标签，不需要单独计算 softmax 的导数——这就是为什么几乎所有框架的交叉熵损失都把 softmax 内置的原因。

---

## 温度参数

温度 τ 控制 softmax 输出的"软硬"程度：

```
pᵢ = exp(zᵢ / τ) / Σⱼ exp(zⱼ / τ)
```

| τ 值 | 效果 | 适用场景 |
|---|---|---|
| τ < 1（低温） | 概率更集中，趋近 argmax | 确定性推理 |
| τ = 1（默认） | 标准 softmax | 训练、标准推理 |
| τ > 1（高温） | 概率更均匀，趋近均匀分布 | 知识蒸馏（教师软化标签）、采样多样性 |

### 知识蒸馏中的温度

在 [[知识蒸馏]] 中，教师模型用高 τ 产生"软标签"：

```
y_teacher = softmax(z_teacher / τ)    # τ=4→20，输出更平滑的类间关系
y_student = softmax(z_student / τ)    # 学生也用相同 τ
```

软标签携带的信息远多于 one-hot——例如"2 像 3 但不像 7"这种类间关系只有软标签能传递。

---

## 关系网络

- 依赖 [[注意力机制]] — softmax 是 Attention 的归一化核心
- 关联 [[激活函数]] — softmax 是多分类输出层的标准激活
- 依赖 [[反向传播]] — softmax+CE 联合梯度 = p - y，极简形式
- 关联 [[flash-attention]] — Flash Attention 的核心优化就是 Online Softmax + Tiling
- 依赖 [[内积]] — softmax 在 Attention 中作用于 Q·Kᵀ 内积

---

## 参考资料

- [[raw/human_ai_knowledge/transformer-vs-mamba-architecture.md]] — Transformer 架构中 softmax 的核心作用
- [[raw/human_ai_knowledge/kimi-attention-residuals.md]] — Softmax 归一化保证 hidden-state 有界
- Bridle, J. S. (1990). "Probabilistic Interpretation of Feedforward Classification Network Outputs" — softmax 首次引入神经网络
