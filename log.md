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

## [2026-08-19] update | 奇异值.md 补充"奇异值分布的实际意义"

- 新增一节：条件数与稳定性、有效维度与低秩近似、主导方向与谱分析、可逆性与正则化、秩亏与冗余探测
- 关联现实应用：Hessian 条件数、LoRA 低秩、谱归一化、Tikhonov 正则化、Muon 压平奇异值尺度
- lint: 0 error / 0 warning / 0 info

## [2026-09-11] ingest | 自动微分、JVP、条件独立、特征值与特征向量、ELBO、交叉验证

- 按 SCHEMA 1.1 查重（文件名、title、aliases），查阅现有正文与 raw，核验原始论文和官方/大学来源。
- Cognition/Math 新增自动微分、JVP、条件独立、特征值与特征向量；Cognition/Model 新增 ELBO；Skill/dl-training 新增 procedure 交叉验证。
- 新页保留 maturity: seed，已有有效 L1、多个实质 L2、来源与真实关系；verified: 2026-09-11，复核周期按理论稳定性与软件迭代区分。
- 新节点关系已双向维护；原有反向传播、贝叶斯网络、变分推断保留概述并链接独立页，减少重复。
- 新页手算实例已用数值计算复核 JVP、特征对及 ELBO 恒等式；本机未安装 JAX，JAX 片段仅核对官方接口。

## [2026-09-11] update | 补强并核验全部 30 个原有 seed

- 数学 15 个、模型 9 个、文化 6 个原 seed 全部补齐例子、推导或证据边界，升级为 growing；保留原 created，updated/verified 为 2026-09-11。
- 纠正二项式笔误、导数连续性条件、谱与积分变换边界、do-演算规则、采样与识别假设；文化页区分史料、族属推断与宗教叙事，统一错误的引用题名。
- 16 个原有非 seed 源页维护回链，局部修正贝叶斯网络的因果边界与无向图马尔可夫毯；这些源页保留原 verified，并记录变更范围。
- 详见 [[Meta/reviews/2026-09-11-concept-expansion]]：逐页成熟度、核验结果、来源类型及残余边界。
- MOC 保持目录 Dataview 查询，新页自动纳入；未改 raw/，未启动 Obsidian 人工视觉验收。
- 最终验证：python3 _system/lint.py 为 0 error / 0 warning / 0 info；git diff --check 通过。

## [2026-09-11] ingest | CLIP、对比学习、表征学习

- 用户要求不存在时补入贝叶斯网络、CLIP、对比学习、表征学习；按文件名、title、aliases 查重，贝叶斯网络已存在，本次复用且未改动该页。
- Cognition/Model 新建 [[CLIP]]、[[对比学习]]、[[表征学习]]，按 Ingest 保留 seed；verified 为 2026-09-11，review_due 为 2027-03-11。
- 表征学习涵盖目标、信息取舍与评估协议；对比学习涵盖正负关系、InfoNCE 风格目标、SimCLR 例子及采样边界；CLIP 涵盖双编码器、双向交叉熵、零样本分类和使用限制。
- 来源核验：Bengio/Courville/Vincent 表征学习综述、CPC/SimCLR/Supervised Contrastive Learning 原论文、Radford 2021 CLIP 论文与官方仓库；引用及支持范围写入对应页面。
- 在词嵌入、PCA、特征工程、数据增强、交叉熵、Transformer 架构六个既有页面补回链，保留原 verified 并记录局部关联维护。
- 对比损失例子复算：logits (4,1,-0.5) 的正例概率为 0.942599，损失为 0.059114；未运行 CLIP 模型或训练实验。
- MOC 按目录自动收录；raw/ 未修改。
- 验证：新节点关系双向检查通过；全库 lint 为 0 error / 0 warning / 0 info，git diff --check 通过。

## [2026-09-11] ingest | 几丁质、碱基对、氨基酸、DNA

- 按文件名、title、aliases 查重，四个概念均无既有节点；新建 Cognition/Biology 子域及目录 MOC，并接入 Cognition 导航。
- 新建 [[几丁质]]、[[碱基对]]、[[氨基酸]]、[[DNA]]，均保留 seed；verified 为 2026-09-11，review_due 为 2027-09-11。
- 正文补充分子组成与连接方式、互补链方向、bp 与核苷酸数量、密码子到氨基酸的例子；区分几丁质与壳聚糖、核苷酸与氨基酸、碱基对与密码子。
- 来源核验涵盖 NHGRI、OpenStax、NCBI Bookshelf 及几丁质材料研究；各页记录引用与支持范围。
- 新节点关系双向维护；DNA 互补链和碱基对计数例子已复核。raw/ 未修改。
- 验证：全库 lint 为 0 error / 0 warning / 0 info，git diff --check 通过。

## [2026-09-11] ingest | 生物学、表征学习与数学基础共11个概念

