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

## [2026-07-13] ingest | Softmax

- 新建概念：Softmax（指数归一化概率函数）
- Level 2（5个子主题）：定义与公式 / 数值稳定性与Log-Sum-Exp / 在注意力机制中 / 与交叉熵损失 / 温度参数
- Level 3：完整推导、√d缩放原理、梯度之美(p-y)、知识蒸馏中的温度
- 占位节点（2个）：[[交叉熵]] [[Log-Sum-Exp]]
- 链接到 [[注意力机制]] [[激活函数]] [[反向传播]] [[flash-attention]] [[内积]]

## [2026-07-13] ingest | 幂变换

- 新建概念：幂变换（Power Transform）
- Level 2（4个子主题）：核心思想 / Box-Cox 变换 / Yeo-Johnson 变换 / 与标准化的关系
- Level 3：偏态与λ选择、公式细节、应用场景、与标准化对比
- 参考素材：Box & Cox (1964), Yeo & Johnson (2000)
- 链接到 [[标准化]] [[主成分分析(PCA)]] [[偏微分方程]]

## [2026-07-09] ingest | 偏微分方程

- 新建概念：偏微分方程（PDE）
- Level 2（5个子主题，一对多）：基本概念 / 经典方程 / 分类与特征 / 求解方法 / 与深度学习的关联
- Level 3（每个子主题2-3个细节，一对多）：偏导数定义、波动/热传导/拉普拉斯方程、特征线理论、分离变量法、傅里叶变换、扩散模型/神经ODE/梯度流
- 参考素材：vector-calculus-fields.md（人机知识，含 🌐 HTML 链接）
- 链接到 [[梯度下降优化]] [[正交]] [[反向传播]] [[扩散模型]] [[标准化]]

## [2026-07-16] audit | Schema 1.1 全库修复

- 保留 `home.md` 网页式 Reading View 为主入口，Graph View 保持辅助角色
- 分离导航层级与单页 L1/L2/L3 披露层级，迁移 47 个内容页和 19 个 MOC
- 统一 frontmatter、L1 定义、关系网络、目录 scope、来源与生命周期字段
- 重写 lint 为默认只读校验，补充迁移脚本和 8 个单元测试
- 校正 KV Cache、FlashAttention、PDE、PCA、幂等性、残差、注意力及训练技能等关键事实边界
- 修复无效 CSS 选择器，并同步 Home/MOC/Obsidian 配置说明
- 最终校验：0 errors / 0 warnings / 0 info；迁移 dry-run 0 changes；`git diff --check` 通过
- 复核记录：[[Meta/reviews/2026-07-16-schema-1.1-audit]]

## [2026-07-17] integrate | 远端新增概念接入 Schema 1.1

- 将远端“幂变换”“Softmax”“交叉熵”“Log-Sum-Exp”迁移到 Schema 1.1，并保留 Home/MOC 的 Dataview 自动入口
- 把 2 个 `status: placeholder` 空节点补全为有定义、主干、关系和来源的 growing 页面，不再保留 TBD 空壳
- 修正幂变换与 PCA、重复标准化、Yeo-Johnson 公式，以及 Softmax 数值稳定性和 CrossEntropyLoss 输入语义等边界
- 在注意力机制、损失函数和标准化中补充反向关系，避免新增页面成为孤儿节点
- lint 新增 TBD 占位定义与无实质 L2 空节点检查；旧 placeholder 迁移为 seed 后仍须补全才能通过
- 校验结果：0 errors / 0 warnings / 0 info；12 个测试通过；迁移 dry-run 0 changes；`git diff --check` 通过
