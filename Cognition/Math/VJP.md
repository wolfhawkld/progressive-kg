---
schema_version: '1.1'
title: VJP
aliases:
- Vector-Jacobian Product
- 向量-雅可比积
- VJP原语
summary: 反向传播的计算原语，用上游梯度向量与雅可比矩阵相乘回传梯度
type: concept
maturity: seed
confidence: medium
tags:
- 自动微分
- 反向传播
- 雅可比矩阵
created: '2026-08-17'
updated: '2026-08-17'
verified:
review_due:
sources:
- https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html
- https://zh.wikipedia.org/zh-hans/%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86
---

# VJP

> 反向传播的计算原语，用上游梯度向量与雅可比矩阵相乘回传梯度。

## 核心思想

VJP（Vector-Jacobian Product，向量-雅可比积）是反向传播（reverse-mode 自动微分）的基本计算单元：

- **定义**：对函数 $f: \mathbb{R}^n \to \mathbb{R}^m$，反向模式需要计算 $v^T J_f$，其中 $J_f$ 是 $f$ 的雅可比矩阵（$m \times n$），$v$ 是上游梯度向量
- **关键优势**：不需要显式构造整个雅可比矩阵，直接计算 $v^T J_f$，一次反向传播成本与正向相近
- **反向模式**：从输出向输入传播梯度，正是神经网络训练的标准方式

## 为什么不用雅可比矩阵

直接构造雅可比矩阵效率极低：

- 对 $f: \mathbb{R}^n \to \mathbb{R}^m$，雅可比是 $m \times n$ 矩阵，$n$ 大时无法存储
- **JVP（正向模式）**：计算 $J_f v$，适合"输入少、输出多"
- **VJP（反向模式）**：计算 $v^T J_f$，适合"输入多、输出少"——恰好是损失函数标量化的情形
- **深度学习选择**：损失是标量（$m=1$），VJP 每次传播所有参数的梯度，因此反向传播用 VJP

## 实现

现代自动微分框架将每个算子实现为 VJP 规则：

- **PyTorch**：`torch.autograd` 的每个节点通过 backward 定义 VJP
- **JAX**：`jax.vjp(f, x)` 返回 VJP 函数
- **框架原则**：算子只需定义"上游梯度如何变成下游梯度"，即可自动组合

## 关系网络

- 组成：[[反向传播]] — VJP 是反向传播的计算原语
- 依赖：[[雅可比矩阵]] — VJP 本质是梯度向量与雅可比矩阵的积
- 应用：[[链式法则]] — 多层 VJP 复合即链式法则的矩阵形式
- 应用：[[向量]] — VJP 作用于向量值函数

## 参考资料

- [The Autodiff Cookbook - JAX](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html) — JVP/VJP 概念与实现
- [自动微分 - 维基百科](https://zh.wikipedia.org/zh-hans/%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86) — 前向/反向模式与计算图
