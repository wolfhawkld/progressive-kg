---
schema_version: '1.1'
title: Metropolis-Hastings算法
aliases:
- Metropolis-Hastings
- MH算法
- MCMC采样
summary: 以提议和接受拒绝构造马尔可夫链，从已知至常数比例的目标分布采样
type: concept
maturity: growing
confidence: high
tags:
- MCMC
- 采样
- 贝叶斯推断
created: '2026-08-17'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://academic.oup.com/biomet/article-abstract/57/1/97/284580
- https://www.osti.gov/biblio/4390578
- https://www.cs.cmu.edu/~epxing/Class/10708-19/notes/lecture-14/
- https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B
---

# Metropolis-Hastings算法

> 以提议和接受拒绝构造马尔可夫链，从已知至常数比例的目标分布采样。

## 核心思想

设目标密度只能写成未归一化形式 $\pi(x)=\tilde\pi(x)/Z$，提议核为 $q(x'\mid x)$。MH 用容易抽样的候选状态，加上接受拒绝校正提议核的偏差：

$$
\alpha(x,x')=\min\left(1,\frac{\tilde\pi(x')q(x\mid x')}{\tilde\pi(x)q(x'\mid x)}\right).
$$

因为 $Z$ 在比值中约去，所以不需要显式计算配分函数；但必须能评价目标密度的相对值，并且提议应覆盖目标分布的有效支持。

## 算法流程与平稳性

1. 选择初始状态 $x^{(0)}$ 和提议分布 $q(\cdot\mid x)$。
2. 在第 $t$ 步从 $q(x'\mid x^{(t)})$ 生成候选 $x'$。
3. 生成 $u\sim Uniform(0,1)$；若 $u\leq\alpha(x^{(t)},x')$，接受候选，否则保持原状态。
4. 重复迭代，使用经过适当预热后的相关样本估计期望。

接受概率使转移核满足详细平衡：

$$\tilde\pi(x)q(x'\mid x)\alpha(x,x')=\min\{\tilde\pi(x)q(x'\mid x),\tilde\pi(x')q(x\mid x')\},$$

右侧关于 $x,x'$ 对称。因此在链满足不可约、非周期等遍历条件时，目标分布是平稳分布，遍历平均才会收敛到目标期望。链上的相邻样本通常相关，不应表述为独立同分布样本。

### 一个数值例子

目标未归一化密度为 $\tilde\pi(x)=\exp(-x^2/2)$，使用对称提议。在当前状态 $x=0$ 提议 $x'=1$ 时，

$$\alpha=\min(1,e^{-1/2})\approx0.607.$$

若提议 $x'=-0.5$，则接受率为 $1$；这体现了向高密度区域移动总是接受，而向低密度区域移动只按概率接受。

## 变体与权衡

- **随机游走 Metropolis**：$x'=x+\epsilon$，实现简单，但步长过小会混合慢，过大又会导致拒绝率高。
- **对称提议**：若 $q(x'\mid x)=q(x\mid x')$，接受率简化为 $\min(1,\tilde\pi(x')/\tilde\pi(x))$，即 Metropolis 原始算法。
- **独立提议**：$q(x')$ 不依赖当前状态，可能在尾部或高维空间产生大量拒绝。
- **梯度方法**：HMC、MALA 和 NUTS 用梯度改善高维探索，但需要可用且稳定的目标梯度。

## 边界与应用

- **后验采样**：贝叶斯后验常只知道似然乘先验的未归一化形式，MH 可绕开边际似然的显式积分。
- **统计物理**：目标为吉布斯分布时，接受率可写成能量差和温度的函数。
- **收敛限制**：有限步数没有“已经收敛”的自动证明；不可约性破坏、提议支持不足、强相关或多峰目标都会造成混合慢和有效样本量低。
- **优化区别**：MH 的目标是从固定分布采样；模拟退火通过改变温度把采样过程转成搜索低能量解。

## 关系网络

- 组成：[[马尔可夫链蒙特卡洛（MCMC）]] — MH 是 MCMC 的基本算法
- 相关：[[吉布斯采样]] — 吉布斯采样是 MH 的特例/替代
- 依赖：[[马尔可夫链]] — MH 构造的采样链是马尔可夫链
- 应用：[[贝叶斯推断]] — 后验采样是 MH 的主要用途
- 相关：[[退火算法]] — 接受准则同源，SA 借用了 Metropolis 接受机制
- 相关：[[配分函数]] — MH 只需未归一化目标，通常不必计算配分函数

## 参考资料

- [Monte Carlo sampling methods using Markov chains and their applications](https://academic.oup.com/biomet/article-abstract/57/1/97/284580) — Hastings 对 Metropolis 方法的推广、理论和误差评估
- [Equation of State Calculations by Fast Computing Machines](https://www.osti.gov/biblio/4390578) — Metropolis 等人的原始算法论文记录
- [Approximate Inference: Markov Chain Monte Carlo](https://www.cs.cmu.edu/~epxing/Class/10708-19/notes/lecture-14/) — 大学课程中的 MH、Gibbs 算法和接受率说明
- [马尔可夫链蒙特卡洛 - 维基百科](https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B) — 思想、Metropolis-Hastings、吉布斯采样、收敛评估
- [Metropolis-Hastings algorithm - Wikipedia](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) — 算法推导与变体
