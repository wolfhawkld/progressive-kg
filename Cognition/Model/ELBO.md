---
schema_version: '1.1'
title: ELBO
aliases:
- Evidence Lower Bound
- 证据下界
- 变分下界
summary: 由变分分布构造的对数边际似然下界，其与对数证据之差为近似后验到真实后验的KL散度
type: concept
maturity: seed
confidence: high
tags:
- 近似推断
- 优化目标
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://arxiv.org/html/1601.00670v9
---

# ELBO

> 由变分分布构造的对数边际似然下界，其与对数证据之差为近似后验到真实后验的KL散度。

## 下界与 KL 分解

给定观测 $x$、隐变量 $z$、固定模型 $p(x,z)$ 与归一化变分分布 $q(z)$，定义：

$$\mathcal L(q)=\mathbb E_q[\log p(x,z)]-\mathbb E_q[\log q(z)].$$

在对数证据有限、相关期望和 KL 可定义的条件下：

$$\log p(x)=\mathcal L(q)+D_{\mathrm{KL}}(q(z)\Vert p(z\mid x)).$$

- KL 非负，所以 $\mathcal L(q)\leq\log p(x)$；下界对象是**对数证据**。
- $q$ 等于真实后验（几乎处处）时取等号。
- 若 $q$ 对真实后验零概率的区域赋正概率，KL 可为无穷，不能把所有表达式当作有限数运算。

## 为什么可以优化它

固定模型和数据后，$\log p(x)$ 不随 $q$ 变化，因此最大化 ELBO 等价于最小化到真实后验的 $D_{\mathrm{KL}}(q\Vert p)$。

利用 $p(x,z)=p(x\mid z)p(z)$，也可写成：

$$\mathcal L(q)=\mathbb E_q[\log p(x\mid z)]-D_{\mathrm{KL}}(q(z)\Vert p(z)).$$

它平衡对数据的解释与偏离先验的程度。避开显式计算证据不意味着所有期望都容易计算；仍可能需要解析推导或采样估计。

## 一个二状态算例

本页构造 $p(x,z=0)=0.2$、$p(x,z=1)=0.3$，于是 $p(x)=0.5$，真实后验为 $(0.4,0.6)$。取 $q=(0.5,0.5)$，使用自然对数：

$$\mathcal L(q)=\tfrac12\log(0.2/0.5)+\tfrac12\log(0.3/0.5)
\approx-0.71356.$$

对数证据 $\log0.5\approx-0.69315$，差约 $0.02041$，恰好是 $D_{\mathrm{KL}}((0.5,0.5)\Vert(0.4,0.6))$。

## 使用边界

ELBO 是优化目标，不是自动保证推断正确的证书。

- 分布族过窄时，即使优化达到最优，仍可能有近似误差。
- 同时改变模型参数时，证据也会变化；“ELBO 上升意味着后验 KL 必然下降”只适用于固定模型。
- 单次随机估计值可能高于真实对数证据；下界性质属于精确期望目标。
- 比较不同模型的 ELBO 还受各自近似间隙影响，不能直接视为精确证据排名。

## 关系网络

- 应用：[[变分推断]] — ELBO 是常用的后验近似优化目标
- 前置：[[KL散度]] — KL 非负性给出下界与间隙
- 前置：[[信息熵]] — $-\mathbb E_q\log q$ 是目标中的熵项
- 相关：[[贝叶斯推断]] — 目标涉及证据和隐变量后验
- 相关：[[EM算法]] — 精确E步把变分下界贴到当前观测对数似然
- 相关：[[变分自编码器]] — ELBO 是 VAE 常用的训练目标

## 参考资料

- [Blei、Kucukelbir、McAuliffe：Variational Inference: A Review for Statisticians](https://arxiv.org/html/1601.00670v9) — 第 2.2 节：ELBO 定义、KL 分解与似然—先验形式

## 变更记录

- 2026-09-11：补充本批数学与AI新节点的反向关联；保留原verified，本次仅核验新增关系。
