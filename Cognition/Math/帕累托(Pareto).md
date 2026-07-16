---
schema_version: '1.1'
title: 帕累托（Pareto）
aliases:
- Pareto
- 帕累托
summary: 区分帕累托原则、帕累托分布与帕累托最优，并用支配关系描述多目标折衷
type: concept
maturity: growing
confidence: high
tags:
- 多目标优化
- 概率分布
- 决策
created: '2026-05-16'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2027-07-16'
sources:
- https://www.itl.nist.gov/div898/handbook/eda/section3/eda3665.htm
- https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/multi-objective-optimization-using-evolutionary-algorithms-978-0-471-87339-6
---

# 帕累托（Pareto）

> 区分帕累托原则、帕累托分布与帕累托最优，并用支配关系描述多目标折衷。

## 三个相关但不同的概念

“帕累托”常指三件事，它们共享历史来源和“不均衡/折衷”的直觉，但不能互相证明：

| 概念 | 性质 | 回答的问题 |
|---|---|---|
| 帕累托原则（80/20） | 经验启发式 | 是否存在值得优先检查的关键少数？ |
| 帕累托分布 | 概率模型 | 某个正值变量是否具有特定幂律尾部？ |
| 帕累托最优 | 多目标/福利判据 | 是否还存在让至少一项目标变好且其他目标不变差的可行解？ |

80/20 法则后来由质量管理语境推广，并不是“所有系统天然服从 80/20”的数学定律。观测到偏斜数据也不能仅凭直觉判定为帕累托分布；对数正态、其他重尾分布和混合分布也可能产生相似外观。

## 帕累托原则

帕累托原则建议先检查结果是否高度集中在少数原因、客户、功能或故障源上。`80` 和 `20` 是常见记忆数字，不是必须精确满足的比例。

### 正确用法

1. 明确结果指标和原因单位。
2. 按贡献排序并画累计贡献曲线。
3. 用真实数据找到阈值，而不是预设一定为 80/20。
4. 同时检查关键少数之间是否存在因果关系、选择偏差或统计波动。

它适合做优先级启发，不足以单独证明“只做 20% 就能得到 80% 成果”。

## 帕累托分布

Pareto Type I 的概率密度为：

$$
f(x)=\frac{\alpha x_m^\alpha}{x^{\alpha+1}},
\qquad x\ge x_m,\ \alpha>0
$$

- $x_m$ 是最小尺度。
- $\alpha$ 越小，尾部越重。
- 均值仅在 $\alpha>1$ 时存在，且为 $\alpha x_m/(\alpha-1)$。
- 方差仅在 $\alpha>2$ 时有限。

### 80/20 与形状参数

当 $\alpha>1$ 时，最高占比 $p$ 的总体份额为：

$$
S(p)=p^{(\alpha-1)/\alpha}
$$

令 $p=0.2$ 且 $S(p)=0.8$，得到 $\alpha\approx1.161$。这说明某个特定 Pareto 分布可产生 80/20，不表示任意重尾数据都满足该比例。由于此时方差无限，有限样本的观测份额还可能大幅波动。

## 帕累托最优

对最小化目标 $F(x)=(f_1(x),\ldots,f_m(x))$，若可行解 $x$ 满足：

$$
f_i(x)\le f_i(y)\ \text{对所有 }i，
\quad\text{且至少一项严格小于},
$$

则称 $x$ 支配 $y$。不被任何其他可行解支配的解称为 Pareto optimal；这些解映射到目标空间后构成 Pareto front。

### 解释边界

- 前沿可能只有一个点，也可能有很多点；目标冲突时常出现多个折衷解，但不是定义保证。
- 帕累托最优只排除可支配的浪费，不决定哪个前沿点更公平、更安全或更符合偏好。
- 极不公平的资源分配也可能是帕累托有效的，因此“有效率”不能等同于“公平”。
- 加权和是选择前沿点的一种标量化方式，但在非凸前沿上可能无法找出所有 Pareto 解。

## 机器学习中的应用

| 冲突目标 | 决策示例 |
|---|---|
| 质量 vs 延迟 | 为部署预算选择模型 |
| 精度 vs 模型大小 | 量化、剪枝和蒸馏方案比较 |
| Recall vs Precision | 按业务损失选择阈值，而不只看单一 F1 |
| 主任务 vs 公平/安全指标 | 先识别前沿，再由政策和约束做选择 |
| 多任务回报 | 比较不同任务权重产生的策略 |

Pareto front 描述可行折衷，最后的选择仍需要偏好、约束、置信区间和测量成本。

## Python：提取非支配点

```python
import numpy as np

def dominates(x, y):
    """最小化问题：x 是否严格支配 y。"""
    return np.all(x <= y) and np.any(x < y)

def pareto_mask(points):
    """O(n²) 基线实现；相同目标向量会同时保留。"""
    n = len(points)
    keep = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i != j and dominates(points[j], points[i]):
                keep[i] = False
                break
    return keep
```

二维问题可先排序再线性扫描，将总体复杂度降为 $O(n\log n)$；重复点是否全部保留需要按“解的身份”还是“唯一目标向量”明确约定。

## 关系网络

- 对比 [[梯度下降优化]] — 单目标优化给出一个标量方向，多目标优化还需定义支配或标量化
- 关联 [[均方误差]] — MSE 可作为多目标系统中的一个质量指标
- 应用 [[超参数调优]] — 多指标调参可先估计 Pareto front 再选方案
- 应用 [[知识蒸馏]] — student 质量、大小和延迟常形成折衷
- 应用 [[模型量化]] — 精度、吞吐、显存和能耗需要联合比较
- 关联 [[正则化]] — $L+\lambda R$ 是把拟合与复杂度偏好标量化的一种方式

## 参考资料

- [NIST：Pareto Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3665.htm) — 分布定义与参数性质
- [Deb, Multi-Objective Optimization Using Evolutionary Algorithms](https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/multi-objective-optimization-using-evolutionary-algorithms-978-0-471-87339-6) — 多目标支配与进化优化
