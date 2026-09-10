---
schema_version: '1.1'
title: VJP
aliases:
- Vector-Jacobian Product
- 向量-雅可比积
- VJP原语
summary: 反向模式自动微分的原语，将输出上游协向量经雅可比转置拉回输入空间
type: concept
maturity: growing
confidence: high
tags:
- 自动微分
- 反向传播
- 雅可比矩阵
created: '2026-08-17'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html
- https://docs.jax.dev/en/latest/301/cookbook.html
---

# VJP

> 反向模式自动微分的原语，将输出上游协向量经雅可比转置拉回输入空间。

## 核心思想

VJP（Vector-Jacobian Product，向量-雅可比积）是反向传播（reverse-mode 自动微分）的基本计算单元：

- **定义**：对函数 $f: \mathbb{R}^n \to \mathbb{R}^m$，在点 $x$ 的雅可比 $J_f(x)\in\mathbb{R}^{m\times n}$ 把输入扰动映射到输出扰动；给定输出空间的上游协向量 $\bar y\in\mathbb{R}^m$，VJP 返回 $J_f(x)^T\bar y\in\mathbb{R}^n$。若把协向量写成行向量，则同一式写作 $\bar y^T J_f(x)$。
- **关键优势**：不需要显式构造整个雅可比矩阵，直接计算其转置作用在上游协向量上的结果；对标量输出的函数，一次反向传播即可得到所有输入分量的梯度
- **反向模式**：从输出向输入传播梯度，正是神经网络训练的标准方式

这里的“向量”在严格表述中是余切向量（协向量）。在欧氏空间用内积把向量与协向量识别后，工程代码通常统一写成列向量的 $J^T\bar y$。

### 一个带维度的例子

令

$$f(x_1,x_2)=(x_1x_2,\,x_1+x_2),\qquad x=(2,3).$$

此时

$$J_f(x)=\begin{bmatrix}3&2\\1&1\end{bmatrix}.$$

若上游梯度为 $\bar y=(5,7)^T$，则

$$\bar x=J_f(x)^T\bar y
=\begin{bmatrix}3&1\\2&1\end{bmatrix}\begin{bmatrix}5\\7\end{bmatrix}
=\begin{bmatrix}22\\17\end{bmatrix}.$$

这说明 VJP 直接给出输出损失对 $x_1,x_2$ 的梯度贡献，而无需把整个雅可比作为中间结果保存。

## 为什么不用雅可比矩阵

直接构造雅可比矩阵效率极低：

- 对 $f: \mathbb{R}^n \to \mathbb{R}^m$，雅可比是 $m \times n$ 矩阵，$n$ 大时无法存储
- **JVP（正向模式）**：计算 $J_f v$，适合"输入少、输出多"
- **VJP（反向模式）**：计算 $J_f^T\bar y$，适合"输入多、输出少"——恰好是损失函数标量化的情形
- **深度学习选择**：损失是标量（$m=1$），VJP 每次传播所有参数的梯度，因此反向传播用 VJP

两种模式的选择取决于输入和输出的维度，不能简单理解为 VJP 总是更快。反向模式通常需要保存或重算前向中间值，因此深层网络还要在显存和计算量之间权衡。

## 复合与链式法则

若先计算 $y=f(x)$，再计算 $z=g(y)$，上游协向量为 $\bar z$，则复合函数的 VJP 按反向顺序计算：

$$\bar y=J_g(y)^T\bar z,\qquad
\bar x=J_f(x)^T\bar y.$$

这正是链式法则的矩阵形式。自动微分系统为每个原语保存局部的 pullback（拉回）规则，再沿计算图反向组合这些规则。

## 实现

现代自动微分框架将每个算子实现为 VJP 规则：

- **PyTorch**：`torch.autograd` 的每个节点通过 backward 定义 VJP
- **JAX**：`jax.vjp(f, x)` 返回 VJP 函数
- **框架原则**：算子只需定义"上游梯度如何变成下游梯度"，即可自动组合

VJP 规则必须遵守算子的真实输入输出形状；广播、归约和重复使用同一张量时，梯度需要按相应维度求和。实际框架还可能通过 checkpoint 在显存和重算之间取舍。

## 关系网络

- 组成：[[反向传播]] — VJP 是反向传播的计算原语
- 依赖：[[雅可比矩阵]] — VJP 本质是梯度向量与雅可比矩阵的积
- 应用：[[链式法则]] — 多层 VJP 复合即链式法则的矩阵形式
- 应用：[[向量]] — VJP 作用于向量值函数
- 对比：[[JVP]] — JVP 沿输入扰动正向传播，VJP 沿输出协向量反向拉回
- 组成：[[自动微分]] — 自动微分系统用局部 VJP 规则组合反向计算

## 参考资料

- [The Autodiff Cookbook - JAX](https://docs.jax.dev/en/latest/notebooks/autodiff_cookbook.html) — JVP/VJP 的维度、代价与实现
- [The Autodiff Cookbook with JVP and VJP - JAX](https://docs.jax.dev/en/latest/301/cookbook.html) — VJP 作为导数线性映射的转置及 pullback
