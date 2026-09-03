# 设计课无敌教练

> 从“我有个概念”到“老师问吧，我准备好了”。

`spatial-design-coach` 是面向建筑学、城乡规划和风景园林学生的开源 Agent Skill。学生把任务书、场地资料和已有成果放进一个独立作业沙盒，它会持续维护项目状态，推进概念、方案、平面、剖面、评图、展板、交图与答辩，并在截止前 72 小时内切换救火模式。

它会积极帮你把作业推进到一致、可提交、可讲清的状态，但不会替你伪造调研、计算、规范结论或完成关键作者性决定。“无敌”是给你打气，不是保证高分或获奖。

**English summary:** An open-source design-studio coach that helps architecture, urban planning, and landscape architecture students move from the project brief to a coherent, defensible submission.

当前发布版本：`0.6.0`

## 当你觉得“我不会做设计”

教练不会用“你很有天赋”敷衍你，也不会把一句打击性评价当成专业结论。它会先承认这轮卡住或评图受挫确实难受，再把“你这个人行不行”、反馈的表达方式和作品中真正可检验的问题分开，从一个足够小、可逆、有通过条件的动作重新开始。

辅导会由浅入深：先看清一个关系或矛盾，再画出一个空间动作，比较它的后果，最后把判断扩展到平面、剖面、系统和答辩。第一步可以小，证据标准不会降低。

```text
$spatial-design-coach 老师说我不会做设计，我现在也不知道从哪开始。请先帮我拆开评价和真实问题，再带我完成一个最小、可验证的下一步。
```

## 设计哲学与核心著作

本轮从维护者提供的 50 本专业参考书中甄选 **24 本**（建筑、城乡规划、风景园林各 8 本），另加入 **《庄子》选篇**。教练把著作中的问题意识连接到具体作业：怎样生活、为谁设计、如何对待环境，以及怎样在不确定中学习。

使用路径是：**来源观点 → 当前矛盾 → 学生的价值取舍 → 空间动作 → 验证与复盘**。例如，保留一处未规定用途的庭院，需要说明谁会使用、允许哪些变化、谁维护，以及与另一方案相比付出了什么代价。学生可以选择是否展开个人反思。

