---
title: 主成分分析（Principal Component Analysis, PCA）
summary: 最经典的线性降维方法。将高维数据投影到方差最大的方向上，用少数主成分保留尽可能多的信息。
level: concept
category: Cognition/Math
tags: []
related: [[奇异值]], [[标准化(Standardization)]], [[内积]], [[正交]], [[均方误差]], [[RRF(Reciprocal Rank Fusion)]]]
created: 2026-05-21
last_verified: 2026-07-08
confidence: medium
status: draft
---
# 主成分分析（Principal Component Analysis, PCA）

> 最经典的线性降维方法。将高维数据投影到方差最大的方向上，用少数主成分保留尽可能多的信息。

---

## 直觉理解

**类比：拍照选角度。** 给一个三维物体拍照，最佳角度是能看清最多细节的方向。PCA 做的事情一样——在数据云团中找到"信息最丰富"的投影方向。

**步骤直觉：**
1. **数据中心化** — 把数据移到原点（减去均值）
2. **找第一主成分** — 找数据伸展最长的方向（方差最大）
3. **找第二主成分** — 在与第一主成分正交的前提下，找次长方向
4. **重复** — 直到找到 k 个主成分

---

## 核心定义/公式

### 协方差矩阵法

$$
\mathbf{C} = \frac{1}{n-1}(\mathbf{X} - \bar{\mathbf{X}})^T(\mathbf{X} - \bar{\mathbf{X}})
$$

对协方差矩阵 $\mathbf{C}$ 做特征值分解：

$$
\mathbf{C}\mathbf{v}_i = \lambda_i \mathbf{v}_i
$$

- $\lambda_i$：第 i 个主成分的方差（特征值越大 → 方向越重要）
- $\mathbf{v}_i$：第 i 个主成分的方向（特征向量）
- 第 i 个主成分 = $\mathbf{X}\mathbf{v}_i$

### SVD 等价法（更稳定）

$$
\mathbf{X} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T
$$

- $\mathbf{V}$ 的列向量就是 PCA 的主成分方向
- $\boldsymbol{\Sigma}^2/(n-1)$ 的对角线就是特征值
- 一步完成，无需显式计算协方差矩阵

### 方差解释率

$$
\text{Explained Variance Ratio}_k = \frac{\sum_{i=1}^k \lambda_i}{\sum_{i=1}^d \lambda_i}
$$

---

## 关键性质/特点

| 性质 | 说明 |
|------|------|
| **线性** | 只能捕捉线性关系，无法处理非线性结构 |
| **正交** | 主成分之间互相正交（线性无关） |
| **方差排序** | 主成分严格按方差从大到小排列 |
| **全局最优** | 在 MSE 意义下是最优线性降维 |
| **无监督** | 不需要标签，纯数据驱动 |
| **方差敏感** | 量纲不同时会被大数值特征主导 → 必须先标准化 |

---

## 与相关概念对比

| 概念 | 线性/非线性 | 监督/无监督 | 核心思想 | 典型应用 |
|------|:----------:|:---------:|---------|---------|
| **PCA** | 线性 | 无监督 | 最大化保留方差 | 降维、去噪、可视化 |
| [[奇异值|SVD]] | 线性 | 无监督 | 矩阵分解 UΣVᵀ | PCA 的计算工具 |
| t-SNE | 非线性 | 无监督 | 保持局部邻域 | 高维数据 2D/3D 可视化 |
| UMAP | 非线性 | 无监督 | 保持拓扑结构 | 大规模数据可视化 |
| LDA | 线性 | 有监督 | 最大化类间差异 | 分类降维 |
| Autoencoder | 非线性 | 无监督 | 神经网络自编码 | 深层非线性压缩 |
| [[内积]] | — | — | $x^Ty$ | PCA 投影计算手段 |
| [[均方误差]] | — | — | $(y-\hat{y})^2$ | PCA 的优化目标 |
| [[标准化(Standardization)]] | — | — | 去量纲 | PCA 的必要前置步骤 |

---

## 深度学习中的应用

| 场景 | 说明 |
|------|------|
| **数据预处理** | 降维加速后续训练（如传统 ML pipeline） |
| **特征可视化** | 对 embedding 做 PCA → 2D 散点图观察聚类 |
| **去噪** | 保留前 k 个主成分，丢弃低方差噪声维度 |
| **权重初始化分析** | 对权重矩阵做 PCA 分析训练动态 |
| **Embedding 分析** | 对词向量/句子向量降维观察语义结构 |
| **白化（Whitening）** | PCA + 方差归一化，去除特征间相关性 |
| **LoRA 初始化** | 部分工作将 PCA 用于低秩适配器的初始化 |

---

## Python 实现（简化版）

### 1. NumPy 手写 PCA（SVD 法）

```python
import numpy as np

def pca(X, n_components=2):
    """
    X: (n_samples, n_features)
    返回: X_pca (n_samples, n_components), components (n_components, n_features)
    """
    # 1. 中心化
    X_centered = X - np.mean(X, axis=0)
    
    # 2. SVD 分解
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    
    # 3. 取前 k 个主成分
    components = Vt[:n_components]
    
    # 4. 投影（也可以直接用 U*S 的前 k 列）
    X_pca = X_centered @ components.T
    
    # 5. 方差解释率
    explained_variance = (S ** 2) / (X.shape[0] - 1)
    explained_variance_ratio = explained_variance / explained_variance.sum()
    
    return X_pca, components, explained_variance_ratio

# 示例
X = np.random.randn(100, 10)
X_pca, comps, evr = pca(X, n_components=2)
print(f"前2主成分方差解释率: {evr[:2].sum():.2%}")
```

### 2. sklearn 标准调用

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),     # PCA 前必须标准化！
    ('pca', PCA(n_components=0.95)),  # 保留 95% 方差
])
X_transformed = pipeline.fit_transform(X)
print(f"保留 {pipeline[-1].n_components_} 个主成分")
```

---

## 记忆要点

| 要点 | 内容 |
|------|------|
| 本质 | 线性降维，找方差最大的投影方向 |
| 计算 | 协方差矩阵特征分解 / SVD |
| 关键约束 | 主成分间正交 |
| 前置要求 | **必须先标准化！** 否则大数值特征劫持主成分 |
| 常用场景 | 降维、可视化、去噪、embedding 分析 |
| 局限性 | 只捕捉线性结构，无法处理非线性流形 |
| 变体 | Kernel PCA（非线性）、Sparse PCA（可解释）、Incremental PCA（大数据流式） |

---

## 记忆口诀

> 去均值，算协方差；特征分解找方向。
> 方差大为第一轴，正交往后排；降维去噪可视化，标准化前置不能忘。

---

## 相关概念

- [[奇异值|SVD]] — PCA 的数值计算工具，更稳定
- [[标准化(Standardization)]] — PCA 前必须标准化，避免量纲偏差
- [[内积]] — PCA 投影 = 数据向量与主成分的内积
- [[正交]] — 主成分之间严格正交
- [[均方误差]] — PCA 用均方误差最小化寻找最优投影
- [[RRF(Reciprocal Rank Fusion)]] — 信息检索中的排序融合，与 PCA 的信息压缩理念相通

---

## 参考资料

- **原始论文**：Pearson, K. (1901). On Lines and Planes of Closest Fit to Systems of Points in Space
- **Hotelling, H. (1933).** Analysis of a complex of statistical variables into principal components
- **sklearn 文档**：[sklearn.decomposition.PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- **Bishop PRML**：Chapter 12.1 — Principal Component Analysis

---
