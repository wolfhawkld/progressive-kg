---
title: 语言域概念地图
level: moc
category: Language
---

# 语言域概念地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "Language"
WHERE level = "concept"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "Language"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
