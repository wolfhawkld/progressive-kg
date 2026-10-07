---
schema_version: '1.1'
title: DDQN（Double Deep Q-Network）
aliases:
- DDQN
- Double DQN
- Double Deep Q-Network
- 双深度Q网络
summary: 将动作选择与价值评估解耦以消除 Q 值高估偏差的 DQN 改进算法，是深度强化学习的经典基线
type: concept
maturity: growing
confidence: high
tags:
- 强化学习
- 深度强化学习
- 算法
created: '2026-10-06'
updated: '2026-10-06'
verified: '2026-10-06'
review_due: '2027-10-06'
sources:
- https://ai.nankai.edu.cn/bijiRL-I.pdf
- https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf
- http://coladrill.github.io/2018/10/21/%E6%B7%B1%E5%BA%A6%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%BB%BC%E8%BF%B0
---

# DDQN（Double Deep Q-Network）

> 将动作选择与价值评估解耦以消除 Q 值高估偏差的 DQN 改进算法，是深度强化学习的经典基线。

DDQN（Double DQN，van Hasselt et al. 2016）是 **DQN 的核心改进之一**：它针对
**Q 值高估（overestimation）** 这一系统性偏差，把 TD 目标中的"最大化"操作拆成
**动作选择**与**动作价值评估**两步，分别由两套参数完成。它不改变网络结构，只改目标
计算方式，却显著提升了价值估计准确性与策略质量。

## 问题：Q 值高估从哪来

**根源是"先加噪声再取最大值"**。设 DQN 对每个动作的输出是真实价值加零均值噪声：

$$Q(s,a;w) = Q^*(s,a) + \epsilon,\quad \mathbb{E}[\epsilon]=0$$

单看每个动作，$Q$ 是真实价值的**无偏估计**；但 TD 目标里要取最大值：

$$\mathbb{E}\left[\max_{a\in\mathcal{A}} Q(s,a;w)\right] \ge \max_{a\in\mathcal{A}} Q^*(s,a)$$

**取最大值的操作把噪声也"取上"了**——被高估的动作赢得 $\max$，于是估计值系统性偏高。这不是无偏估计能挡住的问题：无偏 + 非线性（max）≠ 无偏。

**为什么危害大**：
- 高估误差随动作数增加而增加
- 若高估不均匀，某个**次优动作**的估计值可能超过最优动作，导致**永远选不到最优策略**
- 实验观察：DQN 学习曲线（估计值）长期高于真实策略值，且在部分游戏（Asterix、Wizard of Wor）出现训练不稳定——**估计值上涨与得分下降同时发生**

## 解法：解耦选择与评估

Double Q-learning（van Hasselt 2010）的核心思想：**用一套参数选动作，用另一套参数评估该动作的价值**。

$$y = r + \gamma\, Q\!\left(s', \arg\max_{a'} Q(s',a';\theta);\ \theta^-\right)$$

- **$\theta$（当前值网络）**：负责**选择**最优动作 $a^* = \arg\max_{a'} Q(s',a';\theta)$
- **$\theta^-$（目标网络）**：负责**评估**该动作的价值

**DDQN 的巧妙之处**：DQN 本来就有**目标网络**（$\theta^-$，每 N 步从 $\theta$ 复制），所以第二个价值函数**天然存在，无需额外网络**。DDQN = DQN + 把 max 操作换成"当前网络选动作、目标网络评价值"。其他部分（经验回放、目标网络、损失构造）与 DQN 保持一致。

### 与 DQN 的对比

| | DQN | DDQN |
| --- | --- | --- |
| TD 目标 | $r + \gamma \max_{a'} Q(s',a';\theta^-)$ | $r + \gamma\, Q(s',\arg\max_{a'}Q(s',a';\theta);\theta^-)$ |
| 选择与评估 | 同一网络（目标网络） | 解耦（$\theta$ 选、$\theta^-$ 评） |
| 高估偏差 | 系统性高估 | 显著减轻 |
| 网络结构 | — | **不变** |
| 效果 | 基线 | 更准确的价值估计 + 更高得分 |

## 关系网络
- 前置：[[强化学习]] — DDQN 是深度强化学习的经典算法
- 工具：[[贝尔曼方程]] — TD 目标是贝尔曼最优方程的采样近似
- 前置：[[DQN]] — DDQN 的基线算法（经验回放 + 目标网络）
- 前置：[[Q-learning]] — DDQN 的表格版原型，高估问题的源头
- 相关：[[经验回放]] — DQN/DDQN 的稳定训练机制
- 相关：[[优先经验回放]] — 与 DDQN 常并列的 DQN 改进
- 相关：[[探索与利用]] — ε-greedy 等探索策略是此类价值型算法的直接超参
## 参考资料

- [强化学习经典文章研读(I) - 南开大学](https://ai.nankai.edu.cn/bijiRL-I.pdf) — Double Q-learning 与 Double DQN 原文研读、高估问题实验证据
- [深度强化学习 - 北京大学张志华](https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf) — 高估偏差的不等式推导、DQN 改进方法体系（经验回放/目标网络/DDQN/Dueling/Noisy Net）
- [深度强化学习综述 - Jiayue Cai](http://coladrill.github.io/2018/10/21/%E6%B7%B1%E5%BA%A6%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%BB%BC%E8%BF%B0) — DDQN 与 DQN 的实现差异、两套参数的分工
- [[raw/human_ai_knowledge/tas-vs-rl-boss-ai.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/tas-vs-rl-boss-ai.html) — 人机知识《TAS 与 RL 打 boss 的两条路线对比》：TAS 产出输入序列、RL 产出策略函数；其中用空洞骑士的公开 RL 项目说明打 boss 需要哪些 RL 技巧（Nemesis, 2026-10-07）（案例中点名 Double DQN / Dueling DQN 是打空洞骑士 boss 的改进项之一）
