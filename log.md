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

## [2026-07-26] integrate | 交叉熵与信息论关联概念

- 合并交叉熵的并行升级，保留 Schema 1.1 结构并补充直观示例、极大似然、损失对比、深度学习应用和 perplexity 边界
- 新建 [[信息熵]] 与 [[KL散度]] seed 页面，补齐定义、核心性质、适用边界和关系网络
- 细化 MSE 梯度饱和与 perplexity 的适用条件，避免绝对化解释
- 链接到 [[Softmax]]、[[Log-Sum-Exp]]、[[损失函数]]、[[反向传播]] 和 [[知识蒸馏]]

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

## [2026-07-27] ingest | Adam与AdamW优化器

- 创建 Adam与AdamW优化器概念笔记（seed）
- 覆盖 Adam 算法（偏差校正、几何直觉）和 AdamW（解耦权重衰减）
- 关联：梯度下降优化、动量、Muon优化器、正交
- lint: 0 error / 1 warning（新页面无入链，正常）

## [2026-07-27] link | deep-learning-metaphors -> [21个LLM概念]

- 复制 deep-learning-metaphors.md 到 raw/human_ai_knowledge/
- 给 21 个 LLM 相关概念笔记追加人机知识参考资料引用
- 涉及：Transformer架构、注意力机制、残差连接、位置编码、激活函数、损失函数、归一化层、反向传播、卷积神经网络、循环神经网络、梯度消失与梯度爆炸、正则化、梯度下降优化、动量、Adam与AdamW优化器、Muon优化器、学习率调度、数据增强、知识蒸馏、模型量化、参数高效微调
- 修复正交.md：补齐参考资料节缺失的 standardization-ml-dl-rl 人机知识链接
- lint: 0 error / 0 warning（AGENTS.md 无 frontmatter 除外）

## [2026-08-08] ingest | TPU

- 新增概念页 `Skill/dl-training/TPU.md`（maturity: growing, confidence: high）
- L1：Google 为深度学习设计的专用 ASIC，用脉动阵列专攻矩阵乘加
- L2 子主题：核心架构（脉动阵列与 MXU）、演进（v1→TPU7x 与训练/推理分工）
- 关系：对比 混合精度训练；应用 分布式训练、模型量化；相关 MoE架构、Transformer架构；待建 GPU
- 来源：Google Cloud 官方 TPU 架构文档 + Emergent Mind 综述
- lint：页面无 error；AGENTS.md 缺 frontmatter 为既有问题

## [2026-08-08] ingest | GPU

- 新增概念页 `Skill/dl-training/GPU.md`（maturity: growing, confidence: high）
- L1：数千并行核心的通用并行处理器，高吞吐并行执行海量数学运算，深度学习主流加速器
- L2 子主题：并行执行模型（SIMT 与线程层级）、内存层级与带宽瓶颈、深度学习中的角色与局限
- 关系：对比 TPU；应用 分布式训练、混合精度训练、模型量化；相关 flash-attention、卷积神经网络
- 来源：ThunderCompute 架构指南 + Brenndoerfer 内存层级 + Medium SIMT + Eureka CUDA Cores
- 将 TPU.md 中「待建：GPU」改为真实双链，建立 GPU↔TPU 双向对比
- lint：无 error（AGENTS.md 缺 frontmatter 为既有问题）

## [2026-08-08] ingest | CPU + maintain | 硬件三角补全

- 新增概念页 `Skill/dl-training/CPU.md`（maturity: growing, confidence: high）
- CPU 与 GPU/TPU 建立双向对比，构成 CPU-GPU-TPU 加速器三角
- Maintain 补全 4 条双向缺失关联（用户确认全部追加）：
  - GPU ↔ kv-cache（KV cache 带宽是 GPU 推理瓶颈）
  - GPU ↔ 训练调试（OOM/kernel/CUDA 错误调试）
  - TPU ↔ 注意力机制（脉动阵列加速注意力矩阵乘）
  - CPU ↔ 数据增强（数据预处理/增强常在 CPU 侧）
- 同步更新 4 个目标页 updated：kv-cache、训练调试、注意力机制、数据增强
- lint：无新增 error/warning（AGENTS.md 缺 frontmatter 为既有问题）

## [2026-08-08] fix | lint AGENTS.md frontmatter 豁免

- lint.py 遗漏了 AGENTS.md：根级 agent 规范文件应与 SCHEMA.md/home.md/log.md 同列豁免
- 修复：lint.py 第 463 行豁免集合加入 "AGENTS.md"
- 验证：lint 归零（0 error/0 warning），test_lint.py 12 项全过

## [2026-08-09] upgrade | 3 seed 升级 growing + 3 候选概念 seed 化