- 用户批准增补上一轮建议的全部11项；按文件名、title、aliases查重，并检索raw素材，未修改raw/。
- Cognition/Biology新增：[[核苷酸]]、[[RNA]]、[[蛋白质]]、[[遗传密码]]、[[多糖]]。
- Cognition/Math新增：[[余弦相似度]]、[[互信息]]、[[最大似然估计]]、[[奇异值分解]]。
- Cognition/Model新增：[[自监督学习]]、[[InfoNCE]]。
- 均按Ingest保留seed并核验来源；verified为2026-09-11。稳定生物/数学基础review_due为2027-09-11，自监督学习与InfoNCE为2027-03-11。
- 来源包括NHGRI、OpenStax、NCBI、Stanford课程与教材、MIT线性代数课程，以及CPC、SimCLR、BERT、CLIP和互信息变分界原论文。
- 在21个既有页面维护回链或独立页入口；旧页保留原verified并记录局部变更。奇异值页保留低秩近似概述，PCA的SVD入口改指独立分解页；区分HMM的Baum–Welch似然优化与贝叶斯推断。
- 复核RNA糖—磷酸骨架、链内碱基配对、蛋白质动态构象、核苷酸/多糖单体边界；遗传密码页集中承载翻译例子，其他新页保留概述。
- 复算余弦0.96、离散互信息0.9183 bit、伯努利MLE 0.7、对角矩阵SVD截断误差1，以及InfoNCE概率0.665241/损失0.407606；InfoNCE明确期望下界与采样条件。
- 子域MOC按目录自动收录。最终验证：11个新节点关系双向检查通过；全库lint为0 error / 0 warning / 0 info；git diff --check通过。

## [2026-09-11] maintain | 全库内容审阅与纠错

- 审阅143个知识页面（131 concept、11 procedure、1 hypothesis），修正32页：数学10、模型7、生物3、文化4、训练技能8。
- 修复硬件架构的绝对化描述、CUDA等错误别名、AdamW衰减顺序与显存口径、AMP裁剪前unscale、数学公式条件、因果与贝叶斯语义、模型稳定性过度保证，以及古蜀/僰人/悬棺与宗教叙事的证据边界。
- 详见 [[Meta/reviews/2026-09-11-global-maintenance]]：实际修复、143页覆盖清单、未解决证据缺口与后续触发条件。
- CPU/GPU/TPU核对官方资料后更新verified；其他局部修正保留原verified并写变更记录，所有修改更新updated，未批量改变maturity。24个seed有实质内容。
- AGI路径假设和类比学习法的效果仍待实证，保留空verified；本轮未逐条重核全库外链、运行训练/性能实验或做Obsidian视觉验收。raw/未修改。
- 验证：全库lint为0 error / 0 warning / 0 info；git diff --check通过；AdamW、AMP顺序、矩阵阵列计数和优化器状态字节数示例复算通过。

## [2026-09-11] ingest | 数学与AI概念40项

- 完成用户批准的全部40项，Cognition/Math新增20页，Cognition/Model新增20页，均为有定义、公式、例子、边界与来源的seed。
- 数学覆盖概率、采样、几何与数值分析、约束优化及Fisher信息；模型覆盖统计模型、表征与生成、语言与检索、强化学习及泛化评估。
- 按文件名、title、aliases查重，并检索raw素材；原论文、官方教材与文档核验记录在各页，verified为2026-09-11，复核周期按理论与工具变化区分。
- 48个已有页面补回链，词嵌入、PCA、变分推断、奇异值保留概述并接入独立页；旧页保留created、verified、maturity。新页231条关系均有反向覆盖。
- 详见 [[Meta/reviews/2026-09-11-ai-math-40-concepts]]：40页清单、来源、关键边界、数值复算和验证局限。
- 全库知识页面由143增至183；MOC自动收录。raw/、Obsidian配置、校验脚本未修改；未运行模型训练或GUI验收。
- 最终检查：lint为0 error / 0 warning / 0 info，git diff --check通过，公式定界符和控制字符检查通过。

## [2026-09-11] ingest | 跨类别概念18项

- 新增生物学8、考古文化4、语言学4、方法2，均保留seed，含定义、实质正文、边界、来源与双向关联；concept/procedure页由183增至201。
- Language新增linguistics子域MOC并接入域导航；其他使用现有目录。按文件名/title/aliases查重，并检索raw素材。
- 来源核验和主要修正见 [[Meta/reviews/2026-09-11-cross-domain-18-concepts]]；明确基因与蛋白产物、染色质与染色体、碳十四样品与事件年代、考古分类与族群等边界。
- 19个旧页只补关系并保留原核验日期和成熟度；新增48条反向关系，新页87条出链均有反向覆盖。raw、Obsidian配置和系统脚本未修改。
- 最终验证：全库lint 0 errors / 0 warnings / 0 info，双向关联和控制字符检查通过，git diff --check通过。未进行GUI验收或本地方法效果实验。

## [2026-09-11] ingest | 钟馗

- 新增 [[Culture/thought/钟馗]]，保留seed，含传说与历史证据、节令习俗、夜游/秤鬼/嫁妹图像题材三个实质章节。
- 全库文件名、title、aliases与raw检索未发现重复；核对故宫两件藏品及大都会颜庚作品说明，区分传说记载、画作证据和馆方推测，未裁定最早起源。
- 与仪式、神仙信仰建立双向关联；旧页保留created、verified、maturity，思想与信仰MOC自动收录。
- 全库lint：0 errors / 0 warnings / 0 info；git diff --check通过。raw和配置未修改。

## [2026-09-11] ingest | 佛教、基督教、伊斯兰教

- 新增 [[Culture/thought/佛教]]、[[Culture/thought/基督教]]、[[Culture/thought/伊斯兰教]]，均保留seed；覆盖起源与信仰、经典与主要传统、实践及理解边界。
- 全库文件名/title/aliases查重并检索raw；核对The Pluralism Project的导论及专题资料，来源支持范围记于各页。区分信仰宣认与历史陈述，不把任何单一分支代表整个宗教。
- 特别澄清广义基督教与新教、金刚乘与大乘的包含关系、苏菲与教派的交叉关系，以及宗教身份与族群身份的区别。
- 三页相互建立有说明的比较关系，并与仪式页建立双链；仪式页保留原created、verified、maturity。现有MOC自动收录，raw与配置未修改。
- 验证：全库lint为0 errors / 0 warnings / 0 info，git diff --check通过；3页共9条出链均有反向关系。

