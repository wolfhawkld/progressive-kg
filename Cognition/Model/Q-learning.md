---
schema_version: '1.1'
title: Q-learning
aliases:
- Q-learning
- Q学习
summary: 通过时序差分更新动作价值 Q 的无模型离线策略算法，是深度强化学习算法的表格原型
type: concept
maturity: growing
confidence: high
tags:
- 强化学习
- 时序差分
- 算法
created: '2026-10-06'
updated: '2026-10-06'
verified: '2026-10-06'
review_due: '2027-10-06'
sources:
- https://ai.nankai.edu.cn/bijiRL-I.pdf
- https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf
---

# Q-learning

> 通过时序差分更新动作价值 Q 的无模型离线策略算法，是深度强化学习算法的表格原型。

Q-learning（Watkins 1989）是强化学习最经典的**无模型**（model-free）算法：不需要知道环境的
转移概率，直接通过与环境的交互、用**时序差分**（TD，temporal difference）更新来逼近最优动作
价值函数 $Q^*(s,a)$。它是 DQN/DDQN 等深度方法的表格原型，其 TD 目标中的 max 操作正是
**Q 值高估偏差**的源头。

## 核心更新规则

$$Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha\left[r_{t+1} + \gamma \max_{a'} Q(s_{t+1},a') - Q(s_t,a_t)\right]$$

- **$r_{t+1} + \gamma \max_{a'} Q(s_{t+1},a')$**：TD 目标（用贝尔曼最优方程的采样近似）
- **括号内整体**：TD 误差（TD error）
- **$\alpha$**：学习率；**$\gamma$**：折扣因子
- **直觉**：用"实际拿到的奖励 + 对下一状态的最好估计"来修正当前估计，逐步逼近最优值

### 关键性质

- **无模型**：不需要环境模型（转移概率 $P$），只需交互样本
- **离线策略（off-policy）**：更新用的是 $\max$（greedy 策略），而**行为策略**可以是
  $\epsilon$-greedy 等探索策略——两者不必相同
- **收敛性**：表格设定下，所有状态-动作对无限次访问且 $\alpha$ 满足条件时收敛到 $Q^*$
- **探索/利用**：通常用 $\epsilon$-greedy（以 $\epsilon$ 概率随机探索）

## 局限：高估偏差与维度灾难

- **高估偏差**：TD 目标里的 $\max$ 让"被噪声高估的动作"赢得最大化，导致 $Q$ 估计系统性偏高
  → DDQN 通过解耦选择与评估修正
- **表格限制**：状态空间大（连续状态）时无法维护完整 Q 表 → DQN 用神经网络近似 $Q(s,a;\theta)$

## 关系网络
- 前置：[[强化学习]] — Q-learning 是最经典的无模型 RL 算法
- 工具：[[贝尔曼方程]] — TD 目标是贝尔曼最优方程的采样近似
- 迭代：[[DDQN]] — 解耦选择与评估以修正 Q-learning 的高估偏差
- 迭代：[[DQN]] — 用神经网络函数逼近替代 Q 表
- 待建：时序差分 — Q-learning 所属的学习范式（TD 学习）

## 参考资料

- [强化学习经典文章研读(I) - 南开大学](https://ai.nankai.edu.cn/bijiRL-I.pdf) — Q-learning 与 Double Q-learning 原文研读
- [深度强化学习 - 北京大学张志华](https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf) — TD 目标、高估偏差推导、DQN 改进体系