- 升级 seed → growing（补 verified/review_due）：
  - 信息熵（review_due 2027-08-08）
  - KL散度（review_due 2027-08-08）
  - Adam与AdamW优化器（review_due 2026-11-08，技术类90天）
- 新建 seed 概念页（替换源节点「待建」标记为真实双链）：
  - 偏差-方差分解（均方误差的统计意义）
  - 过拟合（均方误差异常值敏感性）
  - 特征工程（标准化的上位概念）
- 均方误差、标准化 updated 更新为 2026-08-08
- lint：0 error / 0 warning / 0 info

## [2026-08-10] ingest | 新增 Culture 域 + 三星堆/僰人/羽化

- 新增顶层域 Culture/（人文与文明），下设 history-archaeology（历史考古）与 thought（思想信仰）
- 新增 3 个概念页（均 growing, confidence high）：
  - Culture/history-archaeology/三星堆遗址.md — 长江上游青铜时代遗址、古蜀文明、祭祀器物
  - Culture/history-archaeology/古蜀僰人文化.md — 川南僰人悬棺葬、族属之谜
  - Culture/thought/羽化.md — 道教羽化登仙、词义三解、尸解
- 新建 3 个 MOC（Culture 顶层 + 两个子域），home.md 加入 Culture 域导航
- 三角互链：三星堆↔僰人↔羽化 双向关联（中华生死观/精神文化脉络）
- 待建候选：金沙遗址、僚人、悬棺葬、道教、尸解、神仙信仰
- lint：0 error / 0 warning / 0 info

## [2026-08-10] fix | 修正概念页日期为系统时间

- 此前误用会话推断日期（2026-08-08），实际系统时间为 2026-08-10
- 统一修正全部受影响页的 created/updated/verified 为 2026-08-10
- review_due 按正确日期重算：文化/数学类 2027-08-10，技术类 2026-11-08
- 涉及：Culture 三概念、CPU/GPU/TPU、偏差-方差分解/过拟合/特征工程、信息熵/KL散度/Adam、kv-cache/训练调试/注意力机制/数据增强/均方误差/标准化
- 教训：日期必须以 `date` 查询系统时间为准，禁止凭会话信息推断（已记入 progressive-kg skill）

## [2026-08-11] ingest | 向量/矩阵/张量（线性代数递进链）

- 新增 3 个概念页（Cognition/Math，均 growing, confidence high）：
  - 向量.md — 1 阶张量，有序数组，基本数据对象
  - 矩阵.md — 2 阶张量，线性映射与数据表
  - 张量.md — 任意轴 n 维数组，标量/向量/矩阵为其 0/1/2 阶特例
- 递进互链：向量→矩阵→张量（前置/组成/扩展），并关联 内积/外积/正交/奇异值/PCA/词嵌入
- 日期以系统时间 2026-08-11 为准（review_due 按年 2027-08-11）
- lint：0 error / 0 warning / 0 info

## [2026-08-11] link | add-norm-vs-hc-mhc 人机知识 -> [超连接, 残差连接, 归一化层, 梯度消失与梯度爆炸]

- 新增概念页 `Cognition/Model/超连接(Hyper-Connections).md`（growing, confidence high）：
  - HC（ByteDance 2025）多流残差 + mHC（DeepSeek）双随机矩阵约束（Sinkhorn-Knopp）
  - 与 LayerNorm 的幅度 vs 结构控制对比
- 补充双向关联：残差连接（扩展）、归一化层（对比）、梯度消失与梯度爆炸（缓解）
- raw/ 复制 human_ai_knowledge 的 add-norm-vs-hc-mhc 文档，raw 链接可解析
- lint：0 error / 0 warning / 0 info

## [2026-08-14] ingest | 贝叶斯网络

- 新增概念页 `Cognition/Model/贝叶斯网络.md`（growing, confidence high）
- L1：用 DAG 表达随机变量条件依赖的概率图模型，联合分布分解为各节点条件概率之积
- L2 子主题：核心定义与因子分解、条件独立性、概率推理、学习与变体（朴素贝叶斯）
- 关系：前置 KL散度、信息熵；相关 交叉熵；待建 贝叶斯定理/马尔可夫网络/马尔可夫链/因果推断
- 日期按系统时间 2026-08-14，review_due 按年 2027-08-14
- lint：0 error；no inbound 为新节点正常现象

## [2026-08-14] maintain | 贝叶斯网络双向关联

- 在 3 个已存在概念页补上对 [[贝叶斯网络]] 的反向链接（双向）：
  - 信息熵：应用 贝叶斯网络（不确定性度量是概率推理理论基础）
  - KL散度：前置 贝叶斯网络（分布差异度量）
  - 交叉熵：相关 贝叶斯网络（概率模型互补）
- 同步更新 3 页 updated → 2026-08-14
- lint：0 error / 0 warning / 0 info（贝叶斯网络 no-inbound 消除）

