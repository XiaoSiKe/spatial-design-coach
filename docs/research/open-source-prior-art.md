# 开源先例与整合策略

> 调研日期：2026-08-31
>
> 用途：维护者研究，不随运行时 Skill 默认加载。上游版本与许可证快照见 [来源与许可记录](./provenance.md)。

## 结论

尚未发现一个开源 Agent Skill 同时覆盖以下能力：

1. 面向建筑学、城乡规划与风景园林学生；
2. 从项目任务书到方案、成果和答辩；
3. 训练设计判断与跨尺度综合；
4. 在现实截止时间内推进作业，同时保护学生作者性；
5. 保持轻量，并把专业制作交给外部能力。

最接近的先例分散在三类：教学教练、空间技术、成果交付。“设计课无敌教练”的原创工作是连接三类能力：核心训练并推进设计，外援执行专业任务，结果返回后再由核心解释其设计意义。

## 处理词汇

| 处理 | 含义 |
|---|---|
| 蒸馏 | 阅读先例后独立总结通用原则，以本项目语言重新设计行为；不复制提示词、示例、代码或独特表达 |
| 调用 | 把已经成熟的专业能力保留为外部 Skill／MCP，运行时发现后按统一合同移交 |
| 参考 | 只研究论文、架构、测试方法或案例，不把仓库内容放进运行时 |
| 排除 | 缺少有效内容、许可不明且没有独特价值，或方向与空间设计辅导无关 |

仓库公开可读不等于允许复制；仓库许可证也不自动覆盖其中的论文、书籍、图片、数据和第三方文件。

## 教学与设计判断

