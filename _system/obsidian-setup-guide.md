# Obsidian 配置指南

> 在新机器上恢复 Progressive-KG 的 Home 仪表盘、三层阅读样式和可选图谱。

**更新**：2026-07-16

**配置契约**：`home.md` 是主入口；Graph View 是辅助探索工具，不能替代 Home 和 MOC 导航。

---

## 1. 打开 Vault

用 Obsidian 的 **Open folder as vault** 打开仓库根目录。Windows 版 Obsidian 推荐使用 Windows 本地路径，例如：

```text
D:\Documents\progressive-kg
```

WSL 可通过 `/mnt/d/...` 访问同一目录，不需要复制出第二份知识库。若使用其他同步方案，先确认文件监听、插件目录和 Git 不会产生双向冲突。

## 2. 恢复 Home 主入口

1. 用 `Ctrl+O` 打开 `home`。
2. 切换到 Reading View。
3. 将 Home 标签页固定（Pin），或加入 Bookmarks。
4. 退出 Obsidian 前保持 Home 为当前页；工作区会在本机 `.obsidian/workspace.json` 记住它。

当前参考工作区满足：

```text
startup file: home.md
view mode: preview / Reading View
CSS class: kg-home
```

`.obsidian/workspace.json` 是机器和屏幕相关状态，已被 Git 忽略。换机器后需要执行一次上述步骤，不能只靠图谱配置恢复入口。

## 3. 安装插件

打开 `Settings → Community plugins`。

### 必需：Dataview

Home 的“最近更新”“待审阅”和所有 `_moc.md` 动态表格依赖 Dataview。未安装或未启用时，这些区域会显示原始代码块，但普通 Markdown 和链接仍可阅读。

### 可选：Persistent Graph

仅用于保存全局 Graph View 的节点位置。它不影响 Home、MOC、双链或正文阅读；不使用全局图谱时可以不装。

社区插件应通过 Obsidian 安装。不要从另一台机器直接复制整个插件运行目录，以免带入不兼容版本。

## 4. 启用层级 CSS

源文件：

```text
_system/snippets/hierarchy-visual.css
```

本机生效位置：

```text
.obsidian/snippets/hierarchy-visual.css
```

操作：

1. `Settings → Appearance → CSS snippets`，点击文件夹图标。
2. 把源文件复制到该目录。
3. 刷新 snippets 列表并启用 `hierarchy-visual`。
4. 在 Reading View 检查 L1 引用框、L2 色块和 L3 细线。

CSS 只增强视觉，不决定知识语义。修改时先改 `_system/snippets/` 中的版本控制源，再同步到本机 `.obsidian/snippets/`。

## 5. Home 验收

打开 `home.md` 后逐项检查：

- 顶部标题和蓝色定义框正常显示。
- 五个域入口都可点击：Cognition、Skill、Language、Meta、Horizon。
- “最近更新”渲染为表格，并按 `updated` 排序。
- “待审阅”渲染为表格，能显示 growing、低置信度、未核验或到期页面。
- “关于”中的 Schema、日志和模板可打开。
- 进入概念页后，L2/L3 视觉层级仍正常。

若表格显示为代码，先检查 Dataview；若只有样式缺失，检查 CSS snippet；不要先切换到 Graph View 排查。

## 6. 当前 Schema 1.1 Frontmatter

新概念使用 `_system/templates/concept.md`，核心字段如下：

```yaml
---
schema_version: '1.1'
title: 概念名
aliases: []
summary: 一句话完整定义
type: concept
maturity: seed
confidence: low
tags: []
created: '2026-07-16'
updated: '2026-07-16'
verified:
review_due:
sources: []
---
```

不要再使用旧字段：`level`、`category`、`related`、`last_verified`、`status`。关系只写在正文 `## 关系网络`；目录位置负责分类；事实核验完成后才填写 `verified`。

日期写成 ISO `YYYY-MM-DD`。列表使用合法 YAML block list 或 flow list；具体约束以 `SCHEMA.md` 和 lint 为准。

## 7. 可选 Graph View

Graph View 用于发现关系和孤立点，不承担主要导航。参考过滤器：

```text
-path:raw -path:_system -file:_moc -file:home -file:SCHEMA -file:log
```

参考颜色组：

| 查询 | 域 |
|---|---|
| `path:Cognition/Math` | 数学 |
| `path:Cognition/Model` | 模型 |
| `path:Skill/dl-training` | 训练技能 |
| `path:Skill` | 其他技能 |
| `path:Meta` | 元认知 |
| `path:Cognition` | 其他认知 |

`.obsidian/graph.json` 是本机配置。需要迁移时可手动复制，但 Home 是否可用仍以第 5 节验收为准。

## 8. 核心插件与本地配置

当前参考配置开启 Files、Search、Quick Switcher、Graph、Backlinks、Outgoing Links、Properties、Templates、Bookmarks、Outline、File Recovery、Canvas 和 Bases；Daily Notes、Sync 等不是本库必需项。

仓库 `.gitignore` 忽略整个 `.obsidian/`，所以：

- 可版本控制的说明和 CSS 源放在 `_system/`；
- 插件二进制、workspace、个人快捷键保留在本机；
- 配置快照见 `_system/obsidian-config-reference.md`。

## 9. 内容校验

在仓库根目录执行：

```bash
python3 _system/lint.py
python3 -m unittest discover -s _system/tests -v
```

lint 默认只读。需要生成 Markdown 报告时显式加 `--report`；内容变更完成后在 `log.md` 追加记录。
