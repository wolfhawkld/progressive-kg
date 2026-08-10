---
schema_version: 1.1
title: GPU（图形处理单元）
aliases: [Graphics Processing Unit, 图形处理单元, CUDA]
summary: 由数千个并行核心组成的通用并行处理器，借高吞吐并行执行海量数学运算，是深度学习训练与推理的主流加速器
type: concept
maturity: growing
confidence: high
tags: [硬件, 深度学习, 加速器, 并行计算]
created: 2026-08-10
updated: 2026-08-10
verified: 2026-08-10
review_due: 2026-11-08
sources:
  - https://www.thundercompute.com/blog/nvidia-gpu-architecture-explained
  - https://medium.com/online-inference/gpu-architecture-how-nvidia-gpus-execute-parallel-workloads-3bacc9d01bc4
---

# GPU（图形处理单元）

> 由数千个并行核心组成的通用并行处理器，借高吞吐并行执行海量数学运算，是深度学习训练与推理的主流加速器。

---

## 并行执行模型：SIMT 与线程层级

GPU 起源于图形渲染，天然面向大规模数据并行。其执行模型是 **SIMT（单指令多线程）**：一组线程同时执行同一条指令、作用于不同数据。与 CPU 的"少而强"不同，GPU 走"多而宽"路线，用海量并行线程换取高吞吐，靠线程切换掩盖内存延迟。

- **SM（流式多处理器）**：GPU 的基本计算单元，含多个调度器与多种核心
- **线程层级**：线程 → warp（32 线程，调度的最小单位）→ block → grid
- **warp 调度**：以 warp 为单位派发指令；同一 warp 内分支会"分叉"成串行执行（divergence）
- **CUDA Core**：通用单精度计算核心，执行加乘等标量运算

### 三种核心的分工

现代 NVIDIA GPU 在一个 SM 内混合多种核心：

| 核心类型 | 职责 | 典型例子 |
|---|---|---|
| CUDA Core | 通用标量/向量运算 | 20,480 个（B200） |
| Tensor Core | 矩阵乘加专用单元，支持混合精度 | 336 个（消费级）、数百个（数据中心） |
| Ray Tracing Core | 光线追踪（图形专用） | 84 个 |

Tensor Core 针对矩阵乘法（深度学习核心负载）做了专门优化，是当代 AI 训练吞吐的主要来源；CUDA Core 负责其余通用计算。

---

## 内存层级与带宽瓶颈

GPU 性能的真实边界常不在算力而在 **内存带宽**——数据搬运可能比计算本身更慢。理解层级对优化至关重要：

- **HBM（高带宽内存）**：DRAM 垂直堆叠经硅中介层连接，带宽远超 GDDR；如 H100 SXM 用 HBM3 达 3.35 TB/s，B200 用 HBM3e 达 8 TB/s
- **共享内存 / 寄存器**：片上快速存储，kernel 内数据复用
- **缓存层级**：L1/L2 缓存加速局部数据访问
- **合并访问（coalescing）**：线程访问连续内存时一次请求合并，是带宽利用率的关键

### 为什么不能只看 CUDA Core 数

实际吞吐由内存带宽、Tensor Core 可用性、时钟、占用率（occupancy）、kernel 融合、框架实现共同决定。同一个峰值算力下，不同负载可能分别卡在：KV cache 读取、HBM 带宽、未合并内存访问或分支分歧。

---

## 在深度学习中的角色与局限

GPU 自 2012 年 AlexNet 起成为深度学习训练的主流硬件，至今仍是生产 AI 训练的事实标准（PyTorch、JAX 广泛支持）。但它是**通用处理器**，每个计算仍需访问寄存器/共享内存——这与 TPU 的专用化形成根本对照。

- 优势：生态成熟（CUDA/PyTorch/JAX）、灵活通用、HBM 大容量可容纳模型与优化器状态
- 局限：通用性带来带宽与能效开销；峰值吞吐和每瓦性能通常低于专用 ASIC（如 TPU）

---

## 关系网络

- 对比：[[TPU]] — GPU 是通用并行处理器，TPU 是专用矩阵 ASIC；TPU 用脉动阵列规避带宽瓶颈
- 对比：[[CPU]] — CPU 少量强核、低延迟、控制密集；GPU 海量线程、高吞吐、数据并行
- 应用：[[分布式训练]] — 多卡/多机 GPU 集群是分布式训练的主要载体
- 应用：[[混合精度训练]] — Tensor Core 依赖 FP16/bfloat16/INT8 混合精度实现高吞吐
- 应用：[[模型量化]] — 低精度推理（INT8/FP16）在 GPU 上以 Tensor Core 加速
- 相关：[[flash-attention]] — 优化 GPU 上注意力计算、减少 HBM 搬运的 kernel
- 相关：[[卷积神经网络]] — 现代 GPU 架构（Tensor Core）与 CNN 的矩阵化计算紧密耦合

---

## 参考资料

- [NVIDIA GPU Architecture Explained: A Guide for AI - ThunderCompute](https://www.thundercompute.com/blog/nvidia-gpu-architecture-explained) — 2026-08 数据：核心数、HBM 带宽、Tensor Core、B200/H100
- [GPU Architecture: Memory Hierarchy, CUDA and Tensor Cores - Michael Brenndoerfer](https://mbrenndoerfer.com/writing/gpu-architecture-memory-hierarchy-cuda-tensor-cores) — 内存层级、CUDA/Tensor Core 吞吐与瓶颈分析
- [GPU architecture: How NVIDIA GPUs execute parallel workloads - Medium](https://medium.com/online-inference/gpu-architecture-how-nvidia-gpus-execute-parallel-workloads-3bacc9d01bc4) — SIMT、warp 调度、kernel 执行模型
- [Understanding CUDA Cores - Eureka](https://eureka.patsnap.com/blog/artificial-intelligence/what-are-cuda-cores) — SIMT 与线程层级