## [2026-09-11] ingest | 印度教

- 新增 [[Culture/thought/印度教]]，保留seed；补历史与经典、法/业/轮回/解脱、主要虔敬传统和实践，区分共同观念与内部差异。
- 文件名、title、aliases及raw检索未发现重复；核对The Pluralism Project导论与专题。未把所有印度教立场归为单一神学，也未把佛教列为其分支。
- 与佛教、仪式补齐双向关联，旧页保留原核验日期与成熟度；现有MOC自动收录。
- 全库lint为0 errors / 0 warnings / 0 info；git diff --check通过。raw及配置未修改。

## [2026-09-11] ingest | 直接关联seed24项

- 按用户确认新增文化6、生物5、数学5、AI与训练4、语言4，共24个有正文与核验来源的seed。
- 新页118条关系出链均有反向关联；PEFT页的LoRA细节归入独立页，旧页保留原verified与成熟度。
- 全库知识页230个，其中seed111个；lint 0 errors / 0 warnings / 0 info，差异格式检查通过。
- 详情：[[2026-09-11-direct-seed-24-concepts]]。

## [2026-09-14] ingest | 支持向量机

- 新增 [[Cognition/Model/支持向量机]]，保留 seed；三个 L2：最大间隔分类（含泛化界与凸 QP 求解）、对偶形式与核技巧、软间隔与损失函数视角。
- 全库文件名/title/aliases 与 raw 检索均未发现重复；核技巧、对偶问题暂以正文 L3 承载，未拆分为独立概念页（SCHEMA §4.2 拆分条件未满足）。
- 与 11 个已有概念建立双向关联：凸性与凸优化、KKT条件、拉格朗日乘子法、损失函数、正则化、逻辑回归、经验风险最小化、内积、正定与半正定矩阵、标准化、过拟合。
- 来源 4 条（scikit-learn SVM 文档、Cortes & Vapnik 1995 原始论文、Wikipedia SVM 与 Kernel method），均实测 HTTP 200 可访问。
- 全库 lint 为 0 errors / 0 warnings / 0 info（初始孤儿警告已由反向关联消除）；raw 与配置未修改。

## [2026-09-15] ingest | 有向无环图 + 艾宾浩斯遗忘曲线

- 新增 [[Cognition/Math/有向无环图]]（aliases: DAG、Directed Acyclic Graph）：定义与等价刻画（拓扑排序存在、邻接矩阵幂零、良基递推）、无环性为何是关键约束（偏序与递推、概率分解与因果语义）、主要应用与「结构≠语义」的辨析；与 9 个已有概念建立双向关联。
- 新增 [[Cognition/life/艾宾浩斯遗忘曲线]]（aliases: 艾宾浩斯曲线、遗忘曲线、Forgetting Curve）：1885 年无意义音节自我实验与节省率度量、Ebbinghaus 原文公式（c=1.25、k=1.84）及其计算值、影响衰减的因素与复习时机、边界与常见误读（原文并未研究间隔重复）；与 2 个已有概念关联。
- 命名说明：用户报的是「艾宾浩斯曲线」，落库采用更精确的规范名「艾宾浩斯遗忘曲线」以区别于「学习曲线」，原词保留为 alias。
- 查重：两个概念的文件名、title、aliases 及 raw 检索均无重复；DAG 此前仅被 5 处正文引用，无独立节点。
- 来源：DAG 5 条、遗忘曲线 4 条，全部实测 HTTP 200；psychclassics.yorku.ca 不可达，故未采用。
- 全库 lint 为 0 errors / 0 warnings / 0 info（两页初始均为孤儿，已由反向关联消除）；raw 与配置未修改。

## [2026-09-15] ingest | 认知负荷

- 新增 [[Cognition/life/认知负荷]]（aliases: Cognitive Load、认知负荷理论、Cognitive Load Theory）：工作记忆瓶颈与理论来源（Sweller、Miller 1956、chunk 概念）、手段–目的分析为何消耗本应用于建构图式的资源、三类负荷对照表（内在／外在／相关）、五项教学效应（范例、分散注意、通道、完成问题、专长逆转）、边界与争议。
- 与 4 个已有概念建立关联：艾宾浩斯遗忘曲线、类比导航学习法、注意力机制、AGI实现路径-人类智能融合。
- 别名冲突修正：`CLT` 已被 [[中心极限定理]] 占用，本页移除该别名，并在正文「边界」节注明缩写歧义；该冲突由 lint 捕获（error: ambiguous alias）后修正。
- 主动未收录 `element interactivity`：Wikipedia 的 cognitive load 与 cognitive load theory 两个条目均未覆盖该构念，无可靠来源故不写入。
- 来源 6 条，全部实测 HTTP 200；Sweller 1988 原始论文的 DOI/出版商链接返回 403，故未列入并在正文说明。
- 全库 lint 为 0 errors / 0 warnings / 0 info；raw 与配置未修改。

## [2026-09-15] link | memory-classification-and-forgetting -> [艾宾浩斯遗忘曲线, 认知负荷]

