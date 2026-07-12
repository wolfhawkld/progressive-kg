# Obsidian 配置参考（Metis 端 2026-07-12）
> 本机 .obsidian/ 的配置值快照，供 Nemesis 手动同步。
> `.obsidian/` 在 gitignore 中，不参与版本控制。
> 实际操作步骤见 `_system/obsidian-setup-guide.md`。

---

## app.json（编辑器设置）

```json
{ "defaultViewMode": "preview" }
```

- `preview` = Reading view
- 在 Settings → Editor → Default view mode 中设置

## appearance.json（外观）

```json
{
  "baseFontSize": 16,
  "enabledCssSnippets": ["hierarchy-visual"]
}
```

- CSS 源文件在 `_system/snippets/hierarchy-visual.css`
- 复制到本机 `.obsidian/snippets/` 后，通过 Settings → Appearance → CSS snippets 启用

## community-plugins.json

```json
["dataview", "persistent-graph"]
```

- 两个社区插件都通过 Settings → Community plugins → Browse 手动安装
- Dataview：MOC 文件中的 ```` ```dataview ```` 查询依赖此插件
- Persistent Graph：保存图谱节点位置布局

## core-plugins.json（已启用的核心插件）

```json
{
  "file-explorer": true,
  "global-search": true,
  "switcher": true,
  "graph": true,
  "backlink": true,
  "outgoing-link": true,
  "tag-pane": true,
  "page-preview": true,
  "templates": true,
  "note-composer": true,
  "command-palette": true,
  "editor-status": true,
  "outline": true,
  "word-count": true,
  "file-recovery": true,
  "canvas": true,
  "properties": true,
  "bookmarks": true,
  "bases": true
}
```

- 其余核心插件（daily-notes, slides, sync 等）保持关闭

## graph.json（图谱视图）

- **过滤器**：`-path:raw -path:_system -file:_moc -file:home -file:SCHEMA -file:log`
- **节点大小**：1.2x
- **显示孤立节点**：开（便于发现未关联概念）
- **6 个颜色分组**：Cognition/Math(蓝) / Cognition/Model(绿) / Skill/dl-training(橙) / Skill(红) / Meta(紫) / Cognition(青)
- 详细颜色 RGB 值见 graph.json 文件
