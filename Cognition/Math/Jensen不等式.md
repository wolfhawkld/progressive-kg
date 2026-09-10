---
schema_version: '1.1'
title: Jensen不等式
aliases:
- Jensen's inequality
- Jensen inequality
summary: "凸函数作用于加权平均不超过函数值的加权平均，凹函数时不等号反向"
type: concept
maturity: seed
confidence: high
tags:
- 概率论
- 不等式
- 优化
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- https://web.stanford.edu/~boyd/cvxbook/
---

# Jensen不等式

> 凸函数作用于加权平均不超过函数值的加权平均，凹函数时不等号反向

---

## 加权与期望形式

若 $f$ 在包含 $x_i$ 的凸域上凸，$\lambda_i\ge0$ 且 $\sum_i\lambda_i=1$，则
$$
f\left(\sum_i\lambda_i x_i\right)\le\sum_i\lambda_i f(x_i).
$$
在可积条件下，随机变量版本为 $f(E[X])\le E[f(X)]$；凹函数的方向反转。等号条件取决于严格凸性和取值是否集中在同一点。

可复算例子：$X$ 以各 $1/2$ 概率取 $-1,1$，取凸函数 $f(x)=x^2$，则 $f(E[X])=f(0)=0$，而 $E[f(X)]=1$，满足 $0\le1$。

## 条件与应用边界

函数域必须是凸集，且相关期望存在；例如 $f(x)=\log x$ 只能在正半轴上使用。Jensen 只给出平均值的界，不能把 $E[f(X)]$ 直接替换为 $f(E[X])$，除非函数是仿射或有额外等号条件。

取 $f(x)=-\log x$ 可推出算术—几何平均不等式；在信息论中同样的凸性用于熵和散度的界。应用时需检查随机变量是否落在函数域内以及尾部积分是否有限。

## 关系网络

- 基础：[[凸性与凸优化]] — Jensen不等式是凸性的加权平均表达。
- 统计：[[期望与方差]] — 期望形式需要矩和可积性条件。
- 分布：[[概率分布]] — 权重来自概率分布。
- 信息论：[[信息熵]] — 凸函数用于熵和散度不等式。

## 参考资料

- [Boyd & Vandenberghe, Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) — Jensen不等式、凸函数及算术—几何平均例子。
- [Convex Optimization book site](https://web.stanford.edu/~boyd/cvxbook/) — 凸分析教材与课程材料。

