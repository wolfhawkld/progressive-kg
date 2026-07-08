# Progressive-KG Schema

> 渐进式知识图谱的结构约定、层级规则、链接规范与维护协议。
> 本文件是 Agent 和人类共同遵守的知识维护契约。

**版本**: 1.0  
**创建**: 2026-07-01  
**维护者**: Damon + Nemesis

---

## 1. 核心模型：三层渐进式披露（一对多树状展开）

每个知识概念按三个层级组织，每一层对下一层是一对多关系：

```
Level 1 — 定义层（一个概念 → 一句话定义 + 多个 Level 2 子主题链接）
  │
  ├── Level 2 — 要点层（一个子主题 → 一段话 + bullets + 多个 Level 3 细节）
  │     │
  │     ├── Level 3 — 细节层（推导、代码、图示、证明、引用...）
  │     ├── Level 3
  │     └── Level 3
  │
  ├── Level 2
  │     ├── Level 3
  │     └── Level 3
  │
  └── Level 2
        └── Level 3
```

### Level 1 — 定义层

- **形态**：概念笔记文件的 frontmatter `summary` 字段 + 文件开头的 blockquote
- **内容**：一句话定义（≤50 字），说清"是什么"
- **交互**：MOC 中通过 Dataview 渲染为表格行；Obsidian hover 预览自动显示
- **一对多**：一个概念展开为多个 Level 2 子主题（`##` 标题）

### Level 2 — 要点层

- **形态**：概念笔记内的 `##` 标题段落
- **内容**：一段话概述 + 3-5 个 bullet points（关键性质、适用条件、核心公式）
- **交互**：打开文件即见；Obsidian 中可通过 `[[概念名#子主题]]` 直接链接
- **一对多**：一个子主题展开为多个 Level 3 细节（`###` 标题或正文内容）

### Level 3 — 细节层

- **形态**：`##` 标题下的 `###` 子标题 + 正文内容
- **内容**：完整推导、代码示例、图表、证明过程、参考文献链接
- **交互**：滚动展开；如内容极长可拆为独立文件并链接
- **终止层**：不再下钻

### 渐进披露的物理实现

单文件 + Obsidian 原生功能，无需额外插件：

| 层级 | 物理位置 | Obsidian 交互 |
|---|---|---|
| Level 1 | frontmatter `summary` + 文件首行 blockquote | MOC Dataview 表格 / hover 预览 |
| Level 2 | `##` 标题 + 其下第一段 + bullets | 打开文件即见 / `[[file#section]]` 精确链接 |
| Level 3 | `###` 标题下的完整正文 | 滚动展开 / 点击折叠区 |

---

## 2. 文件结构

```
progressive-kg/
├── SCHEMA.md                # 本文件——结构约定与维护契约
├── home.md                  # 入口页，链接到各域 MOC
├── log.md                   # 变更日志（append-only）
│
├── Cognition/               # 认知域
│   ├── _moc.md              # 域级 MOC（Dataview 渲染 Level 1）
│   ├── Math/
│   │   ├── _moc.md          # 子域 MOC
│   │   ├── 正交.md           # 概念笔记（Level 1+2+3）
│   │   ├── 内积.md
│   │   └── ...
│   ├── Model/
│   │   ├── _moc.md
│   │   └── ...
│   └── ...
│
├── Skill/                   # 技能域
├── Language/                # 语言域
├── Meta/                    # 元认知域
├── Horizon/                 # 探索域
│
├── comparisons/             # 跨域对比分析
├── queries/                 # 有价值的查询结果归档
│
├── raw/                     # 原始素材（不可变，Agent 只读）
│   ├── human_ai_knowledge/  # 人机知识文章（迁移）
│   ├── articles/            # 外部文章
│   └── papers/              # 论文
│
└── _system/                 # 系统文件（不参与知识图谱）
    ├── templates/
    │   ├── concept.md       # 概念笔记模板
    │   └── moc.md           # MOC 模板
    ├── lint.py              # 健康检查脚本
    └── migrate.py           # 迁移脚本
```

### 命名约定

- **概念笔记**：中文名或英文名，不加编号。如 `正交.md`、`flash-attention.md`
- **MOC 文件**：`_moc.md`（下划线前缀，Obsidian 中排在目录最前）
- **系统文件**：`_` 前缀目录（`_system/`），不参与图谱
- **raw 文件**：保持原始文件名，不做重命名

---

## 3. Frontmatter 规范

每个概念笔记必须包含以下 YAML frontmatter：

