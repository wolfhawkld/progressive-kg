---
schema_version: 1.1
title: GPU（图形处理单元）
aliases:
- Graphics Processing Unit
- 图形处理单元
summary: 面向图形与大规模数据并行计算的处理器，通过并发线程和专用运算单元提供高吞吐
type: concept
maturity: growing
confidence: high
tags:
- 硬件
- 深度学习
- 加速器
- 并行计算
created: 2026-08-10
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2026-12-11'
sources:
- https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- https://openxla.org/xprof/roofline_model
---

# GPU（图形处理单元）

> 面向图形与大规模数据并行计算的处理器，通过并发线程和专用运算单元提供高吞吐。

## GPU 与 CUDA 的区别

GPU 是硬件类别，CUDA 是 NVIDIA 的并行计算平台和编程模型，二者不是同义词。不同厂商和代际的线程组织、指令与内存系统可以不同。

以下使用 NVIDIA CUDA 解释常见机制；其他 GPU 平台不能直接套用所有名称和线程宽度。

## 并行执行与专用单元

CUDA 将 kernel 的线程组织成 block 和 grid。在 NVIDIA 的 SIMT 模型中，线程以 32 个为一组形成 warp；分支分歧可能降低有效并行度。

| 单元或概念 | 作用与边界 |
|---|---|
| SM | 容纳调度器、寄存器及多种运算资源 |
| 标量运算单元 | 执行其支持的算术、逻辑指令；不能与CPU核心一比一计数 |
| Tensor Core | 加速支持格式的矩阵乘加，格式随架构改变 |
| 光线追踪单元 | 部分图形产品提供，不是所有数据中心GPU都有 |

线程是软件执行实体，运算单元是硬件资源。不能把线程数、CUDA Core 数、SM 数和 Tensor Core 数混成同一个指标。

## 数据搬运与性能

寄存器、共享内存、缓存和设备内存组成不同层级。设备内存可采用 HBM 或 GDDR 等技术，具体容量和带宽取决于产品。

- 合并访存减少完成一组线程访问所需的内存事务。
- 片上数据复用和融合算子可减少设备内存往返。
- 足够的可运行线程有助于隐藏延迟，但高占用率不保证最高性能。
- 计算密集与带宽密集负载具有不同瓶颈，应结合算术强度和实际测量判断。

GPU 也包含矩阵专用硬件；不能以“GPU每次运算都访存、TPU从不访存”解释两者差异。

## 深度学习中的使用边界

GPU 可执行训练与推理中的矩阵乘法、卷积和其他可并行算子。吞吐收益受数据形状、精度、编译器和kernel覆盖影响。

- 支持某种低精度格式，不等于整条模型路径都使用低精度计算。
- 内存容量还需容纳激活、优化器状态、临时工作区或KV缓存。
- 与CPU或TPU比较能效和速度时，需要固定工作负载与测量口径。

## 关系网络

- 对比：[[TPU]] — 两者均有专用矩阵资源，实际瓶颈与数据流设计不同
- 对比：[[CPU]] — 面向不同并行粒度和控制流需求
- 应用：[[分布式训练]] — 多GPU训练涉及设备内与设备间通信
- 应用：[[混合精度训练]] — 低精度算子和高精度状态配合，收益取决于实现
- 应用：[[模型量化]] — 低比特存储及算术需要匹配kernel支持
- 相关：[[flash-attention]] — 通过分块与片上复用减少注意力计算的数据搬运
- 相关：[[卷积神经网络]] — 卷积可映射到GPU支持的并行计算

## 参考资料

- [NVIDIA：CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) — CUDA平台、线程层级、SIMT和内存机制；2026-09-11 核验
- [OpenXLA：Roofline Model](https://openxla.org/xprof/roofline_model) — 计算与带宽瓶颈的区分；2026-09-11 核验

## 变更记录

- 2026-09-11：删除CUDA错误别名；限定NVIDIA示例，移除混用型号的核心数和无依据的性能优劣断言，重核内存与低精度边界。
