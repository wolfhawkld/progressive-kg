---
schema_version: 1.1
title: CPU（中央处理单元）
aliases:
- Central Processing Unit
- 中央处理单元
summary: 执行指令集所定义的算术、逻辑与控制操作的通用处理器，可通过多核、向量和指令级并行提升性能
type: concept
maturity: growing
confidence: high
tags:
- 硬件
- 计算机体系结构
- 并行计算
created: 2026-08-10
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2026-12-11'
sources:
- https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/003/ia-cores-level-1-and-level-2-caches/
- https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/introduction-speculative-side-channel-methods.html
- https://www.intel.com/content/dam/doc/manual/64-ia-32-architectures-optimization-manual.pdf
---

# CPU（中央处理单元）

> 执行指令集所定义的算术、逻辑与控制操作的通用处理器，可通过多核、向量和指令级并行提升性能。

## 指令执行与组成

CPU 按指令集执行程序；常见组成包括控制逻辑、算术逻辑与浮点单元、寄存器和缓存。具体实现可以是顺序执行或乱序执行，不能以“串行”概括所有 CPU。

- 流水线允许多条指令处在不同执行阶段。
- 超标量与乱序机制可利用指令之间的独立性。
- 寄存器保存操作数和中间结果；算术操作不必每次访问主存。

## 存储程序与内存层级

存储程序模型有助于理解通用计算，但体系结构的逻辑模型不等于实际取指与访存通路。现代 CPU 可使用分离的一级指令缓存与数据缓存，同时在更低层共享缓存或主存。

| 层次 | 作用 |
|---|---|
| 寄存器 | 保存当前运算状态与操作数 |
| 缓存 | 利用时间和空间局部性减少慢速访存 |
| 主存 | 容纳程序和较大工作集 |

缓存未命中、依赖链和内存带宽都可能限制性能。GPU、TPU 同样有数据供给与存储瓶颈，不能将它们描述为彻底消除访存成本的装置。

## 多种并行方式

CPU 可以同时利用线程级、向量级与指令级并行；可用程度取决于程序和硬件。

- 多核并行让不同线程在不同核心运行。
- 支持 SMT 的核心可并发维护多个硬件线程，但不等于拥有相同数量的独立核心。
- SIMD 指令对多个数据元素执行相同操作。
- 多路或部分多芯片设计中，NUMA 会使不同内存位置的访问代价不同。

CPU 核心与 GPU 的标量运算单元不是同一计数单位，不能直接按“核心数”比较算力。

## 在训练与推理系统中的角色

CPU 常承担数据加载、预处理、任务调度和主机控制，也能直接运行模型推理或训练。

- 大型稠密训练通常使用加速器，CPU 为其提供数据与控制。
- 小批量、分支密集或不值得支付设备传输成本的负载可能适合 CPU。
- 性能比较应固定任务、精度、batch 和软件实现；不能宣称任何 CPU 都必然慢于任何 GPU。

## 关系网络

- 对比：[[GPU]] — 比较控制流、数据并行与吞吐取向，核心计数不直接等价
- 对比：[[TPU]] — CPU 执行通用主机任务，TPU 加速适合的张量算子
- 应用：[[分布式训练]] — 主机可承担预处理、任务协调和通信控制
- 相关：[[混合精度训练]] — 不同设备可支持不同dtype与算子路径

## 参考资料

- [Intel：IA Cores Level 1 and Level 2 Caches](https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/003/ia-cores-level-1-and-level-2-caches/) — 分离的一级指令/数据缓存；2026-09-11 核验
- [Intel：Introduction to Speculative Execution Side Channel Methods](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/introduction-speculative-side-channel-methods.html) — 乱序、推测执行与微架构状态；2026-09-11 核验
- [Intel：Optimization Reference Manual](https://www.intel.com/content/dam/doc/manual/64-ia-32-architectures-optimization-manual.pdf) — 处理器执行、缓存、SIMD及线程优化；2026-09-11 核验

## 变更记录

- 2026-09-11：重核定义与硬件机制；去除串行、固定核数、每次计算均访问主存和通用性能排序的绝对表述。
