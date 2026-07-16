# Progressive-KG Schema

> 渐进式个人知识图谱的结构契约。本文件同时约束人类、Agent、模板和校验脚本。

**版本**：1.1

**创建**：2026-07-01

**更新**：2026-07-17
**维护者**：Damon + Agent

---

## 1. 两个相互独立的层级

本库同时存在“导航层级”和“内容披露层级”，两者不能混用。

### 1.1 导航层级

```text
Home → Domain MOC → Subdomain MOC → Note
```

- Home 只负责全库入口、最近修改和复核队列。
- Domain MOC 负责子域导航，不把所有后代概念无分组地平铺出来。
- Subdomain MOC 只列出当前目录中的直接概念。
- Note 是最终阅读单元。

### 1.2 单页三层渐进披露

```text
L1 定义 → L2 子主题概览 → L3 深入细节
```

| 层级 | 物理位置 | 目的 |
|---|---|---|
| L1 | frontmatter `summary` + 标题后的定义引用框 | 10 秒内知道“它是什么” |
| L2 | `##` 子主题及开头概述 | 1 分钟掌握主干 |
| L3 | `###`、推导、代码、图表、证据 | 按需深入 |

概念页的正文使用 Obsidian 原生 Markdown；动态 MOC 和仪表盘依赖 Dataview。CSS 只增强视觉，不承载语义。

---

## 2. 页面类型

frontmatter 使用 `type` 表示页面类型，不再使用容易与 L1/L2/L3 混淆的 `level`。

| `type` | 用途 | 默认目录 |
|---|---|---|
| `concept` | 可复用的事实性知识概念 | Cognition、Language |
| `procedure` | 可执行技能、流程和检查表 | Skill |
| `hypothesis` | 尚待证据支持的观点或研究假设 | Horizon |
| `question` | 待探索问题 | Horizon/questions |
| `experiment` | 验证假设的实验记录 | Horizon/experiments |
| `review` | 复盘、审阅和变更决策 | Meta/reviews |
| `moc` | 目录地图 | 各目录 `_moc.md` |

`raw/` 是不可变来源层，不要求统一 frontmatter，也不参与概念页结构校验。

---

## 3. 概念页 Frontmatter

```yaml
---
schema_version: 1.1
title: 正交
aliases: [Orthogonality, 正交性]
summary: 两个向量内积为零时称为正交，表示它们在给定内积下彼此垂直
type: concept
maturity: evergreen
confidence: high
tags: [线性代数, 内积]
created: 2026-04-21
updated: 2026-07-16
verified: 2026-07-16
review_due: 2027-07-16
sources:
  - https://example.org/primary-source
---
```

### 3.1 字段定义

| 字段 | 必填 | 规则 |
|---|---|---|
| `schema_version` | 是 | 当前固定为 `1.1` |
| `title` | 是 | 人类可读显示名；允许与文件名不同 |
| `aliases` | 是 | 搜索别名；允许空列表，所有别名必须全库唯一 |
| `summary` | 是 | 一句话完整定义；建议 25–50 字，硬上限 60 字，不用省略号截断 |
| `type` | 是 | 使用第 2 节中的枚举 |
| `maturity` | 是 | `seed`、`growing`、`evergreen` |
| `confidence` | 是 | `low`、`medium`、`high`，表示证据置信度而非完成度 |
| `tags` | 是 | 允许空列表；只用于跨目录聚类，不重复目录分类 |
| `created` | 是 | 首次形成此笔记的日期 |
| `updated` | 是 | 最近一次内容修改日期 |
| `verified` | 条件必填 | 完成事实和来源核验的日期；未核验时留空 |
| `review_due` | 条件必填 | 下一次建议复核日期；`evergreen` 必填 |
| `sources` | 是 | 来源列表；允许 seed/hypothesis 暂时为空 |

目录位置是唯一分类来源，概念页不再维护易漂移的 `category` 字段。Dataview 使用 `file.folder` 获取所属域。

### 3.2 生命周期

- `seed`：刚捕获，结构或来源可能不完整。
- `growing`：主干已形成，仍需补充关系、来源或细节。
- `evergreen`：定义、关键边界和来源已核验，可稳定复用。

