---
schema_version: '1.1'
title: do-演算
aliases:
- do-calculus
- do算子
- 干预演算
summary: 由 Pearl 提出的因果推断形式化工具，用 do 算子区分干预与观察，推导干预后分布
type: concept
maturity: seed
confidence: medium
tags:
- 因果推断
- 因果图
- Pearl
created: '2026-08-17'
updated: '2026-08-17'
verified:
review_due:
sources:
- https://zh.wikipedia.org/zh-hans/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD
- https://arxiv.org/abs/1305.5506
---

# do-演算

> 由 Pearl 提出的因果推断形式化工具，用 do 算子区分干预与观察，推导干预后分布。

## 核心思想

do-演算是 Judea Pearl 因果推断框架中的形式化工具，用于回答"干预后会发生什么"这一因果问题：

- **do 算子**：$P(Y|do(X=x))$ 表示"把 X 强制设为 x 后 Y 的分布"，区别于条件概率 $P(Y|X=x)$（仅观察）
- **本质区别**：观察是"看到 X=x"，干预是"制造 X=x"，两者在存在混淆时不同
- **反事实语义**：do-演算为反事实推理提供形式化基础

## 三条规则

Pearl 提出了 do-演算的三条规则，用于消除 do 算子、将其化简为可估计的观察分布：

- **规则 1（插入/删除观察）**：若 Y 与变量 Z 在给定某些条件下条件独立，可在干预分布中插入或删除对 Z 的观察
- **规则 2（交换行动与观察）**：在特定图条件下，可将干预 $do(X)$ 与观察 $X$ 互换
- **规则 3（删除干预）**：若 X 与 Y 的因果效应不受其他变量影响，可删除 $do(X)$

**完备性**：Pearl 证明 do-演算在标准因果图假设下是完备的——若一个因果量能被识别，就一定能通过这三条规则化简出来。

## 应用

- **识别问题**：判断因果效应能否从观察数据中识别（不可识别时需工具变量或实验）
- **混淆控制**：通过后门准则（backdoor）选择需控制的变量集合
- **中介分析**：用前门准则（frontdoor）估计间接效应
- **因果推断**：是因果推断中"干预"问题的标准工具

## 关系网络

- 组成：[[因果推断]] — do-演算是因果推断中处理干预的核心工具
- 相关：[[反事实]] — 反事实推理与 do-演算同属 Pearl 因果框架
- 应用：[[贝叶斯网络]] — 贝叶斯网络作为因果图承载 do-演算的图操作

## 参考资料

- [因果推断 - 维基百科](https://zh.wikipedia.org/zh-hans/%E5%9B%A0%E6%9E%9C%E6%8E%A8%E6%96%AD) — 干预、反事实、工具变量概述
- [Causal Inference in Statistics: An Overview](https://arxiv.org/abs/1305.5506) — Pearl 因果框架综述（含 do-演算）
