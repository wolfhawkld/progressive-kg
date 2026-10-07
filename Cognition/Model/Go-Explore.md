---
schema_version: '1.1'
title: Go-Explore
aliases:
- First return, then explore
- 先返回再探索
summary: 先把智能体送回已存档的有希望状态、再从该状态继续探索的强化学习算法族
type: concept
maturity: growing
confidence: high
tags:
- 强化学习
- 探索
- 难探索问题
created: '2026-10-07'
updated: '2026-10-07'
verified: '2026-10-07'
review_due: '2027-10-07'
sources:
- https://www.nature.com/articles/s41586-020-03157-9
- https://arxiv.org/abs/2004.12919
- https://www.uber.com/us/en/blog/go-explore/
- https://www.alphaxiv.org/abs/2004.12919
---

# Go-Explore

> 先把智能体送回已存档的有希望状态、再从该状态继续探索的强化学习算法族

---

## 两步结构：返回，然后探索

Go-Explore（Ecoffet 等，〈First return, then explore〉，Nature 590, 580–586, 2021）的机制可以拆成两句：

> 显式地「**记住**」有希望的状态，**先返回这些状态，再有意探索**。

Uber 的解读把它列成三步：

```text
1. 记住好的探索踏脚石（至今访问过的、有意思的不同状态）
2. 先返回某个状态，然后再探索
3. 先解决问题，然后做鲁棒化（robustification）
```

关键在**顺序**。常规 RL 的探索是「边走边试」——探索产生的状态会被后续步骤覆盖掉，一旦走错就无法回头。Go-Explore 把两件事拆开：**返回是确定性动作，探索才带随机性**。

具体做法是把访问过的状态**存档**（保存成一个可恢复的单元格 / cell），然后：

- **选择**：挑一个 cell（可用启发式，也可随机）
- **返回**：用一条已记录的动作序列回到该 cell（这一步是确定性的、可重复的）
- **探索**：从该 cell 出发做若干步随机动作，把产生的新状态登记为新 cell

---

## 它解决的是什么问题

Go-Explore 针对的是**难探索问题**（hard-exploration）：奖励**极其稀疏**，而状态空间**极其稀释**——正确路径需要一长串精确动作，中间任何一步走偏都无法察觉。

两个具体的失败机制：

- **状态稀释**（detachment）：随机探索能到达的状态集合，相对于"需要到达的关键状态"小得可以忽略；
- **无回顾性**（no revisitation）：即使偶然撞到关键状态，常规探索也不会记住它、更不会专门回去。

**兜底办法恰恰是把 TAS 早就有的那个特权补上**——[[TAS]] 里的 savestate 是游戏外挂的特权，Go-Explore 把它变成了算法的一部分。所以 Go-Explore 常被当作 [[TAS]] 与 [[强化学习]] 之间的一座桥。

---

## 结果与边界

它在 Atari 的难探索游戏上打出了此前无法企及的成绩，其中 **Montezuma's Revenge** 是长期公认的难探索标杆。

三点需要如实标注：

- **第 3 步「鲁棒化」不可省**。找到一条能通关的路径（"先解决问题"）与训练出一个**稳定的策略**是两件事——原论文明确把后者单列为一步。找到路径不等于学会能力。
- **它需要状态可存档**。这个前提在模拟器里成立，在真实物理系统里通常不成立——这是该方法适用范围的根本约束。
- **后续工作仍在推进**：例如 *Cell-Free Latent Go-Explore* 尝试把它搬到不需要显式状态存档 / 去离散化的设定。

---

## 关系网络

- 前置：[[强化学习]] — Go-Explore 是 RL 的一个算法族，解决其中的探索问题
- 相关：[[探索与利用]] — Go-Explore 是"把天平狠狠压向探索"的一类方案
- 相关：[[TAS]] — 直接借用 TAS 的状态存取特权：先返回，再探索
- 对比：[[DQN]] — 常规价值型方法靠 ε-greedy 之类边走边试，无法回头；Go-Explore 把探索与返回解耦

---

## 参考资料

- [First return, then explore (Nature 590, 580–586, 2021)](https://www.nature.com/articles/s41586-020-03157-9) — 正式发表版
- [First return, then explore (arXiv:2004.12919)](https://arxiv.org/abs/2004.12919) — 预印本；47 页，含完整算法与消融
- [Go-Explore: Montezuma's Revenge Solved (Uber Engineering)](https://www.uber.com/us/en/blog/go-explore/) — 官方三步解读：记住踏脚石 → 先返回再探索 → 先解决再鲁棒化
- [First return, then explore (alphaXiv)](https://www.alphaxiv.org/abs/2004.12919) — 概述与影响评述
- [[raw/human_ai_knowledge/tas-vs-rl-boss-ai.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/tas-vs-rl-boss-ai.html) — 人机知识《TAS 与 RL 打 boss 的两条路线对比》（Nemesis, 2026-10-07）

---

## 变更记录

- 2026-10-07：新建。来源为人机知识《TAS 与 RL 打 boss 的两条路线对比》的跨项目关联。
- 主干：两步结构（返回 + 探索）→ 它针对的难探索机制（状态稀释 / 无回顾性）→ 结果与边界（鲁棒化不可省 / 需状态可存档 / 后续工作）。
- **待补**：① 本轮只核到算法的**机制层与官方解读**，Nature 正文的消融数字与超参未逐项核验；② "鲁棒化"具体用了哪些技术（与原 DQN 系列的关系）可补；③ Cell-Free Latent Go-Explore 等后续工作目前只列名，未展开。
