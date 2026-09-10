---
schema_version: '1.1'
title: RNA
aliases:
- Ribonucleic Acid
- 核糖核酸
summary: 由核糖核苷酸以磷酸二酯键连接形成的核酸，通常单链并参与信息传递、蛋白质合成和基因调控
type: concept
maturity: seed
confidence: high
tags:
- 核酸
- 基因表达
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://www.genome.gov/genetics-glossary/Ribonucleic-Acid-RNA?id=180
- https://www.ncbi.nlm.nih.gov/books/NBK9842/
- https://openstax.org/books/biology-2e/pages/15-1-the-genetic-code
---

# RNA

> 由核糖核苷酸以磷酸二酯键连接形成的核酸，通常单链并参与信息传递、蛋白质合成和基因调控。

## 结构与 DNA 的区别

RNA 是由[[核苷酸]]连接形成的核酸。它的糖是核糖，常见碱基为腺嘌呤（A）、尿嘧啶（U）、鸟嘌呤（G）和胞嘧啶（C）；DNA 使用脱氧核糖，并以胸腺嘧啶（T）替代 U。

| 特征 | RNA | [[DNA]] |
|---|---|---|
| 糖 | 核糖 | 脱氧核糖 |
| 常见碱基 | A、U、G、C | A、T、G、C |
| 常见形态 | 单链并可折叠 | 细胞中通常为双链 |
| 典型角色 | 信息中介、催化、调控和部分基因组 | 稳定储存遗传信息 |

“通常单链”不等于 RNA 没有局部双链结构。互补序列可以在同一条 RNA 内折叠，也可以与另一条核酸形成[[碱基对]]；部分病毒以 RNA 作为基因组。

## 三类常见 RNA

不同 RNA 由序列和折叠产生不同功能，不应只把 RNA 理解成 DNA 的临时副本。

| 类型 | 主要作用 |
|---|---|
| mRNA（信使 RNA） | 把部分 DNA 信息带到核糖体，作为翻译模板 |
| tRNA（转运 RNA） | 通过反密码子识别 mRNA，并携带相应氨基酸 |
| rRNA（核糖体 RNA） | 与核糖体蛋白共同构成核糖体，并参与翻译结构与催化 |

细胞中还存在参与 RNA 加工、基因表达调控和其他过程的 RNA。一个 RNA 分子是否编码蛋白质，要看其类型、序列和细胞中的作用，不能由“它是 RNA”直接推出。

## 从 DNA 到蛋白质

在典型的基因表达路径中，DNA 的一段序列先被转录为 RNA；其中的 mRNA 再在核糖体上按[[遗传密码]]读取，排列出[[氨基酸]]序列，形成多肽并进一步成为[[蛋白质]]。

```text
DNA ──转录──> mRNA ──翻译──> 氨基酸序列 ──折叠/组装──> 蛋白质
```

具体的密码子—氨基酸映射和终止信号见[[遗传密码]]；真正的 RNA 加工、阅读框确定和翻译还依赖细胞机器，不能只凭字符切分就断言存在蛋白质产物。

## RNA 的边界

DNA、RNA 和蛋白质使用不同的化学字母表与连接方式。RNA 序列可以携带信息，也可以折叠成具有结构或催化作用的分子；但 RNA 不是“含有遗传信息的所有分子”的总称，[[核苷酸]]、DNA、mRNA 和蛋白质分别处在不同层次。

- RNA 与 DNA 的差异来自糖、碱基和结构稳定性等多方面，不能简单归结为 T 换成 U。
- 遗传信息可以产生非编码 RNA；并非所有 DNA 转录产物都进入蛋白质翻译。
- RNA 的折叠和功能依赖序列、离子环境及与其他分子的相互作用。

## 关系网络

- 来源：[[DNA]] — DNA 序列可通过转录产生 RNA
- 组成：[[核苷酸]] — RNA 是核糖核苷酸连接形成的核酸
- 结构：[[碱基对]] — RNA 可形成局部互补配对和二级结构
- 规则：[[遗传密码]] — mRNA 的密码子按遗传密码指定氨基酸或终止
- 产物：[[蛋白质]] — mRNA 在翻译中提供蛋白质氨基酸序列的信息
- 组成关系：[[氨基酸]] — tRNA 携带氨基酸参与 mRNA 的翻译

## 参考资料

- [NHGRI：Ribonucleic Acid (RNA)](https://www.genome.gov/genetics-glossary/Ribonucleic-Acid-RNA?id=180) — RNA 的结构、常见类型、调控作用和 RNA 基因组
- [NCBI：Expression of Genetic Information](https://www.ncbi.nlm.nih.gov/books/NBK9842/) — mRNA、tRNA、rRNA 以及从 RNA 到蛋白质的表达路径
- [OpenStax Biology 2e §15.1：The Genetic Code](https://openstax.org/books/biology-2e/pages/15-1-the-genetic-code) — DNA—RNA—蛋白质的中心路径和翻译中的三联体读取
