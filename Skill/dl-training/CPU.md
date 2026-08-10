---
schema_version: 1.1
title: CPU（中央处理单元）
aliases: [Central Processing Unit, 中央处理单元]
summary: 通用处理器，遵循冯·诺依曼架构以少量强核心串行执行指令与数据，是计算机的控制与运算中枢
type: concept
maturity: growing
confidence: high
tags: [硬件, 计算机体系结构, 并行计算]
created: 2026-08-10
updated: 2026-08-10
verified: 2026-08-10
review_due: 2026-11-08
sources:
  - https://en.wikipedia.org/wiki/Von_Neumann_architecture
  - https://acenet-arc.github.io/ACENET_Summer_School_General/02-architecture_of_parallel_computers/index.html
---

# CPU（中央处理单元）

> 通用处理器，遵循冯·诺依曼架构以少量强核心串行执行指令与数据，是计算机的控制与运算中枢。

---

## 冯·诺依曼架构与部件

CPU 建立在 1945 年冯·诺依曼提出的"存储程序"原理之上：**指令与数据存放在同一块内存**，CPU 通过同一通路取指和数据。这种通用性让它能运行任意软件，也是理解其局限（冯·诺依曼瓶颈）的起点。

- **控制单元（CU）**：取指、译码、调度指令执行
- **算术逻辑单元（ALU）**：执行加、乘、位运算等
- **寄存器**：CPU 内的极速暂存
- **流水线**：指令分阶段重叠执行，提升吞吐
- **ILP（指令级并行）**：超标量/乱序执行在单核内挖掘并行

### 冯·诺依曼瓶颈

处理器运算速度远快于内存读写速度，指令与数据共享同一通路，导致"等待内存"成为吞吐的根本限制。现代 CPU 用**多级缓存**（L1/L2/L3）和预取缓解这一瓶颈，但无法消除——这正是 GPU/TPU 等并行加速器存在的理由。

---

## 从单核到多核：通用并行

现代 CPU 芯片内含多个冯·诺依曼"核"（多核 CPU），一台机器可再装多个 CPU 芯片。CPU 的并行是**粗粒度**的：以少量强核心 + 线程/进程级并行为主，与 GPU 的海量细粒度线程并行形成对照。

- **核心（core）**：单个处理单元；现代服务器 CPU 含 16–96 个核
- **SMT/超线程**：单核并发执行多线程，提升利用率
- **SIMD**：单指令多数据（如 AVX），面向向量化计算
- **NUMA**：非均匀内存访问，多路 CPU 中不同核访问内存延迟不同

与 GPU（2,500–5,000 个 ALU，宽而多）相比，CPU 核数少但单核更强、低延迟、擅长复杂分支与操作系统类控制密集负载。

---

## 在深度学习中的角色

CPU 不是深度学习的主力加速器（算力与带宽远逊 GPU/TPU），但仍是整个系统不可或缺的"指挥者"：

- **数据预处理**：数据加载、shuffle、batch 组装、增强常在 CPU 侧完成
- **控制与协调**：调度 GPU/TPU 任务、进程管理、指令序列化
- **小模型/推理兜底**：小规模推理、边缘低功耗场景可用 CPU
- **受限环境**：无 GPU 时的训练/推理替代（如 llama.cpp 的 CPU/GGUF 路径）

---

## 关系网络

- 对比：[[GPU]] — CPU 少量强核、低延迟、控制密集；GPU 海量线程、高吞吐、数据并行
- 对比：[[TPU]] — 三者同台：CPU 通用、GPU 通用并行、TPU 专用矩阵 ASIC
- 应用：[[分布式训练]] — 训练节点中 CPU 承担数据预处理与任务调度
- 相关：[[混合精度训练]] — CPU 参与数据转换与格式化，GPU/TPU 负责核心矩阵运算

---

## 参考资料

- [Von Neumann architecture - Wikipedia](https://en.wikipedia.org/wiki/Von_Neumann_architecture) — 存储程序原理、缓存层级、微架构对比
- [Parallel Computer Architecture - ACENET Summer School](https://acenet-arc.github.io/ACENET_Summer_School_General/02-architecture_of_parallel_computers/index.html) — 多核并行、内存组织、现代核心的冯·诺依曼布局
- [Von Neumann Architecture - GeeksforGeeks](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-von-neumann-architecture) — CU/ALU/寄存器组成与工作原理
