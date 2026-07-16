---
schema_version: '1.1'
title: 认知域概念地图
type: moc
scope: Cognition
---

# 认知域概念地图

## 子域导航

- [[Cognition/Math/_moc|📐 数学]]
- [[Cognition/Model/_moc|🤖 模型]]
- [[Cognition/work/_moc|💼 工作]]
- [[Cognition/life/_moc|🌱 生活]]

## 全域概念

```dataview
TABLE summary AS "定义", maturity AS "成熟度", updated AS "更新日期"
FROM ""
WHERE startswith(file.folder, this.scope) AND type != "moc"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", maturity AS "成熟度", review_due AS "复核日期"
FROM ""
WHERE startswith(file.folder, this.scope) AND type != "moc" AND (maturity != "evergreen" OR confidence = "low" OR !verified OR !sources OR (review_due AND review_due <= date(today)))
SORT review_due ASC
```
