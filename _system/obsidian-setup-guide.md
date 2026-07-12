# Obsidian 配置指南

> 在新机器上配置 progressive-kg vault 的完整步骤。
> 基于 2026-07-09 的本机配置整理。

---

## 1. 获取项目

```bash
# WSL 侧
cd ~/.openclaw/workspace
git clone git@github.com:wolfhawkld/progressive-kg.git

# 如果 Obsidian 在 Windows 上运行，需要把 vault 放到 Windows 本地路径
# Obsidian 不支持 WSL 的 UNC 路径 (\\wsl.localhost\...)
# 方案：vault 放 Windows 本地，WSL 用 symlink 访问
cp -r progressive-kg /mnt/c/Users/<username>/Documents/progressive-kg
rm -rf progressive-kg
ln -s /mnt/c/Users/<username>/Documents/progressive-kg progressive-kg
```

---

## 2. 安装社区插件

Settings -> Community plugins -> 关闭 Safe Mode -> Browse

**必须安装的插件：**

### Dataview
- 搜索：`Dataview`
- 用途：MOC 文件中的 ```` ```dataview ```` 查询块依赖此插件渲染
- 不装的话 home.md 和所有 _moc.md 的动态表格会显示为原始代码

### Persistent Graph
- 搜索：`Persistent Graph`
- 用途：保存和恢复 Graph View 的节点位置，避免每次打开图谱时节点随机重排
- 安装后设置：
  - 打开 Graph View (Ctrl+G)，等节点稳定到满意位置
  - Ctrl+P -> 搜索 "Persistent Graph: Save" 保存当前布局
  - 插件设置中打开 "Automatically restore on open"（自动恢复）

---

## 3. Graph View 配置

打开 Graph View (Ctrl+G) -> 点右上角齿轮图标

### 过滤器（Filter / Search 栏）

在搜索栏粘贴以下内容（隐藏非概念节点，保持图谱干净）：

```
-path:raw -path:_system -file:_moc -file:home -file:SCHEMA -file:log
```

作用：
- `-path:raw` — 隐藏原始素材文件
- `-path:_system` — 隐藏脚本和模板
- `-file:_moc` — 隐藏 MOC 索引文件
- `-file:home` / `-file:SCHEMA` / `-file:log` — 隐藏系统文件

**注意：不要按 Ctrl+F 清空搜索栏，这个搜索栏就是过滤器。**

### 颜色分组（Groups）

在齿轮设置底部的 "Groups" 区域添加以下分组（按顺序）：

| Group 查询 | 颜色 | RGB 值 | 对应域 |
|---|---|---|---|
| `path:Cognition/Math` | 🔵 蓝色 | 5227511 | 数学概念 |
| `path:Cognition/Model` | 🟢 绿色 | 6732650 | 模型架构 |
| `path:Skill/dl-training` | 🟠 橙色 | 16754470 | 训练技能 |
| `path:Skill` | 🔴 红色 | 15684432 | 其他技能 |
| `path:Meta` | 🟣 紫色 | 11225020 | 元认知 |
| `path:Cognition` | 🩵 青色 | 3375058 | 其他认知 |

新增域时联系 Nemesis 添加新颜色组。

### 显示设置

| 设置项 | 推荐值 | 理由 |
|---|---|---|
| Node size | 1.2x | 节点稍大，更易点击 |
| Show attachments | 关 | 不显示 raw 文件 |
| Show tags | 关 | 不显示标签节点 |
| Show existing files only | 开 | 隐藏断链的空节点 |
| Show orphans | 开 | 便于发现孤立概念 |

### 或者直接复制配置文件

如果两台机器都是同样的 Obsidian 版本，可以直接复制配置文件：

```bash
# graph.json 包含过滤器、颜色分组、显示设置
cp .obsidian/graph.json <新机器vault>/.obsidian/graph.json
```

---

## 4. 快捷操作备忘

| 操作 | 快捷键 | 说明 |
|---|---|---|
| 全局图谱 | Ctrl+G | 看全景，搜索栏保持 filter 不动 |
| 快速打开概念 | Ctrl+O | 输入概念名直接打开文件 |
| Local Graph | Ctrl+P -> "Open local graph" | 看当前概念的邻居关系 |
| 命令面板 | Ctrl+P | 搜索所有命令 |

**重要提醒：**
- Graph View 的搜索栏是过滤器，不是搜索框。不要 Ctrl+F 清空它
- 查找概念用 Ctrl+O（Quick Open），不要在图谱搜索栏里输
- 不要点击 Obsidian 里红色的断链（未创建的概念），点击会创建空文件

---

## 5. 核心插件状态

以下核心插件保持开启（均为默认）：

```
file-explorer, global-search, switcher, graph, backlink,
canvas, outgoing-link, tag-pane, properties, page-preview,
daily-notes, templates, note-composer, command-palette,
editor-status, bookmarks, outline, word-count, file-recovery, sync, bases
```

---

## 6. YAML Frontmatter 格式规范

生成概念笔记时必须遵守（否则 Obsidian Properties 面板报红）：

```yaml
---
title: 概念名
summary: 一句话定义不超过50字
level: concept
category: Cognition/Math
tags: [标签1, 标签2]
related:
  - "[[概念A]]"
  - "[[概念B]]"
created: 2026-07-09
last_verified: 2026-07-09
confidence: medium
status: draft
---
```

**红线：**
1. `related` 用 YAML 块列表格式（`- "[[item]]"` 换行缩进），**不能用逗号分隔**
2. `summary` **不能用双引号包裹**，直接写裸值
3. `title` 不加引号
4. `tags` 用流式格式 `[tag1, tag2]` 或空 `[]`

---

## 7. 配置文件清单

如果直接复制配置，需要这些文件：

```
.obsidian/
├── graph.json              # 图谱过滤器 + 颜色分组 + 显示设置
├── core-plugins.json       # 核心插件开关状态
├── community-plugins.json  # 社区插件列表 ["dataview", "persistent-graph"]
└── plugins/
    ├── dataview/            # Dataview 插件（从社区安装，不可直接复制）
    └── persistent-graph/    # Persistent Graph 插件（同上）
```

**注意**：`community-plugins.json` 和 `plugins/` 目录不能直接复制——需要在新机器上通过 Obsidian 的 Community Plugins 浏览器重新安装。`graph.json` 和 `core-plugins.json` 可以直接复制。

`workspace.json` **不要复制**——它包含当前窗口布局，与具体机器的屏幕分辨率相关。

---

*整理人：Nemesis · 2026-07-09*
