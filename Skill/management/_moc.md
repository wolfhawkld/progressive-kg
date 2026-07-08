---
title: 管理技能地图
level: moc
category: Skill/management
---

# 管理技能地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "Skill/management"
WHERE level = "concept"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "Skill/management"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
