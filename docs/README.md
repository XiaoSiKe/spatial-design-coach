# 维护者文档

本目录记录“设计课无敌教练”的产品边界、关键决策、研究依据与验收方法。运行时 Skill 不读取 `docs/`；学生使用说明位于仓库根目录 `README.md`。

## 项目身份

- Skill slug：`spatial-design-coach`
- 中文显示名：设计课无敌教练
- 英文显示名：Spatial Design Coach
- 版本：`0.1.0`
- 许可证：MIT
- 服务对象：建筑学、城乡规划、风景园林及相关空间设计学习者

## 权威文档

| 文档 | 唯一职责 |
|---|---|
| [产品需求](./product/prd.md) | 产品目标、工作流、行为要求、边界与用户故事 |
| [名称与语气](./product/voice.md) | 显示名称、简介、欢迎语和表达边界 |
| [轻量核心与能力路由决策](./decisions/0001-lightweight-core-and-capability-routing.md) | 解释为何核心保持轻量，以及怎样移交专业能力 |
| [开源先例](./research/open-source-prior-art.md) | 同类项目比较和吸收／调用策略 |
| [来源地图](./research/source-map.md) | 专业标准、教材、理论、当代议题和案例研究池 |
| [来源与许可记录](./research/provenance.md) | 上游版本、许可证、审阅范围和使用方式 |
| [验收情境](./testing/acceptance-scenarios.md) | 正负触发与十二个端到端行为测试 |
| [首轮需求访谈](./archive/discovery-questions.md) | 30 个问题及其决策轨迹，仅供追溯 |

项目共同术语以根目录 [CONTEXT.md](../CONTEXT.md) 为准。

## 内容归属

- 会改变每次辅导行为的规则放在运行时 `SKILL.md` 或其五个 `references/` 中。
- 产品事实只在 [产品需求](./product/prd.md) 维护，架构取舍只在 ADR 解释。
- 文献、仓库、许可和来源更新只放在 `research/`。
- 历史访谈只保留在 `archive/`，不得作为当前实现要求。
- GIS、空间分析、CAD、建模、图像和演示能力由外部 Skill／MCP 完成，不复制到本仓库。

## 维护规则

1. 修改运行时行为时，同步补充一个可观察的验收情境。
2. 新增理论或开源先例时，先在来源记录中确认出处、版本与许可。
3. 不用版本后缀创建重复文档；发布版本由 Git tag 管理。
4. 不把受版权保护的正文、第三方提示词或外部 Skill 镜像纳入核心。
