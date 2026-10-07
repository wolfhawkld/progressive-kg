---
schema_version: '1.1'
title: DQN（Deep Q-Network）
aliases:
- DQN
- Deep Q-Network
- 深度Q网络
summary: 用深度神经网络逼近动作价值函数并结合经验回放与目标网络的深度强化学习奠基算法
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
- https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf
- http://coladrill.github.io/2018/10/21/%E6%B7%B1%E5%BA%A6%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%BB%BC%E8%BF%B0
---

# DQN（Deep Q-Network）

> 用深度神经网络逼近动作价值函数并结合经验回放与目标网络的深度强化学习奠基算法。

DQN（Deep Q-Network, Mnih et al. 2015）把 Q-learning 从表格搬到**深度神经网络**，让强化学习
首次在 Atari 游戏上从像素输入端到端学习。它的两大工程支柱——**经验回放**（experience replay）
与**目标网络**（target network）——解决了"用非线性函数逼近 + 自举更新"带来的训练不稳定问题，
是深度 RL 的奠基工作，也是 DDQN 等后续改进的基线。

## 核心机制

DQN 由三部分构成：用神经网络逼近 Q 函数、经验回放、目标网络——后两者是让"非线性函数
逼近 + 自举更新"能稳定训练的关键工程手段。

### 神经网络逼近 Q 函数

用参数化网络 $Q(s,a;\theta)$ 替代 Q 表，损失为 TD 误差的平方：

$$L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q(s',a';\theta^-) - Q(s,a;\theta)\right)^2\right]$$

- **$\theta$**：当前值网络参数（实时更新）
- **$\theta^-$**：目标网络参数（每 N 步从 $\theta$ 复制）
- 连续状态（像素）无需人工特征，网络直接从输入学习表示

### 经验回放（Experience Replay）

把交互记录 $(s,a,r,s')$ 存入**回放数组**，事后反复采样用于训练。

- **作用**：打破样本的时间相关性（连续样本高度相关会破坏 SGD 的 i.i.d. 假设）
- **作用**：提高数据效率（一条经验可被多次利用）
- **作用**：稳定训练（避免被最近的糟糕经验带偏）

### 目标网络（Target Network）

单独维护一个延迟更新的网络 $\theta^-$ 来产生 TD 目标。

- **问题**：若用同一个网络既产生目标又更新自己，目标是"移动的靶子"，会引发振荡甚至发散
- **解法**：目标网络参数**每 N 步**才从当前网络复制，使目标在若干步内保持固定
- **额外稳定性**：把奖励与误差裁剪到有限区间，保证 Q 值与梯度处于合理范围

## 已知问题与改进

DQN 虽然开创了深度 RL，但有明显局限，后续工作逐一修正：

| 问题 | 改进 |
| --- | --- |
| **Q 值高估**（max 操作带来系统性偏高） | **DDQN**（解耦选择与评估） |
| 样本利用效率低（均匀采样） | **优先经验回放**（优先重放学得多的样本） |
| 状态价值与动作优势混杂 | Dueling Network（分解为 $V(s)+A(s,a)$） |
| 探索不足（$\epsilon$-greedy 随机性弱） | Noisy Net（在参数上加噪声） |

## 关系网络
- 前置：[[强化学习]] — DQN 是深度强化学习的奠基算法
- 前置：[[Q-learning]] — DQN 用神经网络替代其 Q 表，沿用 TD 目标
- 工具：[[贝尔曼方程]] — TD 目标来自贝尔曼最优方程
- 迭代：[[DDQN]] — 修正 DQN 的 Q 值高估偏差
- 应用：[[反向传播]] — 用 TD 误差的梯度更新网络参数
- 依赖：[[经验回放]] — DQN 的两大稳定机制之一
- 待建：目标网络 — DQN 的另一稳定机制
- 对比：[[Go-Explore]] — 常规价值型方法靠 ε-greedy 边走边试、无法回头；Go-Explore 把探索与返回解耦
## 参考资料

- [深度强化学习 - 北京大学张志华](https://www.math.pku.edu.cn/teachers/zhzhang/drl_v1.pdf) — DQN 课件：经验回放、目标网络、高估问题与改进体系
- [深度强化学习综述 - Jiayue Cai](http://coladrill.github.io/2018/10/21/%E6%B7%B1%E5%BA%A6%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0%E7%BB%BC%E8%BF%B0) — DQN 机制与 DDQN/Dueling/优先回放的对比
