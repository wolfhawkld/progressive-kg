---
schema_version: '1.1'
title: TAS
aliases:
- Tool-Assisted Speedrun
- Tool-Assisted Superplay
- 工具辅助速通
- 塔斯
summary: 以不变动游戏本体为前提，借助模拟器辅助功能构造逐帧精确输入来完成游戏的方式
type: concept
maturity: growing
confidence: high
tags:
- 游戏
- 速通
- 确定性
created: '2026-10-07'
updated: '2026-10-07'
verified: '2026-10-07'
review_due: '2027-10-07'
sources:
- https://en.wikipedia.org/wiki/Tool-assisted_speedrun
- https://zh.wikipedia.org/wiki/TAS%E7%AB%B6%E9%80%9F
- http://tasvideos.org/Glossary
- https://clementgallet.github.io/libTAS/
---

# TAS

> 以不变动游戏本体为前提，借助模拟器辅助功能构造逐帧精确输入来完成游戏的方式

---

## 定义与两条边界

TAS 全称 Tool-Assisted Speedrun，中文「工具辅助速通」。中文维基的表述把前提写得很清楚：

> 是指**以完全不变动游戏本体为前提**，利用游戏机模拟器的辅助功能，以**极高的精度**完成游戏的一种游戏方式。

它产出的是**记录下来的精确输入**：

> A tool-assisted speedrun … is generally defined as a video game playthrough or speedrun composed of **precise inputs recorded with tools** such as emulators.
> （TAS 一般定义为：用模拟器等**工具记录下来的精确输入**所构成的游戏通关或速通录像。）

追求的目标是**理论上的完美通关**——那些人类实机速通做不到的路线与优化。

理解 TAS 必须划清两条边界，因为它夹在中间：

| | 与「金手指／修改器」的边界 | 与「RTA」的边界 |
|---|---|---|
| 差别 | TAS **只操纵控制器输入**，不改游戏数据 | TAS 不在实时约束下，靠工具逐步构造 |
| 原文 | 「在金手指上可以通过**修改游戏数据**（包括但不限于无敌状态）而达致刀枪不入，而 TAS 只能通过模拟精准细致的操控达成极度灵敏的回避效果」 | 与「着重以实时、实力完成游戏为目标」的 RTA（Real Time Attack）相对 |
| 后果 | 因此 TAS 的合法性取决于**输入是否物理上可达** | 在真人对战／RTA 中使用 TAS 算作**作弊** |

**最后一行是 TAS 最微妙的伦理边界**：极端按键组合（例如在同一轴上同时按下「左+右」）在实体控制器上需要硬件改造才能做到，但 TAS 可以轻易模拟。这类技巧是否算数，各游戏社区取态不同。

---

## 使能条件：确定性 + 状态可存取

TAS 能做极致优化的根本原因不是「操作更快」，而是**它站在一个确定性的、可回退的世界里**。

### 1. 确定性是前提

如果同一输入不能得到同一结果，那么「回退重试」就没有意义。TASVideos 的术语表里围绕这一点成组出现：

```text
Determinism（模拟器确定性 / 主机验证确定性）
Desync          · 结果与预期不符，"失步"
Nondeterminism  · 多线程等导致的不确定
```

对**原生运行的 PC 游戏**，工具要主动去争取确定性。libTAS 的做法是插在游戏和系统之间：

> It creates an intermediate layer between the game and the operating system, **feeding the game with altered data (such as inputs, system time)**. We can call such tool a **trans-layer** — an API translation layer. It tries to make the game running **deterministically**, although it is still an issue when dealing with **multithreaded** games.

### 2. 状态可任意存取

```text
Savestate        · 任意时刻存档 / 读档
Frame advance    · 单帧推进
Re-record        · 回退后重录
Slow motion      · 放慢逐帧检查
RAM watch/search · 读内存、定位变量
```

### 3. 由此可以操纵随机数

因为过程确定，游戏的随机数实际上由「你在第几帧做了什么」决定。社区的说法是：所有 RNG 从游戏里**第一个有影响的帧**起就被决定，因此可以**通过输入把随机结果刷成自己想要的**。术语表里对应的是 `Luck manipulation`（运气操纵）。

