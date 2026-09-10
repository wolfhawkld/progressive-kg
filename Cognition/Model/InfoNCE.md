---
schema_version: '1.1'
title: InfoNCE
aliases:
- Information Noise-Contrastive Estimation
- 信息噪声对比估计
summary: 以候选正例分类为形式、通过噪声样本学习表示匹配关系的对比目标
type: concept
maturity: seed
confidence: high
tags:
- 对比损失
- 表示学习
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- https://arxiv.org/abs/1905.06922
- https://arxiv.org/abs/1807.03748
- https://proceedings.mlr.press/v119/chen20j.html
- https://proceedings.mlr.press/v139/radford21a.html
---

# InfoNCE

> 以候选正例分类为形式、通过噪声样本学习表示匹配关系的对比目标。

## 把匹配转成候选分类

InfoNCE 为一个锚点构造一个来自条件分布的正例，并从提议分布或批次中取若干噪声样本作为候选。模型不必直接重构高维输入，而是学习让正例的匹配分数高于候选负例。

设锚点表示为 $z_i$，正例为 $z_i^+$，候选集合为 $\mathcal C_i$，其中包含正例和负例。以温度 $\tau>0$ 缩放相似度 $s$ 时，常见目标为：

$$
\mathcal L_i=-\log
\frac{\exp(s(z_i,z_i^+)/\tau)}
{\sum_{z\in\mathcal C_i}\exp(s(z_i,z)/\tau)}.
$$

分母包含正例；因此它可以理解为在候选集合中识别正例的 [[交叉熵]]，归一化步骤由 [[Softmax]] 完成。$s$ 可以是点积或 [[余弦相似度]]，但两者的数值含义取决于是否对表示做了单位归一化。

### 一个可复算的例子

若候选得分为 $(2,1,0)$，第一个是正例，取 $\tau=1$，则正例概率为：

$$
p^+=\frac{e^2}{e^2+e^1+e^0}\approx0.665,
\qquad \mathcal L\approx0.408.
$$

提高正例相对分数会降低损失；减小温度会放大分数差异，使分布更尖锐，但也会使优化对噪声和错误负例更敏感。

## 正负样本与采样假设

InfoNCE 的关键不只是公式，还包括正例、噪声分布和候选集合如何构造。CPC 中一个正样本来自给定上下文的条件分布，$N-1$ 个负样本来自边缘提议分布；在 SimCLR 或 CLIP 中，其他样本常由同一批次提供。

| 组成 | 作用 | 典型风险 |
|---|---|---|
| 正例 | 定义模型应保持的匹配关系 | 配对规则可能包含错误或过弱语义 |
| 负例 | 提供需要区分的候选 | 假负例会把语义相近样本推远 |
| 温度 | 调整 logits 的尺度和分布尖锐度 | 过小可能导致梯度集中或对噪声敏感 |
| 候选数量 | 改变分类难度和信息估计上限 | 增大候选会增加显存、通信和采样成本 |

因此，InfoNCE 不是“加入越多负例就一定越好”的保证；候选负例是否符合下游任务的相似性定义，通常比数量本身更重要。

## 与互信息下界的关系

在正例来自联合分布、其余候选独立来自边缘分布的标准采样协议下，InfoNCE 与 [[互信息]] 的关系可写为下式。这里 $N$ 是含正例的候选总数，$\mathcal L_N$ 是对采样过程取期望的损失：

$$
I(X;Y)\geq \log N-\mathcal L_N.
$$

下界本身不要求打分器达到最优；密度比形式的最优打分器用于分析最优目标。单个批次的损失并不保证给出数值上有效的总体下界。改变负例分布或引入候选相关性后，不能直接沿用上述解释。由于损失非负，$\log N-\mathcal L_N$ 不超过 $\log N$；当真实互信息很大时，小候选集的下界会受此限制。候选数增大可以使该下界在特定条件下变紧，但计算规模、负例相关性和估计方差也会改变实际效果。

## 与其他对比目标的边界

InfoNCE 是一种以候选分类为核心的对比目标，而“对比学习”是更大的方法集合。监督对比损失可以有多个同类正例，triplet loss 使用边际约束，成对损失也可以不采用 softmax 分类；它们都可能用于对比学习，却不应直接当作同一个公式。

在 [[CLIP]] 中，图像到文本和文本到图像各自对 batch 内候选做温度缩放的交叉熵。这个双向目标与 InfoNCE 风格形式相近，但 CLIP 原论文使用的是对称交叉熵表述，具体的正负配对和数据来源仍由 CLIP 训练协议定义。

## 关系网络

- 方法：[[对比学习]] — InfoNCE 是其中一种常用的候选匹配目标
- 训练范式：[[自监督学习]] — 正负样本可由数据自身或视图变换生成
- 组成：[[交叉熵]] — 将正例识别写成候选集合上的分类损失
- 组成：[[Softmax]] — 对候选匹配分数归一化
- 相似度：[[余弦相似度]] — 单位归一化表示常用的匹配分数
- 理论关联：[[互信息]] — 在特定采样条件下给出下界解释
- 应用：[[CLIP]] — 双向图文批内匹配使用相近的温度对比目标

## 参考资料

- [van den Oord 等：Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748) — 命名 InfoNCE、正负样本采样、密度比估计与互信息下界
- [Chen 等：A Simple Framework for Contrastive Learning of Visual Representations](https://proceedings.mlr.press/v119/chen20j.html) — SimCLR 的批内负例、归一化表示、温度和投影头
- [Radford 等：Learning Transferable Visual Models From Natural Language Supervision](https://proceedings.mlr.press/v139/radford21a.html) — CLIP 的双向图文匹配与对称交叉熵目标
- [Poole 等：On Variational Bounds of Mutual Information](https://arxiv.org/abs/1905.06922) — §2.3 给出InfoNCE期望下界、最优打分及候选数上限的证明；2026-09-11 核验