```yaml
---
title: 正交                          # 概念名（与文件名一致，不含 .md）
summary: 两向量内积为零，方向独立互不影响  # Level 1：一句话定义（≤50字）
level: concept                        # 节点类型：concept | moc | raw | meta
category: Cognition/Math              # 域/子域路径
tags: [线性代数, 内积, 正交初始化]      # 标签（用于跨域聚类）
related: [[内积]], [[外积]], [[Muon优化器]]  # 强关联概念（双向链接）
created: 2026-04-21                   # 创建日期
last_verified: 2026-07-01             # 最后验证日期（lint 时更新）
confidence: high                      # high | medium | low
status: stable                        # stable | draft | stale | contested
sources:                              # Level 3 的原始素材来源
  - raw/human_ai_knowledge/standardization-ml-dl-rl.md
---
```

### 字段说明

| 字段 | 必填 | 用途 |
|---|---|---|
| `title` | ✅ | 概念名，与文件名一致 |
| `summary` | ✅ | Level 1 定义，MOC 中渲染 |
| `level` | ✅ | 节点类型，决定 MOC 查询过滤 |
| `category` | ✅ | 域路径，用于目录组织和 MOC 分组 |
| `tags` | ✅ | 跨域标签，用于 Dataview 聚类查询 |
| `related` | ✅ | 强关联概念，构建双链网络 |
| `created` | ✅ | 创建日期 |
| `last_verified` | ✅ | 最后验证日期，lint 时检查是否过时 |
| `confidence` | ⬜ | 置信度，low 的优先 review |
| `status` | ⬜ | 状态标记，stale/contested 需要人工审阅 |
| `sources` | ⬜ | Level 3 内容的原始来源，可追溯 |

---

## 4. 概念笔记结构规范

每个概念笔记的正文按以下结构组织：

```markdown
---
（frontmatter）
---

# 概念名

> 一句话定义（与 frontmatter summary 一致）。

---

## 子主题 A                    ← Level 2（一对多中的"多"之一）

一段话概述这个子主题是什么、为什么重要。

- **要点 1**：关键性质或公式
- **要点 2**：适用条件
- **要点 3**：与其他概念的关系

### 细节项 A1                  ← Level 3（一对多中的"多"之一）
（完整推导 / 代码 / 图表...）

### 细节项 A2
（...）

---

## 子主题 B                    ← Level 2

一段话概述。

- **要点 1**
- **要点 2**

### 细节项 B1                  ← Level 3
（...）

---

## 关系网络

- 依赖 [[概念X]] — 说明依赖关系
- 扩展到 [[概念Y]] — 说明扩展方向
- 应用于 [[概念Z]] — 说明应用场景

---

## 参考资料

- [来源名称](链接或路径)
- [[raw/原始素材文件]]
```

### 结构规则

1. **Level 1**：文件开头的 blockquote，与 `summary` 一致
2. **Level 2**：每个 `##` 标题是一个子主题，必须有一段话 + bullets
3. **Level 3**：每个 `##` 下可以有多个 `###` 细节项，是完整内容
4. **`---` 分隔线**：Level 2 之间用 `---` 分隔，视觉上区分树状分支
5. **关系网络**：放在正文末尾，集中列出 `[[双链]]`
6. **参考资料**：链接到 raw/ 目录的原始素材

### 参考资料链接格式

来自 human_ai_knowledge 的源文件同时提供本地 MD 链接和 GitHub Pages HTML 链接：

```markdown
- [[raw/human_ai_knowledge/filename.md]] | [🌐 HTML](https://wolfhawkld.github.io/human_ai_knowledge/filename.html) — 说明文字
```

仅本地有 MD 文件（如 2nd_brain 源文件）的只放 wikilink：

```markdown
- [[raw/human_ai_knowledge/filename.md]] — 说明文字
```

### 何时拆分为独立文件

当一个 Level 2 子主题满足以下任一条件时，应拆为独立文件：
- 有 3 个以上 Level 3 细节项且总长超过 200 行
- 被其他概念笔记独立引用（跨概念链接）
- 本身是一个可独立成立的概念

拆分时：
- 新文件名：`父概念-子主题.md`（如 `正交-正交矩阵.md`）
- 父概念文件中该子主题改为：`## [正交矩阵](正交-正交矩阵.md)`
- 子文件 frontmatter 加 `parent: [[正交]]`

---

## 5. MOC 文件规范

MOC（Map of Content）是 Level 1 的渲染层，用 Dataview 自动从概念笔记的 frontmatter 生成。

### 域级 MOC（`_moc.md`）

```markdown
---
title: 数学概念地图
level: moc
category: Cognition/Math
---

# 数学概念地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "Cognition/Math"
WHERE level = "concept"
SORT title ASC
```

## 按标签聚类

```dataview
TABLE summary AS "定义"
FROM "Cognition/Math"
WHERE contains(tags, "线性代数")
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "Cognition/Math"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
```

### home.md

