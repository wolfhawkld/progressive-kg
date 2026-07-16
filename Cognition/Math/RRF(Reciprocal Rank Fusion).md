---
schema_version: '1.1'
title: RRF（Reciprocal Rank Fusion / 倒数排位融合）
aliases:
- RRF
- Reciprocal Rank Fusion
- 倒数排位融合
summary: 将多路结果的名次转换为倒数贡献并求和，在原始分数不可比时生成统一排序
type: concept
maturity: evergreen
confidence: high
tags:
- 信息检索
- 排序融合
created: '2026-04-29'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2027-07-16'
sources:
- https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf
---

# RRF（Reciprocal Rank Fusion / 倒数排位融合）

> 将多路结果的名次转换为倒数贡献并求和，在原始分数不可比时生成统一排序。

## 核心直觉

BM25、向量检索或不同字段检索的原始分数往往不在同一尺度上。RRF 丢弃分数幅度，只用每个候选在各列表中的名次，因此无需先校准异构分数。

代价也来自同一选择：第一名和第二名的原始分数差距无论多大，RRF 只看到它们相差一个名次。

## 核心公式

$$
\operatorname{RRF}(d)=\sum_{i=1}^{N}\frac{1}{k+r_i(d)}
$$

| 符号 | 含义 |
|---|---|
| $N$ | 排名列表数量 |
| $r_i(d)$ | 文档 $d$ 在列表 $i$ 中从 1 开始的名次 |
| $k$ | 平滑超参数 |
| 未出现 | 该列表贡献 0 |

原始论文实验使用 $k=60$，因此 60 成为常见默认值，但它不是算法定理或所有数据集上的最优值。$k$ 较小时更强调榜首差异；$k$ 很大时，有限深度列表内的名次贡献趋于接近，出现于更多列表的候选更占优势。

## 示例

两路列表分别为：

```text
dense: B, A, C, E
sparse: A, D, B, F
```

取 $k=60$：

| 文档 | dense | sparse | RRF |
|---|---:|---:|---:|
| A | 2 | 1 | $1/62+1/61\approx0.03252$ |
| B | 1 | 3 | $1/61+1/63\approx0.03227$ |
| D | — | 2 | $1/62\approx0.01613$ |
| C | 3 | — | $1/63\approx0.01587$ |

A 略高于 B。若出现并列名次、重复文档或列表截断，系统还需明确 rank 和去重规则。

## 优势与限制

| 优势 | 限制 |
|---|---|
| 不要求原始分数同尺度 | 丢弃分数间隔信息 |
| 可容纳某路未召回的候选 | 召回深度会决定谁有资格贡献 |
| 无需训练数据 | $k$、列表权重和截断深度仍是设计选择 |
| 公式简单、易解释 | 默认等权，不能表达某一路更可靠 |

如果各路得分已经可靠校准，可比较 CombSUM、加权分数融合或学习排序；如果列表质量不同，也可使用 weighted RRF，但权重需要验证集或业务依据。

## Python 实现

```python
from collections import defaultdict

def rrf_fusion(ranked_lists, k=60):
    scores = defaultdict(float)
    for ranked in ranked_lists:
        seen = set()
        for rank, doc_id in enumerate(ranked, start=1):
            if doc_id in seen:       # 单个列表内只计第一次出现
                continue
            seen.add(doc_id)
            scores[doc_id] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
```

最后用 `doc_id` 打破同分只是确定性示例；生产系统可用原始排序、时间或其他业务规则处理 tie-break。

## 关系网络

- 关联 [[词嵌入]] — 稠密检索常从嵌入相似度得到其中一路排名
- 关联 [[内积]] — 向量检索常用内积或余弦相似度形成候选列表
- 对比 [[帕累托(Pareto)]] — RRF 把多路排名直接标量化，而 Pareto 方法保留多目标非支配关系

## 参考资料

- [Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf) — RRF 原始论文与 $k=60$ 实验设置
