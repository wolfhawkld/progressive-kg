# Progressive-KG 操作流程

> 本文件定义所有 agent 通用的工作流，与 `SCHEMA.md`（结构契约）配合使用。
> 任何 agent（Hermes、OpenClaw、Codex 或其他工具）操作 progressive-kg 前必须先读这两个文件。

## 1. 生成概念（Ingest）

触发：用户说"生成概念 X" / "记录概念 X" / "新建概念 X"

步骤：
1. **读 SCHEMA.md**：确认当前 schema 版本和格式要求
2. **查重**：搜索文件名、标题和 aliases，避免重复概念
   - 搜索目标域目录下是否已有同名或近义概念
   - 搜索 aliases 字段
   - 如果已存在，告知用户并询问是更新还是新建
3. **检索素材**：
   - 搜索 raw/ 目录
   - 搜索 human_ai_knowledge（如果存在）
   - 如需补充，web_search 查找权威资料
4. **确定域和路径**：根据概念性质选择 Cognition/Math、Cognition/Model、Skill/dl-training 等
5. **生成概念笔记**（按 SCHEMA.md 当前版本格式）：
   - frontmatter：按 SCHEMA.md 要求填写全部必填字段
   - L2 至少 2 个子主题，每个 L2 至少 1 个 L3 或等价展开
   - 关系网络至少 2 个出链（growing/evergreen 要求）
   - 参考资料用 markdown link 格式
6. **写入文件**：到目标域目录
7. **运行 lint**：`python3 _system/lint.py`
8. **更新 log.md**：追加 `## [YYYY-MM-DD] ingest | 概念名`
9. **告知用户**：文件路径 + 概念层级结构摘要

### Ingest 流程中的候选节点规则

在步骤 5（生成概念笔记）和步骤 6（写入文件）之间，处理候选关联概念：

1. **推理候选关联概念**：在写 `## 关系网络` 时，除已存在于 KG 中的概念外，记录"高度相关但不存在"的候选列表
2. **处理候选**：
   - 已有最小定义和主干 -> 创建 `maturity: seed` 页面（L1 必须是有效定义 + 至少一个实质 L2）
   - 信息不足以形成 L1 -> 不创建概念页，在 `Horizon/questions/` 登记待探索问题，正文用 `待建：概念名`
3. **告知用户**：在概念层级结构摘要中列出创建的 seed 节点和登记的待探索问题

### 关联推理方式

关联不是通过 BM25 关键词检索实现的，而是 **Agent 语义推理 -> KG 确认存在 -> 建立双链**：
1. Agent 基于对概念本身的理解，推理出应关联的其他概念
2. 搜索 KG 确认这些概念是否存在
3. 已存在的写入 `## 关系网络`，不存在的作为候选
4. 三层维度共同作用：LLM（语义推理）+ Agent（流程编排+格式约束）+ KG（目标节点确认）

## 2. 查询概念（Query）

触发：用户说"查询概念 X" / "X 和 Y 的关系" / "X 是什么"

步骤：
1. 搜索相关概念（在整个 progressive-kg 目录内搜索）
2. 读取匹配概念的 L1（summary）和 L2（## 标题 + 首段）
3. 如需深度，读取 L3 内容
4. 合成答案，引用来源概念
5. 如查询结果有归档价值，保存到 `queries/` 目录

## 3. 整理域（Consolidate）

触发：用户说"整理 X 域" / "整理数学概念"

步骤：
1. 列出该域所有概念笔记
2. 识别重复或近义概念 -> 建议合并
3. 识别缺失关联 -> 建议新链接
4. 更新所有 `verified` 为当天
5. 运行 lint：`python3 _system/lint.py`
6. 报告健康状态

## 4. 健康检查（Lint）

触发：用户说"检查知识图谱" / "lint"

步骤：
1. 运行：`python3 _system/lint.py`
2. 报告 error/warning/info 数量
3. 如有 error（断链），列出缺失概念，询问是否需要生成

## 5. 概念关联维护（Maintain）

触发：用户说"补全关联" / "检查关联网络"

### 5a. 补全关联（跨概念扫描）

扫描所有概念笔记的"关系网络"节，通过语义推理识别遗漏的关联。例如标准化和幂变换存在"数据预处理前后顺序"关系，但标准化.md 未链接幂变换。发现后报告，由用户确认是否追加。

步骤：
1. 构建所有概念 `title -> summary` 的索引
2. 对每个概念，推理应关联但未关联的其他概念
3. 报告发现的缺失关联，由用户确认是否追加
4. 对于确认的关联，双向在 `## 关系网络` 节追加（两个概念都加）

### 5b. 候选概念节点

概念生成时，如果推理出与已生成概念高度相关但不存在的概念：