以下 25 项已形成[首轮原创方法卡](skills/spatial-design-coach/references/design-lenses.md)。**E** 表示已核读标明的原文节选或前言；**M** 表示依据书介、目录、书目或相关导读形成的方法原型，原著具体章节仍待核读。两者都不表示已读完整部著作，行为测试也不证明文献解释正确。具体版本、阅读范围与缺口见[来源地图](docs/research/source-map.md#selected-readings)。

| 编号 | 甄选著作 | 作者／主编 | 本轮记录 |
| --- | --- | --- | --- |
| B02 | [《建筑：形式、空间和秩序》](skills/spatial-design-coach/references/design-lenses.md#b02) | 程大锦 | 核心·M |
| B03 | [《建筑空间组合论》](skills/spatial-design-coach/references/design-lenses.md#b03) | 彭一刚 | 核心·M |
| B04 | [《建筑学教程1：设计原理》](skills/spatial-design-coach/references/design-lenses.md#b04) | 赫尔曼·赫茨伯格 | 核心·M |
| B06 | [《公共建筑设计原理》](skills/spatial-design-coach/references/design-lenses.md#b06) | 张文忠 | 核心·M |
| B10 | [《图解建筑结构：模式、体系与设计》](skills/spatial-design-coach/references/design-lenses.md#b10) | 程大锦等 | 核心·M |
| B17 | [《建筑的复杂性与矛盾性》](skills/spatial-design-coach/references/design-lenses.md#b17) | 罗伯特·文丘里 | 核心·E |
| B18 | [《建筑模式语言》](skills/spatial-design-coach/references/design-lenses.md#b18) | 克里斯托弗·亚历山大等 | 核心·M |
| B19 | [《场所精神：迈向建筑现象学》](skills/spatial-design-coach/references/design-lenses.md#b19) | 诺伯舒兹 | 核心·M |
| B21 | [《城市规划原理》](skills/spatial-design-coach/references/design-lenses.md#b21) | 吴志强、李德华 | 核心·M |
| B25 | [《城市设计》](skills/spatial-design-coach/references/design-lenses.md#b25) | 王建国 | 核心·M |
| B26 | [《详细规划》](skills/spatial-design-coach/references/design-lenses.md#b26) | 阳建强 | 核心·M |
| B27 | [《乡村规划原理》](skills/spatial-design-coach/references/design-lenses.md#b27) | 李京生 | 核心·M |
| B31 | [《城市意象》](skills/spatial-design-coach/references/design-lenses.md#b31) | 凯文·林奇 | 核心·M |
| B32 | [《美国大城市的死与生》](skills/spatial-design-coach/references/design-lenses.md#b32) | 简·雅各布斯 | 核心·M |
| B33 | [《交往与空间》](skills/spatial-design-coach/references/design-lenses.md#b33) | 扬·盖尔 | 核心·E |
| B35 | [《历史城市保护学导论》](skills/spatial-design-coach/references/design-lenses.md#b35) | 张松 | 核心·M |
| B37 | [《景观设计学：场地规划与设计手册》](skills/spatial-design-coach/references/design-lenses.md#b37) | 约翰·O·西蒙兹、巴里·W·斯塔克 | 核心·M |
| B39 | [《从概念到形式》](skills/spatial-design-coach/references/design-lenses.md#b39) | 格兰特·W·里德 | 核心·M |
| B41 | [《中国古典园林分析》](skills/spatial-design-coach/references/design-lenses.md#b41) | 彭一刚 | 核心·M |
| B42 | [《园冶注释》](skills/spatial-design-coach/references/design-lenses.md#b42) | 计成著，陈植注释 | 核心·M |
| B45 | [《设计结合自然》](skills/spatial-design-coach/references/design-lenses.md#b45) | 伊恩·麦克哈格 | 核心·M |
| B47 | [《植物造景》](skills/spatial-design-coach/references/design-lenses.md#b47) | 苏雪痕 | 核心·M |
| B49 | [《风景园林工程》](skills/spatial-design-coach/references/design-lenses.md#b49) | 孟兆祯 | 核心·M |
| B50 | [《城市绿地系统规划》](skills/spatial-design-coach/references/design-lenses.md#b50) | 许浩 | 核心·E |
| Z01 | [《庄子》选篇](skills/spatial-design-coach/references/design-lenses.md#z01) | 传统归于庄周及后学 | 哲学·E |

《庄子》选篇用于转换观察立场、认识实践中的限度、重新思考“有用”的评价标准；这些是本项目的教学转译。事实、任务书要求、技术验证和学生已确认的决定仍须成立。

<details>
<summary>其余 26 本专题参考书</summary>

保留原清单编号。以下尚未列入本轮核心蒸馏，按项目需要核验版本并选章研究；作者／主编沿用维护者提供的书目，具体版次另行核对。

| 编号 | 参考著作 | 作者／主编 | 本轮记录 |
| --- | --- | --- | --- |
| B01 | 《建筑初步》 | 田学哲、郭逊 | 专题参考 |
| B05 | 《图解思考：建筑表现技法》 | 保罗·拉索 | 专题参考 |
| B07 | 《住宅建筑设计原理》 | 龙灏等 | 专题参考 |
| B08 | 《建筑构造》上、下册 | 覃琳、翁季等 | 专题参考 |
| B09 | 《建筑物理》 | 柳孝图 | 专题参考 |
| B11 | 《建筑设计资料集》 | 中国建筑学会、中国建筑工业出版社组织编写 | 专题参考 |
| B12 | 《中国建筑史》 | 潘谷西 | 专题参考 |
| B13 | 《外国建筑史：十九世纪末叶以前》 | 陈志华 | 专题参考 |
| B14 | 《外国近现代建筑史》 | 罗小未 | 专题参考 |
| B15 | 《华夏意匠：中国古典建筑设计原理分析》 | 李允鉌 | 专题参考 |
| B16 | 《走向新建筑》 | 勒·柯布西耶 | 专题参考 |
| B20 | 《总体设计》 | 凯文·林奇、加里·海克 | 专题参考 |
| B22 | 《国土空间规划原理》 | 吴志强 | 专题参考 |
| B23 | 《中国城市建设史》 | 董鉴泓 | 专题参考 |
| B24 | 《外国城市建设史》 | 沈玉麟 | 专题参考 |
| B28 | 《城市道路与交通规划》上、下册 | 徐循初 | 专题参考 |
| B29 | 《城市工程系统规划》 | 戴慎志 | 专题参考 |
| B30 | 《城市与区域规划空间分析实验教程》 | 尹海伟、孔繁花 | 专题参考 |
| B34 | 《城市更新理论与方法》 | 阳建强 | 专题参考 |
| B36 | 《风景园林概论》 | 丁绍刚 | 专题参考 |
| B38 | 《风景园林设计要素》 | 诺曼·K·布思 | 专题参考 |
| B40 | 《中国古典园林史》 | 周维权 | 专题参考 |
| B43 | 《西方园林史：19世纪之前》 | 朱建宁、赵晶 | 专题参考 |
| B44 | 《西方现代景观设计的理论与实践》 | 王向荣、林箐 | 专题参考 |
| B46 | 《景观生态学：格局、过程、尺度与等级》 | 邬建国 | 专题参考 |
| B48 | 《园林树木学》 | 陈有民 | 专题参考 |

</details>

## 最简单的安装方式：把这句话发给 Codex

复制下面整段发送给 Codex：

```text
请使用 $skill-installer 从下面的 GitHub 地址安装 spatial-design-coach：
https://github.com/XiaoSiKe/spatial-design-coach/tree/main/skills/spatial-design-coach

请安装完整 Skill 目录，保留 agents/、references/、scripts/ 和 assets/。完成后告诉我安装路径，并提醒我在新任务中用 $spatial-design-coach 做一次验证。
```

这条路径适用于带 GitHub Skill 安装能力的 Codex。其他 AI 客户端是否能直接安装，取决于它是否支持 [Agent Skills 规范](https://agentskills.io/specification) 或自己的 Skill 安装器；只说“安装这个仓库”并不是所有客户端都保证理解的通用命令。

## 命令行安装

需要本机已安装 Node.js 与 `npx`：

```bash
npx skills add XiaoSiKe/spatial-design-coach \
  --skill spatial-design-coach \
  --global \
  --agent codex \
  --yes
```

该命令明确选择本仓库中的 `spatial-design-coach`，并安装到 Codex 的用户级 Skill 位置。

## 手动安装

```bash
git clone https://github.com/XiaoSiKe/spatial-design-coach.git
mkdir -p ~/.agents/skills
cp -R spatial-design-coach/skills/spatial-design-coach ~/.agents/skills/
```

必须复制整个 `skills/spatial-design-coach/`，不要只复制 `SKILL.md`；否则会丢失界面元数据、参考文档、沙盒初始化脚本和项目模板。

## 安装后验证

1. 新建一个 Codex 任务；如果 Skill 没出现，完全重启 Codex。
2. 输入 `/skills`，确认列表中有“设计课无敌教练”。
3. 在一个临时空目录运行一次最小验证：

```text
$spatial-design-coach 开始这个设计作业。当前目录是可写测试沙盒，请初始化项目状态，但不要改动目录外的文件。
```

通过表现应当是：只创建 `studio/PROJECT.md`、`studio/outputs/working/` 和 `studio/outputs/final/`；再次运行时进入续作而不覆盖 `PROJECT.md`。

## 三步开始一个设计作业

1. 为这一次课程作业创建独立目录，不要直接使用主目录或整个硬盘根目录。
2. 把任务书、评分表、场地资料、图纸导出、模型截图和教师反馈放进该目录；CAD／BIM／Rhino／GIS 原生文件最好同时提供 PDF、PNG 或 SVG 导出。
3. 在这个目录中打开 Codex，输入：

```text
$spatial-design-coach 开始这个设计作业。请读取任务书和已有成果，建立沙盒项目状态，并告诉我当前最关键的设计矛盾和下一步 Artifact。
```

教练只管理当前作业中的 `studio/` 目录：

```text
studio/
├── PROJECT.md
└── outputs/
    ├── working/
    └── final/
```

- `PROJECT.md` 是任务书、决定、假设、Artifact、必交成果和下一步的唯一项目状态。
- `working/` 保存派生和外援产物；已有目录使用 `-v2` 等新版本，不覆盖。
- `final/` 只保存已确认任务书要求、项目版本和文件 QA 的最终提交文件。
- 学生原始任务书、图纸、模型、照片和数据不会被重命名、重排或覆盖。
- 只读环境会自动降级为聊天状态，并输出可复制续航快照。

## 更新 Skill

GitHub 仓库更新后，用户已经安装的本地副本不会自动变化。使用 `npx skills` 全局安装的版本可这样更新：

```bash
npx skills update spatial-design-coach --global --yes
```

项目级安装使用：

```bash
npx skills update spatial-design-coach --project --yes
```

更新完成后新建一个 Codex 任务；如果新任务仍未发现新版，完全重启 Codex。已经打开的任务可能仍保留更新前加载的 Skill 上下文。

`npx skills list --global --json` 可确认安装范围和 GitHub 来源；运行时版本以完整 Skill 中 `SKILL.md` 的 `metadata.version` 为准。手动复制安装没有可靠的来源记录，更新时应先备份原目录，再用最新 Release 的完整 `skills/spatial-design-coach/` 替换，而不是只覆盖 `SKILL.md`。

### 已有设计作业不会被自动迁移

更新 Skill 不会覆盖已有 `studio/PROJECT.md`。在作业目录先只读检查兼容性：

```bash
python3 ~/.agents/skills/spatial-design-coach/scripts/migrate_project.py \
  --root . \
  --check \
  --json
```

只有确认需要迁移并同意写入时才运行：

```bash
python3 ~/.agents/skills/spatial-design-coach/scripts/migrate_project.py \
  --root . \
  --apply \
  --json
```

迁移只更新 `studio/PROJECT.md` 的状态元数据，写入前创建不覆盖的备份，不修改学生原始任务书、图纸、模型、照片或数据。安装路径不在 `~/.agents/skills/` 时，应改用 `npx skills list --global --json` 返回的实际路径。

### 常见问题

- **安装后当前对话没有生效：** 新建任务或重启 Codex；已开始的任务可能仍使用旧上下文。
- **更新命令找不到来源：** 这通常是手动复制安装；备份后重新安装完整 Skill，并优先改用 `npx skills add` 保留 GitHub 来源。
- **老项目显示 `legacy`：** 代表缺少状态 schema，不代表作业损坏；先审阅检查结果，再明确决定是否执行迁移。
- **显示 `future-schema`：** 当前 Skill 旧于项目状态格式；不要写入项目状态，先更新 Skill。
- **只看到了 `SKILL.md`：** 重新安装完整目录，确认 `agents/` 和 `references/` 都存在。
- **`/spatial-design-coach` 无效：** 它不是自定义斜杠命令；使用 `/skills` 选择或在消息中写 `$spatial-design-coach`。
- **名称出现两次：** 检查是否同时在项目级和用户级安装了同名 Skill；Codex 不会自动合并同名副本。

仓库同时包含 Codex Plugin manifest，但当前没有提交公共 Plugin Directory；学生本地使用优先采用上述独立 Skill 安装路径。

## 八种直接用法

| 你现在要做什么 | 最好提供 | 教练会交付 |
| --- | --- | --- |
| 解读任务书 | 任务书或课程要求 | 项目状态、硬性要求、隐藏矛盾、第一步 |
| 把概念落到空间 | 概念、草图、平面或老师质疑 | 可检验命题、空间机制、验证图纸 |
| 处理分析、案例和理论 | 当前决定与已有资料 | 证据链、迁移条件、待核验项 |
| 生成真正不同的方案 | 已锁定要求和当前命题 | 2–3 个机制与价值取舍不同的方案家族 |
| 深化空间 | 平面、剖面、模型或系统描述 | 尺度、关系、序列、流线和通过条件 |
| 评图或拆老师反馈 | 当前成果和反馈原文 | 主导矛盾、后果、修复动作、复评 Artifact |
| 截止期救火 | 截止时间、必交成果、当前源文件 | 最低完整交付、共享源图、QA／答辩三组工作包 |
| 做展板、汇报和答辩 | 格式要求与当前成果集 | 叙事、每张图的任务、文件检查、模拟质疑 |

### 示例：在沙盒从任务书开始

```text
$spatial-design-coach 开始这个设计作业。请读取沙盒中的课程任务书和现有图纸，建立 PROJECT.md，并给我这周最重要的 3 个动作。
```

### 示例：带现有方案评图

```text
$spatial-design-coach 这是我的总图、两张剖面和上次评图意见。请别先美化，先找概念、空间和表达之间最致命的一处断裂。
```

### 示例：截止期救火

```text
$spatial-design-coach 还有 36 小时交图。请进入救火模式，区分已确认、暂定和未知的必交成果，冻结主线并排出最低完整交付路径。
```

### 示例：保存进度到新对话

```text
$spatial-design-coach 请把当前项目状态导出为“项目续航快照”，让我在新对话继续。
```

## 两种辅导模式

- **成长模式**（默认）：通过提问、对比、反例、评图和迁移练习训练设计判断，逐步减少对教练的依赖。
- **救火模式**：学生明确表示紧急，或截止时间不超过 72 小时时启用。先保最低完整成果和共享源图，再统一表达、检查文件和准备答辩。

救火不是代做。教练会给更直接的工作路径，也可以调用环境中已有的制作能力，但关键设计决定和最终提交责任仍属于学生。

## 外部专业能力

核心 Skill 负责设计判断、项目状态和任务编排。需要实际检索、分析或制作时，它会优先发现当前环境已经安装的 Skill／MCP：

| 需要 | 路由能力 |
| --- | --- |
| 当代案例、规范、政策、数据 | `research-current` |
| GIS、地图、遥感、空间统计 | `geospatial` |
| CAD、BIM、几何校核、参数化 | `cad-modeling` |
| 草图、视觉探索、效果图 | `visual` |
| 展板、PPT、PDF、报告 | `presentation-document` |

外援必须收到当前项目状态、已锁定决定、待验证项和验收标准。返回后由教练检查它支持或推翻了什么；外部工具不能静默重设计项目。没有合适外援时，教练会给可复制移交单、人工步骤和验收清单，不假装已经完成文件或计算。

## 专业、隐私与学术边界

- 不伪造场地调研、访谈、数据、引用、规范、性能计算或完成文件。
- 不把某位大师的外观当快捷键；大师可以借脑子，不能借脸。
- 不把 AI 或外部工具输出自动宣布为设计结论。
- 不代替学生确认关键立场，不保证分数、获奖、审批或规范合规。
- 用户明确要求在当前可写作业沙盒开始或管理项目时，使用 `studio/PROJECT.md` 保存状态；未触发、只读或禁止写入时使用会话状态和续航快照。
- 课程要求时可生成 AI 协作记录，但仍需按课程自己的规定披露。

## 仓库结构

```text
.
├── .codex-plugin/plugin.json
├── skills/spatial-design-coach/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/PROJECT.template.md
│   ├── scripts/
│   │   ├── init_project.py
│   │   └── migrate_project.py
│   └── references/
│       ├── project-state.md
│       ├── studio-workflow.md
│       ├── design-reasoning.md
│       ├── design-lenses.md
│       ├── contemporary-challenges.md
│       ├── studio-standard.md
│       ├── critique-and-delivery.md
│       └── capability-routing.md
├── tests/evals/
├── scripts/
├── docs/
├── CONTEXT.md
└── LICENSE
```

运行时只按当前任务加载相关 reference；产品、研究、测试和维护脚本不会进入学生默认上下文。

## 文档与贡献

- 维护者文档：[`docs/README.md`](docs/README.md)
- 贡献规则：[`CONTRIBUTING.md`](CONTRIBUTING.md)
- 共同术语：[`CONTEXT.md`](CONTEXT.md)

欢迎提交经过授权和去标识化的真实失败情境、行为测试、短小的方法改进，以及完成来源与许可证审查的设计研究。

## License

[MIT License](LICENSE) © 2026 XiaoSiKe