- 人机知识《记忆的分类，以及遗忘的科学说明》发布（human_ai_knowledge，commit 83f700e）：20 条来源，配图 figures/memory-taxonomy.svg。
- 复制话题 MD 到 `raw/human_ai_knowledge/memory-classification-and-forgetting.md`（raw 只读引用）。
- 已存在概念追加参考资料：[[艾宾浩斯遗忘曲线]]（把曲线放回完整遗忘机制家族）、[[认知负荷]]（短期记忆 3–5 项与工作记忆四成分是其「资源有限」前提的实验背景）；两页 updated 同步。
- 未创建新概念：话题中涉及的候选（工作记忆、情景记忆、语义记忆、程序性记忆、间隔重复、提取练习、干扰理论、加工水平效应）均为「高度相关但当前无节点」，按候选规则向用户报告后再决定，本轮不静默建页。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-15] maintain | 补齐 SVM 与 DAG 的正文级核验

- 触发：用户指出"是否该在这两个 skill 生成内容时加 web_search 作为多路信息源之一"——若概念很新，不搜可能不知道它存在或脑中是过期版本。
- 规则侧：`_system/OPERATIONS.md` Ingest 步骤 3 由「**如需补充**，web_search」改为「检索素材（多路来源，强制）」，web_search 列为必做并明确三个目的（发现 / 时效 / 覆盖）；通用注意事项新增 4 条（只验 URL 可达 ≠ 核验、搜索结果不可全信、新概念必须靠 search、教科书常识也要过一遍 search）。SCHEMA.md 未改。
- 内容侧：对 2026-09-14 建的两个 page 补做正文级核验。
  - [[支持向量机]]：`web_search` + `web_extract`（scikit-learn SVM 页、Wikipedia SVM / SMO / Positive-definite kernel）。补入 sigmoid 核、$\gamma>0$、Platt scaling 用额外交叉验证拟合、SMO 出处（Platt 1998, Microsoft Research）；把未落到正文的表述（"只含两个变量的子问题"、自填复杂度 $O(n^2)$~$O(n^3)$）改回来源原话。Sources 增补 2 条。
  - [[有向无环图]]：补入 Wikipedia 原文的邻接矩阵等价判据（$A+I$ 非负 0/1 且特征值全正）与传递规约/哈斯图这组 DAG 特有概念。原有论断（拓扑排序等价性、可达关系即偏序、Kahn 线性时间）经正文确认无误。
- 两页均保留 `maturity: seed`，未自行升级（按流程由人工批准 growing/evergreen）；`verified` 现已具备正文依据。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-15] promote | seed → growing ×4

- 经用户确认，将 4 个已完成正文级核验的节点由 `seed` 升为 `growing`：
  - [[支持向量机]]（关系 11 / 来源 6；verified 与 review_due 同步为 2026-09-15 / 2027-09-15）
  - [[有向无环图]]（关系 9 / 来源 5）
  - [[艾宾浩斯遗忘曲线]]（关系 3 / 来源 4）
  - [[认知负荷]]（关系 4 / 来源 6）
- 升级前逐项核对 growing 硬性条件：≥2 个指向现有概念的关系、有来源、无断链——4 项全部满足。
- `confidence` 保持不变：SVM 与 DAG 为 high；艾宾浩斯遗忘曲线（函数形式仍有争议）与认知负荷（Wikipedia 条目带 citation needed 与疑似 AI 生成文本标记）保持 medium，并在变更记录中写明后续需补的原始文献。
- 4 页均补变更记录；全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-15] ingest | 记忆类型族 4 个概念（工作记忆 / 情景记忆 / 语义记忆 / 程序性记忆）

- 按收紧后的检索规则执行：4 个概念**先做 `web_search`**（确认存在性、标准名称、时效），再 `web_extract` 取正文核验，来源 URL 全部实测可访问。
- 新增 [[工作记忆]]：与短期记忆的区别、四成分（中央执行 / 语音环路 / 视觉空间画板 + 2000 年补入的情景缓冲器）、语音环路约两秒窗口、情景缓冲器为何是必需补丁。
- 新增 [[情景记忆]]：Tulving 1972 提出、"知道 vs 记得"的区分、三标志特征（主观时间 / 自我 / 自我觉知）、与语义记忆的分野、内侧颞叶与海马的分离证据。
- 新增 [[语义记忆]]：1972 年 Tulving–Donaldson 会议由来、"与获得场合无关"这条判定特征、与情景记忆逐项对比、知识的组织性。
- 新增 [[程序性记忆]]：内隐记忆定位、无需意识控制、难以言传、与陈述性记忆的分离（海马受损者可学新技能却记不住经历）、小脑/纹状体/基底神经节。
- 关联网络：四页构成完整三角形（情景 ↔ 语义 ↔ 程序性）+ 工作记忆接入；另补 [[认知负荷]] → [[工作记忆]] 回链（该理论的前提）。
- 全部 `maturity: seed`（新建），`confidence: high`；lint 为 0 errors / 0 warnings / 0 info（无孤儿）。
- 第二批（间隔重复 / 提取练习 / 干扰理论 / 加工水平效应）待用户确认后继续。

## [2026-09-15] ingest | 学习机制族 4 个概念（间隔重复 / 提取练习 / 干扰理论 / 加工水平效应）

