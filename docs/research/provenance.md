# 来源与许可记录

> 开源仓库快照日期：2026-08-31；产品文档复核日期：2026-09-02
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
| [Aaa2122/QGIS-MCP](https://github.com/Aaa2122/QGIS-MCP) | `43fd99d2` | MIT | `README.md`、MCP／QGIS 工作流、`LICENSE` | 地理空间外部调用候选；未进入 runtime | 调用前另行检查依赖、写操作和数据路径 |
| [CartoDB/agent-skills](https://github.com/CartoDB/agent-skills) | `bdc12fe7` | MIT | `README.md`、空间分析 skills、`LICENSE` | CARTO 环境中的外部调用候选 | 未复制；使用时遵守上游依赖和许可 |
| [JB-Rockstar/landscape-architecture-ai](https://github.com/JB-Rockstar/landscape-architecture-ai) | `6f9f7a0f` | 无许可证 | 仓库根与项目说明 | 排除：没有可审阅的有效实现 | 默认保留所有权利，不复制 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `f6fcafeb` | MIT | `README.md`、`geomaster` 相关 skill、`LICENSE` | 已安装时作为大型科学／地理空间外援 | 不镜像大型能力库；调用时复核依赖 |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | `1b875933` | Apache-2.0 | `README.md`、扫描范围、`LICENSE` | 发布安全工具参考，不作为内容来源 | 若复制须保留 Apache-2.0 与 NOTICE；当前未复制 |
| [TEC413/qgis-with-claude](https://github.com/TEC413/qgis-with-claude) | `b15bf5c9` | MIT | `README.md`、QGIS skill、`LICENSE` | 轻量 QGIS 外部调用候选 | 未复制；调用前验证兼容性和写入范围 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | `5e1f3aeb` | MIT（聚合仓库） | `README.md`、目录索引、`LICENSE` | 仅用于发现上游 | 聚合许可不覆盖链接或镜像的上游内容 |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | `69ef37e9` | Apache-2.0；文档 CC-BY-4.0 | 规范、`skills-ref`、许可证 | 结构与兼容验证的规范来源 | 未复制规范文本；引用时按文件级许可 |
| [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) | `9224fe33` | MIT | `README.md`、MCP 配置、`LICENSE` | 三维制作外援候选 | 不将三维制作等同于设计判断；未复制 |
| [anthropics/skills](https://github.com/anthropics/skills) | `3b3fad96` | 文件级混合许可 | 根 README、设计与文档 skills、文件级许可 | 复杂 Skill 结构与视觉／文档能力参考 | 每个目录单独核验；source-available 内容不作为开源复用 |
| [dongwoosuk/rhino-grasshopper-mcp](https://github.com/dongwoosuk/rhino-grasshopper-mcp) | `cefb1de4` | MIT | `README.md`、MCP 实现、`LICENSE` | Rhino／Grasshopper 外部建模候选 | 未复制；调用前核对本地软件与安全范围 |
| [gmakstutis/qWiki](https://github.com/gmakstutis/qWiki) | `52f7d1e9` | MIT（仓库代码） | `README.md`、知识组织、`LICENSE` | 仅参考知识组织方式 | MIT 不重新授权其中书籍、图片与第三方材料 |
| [myloveql/urban-planning-ai-copilot](https://github.com/myloveql/urban-planning-ai-copilot) | `cae3a79f` | MIT | `README.md`、应用路由、`LICENSE` | 仅参考规划任务路由；不是 Skill 依赖 | 未复制完整应用或数据源 |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | `7163c3e1` | MIT | `README.md`、Skill 结构、`LICENSE` | `visual`／`presentation-document` 外援候选 | 未复制；生成物仍需单独检查版权 |
| [nkarasiak/qgis-mcp](https://github.com/nkarasiak/qgis-mcp) | `75499a7b` | GPL-2.0 | `README.md`、MCP 实现、`LICENSE` | 独立进程中的 QGIS 外援候选 | 不复制或打包进 MIT 核心 |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | `c91369c4` | AGPL-3.0 | `README.md`、PPT Skill、`LICENSE` | 独立演示制作外援候选 | 不复制或并入 MIT 核心；网络使用遵守 AGPL |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | `d91ed427` | MIT（聚合仓库） | `README.md`、目录索引、`LICENSE` | 仅用于发现上游 | 聚合许可不覆盖被镜像或链接内容 |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | `5de7275f` | MIT | `README.md`、Skill 结构、`LICENSE` | 系统关系图外援候选 | 未复制；不把软件架构语义机械转为空间语义 |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | `435076e7` | MIT | `README.md`、安装发现逻辑、`LICENSE` | `npx skills` 安装、发现与 smoke test | 未复制实现；README 只引用公开命令 Interface |

## 产品文档

| 来源 | 复核日期 | 范围 | 本项目使用方式 | 复制情况 |
|---|---|---|---|---|
| [OpenAI Skills API](https://developers.openai.com/api/reference/go/resources/skills) | 2026-09-02 | Skill、默认版本与不可变版本资源 | 仅用于区分托管 API 版本和本地 GitHub 安装更新边界 | 未复制正文或示例代码 |
| `npx skills` 本机 CLI `update --help`／`list --global --json` | 2026-09-02 | 全局／项目更新参数、安装来源字段 | 验证 README 中本地更新命令和来源检查方式 | 仅记录公开命令 Interface |

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
