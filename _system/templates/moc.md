---
schema_version: 1.1
title:
type: moc
scope:
---

# 概念地图

## 子域导航

- [[子目录/_moc|子域名称]]

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
WHERE file.folder = this.scope AND type != "moc" AND (maturity != "evergreen" OR confidence = "low" OR !verified OR !sources OR review_due <= date(today))
SORT review_due ASC
```