任何内容修改都更新 `updated`；只有实际核对定义、关键论断和来源后才能更新 `verified`。迁移和格式化不得冒充事实核验。

`review_due` 由知识波动性决定，不设全库统一 90 天：数学基础可按年复核，快速变化的模型和工具可按 30–180 天复核。

---

## 4. 概念页正文结构

```markdown
# 概念名

> 与 frontmatter summary 文字一致的定义。

---

## 子主题 A

一段能够独立说明该分支是什么、为何重要的概述。

- 关键性质
- 适用条件
- 主要边界

### 深入细节 A1

推导、代码、图表、例子或证据。

---

## 子主题 B

概述后可以使用 bullets、表格、公式或代码，不强制固定形式。

---

## 关系网络

- 前置：[[概念A]] — 说明依赖关系
- 对比：[[概念B]] — 说明关键差异
- 应用：[[概念C]] — 说明使用场景

---

## 参考资料

- [来源标题](URL) — 该来源支持什么
```

### 4.1 结构规则

1. `summary` 是 L1 的规范来源；正文定义框是受 lint 约束的镜像，不能独立改写。
2. 禁止再使用 `## 概念` 或 `## 定义` 重复 L1。
3. 普通 L2 必须可独立理解：优先用一句简短概述；若列表、表格、公式或代码本身已构成清晰概览，也可直接作为引导。L2 不能无过渡地直接跳入 L3，并至少包含一种展开形式（结构块、L3 或多个实质段落）。
4. L3 仅在确实需要下钻时使用，不强制每个 L2 都创建 `###`。
5. `关系网络`、`参考资料`、`变更记录`、`记忆口诀`、`记忆要点` 是辅助章节，不计入 L2 内容完整度。
6. `---` 是可选视觉分隔符，不作为结构语义。

### 4.2 拆分规则

满足任一条件时，将子主题升级为独立概念页：

- 本身可独立定义并被多个页面引用；
- 单个 L2 超过约 200 行或含 3 个以上大型 L3；
- 与父概念具有不同的复核周期或来源集合。

父页保留简要概述，并链接到新概念；避免在父子页面复制同一份完整内容。

---

## 5. 链接与关系

### 5.1 链接规则

- 链接目标必须使用真实文件名：`[[kv-cache|KV Cache]]`。
- 标题和别名用于显示与搜索，不作为猜测文件名的依据。
- 子主题链接使用 `[[概念文件#子主题|显示名]]`。
- raw 来源使用存在的仓库相对路径：`[[raw/human_ai_knowledge/file.md]]`。
- 不存在的未来概念不能写成 wikilink；使用 `待建：概念名`，并在 Horizon 中登记。

### 5.2 关系网络

`## 关系网络` 是概念关系的唯一人工维护位置，不再在 frontmatter 重复维护 `related`。

推荐关系标签：`前置`、`组成`、`对比`、`扩展`、`应用`、`相关`。`growing` 和 `evergreen` 页面至少应有 2 个指向现有概念的关系；seed 可以暂时较少。

---

## 6. 来源与证据

- 事实性 `concept`/`procedure` 达到 `evergreen` 前必须至少有一个可访问来源。
- 快速变化的技术优先使用官方文档、规范或原始论文，并记录版本或日期。
- `hypothesis` 必须明确区分“观察”“推断”“待验证问题”，不能用 `high` 置信度代替证据。
- `sources` 保存机器可读地址；`## 参考资料` 可补充来源作用、章节和限制。
- raw 文件不可由 Agent 静默改写；需要修订时创建新版本或评注页。

---

## 7. MOC 与首页

MOC frontmatter：

```yaml
---
schema_version: 1.1
title: 数学概念地图
type: moc
scope: Cognition/Math
---
```

子域 MOC 只查询直接目录：

```dataview
TABLE summary AS "定义", maturity AS "成熟度", verified AS "已核验"
FROM ""
WHERE file.folder = this.scope AND type != "moc"
SORT title ASC
```

域级 MOC 应先显式列出子域入口，再提供可选的全域聚合视图。首页“最近更新”按 `updated` 排序；复核队列按 `review_due`、空来源和低置信度排序。

---

## 8. 自我进化闭环

