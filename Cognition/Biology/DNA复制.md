---
schema_version: '1.1'
title: DNA复制
aliases:
- DNA Replication
- Deoxyribonucleic Acid Replication
summary: 以亲代DNA两条链为模板，半保留合成两个子代双链DNA分子的过程
type: concept
maturity: seed
confidence: high
tags:
- 遗传信息
- 细胞周期
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://www.genome.gov/genetics-glossary/DNA-Replication
- https://openstax.org/books/biology-2e/pages/14-3-basics-of-dna-replication
- https://openstax.org/books/biology-2e/pages/14-4-dna-replication-in-prokaryotes
- https://openstax.org/books/biology-2e/pages/14-5-dna-replication-in-eukaryotes
---

# DNA复制

> 以亲代DNA两条链为模板，半保留合成两个子代双链DNA分子的过程。

DNA 复制是在细胞分裂前复制基因组 DNA 的过程。双链 DNA 分开后，每条亲代链作为模板合成互补的新链；因此每个子代双链 DNA 都保留一条亲代链和一条新合成链，这种方式称为半保留复制。

## 复制叉与链延伸

复制通常从一个或多个复制起点开始。解旋酶打开双链，单链结合蛋白稳定模板，DNA 聚合酶在引物提供的 3′-OH 上以 5′→3′ 方向加入互补脱氧核苷酸。由于两条模板方向相反，一条新链可朝复制叉连续延伸，另一条以冈崎片段不连续合成。

### 引物、片段与连接

引物酶先合成短 RNA 引物；后续过程移除或替换引物，DNA 连接酶封合片段之间的缺口并形成磷酸二酯键。原核和真核生物的聚合酶、复制起点数量、端粒处理和辅助因子不同，但方向性限制相同。

## 保真性与细胞周期

DNA 聚合酶的互补配对和校对降低复制错误，修复系统还可处理残留错配或损伤，但复制并非绝对无误。真核细胞通常在进入分裂前完成 DNA 复制；复制和染色体分离是相互关联但不同的过程。

### 半保留不等于无变化

半保留描述每个子代分子如何继承新旧链，不保证所有碱基都与亲代完全相同。突变、修复、重组和端粒复制等过程会影响最终序列和染色体末端。

## 可复算例子

给定一段亲代双链：

```text
亲代上链  5′-A T G C-3′
亲代下链  3′-T A C G-5′
```

复制时，上链模板指导一条新的 `3′-T A C G-5′` 链，下链模板指导一条新的 `5′-A T G C-3′` 链，于是得到两个双链 DNA 分子，每个都含一条旧链和一条新链。

### 碱基与链数检查

原片段含 4 个碱基对；一次复制产生 2 个 DNA 双链分子，共 8 个碱基对，每个子代分子的一条链来自新合成链。这个小例子只验证互补与半保留计数，不代表真实基因组只有一个复制起点或没有复制蛋白参与。

## 边界与关系

- DNA 复制是 DNA→DNA；转录是 DNA→RNA，翻译是 mRNA→多肽，三者模板和产物不同。
- DNA 聚合酶只能在已有 3′-OH 上沿 5′→3′ 延伸，所以需要引物，并产生连续链与冈崎片段的差异。
- 复制保真性很高但不是绝对正确；突变、损伤、修复和重组使遗传信息传递具有可变性。

## 关系网络

- 模板：[[DNA]] — DNA 双链的碱基序列提供复制模板
- 配对：[[碱基对]] — 互补碱基配对支撑模板复制
- 构件：[[核苷酸]] — 脱氧核糖核苷酸被加入新生 DNA 链
- 组织结构：[[染色体]] — 染色体中的 DNA 在细胞周期中被复制和分配
- 发生场所：[[细胞]] — DNA 复制与细胞分裂周期相协调
- 催化：[[酶]] — 解旋酶、DNA 聚合酶和连接酶等参与复制
- 对比：[[转录]] — 转录以 DNA 为模板产生 RNA，而不是复制 DNA

## 参考资料

- [NHGRI：DNA Replication](https://www.genome.gov/genetics-glossary/DNA-Replication) — 基因组复制、细胞分裂前复制和 DNA 聚合酶
- [OpenStax Biology 2e §14.3：Basics of DNA Replication](https://openstax.org/books/biology-2e/pages/14-3-basics-of-dna-replication) — 半保留模型与 Meselson–Stahl 实验证据
- [OpenStax Biology 2e §14.4：DNA Replication in Prokaryotes](https://openstax.org/books/biology-2e/pages/14-4-dna-replication-in-prokaryotes) — 复制叉、引物、5′→3′ 延伸和冈崎片段
- [OpenStax Biology 2e §14.5：DNA Replication in Eukaryotes](https://openstax.org/books/biology-2e/pages/14-5-dna-replication-in-eukaryotes) — 真核复制起点、片段连接和端粒边界

## 变更记录

- 2026-09-11：新建 seed 概念页；核验半保留复制、5′→3′ 延伸、引物和冈崎片段边界。
