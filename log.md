# 变更日志

> 所有知识图谱操作的 append-only 记录。
> 格式：`## [YYYY-MM-DD] action | subject`

## [2026-07-08] create | Progressive-KG 项目初始化

- 创建 SCHEMA.md（三层渐进披露模型、文件结构、frontmatter 规范、维护协议）
- 创建 home.md 入口页
- 创建概念笔记模板和 MOC 模板
- 创建 log.md 变更日志
- 目录结构：Cognition/, Skill/, Language/, Meta/, Horizon/, comparisons/, queries/, raw/, _system/

## [2026-07-08] ingest | 标准化

- 合并 2nd_brain + human_ai_knowledge 两个版本的标准化知识
- Level 1：一句话定义（≤50字）
- Level 2（5个子主题，一对多）：定义与公式 / ML应用 / DL应用 / RL应用 / Python实现
- Level 3（每个子主题2-4个细节，一对多）：Z-score推导、vs归一化、BN/LN/RMSNorm、状态/奖励/优势标准化等
- raw 源文件：standardization-ml-dl-rl.md + standardization-2nd-brain.md
- 链接到 [[正交]]（正交初始化与标准化互补关系）
