---
schema_version: '1.1'
title: 人文与文明域概念地图
type: moc
scope: Culture
---

# 🏛️ 人文与文明域概念地图

## 子域导航

- [[Culture/history-archaeology/_moc|🏺 历史考古与古文明]]
- [[Culture/thought/_moc|🕉️ 思想与信仰]]

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
