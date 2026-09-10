---
schema_version: '1.1'
title: 马尔可夫链蒙特卡洛（MCMC）
aliases:
- Markov Chain Monte Carlo
- MCMC
- 马尔可夫链蒙特卡洛
summary: 构造以目标分布为平稳分布的马尔可夫链，通过采样逼近后验分布的一族算法
type: concept
maturity: growing
confidence: high
tags:
- 概率论
- 采样
- 贝叶斯
created: '2026-08-17'
updated: '2026-09-11'
verified: '2026-08-17'
review_due: '2027-08-17'
sources:
- https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B
- https://mc-stan.org/docs/2_31/cmdstan-guide/diagnose.html
---

# 马尔可夫链蒙特卡洛（MCMC）

> 构造以目标分布为平稳分布的马尔可夫链，通过采样逼近后验分布的一族算法。

马尔可夫链蒙特卡洛（MCMC）结合马尔可夫链与蒙特卡洛采样：构造一条以**目标分布**（如
贝叶斯后验）为平稳分布的马尔可夫链，让链逐步收敛到目标分布，再从中抽取样本。这让贝叶斯
推断无需计算复杂的归一化积分即可采样后验——是贝叶斯统计在计算上可行的关键。

## 核心思想

1. **目标**：从复杂分布 $P(\theta|D)$ 采样（常只有未归一化的 $P(D|\theta)P(\theta)$）
2. **构造链**：设计转移核，使目标分布是链的唯一平稳分布
3. **收敛**：在满足不可约、非周期等遍历条件时，链运行足够久后逼近目标分布（需评估或丢弃初期样本）
4. **采样**：收敛后用链的样本近似目标分布（估计均值/区间/边缘）

### 经典算法

- **Metropolis-Hastings**：提议新状态，按接受率决定接受/拒绝，灵活但可能低效
- **吉布斯采样**：每次按条件分布采样一个分量，简单高效（需条件分布可采样）
- **NUTS / HMC**：利用梯度的高效变体（现代库如 Stan 采用）

## 收敛与评估

- **R-hat**：比较链间与链内尺度的多链诊断指标，应接近 1；现代实践常以 < 1.01 作为起点，但它不是单独的收敛证明，需结合有效样本量、轨迹图和其他诊断
- **burn-in**：丢弃早期未收敛样本
- **样本相关性**：链内样本不独立（自相关），需足够长链

## 关系网络
- 依赖：[[马尔可夫链]] — MCMC 用马尔可夫链构造采样，平稳分布收敛是关键
- 依赖：[[马尔可夫性质]] — 链的转移依赖马尔可夫性质
- 应用：[[贝叶斯推断]] — 后验采样是 MCMC 的主要用途
- 组成：[[Metropolis-Hastings算法]] — MCMC 的具体算法
- 组成：[[吉布斯采样]] — MCMC 的具体算法
- 相关：[[蒙特卡洛估计]] — 依赖样本的蒙特卡洛扩展

## 参考资料

- [马尔可夫链蒙特卡洛 - 维基百科](https://zh.wikipedia.org/zh-hans/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E9%93%BE%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B) — 思想、Metropolis-Hastings、吉布斯采样、收敛评估

- [Stan：Diagnosing Biased HMC Inferences](https://mc-stan.org/docs/2_31/cmdstan-guide/diagnose.html) — R-hat、有效样本量和多链诊断建议

## 变更记录

- 2026-09-11：收紧 MCMC 遍历条件与 R-hat 阈值，并补充 Stan 诊断建议；保留原事实核验日期。

- 2026-09-11：补充本批数学与AI新节点的反向关联；保留原verified，本次仅核验新增关系。
