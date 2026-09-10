---
schema_version: '1.1'
title: 复核：2026-09-11全库维护
aliases: []
summary: 审阅全库143个知识页面，记录事实纠错、公式条件、关系边界及尚待验证的事项
type: review
maturity: growing
confidence: high
tags: [复核, 知识维护]
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- SCHEMA.md
- _system/OPERATIONS.md
---

# 复核：2026-09-11全库维护

> 审阅全库143个知识页面，记录事实纠错、公式条件、关系边界及尚待验证的事项。

## 范围与结论

按用户“再整体维护下看看哪些概念有问题”的要求，审阅143个知识页面：131个concept、11个procedure、1个hypothesis。本轮修正32页，其他页面的状态是“本轮未发现明确问题”，不代表逐条事实均经独立证明。

- 数学61页、模型45页、生物9页、训练技能17页、文化9页、认知假设1页、方法论1页。
- 全库结构、别名歧义、链接、L1镜像与生命周期接受lint检查；24个seed有实质内容，不是空占位，未批量升级。
- 关键错误通过原始论文、官方文档、教材或具体研究摘要定向核对。未逐条重查所有旧来源，未运行训练或硬件性能实验。
- 开始前git pull无新增提交；raw/保持只读，MOC动态查询继续收录原目录页面。

## 已修复的问题

以下是实际接受的修改，逐页来源及变更记录保存在对应笔记中。

| 范围 | 问题与修复 |
|---|---|
| CPU、GPU、TPU | 删除CPU只能串行、每次运算必经内存、TPU无内存瓶颈等绝对说法；区分缓存、SIMT、矩阵单元与代际规格。CUDA不再作为GPU别名。128²与256²阵列分别是16384与65536个位置，不能混用运算计数。 |
| Adam与AdamW优化器、训练调试 | AdamW衰减作用于旧参数；显存区分参数、梯度与优化器状态，不再用统一倍数。FP16 AMP梯度裁剪前先unscale，再step/update。 |
| 动量、参数高效微调、梯度下降优化 | 补充动量展开的零初值条件；修复主要方法的标题层级；移除过宽的“优化器”同义词。 |
| 奇异值 | 区分PageRank特征向量、LoRA低秩更新和截断SVD；Tikhonov改变滤波因子而非原矩阵奇异值；补相对条件数、矩形矩阵和任务信息边界。 |
| 泰勒展开、中值定理、洛必达法则 | 区分泰勒级数与函数相等所需的余项条件；柯西中值定理避免未经条件直接除法；洛必达法则补可导、分母与极限条件。 |
| 信号处理、偏微分方程、积分变换、拉普拉斯变换、Z变换、卷积 | 补带限采样、CFL离散格式和维度、Hilbert主值、收敛域和初始条件；区分数学卷积与深度学习互相关实现。 |
| 因果推断、贝叶斯推断、MCMC | 普通贝叶斯网络不自动具有因果语义；新增数据不保证更准确；区分变分优化与MCMC近似；R-hat不是单独的收敛证明。 |
| 卷积神经网络、残差连接、联邦学习 | 卷积尺寸补floor与dilation；残差Jacobian用恒等矩阵，pre-activation顺序为Norm→Act→Conv；FedAvg区分权重与差分，安全聚合不等于传输加密。 |
| 超连接 | 更正HC首次提交年份；mHC双随机矩阵的非扩张性质不能等同于完整网络稳定性保证，有限Sinkhorn是近似约束。 |
| 古蜀僰人文化、三星堆遗址、金沙遗址、羽化 | 区分历史族称、悬棺墓主归属、考古物证与信仰解释；删除未经证据支持的传承和族属定论；遗址、文化、博物馆不作为无条件同义词；修正羽化词义范围与引用题名。 |
| RNA、氨基酸、遗传密码 | RNA与氨基酸不是组成关系；蛋白质可含无序构象；碱基配对可发生在同一链内。 |

## 核验与生命周期处理

结构检查与内容核验分别记录，避免把通过lint当作事实准确的证明。

- `python3 _system/lint.py`：0 error / 0 warning / 0 info。
- `git diff --check`：通过。
- 数值抽查：AdamW示例正确结果1.66，先更新再整体衰减为1.666；AMP示例先取消8倍缩放再裁剪得1，反序仅得0.125；矩阵尺寸与FP32优化器状态字节数复算一致。
- CPU/GPU/TPU重写后核对官方架构依据，verified更新为本日；其他局部修正保留既有verified，updated更新并写变更记录。未修改任何页面的maturity。
- 本review的high与verified描述审阅记录及检查结果，不是对全库所有学术主张的统一认证。

