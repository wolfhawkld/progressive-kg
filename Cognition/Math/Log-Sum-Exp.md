---
schema_version: '1.1'
title: Log-Sum-Exp
aliases:
- LSE
- logsumexp
summary: 对一组实数的指数和取对数，并通过平移最大值在不改变结果的前提下避免指数溢出
type: concept
maturity: growing
confidence: high
tags:
- 数值稳定性
- 概率计算
- 凸分析
created: '2026-07-13'
updated: '2026-07-17'
verified: '2026-07-17'
review_due: '2027-07-17'
sources:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html
---

# Log-Sum-Exp

> 对一组实数的指数和取对数，并通过平移最大值在不改变结果的前提下避免指数溢出。

## 定义与范围

对向量 $x\in\mathbb{R}^n$，Log-Sum-Exp（LSE）定义为：

$$
\operatorname{LSE}(x)=\log\sum_{i=1}^{n}e^{x_i}
$$

它是最大值的光滑近似，并满足：

$$
\max_i x_i\leq\operatorname{LSE}(x)\leq\max_i x_i+\log n
$$

因此，分量差距很大时 LSE 接近最大值；分量接近时，多个分量都会对结果产生贡献。

## 数值稳定计算

直接计算 $e^{x_i}$ 可能溢出。令 $m=\max_i x_i$，利用指数的平移不变关系可写成：

$$
\operatorname{LSE}(x)=m+\log\sum_i e^{x_i-m}
$$

此时每个 $x_i-m\leq0$，有限输入不会因正指数过大而溢出。工程实现还需要显式处理空输入、全部为 $-\infty$、NaN、权重为负等边界，不能只机械地套用减最大值。

```python
from scipy.special import logsumexp

value = logsumexp([1000.0, 999.0, 998.0])
```

## 与 Softmax 和交叉熵

LSE 的梯度正是 [[Softmax]]：

$$
\frac{\partial\operatorname{LSE}(x)}{\partial x_i}
=\frac{e^{x_i}}{\sum_j e^{x_j}}
$$

由此可得 $\log\operatorname{softmax}(x)_i=x_i-\operatorname{LSE}(x)$。多类 [[交叉熵]] 对类别 $y$ 的稳定形式则是：

$$
\ell(x,y)=-x_y+\operatorname{LSE}(x)
$$

这解释了框架为何通常直接接收 logits，并把 log-softmax 与负对数似然融合计算。

## 温度与光滑最大值

带温度 $\tau>0$ 的形式为：

$$
\operatorname{LSE}_\tau(x)=\tau\log\sum_i e^{x_i/\tau}
$$

- $\tau\to0^+$ 时趋近最大值。
- 较大的 $\tau$ 让多个分量更充分地参与结果。
- 若需要加权和、符号或遮罩，应使用经过测试的库实现并确认其参数语义。

## 关系网络

- 梯度 [[Softmax]] — LSE 对各输入的梯度组成 Softmax 概率向量
- 应用 [[交叉熵]] — 将分类损失写成 logits 上的稳定表达式
- 应用 [[损失函数]] — 概率模型的对数配分函数与负对数似然常使用 LSE
- 应用 [[flash-attention|FlashAttention]] — 在线 Softmax 分块维护最大值与指数和状态

## 参考资料

- [SciPy：logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html) — 稳定计算接口及权重、符号参数
- [SciPy：softmax](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html) — Softmax 与 LSE 梯度的关系
