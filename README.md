# 设计课无敌教练

> 从“我有个概念”到“老师问吧，我准备好了”。

`spatial-design-coach` 是一个轻量、开源的 Agent Skill，面向建筑学、城乡规划和风景园林学生。它从项目任务书出发，帮你读懂题目、形成设计命题、推演方案、完成图纸，并把汇报与答辩讲清楚。

**English summary:** A lightweight, open-source design-studio coach that helps architecture, urban planning, and landscape architecture students move from the project brief to a coherent, submission-ready design.

## 它能帮你做什么

- 从任务书中拆出设计目标、约束、必交成果和真正的设计矛盾。
- 把“活力”“生态”“在地性”等抽象概念转换为可检查的空间机制。
- 生成和比较 2–3 个机制、价值取舍真正不同的方案，而不是同一构图换件外套。
- 针对实际草图、平面、剖面、模型、展板和教师反馈进行评图，并给出下一轮动作。
- 连接建筑—场地—街区—城市—区域尺度，综合建筑、规划和景观判断。
- 整理必交成果、展板叙事、汇报骨架与模拟答辩。

它是设计教练，不是一键代做器。“无敌”是给你打气，不是保证高分或获奖。

## 安装

### 方式一：一条命令安装（推荐）

需要本机已安装 Node.js 与 `npx`：

```bash
npx skills add XiaoSiKe/spatial-design-coach --skill spatial-design-coach -g
```

安装后重新打开一个 Codex 任务，让新 Skill 进入可用列表。

### 方式二：手动安装

```bash
git clone https://github.com/XiaoSiKe/spatial-design-coach.git
mkdir -p ~/.agents/skills
cp -R spatial-design-coach/skills/spatial-design-coach ~/.agents/skills/
```

如果你的 Agent 使用其他 Skill 目录，将 `skills/spatial-design-coach/` 整个复制到该目录即可；不要只复制 `SKILL.md`，否则会丢失按需加载的参考文档。

> 仓库同时包含 Codex 插件 manifest，但 v0.1.0 尚未提交公共 Plugin Directory。

## 在 Codex 中调用

Codex 中有三种用法：

1. 输入 `/skills`，然后选择“设计课无敌教练”。
2. 在消息中显式写出 `$spatial-design-coach`。
3. 直接描述设计课问题；当语义匹配时，Codex 可以自动调用。

```text
$spatial-design-coach 这是我的任务书和现在的平面，请先帮我判断最核心的设计矛盾。
```

`/spatial-design-coach` **不是** Codex 自定义命令，请使用 `/skills` 或 `$spatial-design-coach`。详见 OpenAI 官方文档：[Build skills](https://developers.openai.com/codex/skills) 和 [Developer commands](https://developers.openai.com/codex/cli/slash-commands)。

## 第一次怎么用

最好直接上传或粘贴**项目任务书**，再附上：

- 当前做到哪一步；
- 已有的草图、图纸、模型或教师反馈；
- 截止时间；
- 现在最卡的一件事。

如果暂时没有任务书，告诉它专业、课题、地点、截止时间和最卡的一点。教练会标记假设后继续，不会因为材料不齐就把你留在门口。

### 示例一：从任务书开始

```text
$spatial-design-coach 这是课程任务书。请先提取项目卡，判断题目真正要解决什么，再给我这周要完成的 3 个动作。
```

### 示例二：带现有方案来评图

```text
$spatial-design-coach 这是我的总图、两张剖面和上次评图意见。请别先帮我美化，先找出概念、空间和表达之间最致命的一处断裂。
```

### 示例三：截止期救火

```text
$spatial-design-coach 还有 36 小时交图。请切换救火模式，根据任务书和当前文件列出必交成果，冻结主线，并排出最值得修复的 3 个问题。
```

## 两种辅导模式

- **成长模式**（默认）：通过提问、对比、评图和反思训练设计判断，逐步减少对教练的依赖。
- **救火模式**：当你明确说紧急，或截止时间不超过 72 小时时启用。先冻结非致命的主线决定，再保住必交成果、图纸一致性和能讲清的逻辑。

救火不等于代做：关键设计决定仍由学生确认。

## 外部专业能力

核心 Skill 保持轻量，只负责设计判断和任务编排。它会优先发现当前环境已安装的 Skill 或 MCP，再按设计目的移交任务：

| 需要 | 路由能力 |
|---|---|
| 当代案例、规范、政策、数据 | `research-current` |
| GIS、地图、遥感、空间统计 | `geospatial` |
| CAD、BIM、几何校核、参数化 | `cad-modeling` |
| 草图、视觉探索、效果图 | `visual` |
| 展板、PPT、PDF、报告 | `presentation-document` |

未安装相应外援时，教练会给出可复制的移交单、人工步骤与验收清单，不会假装已经完成计算、建模或制图。

## 专业与学术边界

- 不伪造场地调研、访谈、数据、引用、性能计算或规范结论。
- 不把某位大师的形式语言当作快捷键；大师可以借脑子，不能借脸。
- 不把外部工具输出自动当作设计结论。
- 不代替学生做关键作者性决定，不保证分数、获奖或规范合规。
- 默认不建立持久学生画像；只在当前对话中保持项目上下文。

## 仓库结构

```text
.
├── .codex-plugin/plugin.json
├── skills/spatial-design-coach/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── studio-workflow.md
│       ├── design-reasoning.md
│       ├── design-lenses.md
│       ├── critique-and-delivery.md
│       └── capability-routing.md
├── docs/
├── CONTEXT.md
└── LICENSE
```

运行时只按需加载当前问题用得上的 reference；产品、调研和测试文档不进入默认上下文。

## 文档与贡献

- 维护者文档：[`docs/README.md`](docs/README.md)
- 贡献规则：[`CONTRIBUTING.md`](CONTRIBUTING.md)
- 共同术语：[`CONTEXT.md`](CONTEXT.md)

欢迎提交真实设计课失败情境、行为测试、短小的方法改进与经过来源审查的设计透镜。

## License

[MIT License](LICENSE) © 2026 XiaoSiKe