## 尚需专项验证

下列事项仍保留证据边界；本轮不将其写成确定结论。

| 对象 | 当前缺口 | 下一步与触发条件 |
|---|---|---|
| [[AGI实现路径-人类智能融合]] | 路径假设尚无本项目对照实验，verified为空是合理状态 | 开始研究该主张时，按页内同预算基线、跨域任务和可证伪指标验证 |
| [[类比导航学习法]] | 本地学习效果尚未验证，不能凭形象程度宣称有效 | 实际采用时比较无提示回忆、迁移任务和延迟保持，保留对照 |
| [[古蜀僰人文化]]、[[僚人]]、[[悬棺葬]] | 族称与墓主归属有研究分歧；摘要不能替代全部史料和遗骸分析 | 写专门历史论断前通读原论文、史料及测年/样本方法；CAS旧链接本轮抓取失败，不能据此判定资料失效 |
| [[三星堆遗址]]、[[金沙遗址]] | 精确分期、器物计数与政治继承需限定报告和口径 | 增补具体年代/数量时核对正式考古报告，区分残片、件数与统计时间 |
| [[CPU]]、[[GPU]]、[[TPU]]、[[Adam与AdamW优化器]] | 实际吞吐、显存和最优超参数依赖硬件、精度、模型与库版本 | 做具体选型或训练时固定版本并测量，不把概念页当性能承诺 |
| [[超连接(Hyper-Connections)]]及其他模型页 | 原论文给定条件的结果不等于本项目复现 | 采用机制前核对论文/实现版本和任务设定，再做消融或数值验证 |
| [[傅里叶变换]]、[[拉普拉斯变换]]、[[Z变换]] | 正交投影的函数空间、单边δ(t)端点处理及z=e^{sT}的采样约定可进一步细化；本轮未发现需立即改写的核心公式错误 | 推导具体例子时显式约定函数空间、积分端点和采样方式；马尔可夫链、张量页也可继续补强原始来源 |
| 全库来源与展示 | 未逐链接测试所有外链，也未进行Obsidian GUI视觉验收 | 引用用于正式写作前重查原文；开启Obsidian时检查Dataview与图谱呈现 |

## 逐页覆盖记录

下表枚举本轮审阅的全部知识页面。“修正”涵盖正文、公式、别名或关系修复；“未见明确问题”只表示本次阅读没有发现可确定错误；“待实证”不等于结构不合格。

