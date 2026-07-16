---
schema_version: '1.1'
title: dl-training概念地图
type: moc
scope: Skill/dl-training
---

# dl-training概念地图

## 当前目录

```dataview
TABLE summary AS "定义", maturity AS "成熟度", verified AS "已核验"
FROM ""
WHERE file.folder = this.scope AND type != "moc"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", maturity AS "成熟度", review_due AS "复核日期"
FROM ""
WHERE startswith(file.folder, this.scope) AND type != "moc" AND (maturity != "evergreen" OR confidence = "low" OR !verified OR !sources OR (review_due AND review_due <= date(today)))
SORT review_due ASC
```