- 流程同第一批：每个概念先 `web_search` 确认存在性与时效，再 `web_extract` 取正文核验；来源 URL 全部实测可访问。
- 新增 [[间隔重复]]：间隔效应的底层依据（Cepeda 2006 的 259/271）、等比拉长间隔的经典建议、SuperMemo 的 ~90% 保留阈值、Leitner/SM-2/FSRS 脉络与边界。
- 新增 [[提取练习]]：提取本身即学习、与重复阅读的对比、"短延迟重复学习占优 / 长延迟测试反超"的交互、五条理论解释（提取努力、必要难度等）、元认知盲区与刺激诱发遗忘等消极面。
- 新增 [[干扰理论]]：前摄/倒摄干扰定义与实例、前摄干扰实验的 70%/40%/25% 回忆率数据、Jenkins 与 Dallenbach 1924 睡眠实验（**原文只给结论未给数字，故未引用第三方站点的 56%/9%**）、区分度等实用含义。
- 新增 [[加工水平效应]]：Craik 与 Lockhart 1972、结构/语音/语义三层、"加工方式重于加工时间"、与复述正统的冲突及与三存储模型的关系辨析、深度难以独立度量的边界。
- 关联：4 页互相成网并接入既有簇；另补 4 条对向回链（[[艾宾浩斯遗忘曲线]] ×4、[[认知负荷]]、[[工作记忆]]、[[在线学习]]）。其中 [[在线学习]] ↔ [[干扰理论]] 是新增的跨域连接（灾难性遗忘 ≡ 倒摄干扰）。
- 全部 `maturity: seed`、`confidence: high`；lint 为 0 errors / 0 warnings / 0 info。
- 至此「记忆与学习」这条线共 10 个节点：工作记忆 / 情景记忆 / 语义记忆 / 程序性记忆 / 艾宾浩斯遗忘曲线 / 认知负荷 / 间隔重复 / 提取练习 / 干扰理论 / 加工水平效应。

## [2026-09-15] promote | 记忆与学习族 seed → growing ×8

- 经用户确认，将两批新建的 8 个节点由 `seed` 升为 `growing`：
  工作记忆（关系 4 / 来源 3）、情景记忆（3 / 3）、语义记忆（3 / 3）、程序性记忆（3 / 3）、
  间隔重复（3 / 3）、提取练习（3 / 3）、干扰理论（3 / 3）、加工水平效应（4 / 3）。
- 升级前逐项核对 growing 条件（≥2 个指向现有概念的关系、有来源、无断链）——8 项全部满足。
- `confidence` 保持 high（各页核心论断均有正文级来源）；每页补变更记录，并写明各自的「后续待补」：
  - 间隔重复：Spacing effect 条目本身带维护模板，其机制部分宜回原始文献补充
  - 提取练习：知识迁移是否成立学界仍有争议，需补更近期的元分析
  - 干扰理论：干扰与衰退的相对权重在不同材料/时间尺度下仍无定论
  - 加工水平效应：「深度」缺少可独立量化的定义，模型解释力仍有争议
  - 四个记忆类型页：分别待补容量测量的范式差异、内侧颞叶分工、语义组织模型、技能习得阶段模型
- 「记忆与学习」簇现状：10 个节点全部为 growing 或以上；lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-16] link | representation-contrastive-clip -> [表征学习, 对比学习, CLIP, InfoNCE]

- 人机知识《表征学习、对比学习与 CLIP 的异同》发布（human_ai_knowledge，commit 7669267）：6 条一手来源，配图 figures/representation-contrastive-clip.svg。
- 复制话题 MD 到 `raw/human_ai_knowledge/representation-contrastive-clip.md`（raw 只读引用）。
- 已存在概念追加参考资料：[[表征学习]]（问题层定位）、[[对比学习]]（方法层定位 + SimCLR 三条发现）、[[CLIP]]（系统层定位 + 弱监督辨析）、[[InfoNCE]]（谱系位置）；四页 updated 同步为 2026-09-16。
- 该话题澄清了三个概念的**层级关系**（问题层 → 方法层 → 系统层），可直接作为本库三页之间的定位说明。
- 检索过程中发现**时效性内容**：CLIP 之后的 SigLIP（pairwise sigmoid 损失、解耦 batch size）与 LLM2CLIP（AAAI 2026），已写入人机知识；本库 [[CLIP]] 页若后续升级应一并补入。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-19] link | jev-vs-bert -> [Transformer架构, 自回归建模, 概率校准, 因果掩码, 解码策略]

- 人机知识《Jev 与 BERT：实现原理对比，以及一个硬件类比的成立边界》发布（human_ai_knowledge，commit f39a15a + 日期修正 8467be3）：6 条来源，配图 figures/jev-vs-bert.svg。
- 复制话题 MD 到 `raw/human_ai_knowledge/jev-vs-bert.md`。
- 已存在概念追加参考资料：[[Transformer架构]]、[[自回归建模]]、[[概率校准]]（RLCD 把校准当奖励目标，并给出「校准是群体属性而非单答案属性」的判据）、[[因果掩码]]、[[解码策略]]；五页 updated 同步为 2026-09-19。
- 该话题澄清了一条可复用判据：**输出空间是否有界**决定模型能否「一次穷举打分」——同时解释低延迟、输出 token 免费与结构性不能生成文本。可回填到本库 [[自回归建模]] 与 [[解码策略]] 的边界讨论。
- 未创建 [[Jev]] 概念节点：其**内部架构官方未公开**（奖励函数、网络结构、训练过程、校准方法均未披露），此时建页只能写成「接口层描述 + 推测」，信息密度不足；等一手论文发布后再评估。
- 时效性提示：Jev 于 2026-09-15 发布，该主题材料更新极快。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-09-19] update | raw 副本同步：jev-vs-bert

