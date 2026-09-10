---
schema_version: '1.1'
title: CLIP（Contrastive Language–Image Pre-training）
aliases:
- Contrastive Language-Image Pre-training
- 对比语言-图像预训练
- 图文对比预训练
summary: 用图像与文本双编码器对齐配对样本，支持自然语言零样本视觉迁移的视觉语言模型
type: concept
maturity: seed
confidence: high
tags:
- 多模态
- 视觉语言
- 对比学习
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-03-11'
sources:
- https://proceedings.mlr.press/v139/radford21a.html
- https://github.com/openai/CLIP
---

# CLIP（Contrastive Language–Image Pre-training）

> 用图像与文本双编码器对齐配对样本，支持自然语言零样本视觉迁移的视觉语言模型。

## 双编码器与共享表示空间

CLIP 以图像—文本配对作为监督信号：图像编码器把图像映射到向量，文本编码器把描述映射到同一空间，训练目标让真实配对更接近、批次中的非配对更远。Radford 等人在 2021 年原始工作中用约 4 亿个互联网图文对训练模型，并在 30 多个视觉数据集上评估零样本迁移。

### 图像与文本编码器

设 $f$、$g$ 表示图像/文本编码器及其投影头，第 $i$ 个配对样本为 $(I_i,T_i)$。两侧骨干输出维度可以不同，投影后都进入共同的 $d$ 维空间。原始工作比较了 ResNet 与 Vision Transformer 图像编码器，文本侧使用 Transformer；具体模型大小和训练配方属于实现选择，不是 CLIP 概念的必要条件。

### 归一化向量

先得到编码结果，再做 $\ell_2$ 归一化：

$$
v_i=\frac{f(I_i)}{\lVert f(I_i)\rVert_2},
\qquad
u_i=\frac{g(T_i)}{\lVert g(T_i)\rVert_2}.
$$

归一化后点积就是余弦相似度。它使相似度主要表示方向关系；没有归一化或使用不同投影头时，数值不能直接与这里的 logits 定义互换。

## 对称的图文对比目标

一个 batch 含 $N$ 个正确配对，矩阵中的对角线是正样本，其余位置是当前 batch 提供的负样本。CLIP 同时训练“图像找文本”和“文本找图像”两个方向。

### 温度缩放与 logits

令可学习的正尺度为 $\alpha=\exp(s)=1/\tau$，则图像 $i$ 与文本 $j$ 的 logit 为：

$$
S_{ij}=\alpha\,v_i^\top u_j
     =\alpha\,\cos(f(I_i),g(T_j)).
$$

$\tau$ 是温度；较小的温度对应更尖锐的 softmax。实现中通常学习 $s$ 或等价的 logit scale，而不是把温度当成固定常数。

### 双向交叉熵

两方向的平均损失可写为：

$$
\mathcal L_{I\to T}=-\frac1N\sum_{i=1}^{N}
\log\frac{\exp(S_{ii})}{\sum_{j=1}^{N}\exp(S_{ij})},
$$

$$
\mathcal L_{T\to I}=-\frac1N\sum_{i=1}^{N}
\log\frac{\exp(S_{ii})}{\sum_{j=1}^{N}\exp(S_{ji})},
\qquad
\mathcal L=\frac{\mathcal L_{I\to T}+\mathcal L_{T\to I}}2.
$$

这就是两个方向的分类交叉熵：每一行或每一列都把配对位置作为目标类别。实际训练中，batch 内负样本并不保证语义上完全不相关，因此数据中的同义描述或多张相似图片会使“负样本”带来噪声。

## 零样本分类与检索

预训练后可以把任务类别写成自然语言候选文本，不更新模型参数，直接比较图像向量与候选文本向量：

$$
\hat y=\arg\max_{c\in\mathcal C}
\alpha\,\cos\bigl(f(I),g(P(c))\bigr),
$$

其中 $P(c)$ 是类别 $c$ 的 prompt。

### 一个具体分类例子

对于一张狗的照片，候选集合可以写成 `a photo of a dog` 与 `a photo of a cat`。分别编码图像和两段文本，归一化后计算两个相似度；得分较高的文本对应零样本预测。OpenAI 官方示例把 CIFAR-100 的类别填入 `a photo of a {class}` 模板，并按相似度取 top-k。

### 检索与迁移

同一空间也可用于图文检索：给定图像按 $v^\top u_j$ 排序文本，或给定文本按 $u^\top v_i$ 排序图像。原始论文在 30 多个视觉数据集上评估了这类零样本迁移；跨域表现仍需按具体任务验证。

## 使用边界与组合偏差

CLIP 分数表示候选图文的模型兼容性，零样本 softmax 也只是给定候选集合内的相对分数。

| 因素 | 影响与边界 |
|---|---|
| 温度 $\tau$ | 固定候选集合且 $\alpha>0$ 时不改变 argmax，但会改变 softmax 的尖锐程度、梯度和置信度；它不自动提供校准概率。 |
| 候选标签 | 这是一个闭合集合分类；候选中没有的类别不可能获胜，类别粒度和文字措辞也会改变结果。 |
| 计数与组合 | 图文相似度不等于可靠的对象计数或空间关系推理；组合概念和细粒度类别需单独评估，不能由整体检索分数推断。 |
| 训练数据 | 互联网图文对含噪声、缺失描述和社会偏差；高相似度不等于事实、因果关系或公平判断，细粒度、OCR 和分布外任务需单独验证。 |

## 关系网络

- 前置：[[对比学习]] — 用配对样本和批内负样本学习跨模态相似度
- 前置：[[表征学习]] — 图像与文本编码器产出可迁移表示
- 前置：[[交叉熵]] — 两个方向的相似度分类都使用交叉熵形式
- 相关：[[Transformer架构]] — 原始 CLIP 的文本编码器及部分图像编码器采用 Transformer
- 相关：[[词嵌入]] — 文本编码器从 token 表示构造句子级向量

## 参考资料

- [Radford 等：Learning Transferable Visual Models From Natural Language Supervision（PMLR, 2021）](https://proceedings.mlr.press/v139/radford21a.html) — 原始 CLIP 的训练目标、数据规模、架构与零样本评估
- [OpenAI CLIP 官方仓库](https://github.com/openai/CLIP) — 官方实现、推理 API、零样本 CIFAR-100 示例和 prompt 模板
