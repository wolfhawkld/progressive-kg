---
schema_version: '1.1'
title: 技能域概念地图
type: moc
scope: Skill
---

# 技能域概念地图

## 子域导航

- [[Skill/dl-training/_moc|🧪 深度学习训练]]
- [[Skill/coding/_moc|💻 编程]]
- [[Skill/Research/_moc|🔬 研究]]
- [[Skill/writing/_moc|✍️ 写作]]
- [[Skill/management/_moc|📋 管理]]

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