```text
raw / 对话 / 观察
        ↓
seed 候选页
        ↓
结构 lint + 去重 + 链接建议
        ↓
来源核验 / 实验验证
        ↓
人工批准为 growing 或 evergreen
        ↓
review_due 到期或依赖变化
        ↓
生成变更提案与 diff，再次批准
```

Agent 可以自动发现问题、生成候选页和提出 diff，但不得在没有可追溯记录的情况下静默改写 evergreen 事实。

### 8.1 Ingest

1. 搜索文件名、标题和 aliases，避免重复概念。
2. 使用模板创建 `seed` 页面，填写来源或 origin。
3. 写 L1、至少两个 L2，并建立已有概念关系。
4. 运行 lint，通过后在 `log.md` 追加记录。

#### 候选节点与占位规则

- 不创建 `summary: TBD`、仅有标题或仅有关系链接的空概念文件；空壳会让图谱看似连通，却没有可复用知识。
- 已有最小定义和主干时，创建 `maturity: seed` 页面：L1 必须是有效定义，正文至少有一个实质 L2，并以两个 L2 为 ingest 目标；来源可以暂时为空。
- 信息不足以形成 L1 时，不创建概念页：在 `Horizon/questions/` 登记待探索问题，并在正文用 `待建：概念名`，不写未解析 wikilink。
- 旧版 `status: placeholder` 迁移为 `seed` 只是生命周期映射，仍须补齐定义和正文才能通过 lint；Agent 不得通过跳过校验让占位永久化。

### 8.2 Update

1. 修改内容并更新 `updated`。
2. 如完成事实核验，再更新 `verified`、`review_due` 和 `confidence`。
3. 对 evergreen 修改保留来源和变更摘要。
4. 运行 lint，并在 `log.md` 追加记录。

### 8.3 Review

1. 从首页复核队列选择页面。
2. 检查来源可访问性、关键论断、断链和重复内容。
3. 在 `Meta/reviews/` 记录有实质判断的复核。
4. 通过后调整 maturity；未通过则保留 seed/growing 并写明缺口。

---

## 9. Lint 契约

`_system/lint.py` 至少检查：

| 检查项 | 严重度 |
|---|---|
| YAML 无法解析、必填字段缺失、非法枚举 | error |
| 断开的 wikilink、raw 链接或本地 Markdown 链接 | error |
| MOC scope 与目录不一致 | error |
| L1 定义缺失或与 summary 不一致 | error |
| `TBD` 等占位定义或无实质 L2 的空知识节点 | error |
| 文件名、title、alias 发生全库歧义 | error |
| growing/evergreen 关系不足或 evergreen 无来源 | warning/error |
| verified/review_due 生命周期不一致 | warning |
| 普通 L2 缺少概述或展开内容 | warning |
| 空标签、可复用知识页的孤儿、建议拆分 | info/warning |

lint 默认只读并输出终端报告；只有显式 `--report` 才写 `_system/lint-report.md`，只有显式修复命令才能改内容。

---

## 10. 目录约定

```text
progressive-kg/
├── home.md
├── SCHEMA.md
├── log.md
├── Cognition/
├── Skill/
├── Language/
├── Meta/
│   └── reviews/
├── Horizon/
│   ├── questions/
│   └── experiments/
├── comparisons/
├── queries/
├── raw/
└── _system/
    ├── templates/
    │   ├── concept.md
    │   ├── moc.md
    │   └── review.md
    ├── lint.py
    ├── migrate_schema_v1_1.py
    ├── requirements.txt
    ├── tests/
    └── snippets/
```

- 文件名使用稳定、简洁的概念名；显示名和外文名放入 `title`/`aliases`。
- `_moc.md` 固定作为目录入口。
- `comparisons/` 和 `queries/` 保存有复用价值的综合产物，不复制概念页正文。
- `log.md` 只追加有意义的知识库操作，不记录每次无变化的定时检查。

---

## 11. 版本历史

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-07-01 | 1.0 | 建立三层披露、frontmatter、MOC 和维护协议 |
| 2026-07-16 | 1.1 | 分离导航与披露层级；引入 type、maturity、updated/verified/review_due；放宽 L2；统一关系、来源和自我进化闭环 |
| 2026-07-17 | 1.1 | 明确禁止永久空占位；候选概念使用 seed，信息不足时转入 Horizon 问题队列 |
