---
schema_version: 1.1
title: TPU（张量处理单元）
aliases: [Tensor Processing Unit, 张量处理单元]
summary: Google 为深度学习设计的专用集成电路，用脉动阵列专攻矩阵乘加运算，无法运行通用软件
type: concept
maturity: growing
confidence: high
tags: [硬件, 深度学习, 加速器]
created: 2026-08-08
updated: 2026-08-08
verified: 2026-08-08
review_due: 2026-11-08
sources:
  - https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm
  - https://emergentmind.com/topics/tensor-processing-unit-tpu
---

# TPU（张量处理单元）

> Google 为深度学习设计的专用集成电路，用脉动阵列专攻矩阵乘加运算，无法运行通用软件。

---

## 核心架构：脉动阵列与 MXU

TPU 是面向特定工作负载的 ASIC，核心思想是用专用硬件规避通用处理器（CPU/GPU）的"冯·诺依曼瓶颈"——计算过程中反复访问内存的耗时。脉动阵列（systolic array）把数千个乘加单元（MAC/ALU）直接物理相连，构成一个大矩阵，数据流经阵列时持续累加，无需在矩阵乘过程中访问内存。

- 数据经 **infeed 队列** 流入 → 载入 **HBM 高带宽内存** → 参数进入 **MXU** → 结果在 MAC 间传递累加 → 经 **outfeed 队列** 读回
- 每个 **TensorCore** 由 MXU（矩阵乘，算力主体）、向量单元（激活/softmax）、标量单元（控制流/地址计算）组成
- MXU 规格：v6e/TPU7x 为 256×256 乘加阵列，更早版本 128×128；每周期执行 **16K 次乘加**
- 输入格式 **bfloat16**，累加用 **FP32**，兼顾吞吐与数值稳定性

### 与 CPU/GPU 的本质差异

| | CPU | GPU | TPU |
|---|---|---|---|
| 定位 | 通用处理器 | 通用并行处理器 | 专用矩阵处理器 |
| 核心结构 | 少量通用核 | 2500–5000 个 ALU | 脉动阵列直连 MAC |
| 通用软件 | 可以 | 可以 | 不可以 |
| 每次计算取内存 | 是（瓶颈） | 是（共享内存） | 否（阵列内流转） |

GPU 仍是通用处理器，每个计算都要访问寄存器/共享内存；TPU 通过硬件专用化换来更高吞吐和能效，代价是只能跑神经网络这类矩阵密集负载。

---

## 演进：七代与训练/推理分工

TPU 从 2015 年推理专用起步，逐步演进为完整的训练平台：

- **TPU v1 (2015)**：仅推理，256×256 INT8 阵列
- **TPU v2 (2017)**：转向浮点，双 128×128 bfloat16 阵列，引入 **bfloat16** 格式，成为完整训练平台；每核共享 8GB HBM
- **TPU v3 (2018)**：引入液冷，算力翻倍
- **TPU v4 (2021)**：转向 3D torus 互连，引入 TPU Cube（4×4×4 拓扑）与光互连
- **TPU v5e / v5p (2023)**：拆分成本高效型（v5e）与高性能型（v5p）；v5p 每芯片 4 个 SparseCore
- **TPU v6e / TPU7x (Ironwood)**：MXU 扩到 256×256；7x 支持单主机 2×2×1 拓扑

### 规模扩展：Pod、Slice 与 Multislice

- **TPU Pod**：通过专用网络互连的一组连续 TPU
- **Slice**：同一 Pod 内由高速 **ICI 互连** 连成的芯片集合
- **Multislice**：跨 slice 用数据中心网络（DCN）通信，突破单 slice 规模上限
- SparseCore 加速稀疏运算（主要是带 embedding 的推荐模型）

---

## 关系网络

- 对比：[[混合精度训练]] — bfloat16 是 TPU 的输入格式，混合精度思想与 TPU 数值设计相互成就
- 应用：[[分布式训练]] — TPU Pod/Slice/Multislice 是分布式训练的大规模硬件载体
- 应用：[[模型量化]] — 低精度（INT8/bfloat16）是 TPU 高吞吐的核心来源
- 相关：[[MoE架构]] — 大规模 MoE 模型常以 TPU 集群训练
- 相关：[[Transformer架构]] — 现代 TPU 主要针对 Transformer 的矩阵乘负载优化
- 对比：[[GPU]] — 最直接的对比对象：GPU 是通用并行处理器，TPU 是专用矩阵 ASIC

---

## 参考资料

- [TPU architecture - Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm) — 官方系统架构（MXU、脉动阵列、拓扑、SparseCore），2026-08 更新
- [Tensor Processing Unit (TPU) Overview - Emergent Mind](https://emergentmind.com/topics/tensor-processing-unit-tpu) — 学术综述：数据流范式、内存层级、软硬件协同
- [Google TPU 官网](https://cloud.google.com/tpu) — 产品定位与 AI Hypercomputer
- [Google TPU Architecture: 7 Generations Explained - Introl](https://introl.com/blog/google-tpu-architecture-complete-guide-7-generations) — 七代演进梳理与 bfloat16 起源