| 目录 | 页面 | 本轮状态 |
|---|---|---|
| Cognition | [[Cognition/AGI实现路径-人类智能融合]] | 待实证，保留未核验状态 |
| Cognition/Biology | [[Cognition/Biology/DNA]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/RNA]] | 修正 |
| Cognition/Biology | [[Cognition/Biology/几丁质]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/多糖]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/核苷酸]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/氨基酸]] | 修正 |
| Cognition/Biology | [[Cognition/Biology/碱基对]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/蛋白质]] | 未见明确问题 |
| Cognition/Biology | [[Cognition/Biology/遗传密码]] | 修正 |
| Cognition/Math | [[Cognition/Math/JVP]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/Log-Sum-Exp]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/RRF(Reciprocal Rank Fusion)]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/VJP]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/Z变换]] | 修正 |
| Cognition/Math | [[Cognition/Math/中值定理]] | 修正 |
| Cognition/Math | [[Cognition/Math/主成分分析(PCA)]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/乘积法则]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/二项式定理]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/互信息]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/余弦相似度]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/信号处理]] | 修正 |
| Cognition/Math | [[Cognition/Math/信息熵]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/偏差-方差分解]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/偏微分方程]] | 修正 |
| Cognition/Math | [[Cognition/Math/傅里叶变换]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/内积]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/功率谱密度]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/卷积]] | 修正 |
| Cognition/Math | [[Cognition/Math/向量]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/商法则]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/均方误差]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/外积]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/奇异值]] | 修正 |
| Cognition/Math | [[Cognition/Math/奇异值分解]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/奇点]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/希尔伯特变换]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/帕累托(Pareto)]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/幂变换]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/幂等性(Idempotence)]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/幂级数]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/幂级数解]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/张量]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/微分法则总览]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/拉普拉斯变换]] | 修正 |
| Cognition/Math | [[Cognition/Math/收敛半径]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/最大似然估计]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/条件独立]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/柯西中值定理]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/标准化]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/梅林变换]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/正交]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/池化]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/泰勒展开]] | 修正 |
| Cognition/Math | [[Cognition/Math/洛必达法则]] | 修正 |
| Cognition/Math | [[Cognition/Math/特征值与特征向量]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/特征工程]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/矩阵]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/积分变换]] | 修正 |
| Cognition/Math | [[Cognition/Math/罗尔定理]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/自动微分]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/自指]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/莱布尼茨公式]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/贝叶斯定理]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/过拟合]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/链式法则]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/雅可比矩阵]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/频谱]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/马尔可夫性质]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/马尔可夫链]] | 未见明确问题 |
| Cognition/Math | [[Cognition/Math/高阶导数]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/CLIP]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/ELBO]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/InfoNCE]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/KL散度]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/Metropolis-Hastings算法]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/MoE架构]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/RoPE]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/Softmax]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/Transformer架构]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/do-演算]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/flash-attention]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/kv-cache]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/交叉熵]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/位置编码]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/卷积神经网络]] | 修正 |
| Cognition/Model | [[Cognition/Model/反事实]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/反向传播]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/变分推断]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/吉布斯分布]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/吉布斯采样]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/因果推断]] | 修正 |
| Cognition/Model | [[Cognition/Model/在线学习]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/对比学习]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/归一化层]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/循环神经网络]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/感受野]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/扩散模型]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/损失函数]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/梯度消失与梯度爆炸]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/正则化]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/残差连接]] | 修正 |
| Cognition/Model | [[Cognition/Model/注意力机制]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/激活函数]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/联邦学习]] | 修正 |
| Cognition/Model | [[Cognition/Model/自监督学习]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/表征学习]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/词嵌入]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/贝叶斯推断]] | 修正 |
| Cognition/Model | [[Cognition/Model/贝叶斯网络]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/超连接(Hyper-Connections)]] | 修正 |
| Cognition/Model | [[Cognition/Model/退火算法]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/配分函数]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/隐马尔可夫模型]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/马尔可夫网络]] | 未见明确问题 |
| Cognition/Model | [[Cognition/Model/马尔可夫链蒙特卡洛（MCMC）]] | 修正 |
| Culture/history-archaeology | [[Culture/history-archaeology/三星堆遗址]] | 修正 |
| Culture/history-archaeology | [[Culture/history-archaeology/僚人]] | 未见明确问题 |
| Culture/history-archaeology | [[Culture/history-archaeology/古蜀僰人文化]] | 修正 |
| Culture/history-archaeology | [[Culture/history-archaeology/悬棺葬]] | 未见明确问题 |
| Culture/history-archaeology | [[Culture/history-archaeology/金沙遗址]] | 修正 |
| Culture/thought | [[Culture/thought/尸解]] | 未见明确问题 |
| Culture/thought | [[Culture/thought/神仙信仰]] | 未见明确问题 |
| Culture/thought | [[Culture/thought/羽化]] | 修正 |
| Culture/thought | [[Culture/thought/道教]] | 未见明确问题 |
| Meta/methodology | [[Meta/methodology/类比导航学习法]] | 待实证，保留未核验状态 |
| Skill/dl-training | [[Skill/dl-training/Adam与AdamW优化器]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/CPU]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/GPU]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/Muon优化器]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/TPU]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/交叉验证]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/分布式训练]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/动量]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/参数高效微调]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/学习率调度]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/数据增强]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/梯度下降优化]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/模型量化]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/混合精度训练]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/知识蒸馏]] | 未见明确问题 |
| Skill/dl-training | [[Skill/dl-training/训练调试]] | 修正 |
| Skill/dl-training | [[Skill/dl-training/超参数调优]] | 未见明确问题 |

## 关系网络

- 依据：[[SCHEMA]] — frontmatter、关系、生命周期及审阅契约
- 复核：[[奇异值]] — 数学应用中的概念混淆与边界修正
- 复核：[[训练调试]] — AMP执行顺序的实际操作影响
- 复核：[[古蜀僰人文化]] — 历史判断的证据层级

## 参考资料

- [[SCHEMA]] — Schema 1.1及Review/Update要求
- [_system/OPERATIONS.md](../../_system/OPERATIONS.md) — Lint与Maintain操作流程
- 各已修正页面的“参考资料”和“变更记录” — 本次纠错的具体外部依据、作用与局限