- 因 human_ai_knowledge 侧改稿（该仓库 commit 66248eb），同步更新 raw 副本 `raw/human_ai_knowledge/jev-vs-bert.md`。
- 修订内容：硬件类比一节由「失效的三点」改为「适用层级 + 跨层提示」；保留「两根轴被压成一根」这条实质判断（会导出错误预测），另两条降级为提示。
- 按 raw 规则，此处为**显式记录**的同步（非静默改写）。节点关系与参考资料无需变动：本文已关联的 [[Transformer架构]]、[[自回归建模]]、[[概率校准]]、[[因果掩码]]、[[解码策略]] 五页不受影响。

## [2026-09-22] link | rlhf-rlvr-rlcd -> [强化学习, 策略梯度, 概率校准, 贝尔曼方程, 马尔可夫决策过程]

- 人机知识《RLHF / RLVR / RLCD：三种 RL 后训练范式的对比》发布（human_ai_knowledge，commit 71d0476）：10 条来源，配图 figures/rlhf-rlvr-rlcd.svg。
- 复制话题 MD 到 `raw/human_ai_knowledge/rlhf-rlvr-rlcd.md`。
- 已存在概念追加参考资料：[[强化学习]]、[[策略梯度]]（PPO / GRPO 算法层）、[[概率校准]]（把校准当奖励的 RLCD 路线与前驱 Rewarding Doubt）、[[贝尔曼方程]]（value function 与 value-free 的取舍）、[[马尔可夫决策过程]]（LLM 后训练的 MDP 实例化）；五页 updated 同步为 2026-09-22。
- 该话题澄清了两条可回填本库的判据：
  - **奖励信号的客观性与适用域呈反向关系**：主观偏好（开放域）→ 客观正确（有真值）→ 客观校准（有界决策）。可回填到 [[强化学习]] 的适用边界讨论。
  - **RLVR 的能力上限争议**（NeurIPS 2025, arXiv 2504.13837）：pass@k 下 base model 在高 k 反超，RL 提升的是采样效率。这是一条重要的**反直觉且有出处**的结论，本库现有 RL 相关页尚未覆盖。
- 候选概念未建页（按规则报告）：[[RLHF]]、[[RLVR]]、[[RLCD]]、[[GRPO]]、[[奖励模型]]、[[过程奖励模型]]、[[熵坍缩]] 均无节点；其中 GRPO 与奖励模型具备独立定义与足够主干，可考虑建成 seed。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-04] ingest | 艺术域新建 + 赋格 / 升格 / 降格

- **新建子域 `Culture/arts`**（含 `_moc.md`），并在 `Culture/_moc.md` 的子域导航中挂上入口。原因：现有 Culture 两个子域为历史考古与思想信仰，均不适合音乐/影视类概念。
- 新增 [[赋格]]：定义（**复音音乐的固定创作形式，不是"曲式"**）、主题/答题（纯正 vs 守调）/对题（固定 vs 自由）/密接和应（含 stretto maestrale 与 fuga contraria）、四声部进入顺序、三部分结构、*fuga* = flight/escape 词源、巴赫《平均律》与《赋格的艺术》实例。**关联到本库既有 [[自指]]**（Hofstadter 的 strange loop 音乐范例）。
- 新增 [[升格]] 与 [[降格]]：以 24 格/秒为基准的变速摄影；overcranking / undercranking 的手摇机源流；升格与"后期放慢"的区别（后者无时间分辨率增益）；降格的极端形式即延时摄影；代价（帧率越高越需要光、素材量上升）。二者互为一对对比关系。
- ⚠️ **歧义处理（重要）**：`升格/降格` 存在三个互不相同的技术含义。生成前已发 clarify 询问，**超时未回复**；按"不阻塞"规则取默认值（① 电影摄影），并在两页内各加「同名辨析」节，把 ② 词义升格/降格（Elevation/Degeneration，含 *knight* / *terrific* / *nice* / *knave* / *awful* 实例）与 ③ 语域升格/降格 并列写清。**若用户本意是语言学含义，只需迁移域到 Language/linguistics，内容可直接复用。**
- 关联：`信号处理` ← 升格/降格（帧率≈时间采样率的分析性类比，已标注为非来源直述）；`自指` ← 赋格。三页均有入链，非孤儿。
- 三页均 `maturity: seed`、`confidence: high`；新增 6 条来源全部实测可访问（百度百科 403 已排除）。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-04] update | 赋格 / 升格 / 降格 补入哲学层（依用户澄清来源）

- **触发**：用户澄清这三个词是在**《哥德尔、艾舍尔、巴赫》（GEB）、《禅与摩托车维修艺术》这类书**里读到的，不是音乐/影视语境；并要求**保留音乐/摄影解释、另加哲学解释**。此前按搜索结果默认取音乐/电影含义，属依据不足的推断，已修正定位（不删原内容，改为双层结构）。
- [[赋格]] 新增「哲学层：赋格作为论证形式」：
  - GEB 英文副书名即 *A metaphorical fugue on minds and machines in the manner of Lewis Carroll*——**整本书自称一首赋格**；
  - 赋格在 GEB 中演示「缠结的层次结构」：多声部既独立又融合；
  - 关键例证 **Canon a 2 per tonos**（《音乐的奉献》BWV 1079）：逐轮升高一个调，转完若干圈回到原调——「升上去，却回到了原位」。