- **已有最小定义**：创建 `maturity: seed` 页面（L1 必须是有效定义 + 至少一个实质 L2，来源可暂时为空）
- **信息不足**：不创建概念页，在 `Horizon/questions/` 登记待探索问题，正文用 `待建：概念名`（不写未解析 wikilink）

**禁止行为：** 不创建 `summary: TBD`、仅有标题或仅有关系链接的空概念文件。

### seed 节点升级

触发：用户说"升级 seed X" / "生成概念 X"（目标恰好是 seed 节点）

步骤：
1. 删除原 seed 节点
2. 按完整概念生成流程重建（三层结构）
3. `maturity: growing` 或更高，补齐 `verified` 和 `review_due`

### seed 节点批量升级

触发：用户说"升级所有 seed"

步骤：列出所有 `maturity: seed` 的节点，逐个确认是否升级。如有任何 seed 节点用户不想升级，可以手动删除。

## 6. 查看 seed 节点

触发：用户说"查看 seed 节点" / "列出 seed"

步骤：搜索所有 `maturity: seed` 的概念笔记，列出一览表

## 7. 去重与合并策略

当前 lint.py 只检查结构问题，不检查语义重复。以下策略按优先级排列，目前均为手动触发：

| 策略 | 优先级 | 影响 | 状态 |
|---|---|---|---|
| **占位空节点** | P0 - 已实现 | 防止关联断链，提供"待生成"提示 | 已加入 Ingest 流程 |
| **近义概念检测** | P1 - 建议尽快实现 | 防止"Box-Cox 变换"和"幂变换"作为两个独立概念存在 | 加入 Consolidate 流程 |
| **缺失关联检测** | P1 - 建议尽快实现 | 补全遗漏的双链，提升图谱密度 | 加入"补全关联"操作 |
| **强弱关联分级** | P2 - 可延后 | 区分"核心依赖"vs"松散相关"，避免双链过密 | 后续迭代 |
| **自动合并候选** | P2 - 可延后 | 对明显高度重合的概念自动建议合并（去重） | 后续迭代 |
| **关联置信度衰减** | P3 - 可延后 | 超过90天未被验证或增长的关联自动降 confidence | 后续迭代 |

## 8. 跨项目工作流：human_ai_knowledge 关联

当用户说"生成人机知识"时，human_ai_knowledge 项目独立完成话题文章生成和 HTML 发布（流程不变）。完成后，自动触发以下概念关联步骤：

1. **复制话题 MD 到 raw/**：`cp human_ai_knowledge/topic.md progressive-kg/raw/human_ai_knowledge/`
2. **识别话题中的概念**：扫描话题内容，识别涉及的 concept
3. **逐个概念处理**：
   - **已存在**：在 progressive-kg 对应概念笔记的 `参考资料` 节追加 markdown link
   - **不存在**：提示用户"话题中提到概念 X，progressive-kg 中尚未有此概念节点，是否生成？"
4. **更新 log.md**：追加 `## [YYYY-MM-DD] link | topic-filename -> [概念A, 概念B]`

## 通用注意事项

- **raw/ 文件不可修改** -- 只读引用
- **新建概念前必须查重** -- 搜索文件名、title 和 aliases
- **frontmatter 格式必须严格遵守 SCHEMA.md** -- 格式红线见 vault 内 `_system/` 或 agent skill 的 references
- **Graph view 过滤器不要清空** -- 搜索栏的内容就是 filter，Ctrl+F 清空后会丢失过滤。恢复：粘贴 `-path:raw -path:_system -file:_moc -file:home -file:SCHEMA -file:log`
- **Obsidian vault 必须放 Windows 本地路径** -- 不支持 WSL UNC 路径，WSL 侧用 symlink 访问
- **不要点击 Obsidian 里的红色断链** -- 会创建空文件。断链表示概念尚未迁移/创建
- **CSS snippet 不可跳过**：`_system/snippets/hierarchy-visual.css` 需复制到 `.obsidian/snippets/` 并在 Setting -> Appearance 中启用
- **跨机器配置同步**：见 vault 内 `_system/obsidian-setup-guide.md`

## 系统脚本

| 脚本 | 用途 | 运行方式 |
|---|---|---|
| `_system/lint.py` | 健康检查（YAML、断链、L1 一致性、空占位、关系不足等） | `python3 _system/lint.py` |
| `_system/migrate_schema_v1_1.py` | Schema 1.0 -> 1.1 批量迁移 | `python3 _system/migrate_schema_v1_1.py` |
| `_system/migrate.py` | 从 2nd_brain 批量迁移（旧版 1.0） | `python3 _system/migrate.py` |
| `_system/fix_frontmatter.py` | 修复 1.0 frontmatter 格式问题（旧版） | `python3 _system/fix_frontmatter.py` |
| `_system/tests/test_lint.py` | lint.py 测试套件 | `python3 _system/tests/test_lint.py` |

执行维护操作前先 `git pull`，完成后 `git push`。
