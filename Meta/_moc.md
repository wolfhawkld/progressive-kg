---
schema_version: '1.1'
title: 元认知概念地图
type: moc
scope: Meta
---

# 元认知概念地图

## 子域导航

- [[Meta/methodology/_moc|🧭 方法论]]
- [[Meta/reviews/_moc|🔁 复盘与审阅]]

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