| 项目 | 类型 | 可借鉴内容 | 决定 |
|---|---|---|---|
| [w31r4/software-taste](https://github.com/w31r4/software-taste) | 单 Skill | 从学习者真实作品出发，一次聚焦高价值矛盾，用冲突思想训练判断 | 蒸馏为“真实成果优先、主导矛盾、设计透镜、迁移复盘” |
| [Far-200/think-before-code](https://github.com/Far-200/think-before-code) | Skill 套件 | 问题解码、概念解释、模式迁移、先由学习者表达 | 蒸馏为“任务书解码、自己的话、适用与失效条件” |
| [cinob/universal-ai-tutor](https://github.com/cinob/universal-ai-tutor) | 单 Skill | 最小入门诊断、渐退式辅导、独立完成与迁移检查 | 蒸馏为“少问高价值问题、成长模式、迁移检查” |
| [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) | 教育 Skill 集合 | 卡点诊断、渐进提示、形成性反馈、项目学习、自我解释 | CC BY-SA 4.0；只参考教育方法和其一手来源，不直接改编进 MIT 核心 |
| [connerkward/ckw-design-skill](https://github.com/connerkward/ckw-design-skill) | 设计 Skill 套件 | 先明确意图和领域语言；生成后查看真实结果再批评 | 蒸馏为“意图先行、实际成果复核”，不引入前端专用规则 |
| [obra/superpowers](https://github.com/obra/superpowers) | Skill 框架 | 按任务复杂度缩放流程、比较方向、写清取舍、验证后推进 | 蒸馏轻量流程，不复制框架或命令体系 |
| [dungnotnull/Game-Development-Programming-Tutor-agent-skill](https://github.com/dungnotnull/Game-Development-Programming-Tutor-agent-skill) | 重型教学 Skill | 诊断、里程碑、脚手架与行为测试 | 参考教学闭环；不引入多代理、注册表或复杂 schema |

这些项目共同支持一条教学原则：先看学生做了什么，再判断卡在哪里；帮助应逐级增加，理解形成后才替换为具体动作。空间设计版本必须额外处理场地、尺度、时间、材料、生态、社会价值和成果表达。

## 建筑、规划、景观与空间技术

| 项目 | 类型 | 适合任务 | 集成方式 |
|---|---|---|---|
| [ltf0109/urban-planning-ai-kit](https://github.com/ltf0109/urban-planning-ai-kit) | 规划空间 Skill 套件 | 规划证据、坐标、选址、MCDA、QGIS | 调用／参考；核心只保留“分析必须返回设计后果” |
| [Sijie-Yang/Reasoning4UP](https://github.com/Sijie-Yang/Reasoning4UP) | 论文项目 | 规划 AI 的感知、基础、推理与分析／生成／验证／评价／协作／决策框架 | 无许可证；只引用论文思想，不复制仓库内容 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 科研 Skill 集合 | `geomaster` 的 GIS、遥感、空间统计和数据源 | 已安装时调用，不复制大型能力库 |
| [maplibre/maplibre-agent-skills](https://github.com/maplibre/maplibre-agent-skills) | 地图 Skill 集合 | Web 地图、图层、标注、字体、瓦片与制图 | 调用；参考由真实失败情境驱动 eval 的方法 |
| [CartoDB/agent-skills](https://github.com/CartoDB/agent-skills) | 地理空间 Skill 集合 | 热点、空间自相关、GWR、选址、服务区、复合评分 | CARTO 环境中调用，核心保持供应商无关 |
| [TEC413/qgis-with-claude](https://github.com/TEC413/qgis-with-claude) | QGIS Skill | CLI 计算、MCP 管理实时工程、截图反馈 | 轻量 QGIS 外援，调用前复核环境与许可 |
| [maydengximin-sketch/qgis-map-workflow](https://github.com/maydengximin-sketch/qgis-map-workflow) | QGIS Skill | 数据到可编辑 `.qgz` 与出版级地图，含 QA | 优先作为地图交付外援之一 |
| [nkarasiak/qgis-mcp](https://github.com/nkarasiak/qgis-mcp) | QGIS MCP | 控制 QGIS Desktop | GPL 工具保持独立进程，只在用户环境已安装时调用 |
| [Aaa2122/QGIS-MCP](https://github.com/Aaa2122/QGIS-MCP) | QGIS MCP | QGIS 工具与可恢复视觉工作流 | 可选工具层；使用前单独验证安全与兼容性 |
| [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | CAD Skill 集合 | brief、几何生成、测量、确定性检查和快照复核 | CAD 外援；蒸馏“目的—产物—验证”交付逻辑 |
| [CavanJB/openclaw-pdf-to-cad-agent-skill](https://github.com/CavanJB/openclaw-pdf-to-cad-agent-skill) | 单 Skill | PDF 工程图转 CAD，标记 `needs_review` | 按需调用；蒸馏“不确定即人工复核” |
| [dongwoosuk/rhino-grasshopper-mcp](https://github.com/dongwoosuk/rhino-grasshopper-mcp) | MCP | Rhino／Grasshopper 参数化建模 | 外部建模能力，不进入核心 |
| [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) | MCP | Blender 三维制作 | 外部视觉／建模能力，不等同于设计判断 |
| [myloveql/urban-planning-ai-copilot](https://github.com/myloveql/urban-planning-ai-copilot) | 完整应用 | 规划图解析、用地、POI、产业与知识问答 | 参考任务路由，不作为 Skill 依赖 |
| [JB-Rockstar/landscape-architecture-ai](https://github.com/JB-Rockstar/landscape-architecture-ai) | 空仓库 | 仅有项目愿景 | 排除；没有可审阅实现且无许可证 |

## 成果表达与汇报

| 项目 | 适合任务 | 集成方式 |
|---|---|---|
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | 过程图解、方案比较、审计页和项目回顾 | 作为 `visual` 或 `presentation-document` 外援调用 |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | 工作流、数据流和可验证关系图 | 可用于系统关系图；不得把软件架构语义机械套为空间语义 |
| [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 编辑式幻灯片和视觉叙事 | AGPL 工具保持外部调用，不复制代码 |
| [anthropics/skills](https://github.com/anthropics/skills) 中的 `canvas-design`／`frontend-design` | 视觉方向和静态视觉产物 | 逐个 Skill 复核 Apache-2.0 文件与 NOTICE；本项目仍只独立总结或外部调用 |
| [anthropics/skills](https://github.com/anthropics/skills) 中的 `pptx` | PPTX 生产与验证 | source-available、非开源；不得复制或制作衍生物，只能在授权环境使用 |

## 规范、发现与安全

| 项目 | 用途 | 决定 |
|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Agent Skills 开放规范 | 用于结构与兼容性验证；复制其内容时遵守 Apache-2.0 与 NOTICE |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | `npx skills` 安装与发现 | 作为安装路径之一，不写成唯一运行时 |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | Skill／MCP 安全扫描 | 可作为发布安全检查，不替代人工审阅 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Skill 目录 | 只用于发现，内容与许可必须追到上游 |
| [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | Skill 聚合与镜像 | 只用于发现；聚合仓库许可证不覆盖被镜像内容 |

[gmakstutis/qWiki](https://github.com/gmakstutis/qWiki) 可用于参考建筑理论知识库的组织方式，但仓库许可证不自动重新授权其中收录的书籍、文章、图片或笔记素材，运行时不得复制其第三方正文。

## 蒸馏进入核心的十条规则

这些规则由多个先例启发并针对空间设计独立重写，不是任何单一仓库的衍生提示词：

1. 任务书优先。
2. 学生真实成果优先。
3. 先诊断卡点再给建议。
4. 一次聚焦一个主导矛盾。
5. 按问题、提示、对比、局部示范、救火路径逐级加力。
6. 概念必须落为空间机制。
7. 方案必须产生真实的机制与价值取舍差异。
8. 分析必须返回设计后果。
9. 外部产物必须验证并重新解释其设计意义。
10. 完成作业后总结可迁移方法。

## 许可证边界

- MIT 允许在保留版权与许可声明的条件下复制、修改与再分发；本项目仍优先独立总结，避免无必要的代码或提示词搬运。
- Apache-2.0 的复制或衍生使用必须保留许可证、相关版权和 NOTICE 要求；不能仅因“允许改写”就无条件并入 MIT 文件。
- CC BY-SA 4.0 改编材料必须署名并以相同许可分享；因此不直接混入 MIT 核心，优先回到一手教育研究独立形成方法。
- GPL／AGPL 代码保持在独立外部工具边界；本项目不复制、链接或打包相关实现。
- 无许可证仓库按“保留所有权利”处理：可以引用事实或论文，不复制、修改或再发布仓库内容。
- source-available 不等于开源；使用范围以其专用条款为准。
- 聚合仓库的许可证不覆盖上游内容；书籍、论文、图片和数据也必须分别核验版权与使用条件。

详细上游快照、审阅范围和直接复用状态见 [来源与许可记录](./provenance.md)。
