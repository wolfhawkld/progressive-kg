---
schema_version: '1.1'
title: 复核：18个跨类别概念增补
aliases: []
summary: 记录生物、考古文化、语言与方法共18个节点的增补依据、概念边界及双向关联检查
type: review
maturity: growing
confidence: high
tags:
- 复核
- 概念增补
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- SCHEMA.md
- _system/OPERATIONS.md
---

# 复核：18个跨类别概念增补

> 记录生物、考古文化、语言与方法共18个节点的增补依据、概念边界及双向关联检查。

## 范围与取舍

根据用户“其他几个 category 里的相关概念，你认为必要的”的授权，在数学与 AI 40 项完成后补入 18 项。

- 生物学 8 项：补足遗传信息表达和糖类结构的基础链条。
- 考古与文化 4 项：为遗址、葬俗和信仰页增加方法与解释边界。
- 语言学 4 项：填补语言域的基础概念，并连接现有交互假设与词嵌入。
- 方法 2 项：支持本库持续核验；以 procedure 记录本地可执行流程。

Language 新建 linguistics 子域及 MOC，域地图增加入口；其他沿用已有子域。concept 与 procedure 页面总量由 183 增至 201，另有 1 个既存 hypothesis；此计数不含 MOC、review 和 raw。所有新页保留 seed，成熟度不因正文完整而自动提升。

## 新增页面

逐页来源及支持范围见页面参考资料；本表给出实际位置。

| 节点 | 类型 | 来源数 |
|---|---|---|
| [[Cognition/Biology/基因]] | concept | 3 |
| [[Cognition/Biology/染色体]] | concept | 4 |
| [[Cognition/Biology/细胞]] | concept | 4 |
| [[Cognition/Biology/转录]] | concept | 4 |
| [[Cognition/Biology/翻译（生物学）]] | concept | 3 |
| [[Cognition/Biology/酶]] | concept | 3 |
| [[Cognition/Biology/单糖]] | concept | 3 |
| [[Cognition/Biology/糖苷键]] | concept | 3 |
| [[Culture/history-archaeology/考古地层学]] | concept | 3 |
| [[Culture/history-archaeology/碳十四测年]] | concept | 4 |
| [[Culture/history-archaeology/考古学文化]] | concept | 3 |
| [[Culture/thought/仪式]] | concept | 3 |
| [[Language/linguistics/语义学]] | concept | 1 |
| [[Language/linguistics/语用学]] | concept | 1 |
| [[Language/linguistics/言语行为理论]] | concept | 1 |
| [[Language/linguistics/指称]] | concept | 1 |
| [[Meta/methodology/证据溯源]] | procedure | 2 |
| [[Meta/methodology/三角互证]] | procedure | 1 |

## 核验重点与限制

按文件名、title 和 aliases 查重，并检索 raw 素材；浏览权威机构、学术条目与方法文献核对定义和关键边界。

- 生物：区分基因与蛋白产物、转录与翻译、单体与聚合物，以及酶的催化性质。
- 考古：区分地层先后、样品测年和历史事件；考古学文化不自动指认族群。
- 语言：区分意义规则、语境推断、话语行动与指称；不把这些理论当作 AGI 假设的实证支持。
- 方法：溯源不担保真实性，多个一致来源不必独立。三角互证分类核对 Carter 等摘要；本地流程是应用建议，未声称经过效果实验。

只补关联的旧页保留 created、verified、maturity，并记录修改原因。核验范围是新页与新增关系，不声称重新验证全部旧页和全部历史来源。未进行 Obsidian GUI 验收。

## 验证记录

交付前运行全库 lint、双向关联检查、控制字符检查和 git diff --check。

最终结果：lint 为 0 errors / 0 warnings / 0 info；87 条新页出链均有反向关系；控制字符检查及 git diff --check 通过。19 个旧知识页的 created、verified、maturity 与提交前一致。新增48条反向关系，raw 和系统配置保持原样。

## 关系网络

- 相关：[[Meta/reviews/2026-09-11-ai-math-40-concepts]] — 本轮之前完成的数学与 AI 批次
- 相关：[[证据溯源]] — 来源核验的维护方法
- 相关：[[三角互证]] — 对证据一致与分歧的处理方法

## 参考资料

- [[SCHEMA]] — 结构、关系和生命周期规则
- [_system/OPERATIONS.md](../../_system/OPERATIONS.md) — Ingest 与维护流程
