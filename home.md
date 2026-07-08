# 🏠 Progressive-KG

> 渐进式知识图谱——分层级、可下钻、双链网络的外脑知识系统。

## 域导航

- [[Cognition/_moc|🧠 认知]] — 数学、模型、工作、生活
- [[Skill/_moc|⚡ 技能]] — 编程、写作、管理
- [[Language/_moc|📝 语言]] — 学术英语
- [[Meta/_moc|🔮 元认知]] — 方法论、复盘
- [[Horizon/_moc|🔭 探索]] — 待探索问题、实验记录

## 最近更新

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", category AS "域"
FROM ""
WHERE level = "concept"
SORT last_verified DESC
LIMIT 10
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM ""
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
LIMIT 10
```

---

## 关于

- 结构约定：[[SCHEMA]]
- 变更日志：[[log]]
- 概念模板：[[_system/templates/concept]]
- MOC 模板：[[_system/templates/moc]]