## [2026-08-14] ingest | 贝叶斯定理 + 马尔可夫链

- 新增 2 个概念页（Cognition/Math，均 growing, confidence high）：
  - 贝叶斯定理.md — 证据更新先验为后验的核心公式，贝叶斯推断基石
  - 马尔可夫链.md — 无记忆性随机过程，转移矩阵，稳态收敛，MCMC 基础
- 三角互链：贝叶斯网络页的「待建：贝叶斯定理」「待建：马尔可夫链」替换为真实双链（应用）
- 两新节点互链 + 关联信息熵，且各自指向贝叶斯网络
- 日期按系统时间 2026-08-14，review_due 按年 2027-08-14
- lint：0 error / 0 warning / 0 info

## [2026-08-16] ingest | 傅里叶变换

- 新增概念页 `Cognition/Math/傅里叶变换.md`（growing, confidence high）
- L1：把时域/空域信号分解为不同频率正弦/复指数分量的线性积分变换，揭示频域结构
- L2 子主题：核心定义（CFT/DFT/FFT 三档公式）、傅里叶家族关系表、关键性质（卷积定理）、化学分析类比
- 关系：应用 偏微分方程；前置 内积；相关 正交；待建 卷积/信号处理/频谱
- 日期按系统时间 2026-08-16，review_due 按年 2027-08-16
- lint：0 error；no inbound 为新节点正常现象

## [2026-08-16] maintain | 傅里叶变换双向关联

- 在 3 个已存在概念页补上对 [[傅里叶变换]] 的反向链接（双向）：
  - 偏微分方程：应用 傅里叶变换（微分变频域乘法）
  - 内积：应用 傅里叶变换（复指数基上的投影）
  - 正交：应用 傅里叶变换（复指数构成正交基）
- 同步更新 3 页 updated → 2026-08-16
- lint：0 error / 0 warning / 0 info（傅里叶 no-inbound 消除）

## [2026-08-16] ingest | 泰勒展开

- 新增概念页 `Cognition/Math/泰勒展开.md`（growing, confidence high）
- L1：用函数在某点的各阶导数构造幂级数，在展开点附近用多项式逼近光滑函数
- L2 子主题：核心定义（公式/Maclaurin/余项/常用展开）、与幂级数的关系、关键性质
- 关系：相关 傅里叶变换；前置 内积；应用 偏微分方程；待建 幂级数/收敛半径
- 日期按系统时间 2026-08-16，review_due 按年 2027-08-16
- lint：0 error；no inbound 为新节点正常现象

## [2026-08-16] ingest | 拉普拉斯变换

- 新增概念页 `Cognition/Math/拉普拉斯变换.md`（growing, confidence high）
- L1：把时域函数映射到复频域的积分变换，微分变乘法，求解微分方程与线性系统的利器
- L2 子主题：核心定义（公式/收敛/常用变换对表）、与傅里叶/幂级数的关系、微分变乘法性质
- 关系：相关 傅里叶变换（复平面推广）；应用 偏微分方程；相关 泰勒展开；待建 Z变换/积分变换
- 日期按系统时间 2026-08-16，review_due 按年 2027-08-16
- lint：0 error；no inbound 为新节点正常现象

## [2026-08-16] ingest | 微分法则家族（3 个小概念）

- 新增 3 个概念页（Cognition/Math，均 growing, confidence high）：
  - 链式法则.md — 复合函数求导，反向传播的数学基石（应用 [[反向传播]]）
  - 乘积法则.md — 两函数乘积求导 (fg)'=f'g+fg'，含莱布尼茨推广
  - 洛必达法则.md — 0/0 与 ∞/∞ 不定式极限，用导数之比求解
- 三法则互链（相关），并关联库内已有 反向传播/向量/泰勒展开/傅里叶变换 等
- 日期按系统时间 2026-08-16，review_due 按年 2027-08-16
- lint：0 error；仅拉普拉斯变换页的 no-inbound 遗留 warning（新节点正常）

## [2026-08-16] maintain | 微积分工具家族双向关联

- 补全 6 处双向链接（泰勒展开/拉普拉斯变换/傅里叶变换/洛必达法则 家族互链 + 挂接既有页）：
  - 傅里叶变换页：补 相关 泰勒展开、相关 拉普拉斯变换
  - 泰勒展开页：补 相关 拉普拉斯变换、相关 洛必达法则
  - 偏微分方程页：补 应用 拉普拉斯变换
  - 反向传播页：补 依赖 链式法则
- 同步更新 4 页 updated → 2026-08-16
- lint：0 error / 0 warning / 0 info（家族全部 no-inbound 消除）

## [2026-08-17] ingest | 微积分待建候选全部实体化（11 个概念）