```markdown
# 🏠 Progressive-KG

## 域导航

- [[Cognition/_moc|🧠 认知]] — 数学、模型、工作、生活
- [[Skill/_moc|⚡ 技能]] — 编程、写作、管理
- [[Language/_moc|📝 语言]] — 学术英语
- [[Meta/_moc|🔮 元认知]] — 方法论、复盘
- [[Horizon/_moc|🔭 探索]] — 待探索问题、实验记录

## 最近更新

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM ""
WHERE level = "concept"
SORT last_verified DESC
LIMIT 10
```
```

---

## 6. 链接规范

### 双链（`[[wikilink]]`）

- **概念间链接**：`[[概念名]]` 或 `[[概念名|显示文本]]`
- **子主题链接**：`[[概念名#子主题]]`（链接到 Level 2）
- **raw 链接**：`[[raw/文件名]]`（链接到原始素材）

### 链接密度规则

- 每个概念笔记的"关系网络"节至少有 2 个出链
- 每个 Level 2 子主题正文中至少有 1 个相关概念链接
- 孤儿页（无入链的概念）会被 lint 标记

---

## 7. 维护协议

### Ingest（摄入新概念）

1. 确认概念所属域和子域
2. 用 `_system/templates/concept.md` 创建新文件
3. 填写 frontmatter（`summary` 必须是一句话定义）
4. 写 Level 2 子主题（至少 2 个）和 Level 3 细节
5. 在关系网络中链接到至少 2 个相关概念
6. 更新所属域的 `_moc.md`（Dataview 自动渲染，无需手动改）
7. 在 `log.md` 追加：`## [YYYY-MM-DD] ingest | 概念名`

### Update（更新已有概念）

1. 修改内容，bump `last_verified` 为当天
2. 如新增子主题，确保 `##` 结构完整
3. 如拆分独立文件，更新父文件的链接
4. 在 `log.md` 追加：`## [YYYY-MM-DD] update | 概念名 — 变更摘要`

### Lint（健康检查）

由 `_system/lint.py` 执行，检查项：

| 检查项 | 规则 | 严重度 |
|---|---|---|
| 孤儿页 | 无入链的概念笔记 | warning |
| 断链 | `[[wikilink]]` 指向不存在的文件 | error |
| 缺失 frontmatter | 必填字段缺失 | error |
| 过时节点 | `last_verified` 超过 90 天 | warning → 标记 `status: stale` |
| 缺少出链 | "关系网络"节出链 < 2 | warning |
| 文件过长 | 超过 300 行且未拆分 | info |
| 标签外溢 | 使用了未在 SCHEMA 中定义的域 | info |

lint 结果输出到 `_system/lint-report.md`，并追加到 `log.md`。

### Consolidate（整理合并）

当 Damon 说"整理 X 域"时：
1. Agent 扫描该域所有概念笔记
2. 识别重复概念 → 合并（保留较完整的，迁移链接）
3. 识别缺失关联 → 建议新链接
4. 更新所有 `last_verified`
5. 重建 MOC（Dataview 自动完成）
6. 在 `log.md` 追加整理记录

---

## 8. 迁移规则

### 从 2nd_brain 迁移

1. 保留原目录结构（Cognition/Math/ 等）
2. 为每个概念笔记添加 frontmatter：
   - `summary`：从文件第一段或 blockquote 提取
   - `level: concept`
   - `category`：根据目录路径生成
   - `tags`：从文件末尾的标签行提取
   - `created`：从文件末尾的创建时间提取
   - `last_verified`：设为迁移当天
3. 将 `moc.md` 重命名为 `_moc.md`，替换内容为 Dataview 查询
4. 在 `log.md` 记录迁移

### 从 human_ai_knowledge 迁移

1. 将 48 篇 .md 文件复制到 `raw/human_ai_knowledge/`（不可变层）
2. 为每篇有独立概念价值的文章创建概念笔记
3. 概念笔记的 `sources` 字段链接到 raw 文件
4. 概念笔记只提取 Level 1+2（定义 + 要点），Level 3 链接到 raw 原文
5. 在 `log.md` 记录迁移

---

## 9. 与 Agent 的交互约定

| 操作 | 触发方式 | Agent 行为 |
|---|---|---|
| Ingest | Damon 说"记录概念 X" | 读素材 → 生成概念笔记 → 更新 log |
| Query | Damon 问"X 和 Y 的关系" | 读 MOC → 读 Level 2 → 合成答案 → 有价值则归档到 queries/ |
| Lint | Hermes cron 每周 | 跑 lint.py → 标记过时 → 报告 |
| Consolidate | Damon 说"整理 X 域" | 扫描 → 合并重复 → 更新链接 → 重建 MOC |
| Migrate | Damon 说"迁移 2nd_brain" | 运行 migrate.py → 批量加 frontmatter |

Agent 操作前必须先读 SCHEMA.md（本文件）和目标域的 _moc.md，避免创建重复概念。

---

## 10. 版本历史

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-07-01 | 1.0 | 初始版本，定义三层渐进披露模型、文件结构、frontmatter、MOC、链接、维护协议 |
