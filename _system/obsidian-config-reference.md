# Obsidian 配置参考

> 2026-07-16 本机 `.obsidian/` 快照。该目录被 Git 忽略，本文件只用于跨机器手动恢复。

## 入口契约

- 主入口：`home.md`
- 默认视图：Reading View（`preview`）
- Home CSS class：`kg-home`
- Graph View：辅助入口，不替代 Home/MOC

当前本机 `workspace.json` 的主 leaf 打开 `home.md`，mode 为 `preview`。换机器后按 setup guide 手动打开并固定 Home。

## app.json

```json
{
  "defaultViewMode": "preview"
}
```

## appearance.json

```json
{
  "baseFontSize": 16,
  "enabledCssSnippets": ["hierarchy-visual"]
}
```

CSS 版本控制源：`_system/snippets/hierarchy-visual.css`。

## 社区插件

```json
["dataview", "persistent-graph"]
```

- Dataview：Home 和 MOC 动态表格的必需依赖。
- Persistent Graph：可选，只保存全局图谱布局。

本机 manifest 快照：Dataview `0.5.68`，Persistent Graph `0.3.2`。版本号只描述当前机器，不是仓库兼容性保证；安装时使用 Obsidian 社区插件渠道提供的兼容版本。

## 核心插件

当前开启：

```text
file-explorer, global-search, switcher, graph, backlink,
outgoing-link, tag-pane, page-preview, templates, note-composer,
command-palette, editor-status, outline, word-count, file-recovery,
canvas, properties, bookmarks, bases
```

当前关闭且非本库必需：

```text
daily-notes, sync, slides, audio-recorder, workspaces,
publish, footnotes, webviewer
```

## Graph View

过滤器：

```text
-path:raw -path:_system -file:_moc -file:home -file:SCHEMA -file:log
```

设置快照：

- node size multiplier：`1.2`
- tags/attachments：隐藏
- orphans：显示
- unresolved：本机 `hideUnresolved=false`；Schema lint 负责阻止仓库断链
- 六个颜色组：Math、Model、dl-training、Skill、Meta、Cognition

## 不应跨机器覆盖的文件

- `workspace.json`：窗口布局、当前页和最近文件。
- `hotkeys.json`：个人快捷键。
- 插件 `data.json`：可能含机器或版本相关状态。

复制配置前先备份目标机器的 `.obsidian/`，并始终用 `home.md` 的实际渲染结果做最终验收。