> **这三条合起来才是 TAS 的能力**:构造输入 → 回退试错 → 确定性保证试验可重复。缺任何一条，TAS 都做不成。

---

## 输入即产物：movie file 与 sync verification

TAS 的作品不是「一段视频」，而是一份**输入录像文件**（movie file）。视频只是它的渲染结果。这个区别带来一个 TAS 独有的验证方式——**Sync Verification**：

> 让别人在自己的模拟器上重放你的输入文件，确认它真的能按预期通关。

**这是一种天然可证伪的验证形式**：输入文件是确定的，任何人可独立复现。相比之下，一个「AI 打过了 boss」的结论需要跑多个随机种子、汇报分布——见 [[强化学习]]。

---

## 与「AI 打游戏」的关系

TAS 常被误认为是一种 AI，实际上它在坐标系上与 RL 分处两头。要点：

| 维度 | TAS | [[强化学习]] |
|---|---|---|
| 产出 | 一条输入序列（movie file） | 一个策略函数 |
| 有没有模型 | 没有，不含待学习参数 | 有 |
| 状态存取 | **默认特权**（savestate / 回退重录 / 读内存） | 无回退；观测常为像素 |
| 优化目标 | 客观指标（帧数/时间），外部可复算 | 人为奖励，可能被 [[奖励黑客]] 钻空子 |
| 知识位置 | 人与社区文档（可读、可审计） | 网络权重（不可读、需重训） |

**最关键的一点是"状态存取"这一行**：TAS 与 RL 的差距主要不是「聪明程度」，而是「特权」。

而这条边界并非不可跨越——[[Go-Explore]] 正是把「回到某个已存档状态再继续探索」的思想引入 RL，用来解决硬探索问题。所以更准确的说法是：**分界不在有没有回退，而在回退是默认特权，还是需要额外机制去争取。**

---

## 关系网络

- 相关：[[强化学习]] — 两条「让程序打 boss」的路线；TAS 产出输入序列、RL 产出策略函数，差别在可用的「特权」
- 相关：[[Go-Explore]] — 把 TAS 的状态回退思想搬进 RL 的算法族
- 对比：[[奖励黑客]] — 两边都会「钻空子」：TAS 钻**游戏实现**的漏洞（社区欢迎），RL 钻**奖励规格**的漏洞（是问题）
- 组成：[[速通]] — TAS 是速通的子类别（工具辅助）；与 RTA 不同台竞技

---

## 参考资料

- [Tool-assisted speedrun (Wikipedia)](https://en.wikipedia.org/wiki/Tool-assisted_speedrun) — 定义："precise inputs recorded with tools"；目标为 theoretically perfect playthroughs
- [TAS竞速（中文维基）](https://zh.wikipedia.org/wiki/TAS%E7%AB%B6%E9%80%9F) — 中文定义（不变动游戏本体为前提）；1999 年源自《毁灭战士》源码修改版的历史；与金手指／RTA 的两条边界
- [TASVideos Glossary](http://tasvideos.org/Glossary) — Determinism / Desync / Savestate / Frame advance / Luck manipulation / Sync Verification 等术语的权威清单
- [libTAS](https://clementgallet.github.io/libTAS/) — "trans-layer"：喂改过的输入与系统时间，努力让游戏确定性运行；面向多线程游戏仍是不确定性来源
- [[raw/human_ai_knowledge/tas-vs-rl-boss-ai.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/tas-vs-rl-boss-ai.html) — 人机知识《TAS 与 RL 打 boss 的两条路线对比》：以空洞骑士为例展开两侧的工程实态（Nemesis, 2026-10-07）

---

## 变更记录

- 2026-10-07：新建。来源为人机知识《TAS 与 RL 打 boss 的两条路线对比》的跨项目关联。
- 主干：定义与两条边界（vs 金手指 / vs RTA）→ 使能条件（确定性 + 状态存取 + RNG 操纵）→ 输入即产物（movie file / sync verification）→ 与 RL 的坐标对照。
- **待补**：① 术语表只取到了词条清单，`Luck manipulation` 等词条的具体正文未逐条抓取；② 各游戏社区的"硬件改造技巧是否算数"取态差异可补实例；③ 待建节点「速通」建成后，"两条边界"一节可改为指向它。
