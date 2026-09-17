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

<!-- living-memory:begin -->
## Living Memory 日常触发（本机可选集成）

若存在 `_system/living-memory.local.json`，在下列流程成功后调用收尾钩子：

- **Query**：已检索、阅读所需层级并合成有来源的回答；无匹配也可以结束查询。
- **Ingest / Consolidate**：实际修改完成，且已通过本库要求的 lint。仅提出建议或操作失败时不调用。

```bash
python3 _system/living_memory_hook.py query --operation-id <本次操作ID>
python3 _system/living_memory_hook.py ingest --operation-id <本次操作ID>
python3 _system/living_memory_hook.py consolidate --operation-id <本次操作ID>
```

只执行与本次流程相符的一条命令。每次新操作生成新 ID；同一次操作重试复用 ID。钩子从本地配置定位 Living Memory，核对知识根目录，并刷新当前加载范围内的节点、关系和时间状态。未配置的协作者可跳过。

查询、生成、资料呈现和系统读取都**不代表用户已经重温或掌握**。此钩子不得调用 `review`；用户明确确认重温时，另用 Living Memory CLI 或 Web 的确认入口。不得修改笔记的学习时间，或借此更新 `verified`、`maturity` 等内容字段。

刷新失败时保留已完成的知识操作和查询答案，说明“图谱刷新待恢复”，不要宣称已同步；服务恢复后重试同一命令。此集成依赖 Agent 遵循流程，不是自动监视所有文件修改的后台服务。
<!-- living-memory:end -->