- 新增 11 个概念页（Cognition/Math，均 growing, confidence high）：
  - 幂级数、收敛半径（泰勒展开的上下位）
  - Z变换、积分变换（拉普拉斯的关联/上位）
  - 卷积、信号处理、频谱（傅里叶的关联/应用）
  - 雅可比矩阵（链式法则的载体）
  - 商法则、莱布尼茨公式（乘积法则的推论/推广）
  - 中值定理（洛必达的理论基础）
- 把 6 个源页的「待建」标记替换为真实双链，形成完整家族网
- 修复：幂级数 definition 与 summary 一致化、莱布尼茨 broken wikilink、信号处理 L2 lead
- 日期按系统时间 2026-08-17，review_due 按年 2027-08-17
- lint：0 error / 0 warning / 0 info

## [2026-08-17] ingest | 贝叶斯/马尔可夫待建候选实体化（5 个概念）

- 新增 5 个概念页（均 growing, confidence high）：
  - Cognition/Model/贝叶斯推断.md（贝叶斯定理的方法论延伸）
  - Cognition/Model/因果推断.md（相关 vs 因果、do-演算、反事实）
  - Cognition/Math/马尔可夫性质.md（无记忆性，马尔可夫链定义性假设）
  - Cognition/Model/马尔可夫网络.md（无向图模型，与贝叶斯网络相对）
  - Cognition/Model/马尔可夫链蒙特卡洛（MCMC）.md（采样后验的算法族）
- 把源页待建替换为真实双链：贝叶斯网络（马尔可夫网络/因果推断）、贝叶斯定理（贝叶斯推断）、马尔可夫链（马尔可夫性质/MCMC）
- 修复：因果推断 L2 lead
- 日期按系统时间 2026-08-17，review_due 按年 2027-08-17
- lint：0 error / 0 warning / 0 info

## [2026-08-17] maintain | 待建概念双链修复（已存在部分）

- 卷积.md: 「待建：池化、感受野」拆分为「相关 [[感受野]]」真实双链 + 「待建：池化」保留
- Z变换.md: 「待建：数字信号处理」改为「应用 [[信号处理]]」真实双链
- 依据 Schema 1.1：已存在概念不再用「待建」占位，直接建立真实双链
- lint: 0 error / 0 warning / 0 info

## [2026-08-17] ingest | 文化族 6 个待建概念实体化

- 实体化：金沙遗址、僚人、悬棺葬（history-archaeology）；道教、尸解、神仙信仰（thought）
- 全部为 seed，含真实双链和参考资料（web 查证史实）
- 源文件「待建」改为真实双链：三星堆遗址→金沙遗址、古蜀僰人文化→僚人/悬棺葬、羽化→道教/尸解/神仙信仰
- Culture 域待建清零
- lint: 0 error / 0 warning / 0 info

## [2026-08-17] ingest | 概率族 8 个待建概念实体化

- 实体化：do-演算、反事实、变分推断、隐马尔可夫模型、配分函数、吉布斯分布、Metropolis-Hastings算法、吉布斯采样
- 全部为 seed，含真实双链和参考资料
- 源文件「待建」改为真实双链：因果推断、贝叶斯推断、马尔可夫网络、MCMC、马尔可夫性质
- 修复变分推断.md L2 缺引导段
- 概率族待建清零；剩余微积分族待建 15 处
- lint: 0 error / 0 warning / 0 info

## [2026-08-17] ingest | 池化概念实体化

- 创建 池化.md（Cognition/Math, seed）
- 卷积.md 待建 -> 真实双链；卷积神经网络.md 补池化回链
- 修复池化.md L2 缺引导段
- lint: 0 error / 0 warning / 0 info

## [2026-08-17] ingest | 微积分族 11 个待建概念实体化

- 微分法则族：罗尔定理、柯西中值定理、二项式定理、高阶导数、微分法则总览
- 分析族：幂级数解、奇点、VJP、功率谱密度、梅林变换、希尔伯特变换
- 全部为 seed，含真实双链和参考资料
- 13 个源文件「待建」改为真实双链：中值定理、乘积法则、傅里叶变换、商法则、幂级数、拉普拉斯变换、收敛半径、洛必达法则、积分变换、莱布尼茨公式、链式法则、雅可比矩阵、频谱
- 全库「待建」清零
- lint: 0 error / 0 warning / 0 info

## [2026-08-19] ingest | 退火算法

- 创建 退火算法.md（Cognition/Model, seed）
- 覆盖：核心思想（金属退火类比）、算法骨架（Metropolis 准则）、降温计划、与 MH/贪心/遗传算法的关系、应用
- 关联：Metropolis-Hastings（接受准则同源）、梯度下降优化（对比）、超参数调优（应用）、MCMC
- 回链：Metropolis-Hastings、超参数调优 补反向链接
- lint: 0 error / 0 warning / 0 info
