---
title: 模型架构概念地图
level: moc
category: Cognition/Model
---

# 模型架构概念地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "Cognition/Model"
WHERE level = "concept"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "Cognition/Model"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
