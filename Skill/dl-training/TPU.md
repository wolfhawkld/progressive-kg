---
schema_version: 1.1
title: TPU（张量处理单元）
aliases:
- Tensor Processing Unit
- 张量处理单元
summary: Google设计的机器学习专用加速器，以矩阵乘加阵列及向量、标量单元执行适合的张量计算
type: concept
maturity: growing
confidence: high
tags:
- 硬件
- 深度学习
- 加速器
created: 2026-08-10
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2026-12-11'
sources:
- https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm
- https://openxla.org/xprof/roofline_model
- https://arxiv.org/abs/1704.04760
---

# TPU（张量处理单元）

> Google设计的机器学习专用加速器，以矩阵乘加阵列及向量、标量单元执行适合的张量计算。

## 矩阵单元与片上复用

TPU 的矩阵乘单元（MXU）采用脉动阵列，让操作数和中间结果在相邻乘加单元间传递，减少反复从较远存储读取数据的需求。

- TensorCore 包含一个或多个 MXU，以及向量单元和标量单元。
- 向量单元处理激活等计算，标量单元处理地址和控制相关操作。
- 数据仍需在HBM、片上存储和计算单元间移动，阵列复用不消除内存带宽瓶颈。

Google架构概览包含用于解释概念的简化动画；其“矩阵乘过程中不访问内存”不能理解为整次计算或整个芯片无需访存。

## 规格与计数口径

不同代际的阵列尺寸、数量、格式及互连不同，不能将某一代规格写成TPU定义。

| 计数 | 含义 |
|---|---|
| $128\times128$ | 16,384个阵列位置 |
| $256\times256$ | 65,536个阵列位置 |
| MAC与FLOP | 一次乘加常按两次浮点操作计数，比较前应统一口径 |

阵列位置数并不单独决定实测每周期吞吐；还需要时钟、阵列利用率、数据格式和实际执行规则。官方总览将不同尺寸与统一“16K MAC/cycle”并列，本页不把这条混合描述外推到所有型号。

训练TPU常使用BF16乘法与FP32累加的路径，但支持格式应查具体版本；不能将BF16等同于整数模型量化。

## 主机与软件执行

TPU是加速器，主机CPU运行操作系统和控制程序，框架与编译器把支持的张量计算映射到TPU。

- JAX和PyTorch/XLA等可表达并提交TPU计算。
- 通用Python程序并非整段直接在TPU芯片上执行。
- 不支持的操作、动态形状或不适合的计算可能需要改写、主机处理或无法编译。
- 专用化有助于适合的负载，但不能据此保证比任何GPU都快或省电。

## 扩展与性能边界

TPU系统使用片间互连协调多个芯片；不同规模涉及不同通信路径。

- Pod：通过专用网络组合的一组TPU。
- Slice：同一Pod内由ICI连接的芯片集合。
- Multislice：通过DCN在多个slice之间交换数据。
- 部分型号具有SparseCore，用于加速稀疏或embedding相关负载。

Roofline分析仍需同时考虑计算上限和HBM等存储层级带宽；小矩阵、数据布局、通信和算子支持都会影响利用率。

## 关系网络

- 应用：[[混合精度训练]] — BF16计算与FP32累加是常见路径之一
- 应用：[[分布式训练]] — Slice及Multislice涉及不同通信层级
- 相关：[[模型量化]] — 支持的低比特存储与算术格式取决于TPU版本和编译器
- 相关：[[MoE架构]] — 专家路由及通信需要与硬件拓扑配合
- 相关：[[Transformer架构]] — 矩阵密集部分可映射到TPU计算单元
- 对比：[[GPU]] — 专用化与可编程性程度不同，均存在数据搬运成本
- 对比：[[CPU]] — 主机执行通用控制任务，TPU承担适合的算子

## 参考资料

- [Google Cloud：TPU architecture](https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm) — MXU、主机、向量/标量单元及系统互连；概览存在跨代计数混合；2026-09-11 核验
- [OpenXLA：Roofline Model](https://openxla.org/xprof/roofline_model) — TPU的HBM、VMEM等带宽限制；2026-09-11 核验
- [Jouppi等：In-Datacenter Performance Analysis of a Tensor Processing Unit](https://arxiv.org/abs/1704.04760) — 第一代65,536个8-bit MAC及明确的代际上下文；2026-09-11 核验

## 变更记录

- 2026-09-11：纠正无访存瓶颈、纯矩阵机器和无法运行软件的过度表述；区分主机/加速器、阵列大小/MAC/FLOP，移除未逐代核验的产品年表。