- [[升格]] / [[降格]] 各新增哲学层，核心例证为**艾舍尔《上升与下降》(1960)**：Penrose stairs（永无止境楼梯）上**两队装束相同的人，一队上升一队下降，谁都没有真正位移**。由此提炼出两页共用的判据：
  - **真层级**（上升单调、不可回返）vs **缠结的层级**（升格/降格都退化为绕行）；
  - 在环里，「降格」也无法退回基础层——它问的不是「退了多少」，而是「层级图是树还是环」。
- 三页关系升级为互连三角（赋格 ↔ 升格 ↔ 降格，各 3 条关系），并保留既有 [[自指]]、[[信号处理]] 连接。
- ⚠️ **未能核验**：「升格/降格」在 GEB 与《禅与摩托车维修艺术》中的**逐字用法**——多轮定向检索均未找到（中文译本用词可能不同）。已在三页变更记录中标注；如用户提供原句，可按原文对齐。
- 候选概念（按规则报告未建页）：**缠结的层次结构 / 怪圈**——三个页面现在都依赖这一概念，它具备独立定义与足够主干（GEB 核心论题），建议建成 seed。
- 新增来源 7 条（GEB 维基、艾舍尔《上升与下降》英文维基、《音乐的奉献》英文维基等），全部实测可访问。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-04] rewrite | 赋格 / 升格 / 降格 哲学层按「格 = 道德地位」重写（二稿）

- **触发**：用户给出更准确的读法——「这三个词在说的其实都是类似**人格**之类的格，**赋格就是赋予某个本来无格的对象以格**，升格、降格则说明**格有高低级别之分**」。
- **据此把「格」定为「人格／位格／道德地位」义**，三个词共用同一词根：**赋格问「有没有格」，升格／降格问「格有多高」**。初稿的 GEB「缠结层级／怪圈」读法降为对照义（赋格页保留为「附」节；升格／降格页移入「辨析」节），正文不再以它为主线。
- [[赋格]] 正文改为「哲学层：格——赋格」：
  - **道德行动者**（moral agents）／**道德受动者**（moral patients）之分（Floridi & Sanders）；
  - 道德地位的五种理论（物种属性／认知属性／道德主体性／感受能力／关系）——即"赋格标准"的五种答案；
  - **Aldo Leopold**：传统伦理学「**无法赋予非人类存有者道德地位**」——「无法赋予」即「无格」；其土地伦理（《沙乡年鉴》1949）主张"把伦理考量扩展到生态整体"；
  - 四种赋格范围（泛人道主义／感知主义／生机主义／整体主义）的分歧在**赋给谁**。
- [[升格]] 正文改为「哲学层：升格——格的等级」，核心实据是 **Pirsig 良质形而上学（MOQ；《禅与摩托车维修艺术》1974 提出、《莱拉》1991 定型）**：
  - 四层次 无机→生物→社会→智识，「**in ascending order of morality**（按道德性递增排序）」——**这是"格有高低"的逐字对应**；
  - 「演化＝这些价值模式的**道德进展**」：生物战胜无机、智识战胜社会都被直接定义为道德发展；
  - 给出可操作判据：**演化尺度上自由度更大者取得道德优先**。
- [[降格]] 正文改为「哲学层：降格——格的剥夺」：
  - 降格不是"格低一点"而是**取消资格**——Leopold 所述把成员"忽略甚至消除"；
  - 三种机制：范畴重划（MOQ 层级间的还原）／标准收紧（抬高受动者门槛）／法律撤销；
  - **升格与降格的举证责任不对称**（由伤害的可逆性决定）。
- 三页 `summary`／定义引用块改为**双层一句话**（音乐/电影义 + 哲学义，均在 60 字上限内）；`maturity` seed → **growing**；`confidence` high → **medium**（音乐/电影义高置信；哲学层的**概念**有实据，但**该词在该义上的既有用法**未获证实）。
- 三页各加 `待建：道德地位` 关系（哲学层的核心概念，尚无节点）。
- ⚠️ 仍**未能核验**「赋格／升格／降格」在该义上的**逐字用例**：检索只找到"赋予……道德地位"的说法，未找到该词组本身，故本页整理的是**概念**而非词的出处。已写入三页变更记录与「后续待补」。
- 新增来源 6 条（Moral status / Land ethic / Pirsig MOQ 维基、Philosophy Now、道德地位五种理论、位格），全部实测 HTTP 200。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-04] ingest | 道德地位（Culture/thought）

- **立项依据**：[[赋格]]／[[升格]]／[[降格]] 三页的哲学层共同依赖此概念，此前只挂 `待建：道德地位`。
- **查重**：全库无同名文件、title 或 alias（仅三页正文与 log 提及）。
- **强制检索**：web_search 3 路（中英、定义／标准／边界）→ 找到权威源 **Stanford Encyclopedia of Philosophy「The Grounds of Moral Status」**，另抓到 2026 年 *AI and Ethics* 关系观新论。web_extract 抓正文核验（非仅验链接）。
- **节点结构**（`Culture/thought/道德地位.md`，L2 ×5）：
  - **定义与两个容易混的点**：SEP 定义逐字引用（"matters … **for its own sake**"）；「有义务 ≠ 有地位」；道德行动者／受动者之分（Floridi & Sanders）与"部分道德地位"。
  - **格的来源：属性观与关系观**：property-based（内在特征：意识／感受苦乐）vs relational（社会与制度中介的关系）；2026 年论文指出属性观"通常得出当前 AI 落在道德领域之外"，而关系观把格定位在关系中；并列出 SEP §5 的 **7 条具体标准清单**（精密认知能力／发展潜能／初级认知能力／属于精密认知物种／特殊关系／尚未完全实现／其他）——这张清单本身就是"赋格标准"候选表。
  - **格是否分等级：标量观 vs 阈值观**（核心节）：SEP 记录道德地位"**以程度出现**"并设最高程度 **完整道德地位（FMS）**；阈值观逐字引用（"不因该实体拥有多少 X、把 X 展现得多好而改变"）——**这直接决定"升格／降格"是否可能**：同一档内做得更好不会升格。
  - **边界之争：谁有格**：动物／未来世代／自然与生态系统（Leopold 土地伦理：人应视自己为生物共同体的"普通成员与公民"、把伦理考量扩展到生态整体）／生态系统整体／人工系统。
  - **与三个词的对应**：赋格=有没有格（对应"格的来源"）；升格=格有多高（对应标量观／阈值观）；降格=格的剥夺（对应"边界之争"）。三个词是**同一概念上的三个动作**。
