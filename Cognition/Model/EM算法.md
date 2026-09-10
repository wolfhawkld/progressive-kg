---
schema_version: '1.1'
title: EM算法
aliases:
- Expectation-Maximization
- EM Algorithm
- 期望最大化算法
summary: 在含隐变量或缺失数据的模型中交替计算期望并最大化参数似然的迭代算法
type: concept
maturity: seed
confidence: high
tags:
- 统计推断
- 最大似然
- 隐变量
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://doi.org/10.1111/j.2517-6161.1977.tb01600.x
- https://www.cs.cmu.edu/~epxing/Class/10708-19/notes/lecture-06/
---

# EM算法

> 在含隐变量或缺失数据的模型中交替计算期望并最大化参数似然的迭代算法。

EM（Expectation-Maximization）把难以直接最大化的观测数据似然，转化为对隐变量后验加权的完整数据目标。它常用于混合模型、隐马尔可夫模型和含缺失值的概率模型。

## 两步迭代与单调性

设观测为 $x$、隐变量为 $z$、参数为 $\theta$。给定旧参数 $\theta^{(t)}$，E 步计算

$$
q^{(t)}(z)=p(z\mid x,\theta^{(t)}),
$$

M 步最大化

$$
Q(\theta\mid\theta^{(t)})
=\mathbb E_{q^{(t)}(z)}[\log p(x,z\mid\theta)],
\qquad
\theta^{(t+1)}=\arg\max_\theta Q(\theta\mid\theta^{(t)}).
$$

### 理论保证与实际优化

在模型和期望计算满足条件、M 步精确最大化时，观测数据对数似然不会下降。这个保证不等于找到全局最优：EM 通常只收敛到局部极值或鞍点附近。广义 EM 只要使 $Q$ 不下降即可，但需要重新核对相应收敛条件。

## 可复算例子

考虑两个 Bernoulli 成分，观测数据为 $(1,1,0)$。初始混合权重 $\pi=0.5$，成分成功概率 $\theta_1=0.8,\theta_2=0.2$。

### 一次 E 步和 M 步

对 $x=1$，成分 1 的责任度为

$$
\gamma_1(1)=\frac{0.5\times0.8}{0.5\times0.8+0.5\times0.2}=0.8;
$$

对 $x=0$，$\gamma_1(0)=0.2$。于是三条样本的责任度为 $(0.8,0.8,0.2)$，M 步给出

$$
\pi'=\frac{1.8}{3}=0.6,\qquad
\theta_1'=\frac{0.8+0.8}{1.8}\approx0.889,\qquad
\theta_2'=\frac{0.2+0.2}{1.2}\approx0.333.
$$

这只是一次迭代；继续 E/M 步并检查似然或参数变化，才是完整拟合流程。

## 边界与关系

- 初值会影响收敛到的局部解，常用多次随机初始化并比较最终目标值。
- 隐变量模型的参数化若允许退化，似然可能无界；还要处理标签置换、数值下溢和不完全 M 步。
- EM 是似然优化方法，不自动给出后验不确定性；若要完整贝叶斯推断，需要额外的先验和推断方法。

## 关系网络

- 应用：[[高斯混合模型]] — GMM 用 EM 估计混合权重、均值和协方差
- 对比：[[变分推断]] — VI 优化分布族，EM 交替优化隐变量期望和参数
- 前置：[[最大似然估计]] — EM 常用于含隐变量的最大似然估计
- 相关：[[贝叶斯推断]] — EM 的似然优化与贝叶斯后验推断目标不同
- 相关：[[ELBO]] — 精确E步把变分下界贴到当前观测对数似然
- 相关：[[隐马尔可夫模型]] — Baum–Welch是HMM参数学习中的EM实例
- 相关：[[重参数化技巧]] — EM 对隐变量取期望并更新参数，重参数化直接估计可微期望梯度

## 参考资料

- [Dempster、Laird、Rubin：Maximum Likelihood from Incomplete Data Via the EM Algorithm](https://doi.org/10.1111/j.2517-6161.1977.tb01600.x) — EM 的一般框架、似然单调性与收敛理论
- [CMU：Learning Partially Observed Graphical Models and the EM Algorithm](https://www.cs.cmu.edu/~epxing/Class/10708-19/notes/lecture-06/) — 隐变量图模型上的 E/M 步推导

## 变更记录

- 2026-09-11：新建 seed 概念页；Bernoulli 混合模型的一次迭代和收敛边界已核验。
