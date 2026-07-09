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

## [2026-07-09] ingest | 偏微分方程

- 新建概念：偏微分方程（PDE）
- Level 2（5个子主题，一对多）：基本概念 / 经典方程 / 分类与特征 / 求解方法 / 与深度学习的关联
- Level 3（每个子主题2-3个细节，一对多）：偏导数定义、波动/热传导/拉普拉斯方程、特征线理论、分离变量法、傅里叶变换、扩散模型/神经ODE/梯度流
- 参考素材：vector-calculus-fields.md（人机知识，含 🌐 HTML 链接）
- 链接到 [[梯度下降优化]] [[正交]] [[反向传播]] [[扩散模型]] [[标准化]]
