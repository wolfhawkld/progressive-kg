---
schema_version: '1.1'
title: Fisher信息
aliases:
- Fisher information
- Fisher information matrix
summary: 模型对数似然梯度外积的期望，刻画观测分布对参数局部变化的敏感度
type: concept
maturity: seed
confidence: high
tags:
- 统计学
- 概率论
- 信息论
created: '2026-09-11'
updated: '2026-09-11'
verified: '2026-09-11'
review_due: '2027-09-11'
sources:
- https://ocw.mit.edu/courses/14-381-statistical-method-in-economics-fall-2018/15224973dfc1c2b4287804c8712681f7_MIT14_381F18_lec6.pdf
- https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/5d8f16adc3385c9ff2975b121bd620e4_MIT6_441S16_course_notes.pdf
---

# Fisher信息

> 模型对数似然梯度外积的期望，刻画观测分布对参数局部变化的敏感度

---

## 定义与等价形式

对密度或质量函数 $p(x\mid\theta)$，得分为 $s_\theta(X)=\nabla_\theta\log p(X\mid\theta)$。在支持集不随 $\theta$ 变化且可交换微分与积分等正则条件下，Fisher 信息矩阵为
$$
I(\theta)=E_\theta[s_\theta(X)s_\theta(X)^\top]
=-E_\theta[\nabla_\theta^2\log p(X\mid\theta)].
$$
在这些正则条件下得分期望为零，因而该二阶矩也等于得分的协方差。它是半正定矩阵；独立同分布 $n$ 个观测的信息为 $nI(\theta)$。

可复算例子：取 $0<p<1$，单次 Bernoulli 观测 $X\sim\operatorname{Bernoulli}(p)$ 时，$s_p(X)=(X-p)/(p(1-p))$，所以 $I(p)=1/[p(1-p)]$；在 $p=0.5$ 时信息为 4。

## 估计与边界

在常规渐近条件下，最大似然估计量的协方差近似为 $I_n(\theta)^{-1}$，Fisher 信息也出现在 Cramér–Rao 方差下界中。实际计算的观测信息是 $-\nabla^2\log p(x\mid\theta)$，它依赖已观测样本，与期望信息不可混同。

参数依赖支持集、不可微似然、边界参数或信息矩阵奇异时，上述等价式和正态渐近可能失效。信息大只表示局部参数变化更容易被区分，不自动保证模型正确或全局可识别。

## 关系网络

- 估计：[[最大似然估计]] — MLE 的渐近协方差由信息矩阵控制。
- 矩：[[期望与方差]] — Fisher信息是得分二阶矩。
- 曲率：[[海森矩阵]] — 与对数似然负 Hessian 的期望相连。
- 分布：[[高斯分布]] — 高斯参数提供可复算的信息矩阵例子。

## 参考资料

- [MIT 14.381 Lecture 6](https://ocw.mit.edu/courses/14-381-statistical-method-in-economics-fall-2018/15224973dfc1c2b4287804c8712681f7_MIT14_381F18_lec6.pdf) — Fisher信息定义、信息等式和 Cramér–Rao 下界条件。
- [MIT 6.441 Information Theory Notes](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/5d8f16adc3385c9ff2975b121bd620e4_MIT6_441S16_course_notes.pdf) — Fisher信息矩阵与负期望 Hessian 的关系。