- **关系**：新增出链 4 条（[[赋格]]／[[升格]]／[[降格]]／[[三位一体]]）+ 2 条 `待建`（人格、感受能力）。**[[三位一体]] 已同步加回链**以保持双向。
- **解决既有断层**：三页的 `待建：道德地位` 全部替换为 `[[道德地位]]`。
- 新增来源 6 条，全部抓取正文核验；SEP 定义、FMS、阈值观为逐字引用。
- ⚠️ 遗留：人工系统一节目前只到"争论活跃"，未展开具体主张与反驳；关系观的具体论证结构待补。已写入「后续待补」。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-04] ingest | 人格（Culture/thought）

- **立项依据**：由上一节点 [[道德地位]] 的 `待建：人格` 立项，用于划开「格」在伦理／法律与心理学上的两种用法。
- **查重**：全库无同名文件、title 或 alias。
- **强制检索**：web_search 4 路（中英、哲学／法律／心理学）→ 找到 SEP 两个词条（**Locke on Personal Identity**、Personal Identity and Ethics）与 IEP 两个词条（Persons、Personal Identity），另抓到法律与心理学侧来源。web_extract 抓正文核验。
- **关键实据（逐字）**：洛克本人把 "person" 定为 **"…Forensick Term appropriating Actions and their Merit; and so belongs only to intelligent Agents capable of a Law, and Happiness and Misery."**（L-N 2.27.26）——**"人格"首先是法庭用语**，锚点有二：能反思 + **能被追责**。同处 L-N 2.27.9 给出意识的回溯延伸与人格同一性。
- **节点结构**（`Culture/thought/人格.md`，L2 ×5）：
  - **人格作为"法庭用语"**：洛克的三分——实体同一性／人的同一性（human being）／人格同一性（person），被刻意分开。
  - **人格同一性的几套判据**：心理连续性／生理连续性／躯体连续性／简单论（灵魂）四套对照表；心理判据的当代形式逐字引用（"uniquely psychologically continuous"）；**帕菲特的转折**——要紧的是心理连续性本身，"人格同一性"并非存活中要紧之事。
  - **法律上的人格：从人格到人格权**：自然人 vs **法人**（"由法律所创设"的抽象权利主体）；人格权（公开发表权／隐私权）；中国《民法典》人格权编；法人人格权的未决争议。
  - **同名辨析：心理学意义上的"人格"**：哲学／法律义（personhood）vs 心理学义（personality）对照表；后者即**五大性格特质／大五人格／五因素模型（OCEAN）**，"用于研究人格的五因素分类法"。
  - **与道德地位的分工**：**人格比道德地位窄，且偏向"行动者"一侧**——有格者不必有人格（婴儿、严重认知障碍者、动物通常有格而非完全人格）。因此 [[赋格]] 的"赋予本来无格者以格"实为两步：先问算不算数，再问算不算主体。
- **关系**：新增出链 3 条（[[道德地位]]／[[三位一体]]／[[赋格]]）+ 2 条 `待建`（大五性格特质、人格同一性）。**[[三位一体]]、[[赋格]] 已同步加回链**保持双向。
- **解决既有断层**：[[道德地位]] 的 `待建：人格` 已替换为 `[[人格]]`。
- 新增来源 7 条，全部抓取正文核验。
- ⚠️ 遗留：① 中国法部分只引《民法典》人格权编的条目枚举（据人格权编草案三次审议稿），未逐条核正式条文；② 法人人格权的争议只列批评一方，未列支持理由；③ 待建节点「人格同一性」建成后，本页"判据"一节应改为指向它并保留概述。
- 全库 lint 为 0 errors / 0 warnings / 0 info。

## [2026-10-06] ingest | 示范学习

- 新增概念页 `Cognition/Model/示范学习.md`（growing, confidence high）
- L1：从专家示范数据直接学习策略，模仿专家行为，是奖励信号难定义时的替代路线
- L2 子主题：核心问题（无奖励信号，与标准 RL 对比表）、主要方法（BC/DAgger/IRL/对抗式）、应用
- 关键概念：分布偏移/复合误差（BC 致命问题）、DAgger 数据聚合、逆强化学习双层优化、GAIL
- 关系：对比 在线学习；应用 损失函数；依赖 反向传播；待建 强化学习/逆强化学习/行为克隆/生成对抗网络
- 日期按系统时间 2026-10-06，review_due 按年 2027-10-06
- lint：0 error；no inbound 为新节点正常现象
