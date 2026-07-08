---
title: 生活知识地图
level: moc
category: Cognition/life
---

# 生活知识地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "Cognition/life"
WHERE level = "concept"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "Cognition/life"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
