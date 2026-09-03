# 维护者文档

本目录记录“设计课无敌教练”的产品边界、关键决策、研究依据与验收方法。运行时 Skill 不读取 `docs/`；学生使用说明位于仓库根目录 `README.md`。

## 项目身份

- Skill slug：`spatial-design-coach`
- 中文显示名：设计课无敌教练
- 英文显示名：Spatial Design Coach
- 版本：`0.6.1`
- 许可证：MIT
- 服务对象：建筑学、城乡规划、风景园林及相关空间设计学习者

## 权威文档

| 文档 | 唯一职责 |
|---|---|
| [产品需求](./product/prd.md) | 产品目标、工作流、行为要求、边界与用户故事 |
| [名称与语气](./product/voice.md) | 显示名称、简介、欢迎语、支持式表达和语气边界 |
| [ADR-0001：轻量核心与能力路由](./adr/0001-lightweight-core-and-capability-routing.md) | 解释为何核心保持轻量，以及怎样移交专业能力 |
| [ADR-0002：Deep 项目状态与评测驱动演进](./adr/0002-deep-project-state-and-eval-driven-evolution.md) | 解释统一项目状态与评测驱动演进 |
| [ADR-0003：单作业沙盒与文件化项目状态](./adr/0003-assignment-sandbox-and-file-backed-state.md) | 解释 `studio/PROJECT.md`、原始文件保护和只读降级 |
| [ADR-0004：Skill 更新与项目状态迁移](./adr/0004-skill-updates-and-project-state-migration.md) | 解释本地更新、版本源、任务刷新和显式项目迁移 |
| [开源先例](./research/open-source-prior-art.md) | 同类项目比较和吸收／调用策略 |
| [来源地图](./research/source-map.md) | 专业标准、25 项入选来源的阅读范围、当代议题与案例研究 |
| [来源与许可记录](./research/provenance.md) | 上游版本、许可证、审阅范围和使用方式 |
| [验收情境](./testing/acceptance-scenarios.md) | 30 个端到端行为的可观察验收标准 |
| [`tests/evals/`](../tests/evals/) | 30 个单轮案例、9 个 journey、6 个 studio packet 与运行方法 |
| [首轮需求访谈](./archive/discovery-questions.md) | 30 个问题及其决策轨迹，仅供追溯 |

项目共同术语以根目录 [CONTEXT.md](../CONTEXT.md) 为准。

## 运行时与文档关系

| 改动类型 | 权威实现 | 必须同步 |
|---|---|---|
| 名称、简介、欢迎语与支持式表达 | [`product/voice.md`](./product/voice.md) | `agents/openai.yaml`、Plugin manifest、`SKILL.md` 欢迎语、SDC-001／013 与 JRN-001 |
| 辅导入口与路由 | [`SKILL.md`](../skills/spatial-design-coach/SKILL.md) | 对应 runtime reference 和行为 case／journey |
| 项目状态与决定 | [`project-state.md`](../skills/spatial-design-coach/references/project-state.md) | 项目模板、ADR-0002／0003、状态 journey |
| Skill 更新与项目迁移 | `SKILL.md` 元数据、`migrate_project.py` | Plugin 版本、项目模板、ADR-0004、README 与迁移单测 |
| 阶段、推理与交付 | `studio-workflow.md`、`design-reasoning.md`、`studio-standard.md`、`critique-and-delivery.md` | 产品需求与对应行为评测 |
| 理论与当代议题 | `design-lenses.md`、`contemporary-challenges.md` | README 书目选择、来源地图的实际阅读范围、provenance 与行为评测 |
| 外部专业能力 | [`capability-routing.md`](../skills/spatial-design-coach/references/capability-routing.md) | ADR-0001 与 Adapter case／journey |
| 发布与测试 | `tests/evals/`、`scripts/`、CI | [验收情境](./testing/acceptance-scenarios.md) 与版本元数据 |

产品事实只在 [产品需求](./product/prd.md) 维护，架构取舍只在 ADR 解释，项目共同术语以根目录 [CONTEXT.md](../CONTEXT.md) 为准。历史访谈仅供追溯，不是当前要求。GIS、CAD、建模、图像和演示实现保持为外部 Skill／MCP，不复制进核心。

初始化和迁移脚本共用运行时内部模块 [`_project_paths.py`](../skills/spatial-design-coach/scripts/_project_paths.py)，统一检查沙盒路径、符号链接和文件类型。仓库评测执行器与发布检查共用 [`_eval_contract.py`](../scripts/_eval_contract.py) 的队列、覆盖关系和汇总规则；它不进入运行时 Skill。仓库验证器集中枚举源文件，排除本地报告、依赖和缓存目录。

## 维护规则

1. 修改运行时行为时，同步更新相应单轮 case 或多轮 journey，并在涉及图纸时更新合成 studio packet。
2. 新增理论或开源先例时，先在来源记录中确认出处、版本与许可。
3. 不用版本后缀创建重复文档；发布版本由 Git tag 管理。
4. 不把受版权保护的正文、第三方提示词或外部 Skill 镜像纳入核心。
5. 运行 `python3 scripts/validate_repo.py`，确认元数据、欢迎语、评测数量和文档链接没有漂移。
6. 发布版本时同步 Skill、Plugin、产品基线和模板版本；项目 schema 只在状态结构不兼容时递增。
