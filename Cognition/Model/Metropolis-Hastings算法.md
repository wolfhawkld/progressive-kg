---
schema_version: '1.1'
title: Metropolis-Hastings算法
aliases:
- Metropolis-Hastings
- MH算法
- MCMC采样
summary: 一种马尔可夫链蒙特卡洛采样算法，按接受率决定接受或拒绝提议状态，从任意目标分布采样
type: concept
maturity: seed
confidence: medium
tags:
- MCMC
- 采样
- 贝叶斯推断
created: '2026-08-17'
updated: '2026-08-17'
verified:
review_due:
sources:
- https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B
---

# Metropolis-Hastings算法

> 一种马尔可夫链蒙特卡洛采样算法，按接受率决定接受或拒绝提议状态，从任意目标分布采样。

## 核心思想

Metropolis-Hastings（MH）是最基本的 MCMC 算法，用于从难以直接采样的目标分布 $p(x)$ 中生成样本：

- **提议分布**：从提议分布 $q(x'|x)$ 提出新状态 $x'$
- **接受率**：按概率 $\alpha = \min\left(1, \frac{p(x')q(x|x')}{p(x)q(x'|x)}\right)$ 决定接受或拒绝
- **关键优势**：接受率只依赖 $p$ 的比值，因此无需知道归一化常数 $Z$（配分函数）

## 算法流程

1. 初始化状态 $x^{(0)}$
2. 从提议分布 $q(x'|x^{(t)})$ 提议新状态 $x'$
3. 计算接受率 $\alpha$
4. 以概率 $\alpha$ 接受（$x^{(t+1)} = x'$），否则保持（$x^{(t+1)} = x^{(t)}$）
5. 重复直到链收敛（平稳分布 = 目标分布）

**理论保证**：构造的马尔可夫链以目标分布为平稳分布，长链样本近似独立同分布于 $p(x)$。

## 变体与权衡

- **随机游走 Metropolis**：$x' = x + \epsilon$，$\epsilon$ 为噪声——简单但可能低效（高维下接受率低）
- **对称提议**：若 $q(x'|x) = q(x|x')$，接受率退化为 $\min(1, p(x')/p(x))$（Metropolis 原版）
- **局限性**：高维空间随机游走效率低、样本自相关高
- **改进**：HMC（哈密顿蒙特卡洛）、NUTS 利用梯度信息提高效率（现代库如 Stan 采用）

## 应用

- **贝叶斯后验采样**：从后验分布生成样本做推断
- **统计物理**：从吉布斯分布（Boltzmann 分布）采样
- **组合优化**：模拟退火与 MH 同源

## 关系网络

- 组成：[[马尔可夫链蒙特卡洛（MCMC）]] — MH 是 MCMC 的基本算法
- 相关：[[吉布斯采样]] — 吉布斯采样是 MH 的特例/替代
- 依赖：[[马尔可夫链]] — MH 构造的采样链是马尔可夫链
- 应用：[[贝叶斯推断]] — 后验采样是 MH 的主要用途

## 参考资料

- [马尔可夫链蒙特卡洛 - 维基百科](https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B) — 思想、Metropolis-Hastings、吉布斯采样、收敛评估
- [Metropolis-Hastings algorithm - Wikipedia](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) — 算法推导与变体
