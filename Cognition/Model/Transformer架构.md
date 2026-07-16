---
schema_version: '1.1'
title: Transformer架构
aliases:
- Transformer
summary: 以注意力和逐位置前馈网络建模序列，训练时可并行处理位置，自回归生成仍需逐步解码
type: concept
maturity: growing
confidence: high
tags:
- 模型架构
- 注意力机制
- LLM
created: '2026-07-08'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2027-01-16'
sources:
- https://arxiv.org/abs/1706.03762
---

# Transformer架构

> 以注意力和逐位置前馈网络建模序列，训练时可并行处理位置，自回归生成仍需逐步解码。

Transformer 用注意力在位置之间交换信息，再用逐位置前馈网络变换表示。与 RNN 相比，它在训练时不必沿时间步递归，因此序列位置可并行计算；decoder-only 模型在自回归生成时仍必须按 token 顺序解码。

核心架构

原始 Transformer 是 Encoder–Decoder；现代系统也可只保留编码器或带因果掩码的解码器。

### Encoder-Decoder结构

```
Encoder: 输入 → N层编码器 → 编码表示
Decoder: 编码表示 + 已生成 → N层解码器 → 输出
```

### 编码器层 (Encoder Layer)

```
输入 → Multi-Head Attention → Add & Norm → Feed Forward → Add & Norm → 输出
```

1. **多头自注意力**: 各位置互相注意
2. **前馈网络 (FFN)**: 逐位置非线性变换
3. **残差连接 + LayerNorm**: 稳定训练

### 解码器层 (Decoder Layer)

```
输入 → Masked Self-Attention → Add & Norm
    → Cross-Attention → Add & Norm
    → Feed Forward → Add & Norm → 输出
```

1. **Masked自注意力**: 不能看未来
2. **Cross-Attention**: Query来自解码器，K/V来自编码器
3. **前馈网络**

## 关键组件

注意力、逐位置 FFN、残差与归一化共同构成层结构，位置方案则补充序列顺序。

### 多头注意力 (Multi-Head Attention)

```
MultiHead(Q,K,V) = Concat(head_1,...,head_h) * W^O
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

- 各头使用不同投影，并行形成多组内容交互
- 头数和 head dimension 是架构超参数，没有通用的 8/16 头配置

### 前馈网络 (FFN)

```
FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
```

- 通常由两次线性变换和 ReLU、GELU 或门控激活组成
- 原始 Transformer 使用约 4 倍中间维度，现代模型的比例会随 SwiGLU、参数预算等变化

### 层归一化 (LayerNorm)

```
LN(x) = γ * (x - μ) / σ + β
```

- 稳定训练，适应变长序列
- **Pre-Norm vs Post-Norm**: Pre-Norm 常更易训练很深的网络，但二者在表示尺度和最终归一化等方面有不同权衡

### 位置编码 (Positional Encoding)

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

- 为序列添加位置信息
- 现代变体: 可学习位置编码、RoPE、ALiBi

## 主要变体

三类变体的区别在于保留哪些模块以及训练时允许每个位置读取哪些上下文。

### Encoder-only (BERT系列)
- 双向上下文理解
- **应用**: 文本分类、命名实体识别、语义匹配

### Decoder-only (GPT系列)
- 单向自回归生成
- **应用**: 文本生成、对话、代码生成

### Encoder-Decoder (T5, BART)
- 编码器理解，解码器生成
- **应用**: 翻译、摘要、问答

## 计算复杂度

| 操作 | 复杂度 | 说明 |
|-----|--------|------|
| 自注意力 | O(n²d) | 序列长度二次方 |
| FFN | O(nd²) | 隐藏层维度 |
| 总体 | O(n²d + nd²) | 注意力与投影/FFN谁主导取决于 $n$、$d$ 与实现 |

## 与RNN对比

| 特性 | Transformer | RNN |
|-----|------------|-----|
| 时间步并行性 | 训练时通常可并行；自回归生成仍串行 | 隐状态沿时间递归，训练和生成均有时间步依赖 |
| 信息路径 | 单层全局注意力可直接连接任意位置 | 信息需沿递归状态逐步传递 |
| 序列长度项 | 全局注意力为二次；局部/稀疏变体可降低 | 递归扫描为线性，但每步仍有隐藏维计算 |
| 内存与延迟 | 依赖注意力形式、KV Cache 与并行度 | 依赖状态大小、截断反传与并行批量 |

## 扩展阅读

- **Vision Transformer (ViT)**: 图像patch化 + Transformer
- **Swin Transformer**: 层次化、滑动窗口注意力
- **Longformer/BigBird**: 稀疏注意力，支持长序列

## 关系网络
- [[注意力机制]] - Transformer的核心
- [[位置编码]] - 为无位置偏置的注意力添加位置信息
- [[残差连接]] - 深层网络训练的关键
- [[归一化层]] - LayerNorm稳定训练
- [[混合精度训练]] - 常用于降低训练显存和提高吞吐
- [[梯度消失与梯度爆炸]] - Pre-Norm缓解的问题

## 参考资料

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — 原始 Encoder–Decoder Transformer、复杂度与并行性讨论
