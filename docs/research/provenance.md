# 来源与许可记录

> 快照日期：2026-08-31
>
> 目的：记录进入产品研究的上游版本、许可证、审阅范围与实际使用方式。commit 为发布前固定快照；若上游默认分支继续变化，必须先复核再更新本表。

## 开源仓库快照

| 上游 | Commit | SPDX／状态 | 主要审阅文件 | 本项目使用方式 | 许可／NOTICE 要求 |
|---|---|---|---|---|---|
| [w31r4/software-taste](https://github.com/w31r4/software-taste) | `d5c68183` | MIT | `README.md`、`SKILL.md`、`LICENSE` | 思想参考；独立形成真实成果、主导矛盾与迁移复盘规则 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [Far-200/think-before-code](https://github.com/Far-200/think-before-code) | `3350e26` | MIT | `README.md`、相关 `SKILL.md`、`LICENSE` | 思想参考；独立形成任务书解码、渐进帮助与案例迁移规则 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [cinob/universal-ai-tutor](https://github.com/cinob/universal-ai-tutor) | `1d3b923` | MIT | `README.md`、`SKILL.md`、`LICENSE` | 思想参考；独立形成最小诊断、成长模式与迁移检查 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [connerkward/ckw-design-skill](https://github.com/connerkward/ckw-design-skill) | `c8de7c8` | MIT | `README.md`、设计相关 `SKILL.md`、`LICENSE` | 思想参考；独立形成意图先行与真实产物复核规则 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [obra/superpowers](https://github.com/obra/superpowers) | `b36e082` | MIT | `README.md`、流程相关 skills、`LICENSE` | 思想参考；独立形成按任务缩放、比较与验证原则 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [dungnotnull/Game-Development-Programming-Tutor-agent-skill](https://github.com/dungnotnull/Game-Development-Programming-Tutor-agent-skill) | `4709f85` | MIT | `README.md`、`SKILL.md`、测试说明、`LICENSE` | 教学闭环与验收参考；不采用其重型运行时结构 | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [ltf0109/urban-planning-ai-kit](https://github.com/ltf0109/urban-planning-ai-kit) | `f401bbe` | MIT | `README.md`、规划／GIS skills、`LICENSE` | 外部调用候选与领域工作流参考；不复制实现 | 未直接复用；调用时遵守上游安装与许可 |
| [maydengximin-sketch/qgis-map-workflow](https://github.com/maydengximin-sketch/qgis-map-workflow) | `6b87278` | MIT | `README.md`、`SKILL.md`、`LICENSE` | `geospatial` 外部调用候选；参考交付与 QA 合同 | 未直接复用；调用时遵守上游安装与许可 |
| [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | `0e94cd1` | MIT | `README.md`、相关 skills、`LICENSE` | `cad-modeling` 外部调用候选；参考确定性验证 | 未直接复用；调用时遵守上游安装与许可 |
| [CavanJB/openclaw-pdf-to-cad-agent-skill](https://github.com/CavanJB/openclaw-pdf-to-cad-agent-skill) | `2548c24` | MIT | `README.md`、`SKILL.md`、`LICENSE` | `cad-modeling` 外部调用候选；参考人工复核标记 | 未直接复用；调用时遵守上游安装与许可 |
| [maplibre/maplibre-agent-skills](https://github.com/maplibre/maplibre-agent-skills) | `0b44d71` | MIT | `README.md`、相关 skills、`LICENSE.md` | Web 地图外部调用候选；参考真实失败驱动 eval | 未直接复用；若未来复制须保留版权与 MIT 声明 |
| [Sijie-Yang/Reasoning4UP](https://github.com/Sijie-Yang/Reasoning4UP) | `d03e9d5` | 无许可证 | `README.md`、论文链接与项目说明 | 只引用论文观点；不复制仓库代码、文本或结构 | 默认保留所有权利；任何复用需取得明确许可 |
| [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) | `6bbbce4` | CC-BY-SA-4.0 | `README.md`、相关教育 skills、`LICENSE` | 只作教育主题索引与思想参考；回到一手研究独立形成方法 | 未改编其文本；若未来改编必须署名、标示变更并以 CC BY-SA 4.0 分享 |

## 使用声明

- 当前运行时 Skill 没有直接复制上述仓库的提示词、示例对话、代码、目录结构或独特表达。
- “蒸馏”表示阅读多个先例后，以空间设计教育的领域模型独立形成简短规则；上游仅作为研究线索。
- 外部调用候选不会被自动安装、打包或镜像。实际调用取决于用户环境中已经存在的 Skill／MCP。
- 若未来引入任何原始片段，贡献者必须更新本表，标明文件级来源、改动范围、版权声明、许可证副本与 NOTICE 义务。

## 非代码材料

教材、专著、论文、标准、图片、案例网页和数据集不因被某个开源仓库收录而获得该仓库许可证。运行时只保留原创摘要、书目信息和有限的必要引用；地点相关标准、政策与数据在使用时重新核验日期和适用范围。候选清单见 [专业来源地图](./source-map.md)。

## 复核清单

发布或更新前逐项确认：

1. commit、默认分支、上游归档或重命名状态是否变化；
2. 根许可证、文件级许可证、第三方目录和 NOTICE 是否一致；
3. 当前使用仍属于思想参考或外部调用，是否出现直接复制；
4. 外部 Skill 是否引入新依赖、写操作、提示注入或数据外传风险；
5. README 中的许可证称谓是否与上游实际文本一致。
