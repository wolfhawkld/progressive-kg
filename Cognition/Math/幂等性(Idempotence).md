---
schema_version: '1.1'
title: 幂等性（Idempotence）
aliases:
- Idempotence
- 幂等性
summary: 操作满足 f(f(x))=f(x)，即首次应用后再次应用不会继续改变结果
type: concept
maturity: evergreen
confidence: high
tags:
- 数学性质
- 分布式系统
- HTTP
created: '2026-05-23'
updated: '2026-07-16'
verified: '2026-07-16'
review_due: '2027-07-16'
sources:
- https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2
- https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
---

# 幂等性（Idempotence）

> 操作满足 f(f(x))=f(x)，即首次应用后再次应用不会继续改变结果。

## 核心定义

若函数或操作 $f$ 对定义域内任意 $x$ 都满足：

$$
f(f(x))=f(x),
$$

则 $f$ 是幂等的。关键有两个：比较的是同一操作的复合，而不是“重复计算得到同一个值”；等式必须对全部输入成立，而不只是某个收敛点。

### 直觉

- 绝对值：$|\,|x|\,|=|x|$
- 集合去重：去重后的集合再去重不变
- 投影：投到同一子空间后，再投一次仍在原位置
- 赋固定值：把状态设为 `closed`，重复设置仍是 `closed`

如果 $f$ 幂等，则任意整数 $n\ge1$ 都有 $f^n(x)=f(x)$；所有输出也都是 $f$ 的不动点。

## 幂等与不动点

“算子有不动点”弱于“算子幂等”。梯度下降更新 $G$ 在最优点可能满足 $G(w^*)=w^*$，但一般仍有 $G(G(w))\ne G(w)$，所以 $G$ 不是幂等算子。

| 例子 | 是否幂等 | 原因 |
|---|---|---|
| 投影矩阵 $P$ | 是 | 对所有向量都有 $P^2x=Px$ |
| 梯度下降一步 | 通常否 | 远离不动点时第二步仍会更新 |
| Bellman 算子 | 通常否 | $V^*$ 是不动点，不代表 $T(T(V))=T(V)$ |
| 同一输入上重算 MSE | 不是该概念 | 这是确定性重算，不是把输出再次传给同一算子 |
| 用固定 $\mu,\sigma$ 重复做 Z-score | 通常否 | 第二次应用 $(x-\mu)/\sigma$ 仍会改变值 |
| L1/L2 正则化训练 | 通常否 | 再训练或再收缩通常继续改变参数 |

## 线性代数中的幂等

正交投影矩阵可写为：

$$
P=A(A^TA)^{-1}A^T
$$

当 $A$ 列满秩时有 $P^2=P$；一般情形可用 Moore–Penrose 伪逆。幂等矩阵的特征值只能是 0 或 1。[[主成分分析(PCA)]] 的“投影回选定主成分子空间”是幂等的，但降维坐标变换本身输入输出维度不同，不能不加区分地写成 $f(f(x))$。

## HTTP 语义

HTTP 所说的幂等，是多次发送相同请求时，服务器上“预期效果”与发送一次相同；响应状态码和日志等附带行为可以不同。

| 方法 | 规范语义是否幂等 | 说明 |
|---|:---:|---|
| GET / HEAD / OPTIONS | 是 | 还具有安全语义；实现仍可能记录日志等附带行为 |
| PUT | 是 | 对同一目标反复提交同一表示，预期最终状态相同 |
| DELETE | 是 | 重复删除可返回不同状态码，但目标仍处于不存在状态 |
| POST | 否 | 方法语义不保证幂等；可额外用幂等键实现业务去重 |
| PATCH | 不保证 | 补丁可能是“设值”也可能是“递增”，具体操作可自行设计为幂等 |

“方法语义幂等”不等于一次请求可以随意重放：认证、并发更新、条件请求和外部副作用仍需单独处理。

## 分布式系统中的实现

网络超时会让客户端无法判断服务端是否已经执行，因此安全重试通常需要一个可持久化的业务身份，而不只是重复发送相同 JSON。

### 幂等键

典型流程为：

1. 客户端为一次业务操作生成稳定键。
2. 服务端在事务内创建“键 → 处理状态/结果”记录。
3. 相同键和相同请求再次到达时，返回已保存结果。
4. 相同键却携带不同请求参数时拒绝处理。

并发请求、处理中的状态、失败重试和键的过期策略都必须定义；仅用进程内字典不足以提供生产级保证。

### 数据库约束

唯一索引可阻止重复插入，是实现幂等的重要构件，但它不会自动撤销已经发送的消息、扣款或其他外部副作用，也不会自动返回首次请求的完整结果。

```sql
INSERT INTO orders (request_id, amount)
VALUES ('req-123', 100)
ON CONFLICT (request_id) DO NOTHING;
```

通常还需把业务写入、幂等记录和待发送事件放入同一事务，或配合 outbox/inbox 等模式。

## Python 验证

```python
import numpy as np

A = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])
P = A @ np.linalg.pinv(A)  # 到 A 列空间的正交投影

assert np.allclose(P @ P, P)

mu, sigma = 10.0, 2.0
zscore = lambda x: (x - mu) / sigma
assert not np.isclose(zscore(zscore(14.0)), zscore(14.0))
```

## 关系网络

- 关联 [[正交]] — 正交投影是最典型的幂等线性算子
- 应用 [[主成分分析(PCA)]] — 重构到固定主成分子空间的投影满足 $P^2=P$
- 对比 [[梯度下降优化]] — 收敛点是不动点，但单步更新算子通常不幂等
- 对比 [[标准化]] — 固定参数的 Z-score 重复应用通常仍会改变数据

## 参考资料

- [RFC 9110 §9.2.2：Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) — HTTP 幂等语义
- [Fielding：Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) — REST 架构背景
- Kleppmann, *Designing Data-Intensive Applications*, Chapter 8 — 重试、故障与分布式语义
