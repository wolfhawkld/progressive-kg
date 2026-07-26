# AGENTS.md - Progressive-KG

> 本文件是所有 agent 操作此知识库的统一入口。
> 无论你是什么 agent（Hermes、OpenClaw、Codex 或其他工具），操作前先读这两个文件：

## 必读文件

1. **`SCHEMA.md`** - 结构契约（frontmatter 格式、层级规则、链接规范、生命周期）
2. **`_system/OPERATIONS.md`** - 操作流程（Ingest/Query/Consolidate/Lint/Maintain 等工作流）

## 快速索引

| 需求 | 读哪里 |
|---|---|
| 概念笔记怎么写 | `SCHEMA.md` 第 3-4 节 |
| frontmatter 字段 | `SCHEMA.md` 第 3 节 |
| 生成/查询/整理概念 | `_system/OPERATIONS.md` |
| 运行健康检查 | `python3 _system/lint.py` |
| Obsidian 配置 | `_system/obsidian-setup-guide.md` |

## 触发词

用户可能用以下语句触发操作（详见 `_system/OPERATIONS.md`）：

- "生成概念 X" / "新建概念" / "记录概念" -> Ingest
- "查询概念 X" / "X 是什么" -> Query
- "整理 X 域" -> Consolidate
- "检查知识图谱" / "lint" -> Lint
- "补全关联" -> Maintain
- "升级 seed" / "查看 seed" -> seed 节点管理

## 黄金规则

1. **SCHEMA.md 是权威来源** - 不要凭记忆写 frontmatter，每次操作前确认当前 schema 版本
2. **写完必须 lint** - `python3 _system/lint.py` 通过才算完成
3. **raw/ 不可修改** - 只读引用
4. **新建前必须查重** - 搜索文件名、title 和 aliases
5. **git 同步** - 操作前 `git pull`，完成后 `git push`
