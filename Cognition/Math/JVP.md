---
schema_version: '1.1'
title: JVP
aliases:
- Jacobian-Vector Product
- 雅可比-向量积
summary: 计算雅可比矩阵与输入方向向量的乘积，得到向量函数沿该方向的一阶变化
type: concept
maturity: seed
confidence: high
tags:
- 方向导数
- 计算图
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- https://docs.jax.dev/en/latest/_autosummary/jax.jvp.html
- https://docs.jax.dev/en/latest/jacobian-vector-products.html
---

# JVP

> 计算雅可比矩阵与输入方向向量的乘积，得到向量函数沿该方向的一阶变化。

## 方向导数与维度

给定可微函数 $f:\mathbb R^n\to\mathbb R^m$、输入点 $x$ 和方向 $v\in\mathbb R^n$：

$$\operatorname{JVP}_f(x;v)=J_f(x)v
=\left.\frac{d}{dt}f(x+tv)\right|_{t=0}\in\mathbb R^m.$$

- $v$ 不必归一化，其长度也影响返回值大小。
- $f(x+\epsilon v)\approx f(x)+\epsilon J_f(x)v$ 是局部一阶近似，不能替代有限距离上的真实变化。
- 计算 JVP 可以逐算子传播切向量，不要求显式构造整个 $m\times n$ 雅可比矩阵。

## 一个可复算的例子

本页取 $f(x_1,x_2)=(x_1x_2,x_1^2+x_2)$、$x=(2,3)$、$v=(1,-1)$：

$$J_f(x)=\begin{pmatrix}3&2\\4&1\end{pmatrix},\qquad
J_f(x)v=\begin{pmatrix}1\\3\end{pmatrix},\qquad f(x)=(6,7).$$

### JAX 对应写法

```python
import jax
import jax.numpy as jnp


def f(x):
    return jnp.stack((x[0] * x[1], x[0] ** 2 + x[1]))

x = jnp.array([2.0, 3.0])
v = jnp.array([1.0, -1.0])
y, tangent = jax.jvp(f, (x,), (v,))
# y = [6, 7]，tangent = [1, 3]
```

`primals` 与 `tangents` 的结构和对应数组形状应匹配；这里的 tuple 表示函数的位置参数。

## 与 VJP 的选择

两者是同一局部线性映射的正向作用与转置作用，输入向量所在空间不同。

| 运算 | 输入向量维度 | 输出维度 | 常见用途 |
|---|---:|---:|---|
| JVP：$J_fv$ | $n$ | $m$ | 少数输入方向的敏感性 |
| VJP：$J_f^Tu$ | $m$ | $n$ | 标量目标的参数梯度 |

只求一个输入方向时，即使输入维度很大，JVP 也可能合适；“输入少用前向”主要是构造完整雅可比时的成本判断。

## 关系网络

- 前置：[[雅可比矩阵]] — JVP 是该矩阵作用于方向向量
- 前置：[[链式法则]] — 复合函数通过逐层 JVP 传播
- 相关：[[自动微分]] — JVP 是前向模式的基本运算
- 对比：[[VJP]] — 回传的是输出端权重，维度与方向不同

## 参考资料

- [JAX：jax.jvp](https://docs.jax.dev/en/latest/_autosummary/jax.jvp.html) — 输入、切向量与返回值的接口契约；2026-09-11 查阅
- [JAX：Forward- and reverse-mode autodiff](https://docs.jax.dev/en/latest/jacobian-vector-products.html) — 前向传播与 VJP 的关系
