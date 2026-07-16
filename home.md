---
cssclasses: [kg-home]
---

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
TABLE summary AS "定义", updated AS "更新日期", file.folder AS "域"
FROM ""
WHERE contains(["concept", "procedure", "hypothesis", "question", "experiment", "review"], type)
SORT updated DESC
LIMIT 10
```

## 待审阅

```dataview
TABLE summary AS "定义", maturity AS "成熟度", confidence AS "置信度", review_due AS "复核日期"
FROM ""
WHERE contains(["concept", "procedure", "hypothesis", "question", "experiment", "review"], type) AND (maturity != "evergreen" OR confidence = "low" OR !verified OR !sources OR (review_due AND review_due <= date(today)))
SORT review_due ASC
LIMIT 10
```

---

## 关于

- 结构约定：[[SCHEMA]]
- 变更日志：[[log]]
- 概念模板：[[_system/templates/concept]]
- MOC 模板：[[_system/templates/moc]]
- 复核模板：[[_system/templates/review]]
- Obsidian 配置：[[_system/obsidian-setup-guide]]
