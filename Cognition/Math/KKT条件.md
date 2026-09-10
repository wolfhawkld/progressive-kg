---
schema_version: '1.1'
title: KKT条件
aliases:
- Karush-Kuhn-Tucker conditions
- KKT conditions
summary: "约束优化的驻点、可行性、互补松弛与乘子符号共同组成的最优性条件"
type: concept
maturity: seed
confidence: high
tags:
- 优化
- 数学规划
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf
- https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
---

# KKT条件

> 约束优化的驻点、可行性、互补松弛与乘子符号共同组成的最优性条件

---

## 条件系统

对最小化 $f(x)$、不等式 $g_i(x)\le0$ 和等式 $h_j(x)=0$，令
$$
L=f+\sum_i\lambda_i g_i+\sum_j\nu_jh_j.
$$
KKT 条件包括驻点 $\nabla_xL=0$、原始可行性 $g_i(x)\le0,h_j(x)=0$、对偶可行性 $\lambda_i\ge0$ 和互补松弛 $\lambda_i g_i(x)=0$。

可复算例子：最小化 $f(x)=x^2$，约束 $x\ge1$ 写成 $g(x)=1-x\le0$。取 $x=1,\lambda=2$，有 $2x+\lambda(-1)=0$、$g(x)=0$、$\lambda\ge0$ 且 $\lambda g(x)=0$，因此满足 KKT。

## 充分性与边界

对可微凸优化，若目标和不等式函数凸、等式约束仿射，则任何满足KKT条件的原始—对偶点都给出全局最优解；这一充分性不要求Slater条件。Slater等约束资格可用于保证最优点存在相应乘子，从而获得KKT的必要性和强对偶结论。非凸问题中 KKT 常只是必要条件，且还依赖约束资格；不满足资格时最优点可能没有标准 KKT 乘子。

互补松弛表示非活跃约束的乘子为零，但不能把所有约束都当作等式。符号约定若改成 $g_i(x)\ge0$，对应乘子不等式也要反向，不能混用公式。

## 关系网络

- 前置：[[拉格朗日乘子法]] — KKT扩展拉格朗日驻点到不等式约束。
- 理论：[[凸性与凸优化]] — 凸性给出充分性，Slater等约束资格用于必要性与强对偶。
- 曲率：[[正定与半正定矩阵]] — 二阶充分条件与 PSD/PD 曲率相关。
- 二阶：[[海森矩阵]] — 检查局部约束极值的曲率。

## 参考资料

- [Boyd & Vandenberghe Convex Optimization Slides](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf) — Lagrangian、对偶问题和 KKT 系统概览。
- [Boyd & Vandenberghe Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) — KKT 必要性、充分性及 Slater 条件。

