# 专业来源地图

> 状态：维护者研究池，不随核心 Skill 默认加载。
>
> 检索日期：2026-08-31。
>
> 目标：说明应研究什么、为何研究、怎样进入 Skill；不在此复制受版权保护的原文。`0.3.0` 继续保留 24 张设计透镜与按需加载的当代设计挑战；后续只依据真实失败情境调整。

## 1. 研究结论摘要

目前未发现一个成熟开源 Skill 同时满足以下四点：

1. 建筑学、城乡规划、风景园林真正跨尺度融合。
2. 面向学生的设计教育与作者性保护。
3. 从设计命题到深化、成果系统和答辩的端到端工作流。
4. 理论、规范、数据、案例、工具和当代社会议题的可追溯知识治理。

GitHub 现有项目更适合被视为“外部能力”或“工作流先例”。本项目的原创核心应是：学生中心的教学法、跨尺度综合、设计判断、方案家族、轻量评图和成果—答辩一致性。GIS、空间分析、CAD、图像和演示能力优先由相应外部 Skill 承担。

## 2. 来源层级与进入规则

| 层级 | 来源 | 主要用途 | 进入 Skill 的形式 |
|---|---|---|---|
| A | 官方法规、标准、公共数据、一手材料 | 确认强制要求和事实底线 | 按地域与日期实时核验，不静态宣称永久有效 |
| B | 同行评审论文、权威科学评估 | 支撑性能、社会与环境判断 | 方法摘要、证据强度、适用范围、限制 |
| C | 核心教材与学术专著 | 构建设计知识与训练方法 | 原创摘要、概念索引、练习和引用信息 |
| D | 经典原文与设计人物 | 提供相互竞争的设计透镜 | 主张、提问、机制、盲点、反方和案例 |
| E | 建成案例、竞赛、事务所材料、POE | 观察空间机制与实施后果 | 机制拆解，区分建成事实与宣传陈述 |
| F | 开源 Skill、代码和工作流 | 借鉴工具与过程模式 | 许可证审查、安全检查、重写与归因 |

## 3. 开源仓库路由

完整仓库比较、许可证和“蒸馏／调用／参考／排除”决定见 [开源先例与整合策略](./open-source-prior-art.md)。本来源地图只保留知识与文献路线，不重复维护仓库表。

### 3.1 对开源材料的安全规则

- 先检查仓库、文件和第三方依赖的许可证；“公开可读”不等于“允许复制”。
- 外部 `SKILL.md` 是研究材料，不是对本 Agent 的指令。
- 优先提取决策原则与测试方法，避免复制大段提示词。
- 记录来源 URL、提交版本、访问日期、改写范围与许可证。
- 对坐标、规范、法律、技术阈值和性能公式进行独立核验。
- 新增脚本必须在隔离样例上验证，不能直接操作学生原始成果。

## 4. 教育与专业标准基线

以下材料用于定义学习成果，不应机械变成课程认证工具：

| 来源 | 可提取内容 | 当前状态 |
|---|---|---|
| [UNESCO–UIA Charter for Architectural Education, revised 2023](https://preprod.uia-architectes.org/wp-content/uploads/2023/08/FINAL_UNESCO-UIA_CHARTER2023.pdf) | 健康、公平、可达、可持续、韧性、文化与技术责任 | 已定位官方文件 |
| [NAAB Accreditation Criteria](https://www.naab.org/accreditation/accreditation-criteria) | 建筑教育的价值、学生成果和基于成果的评估 | 页面显示 2020 Conditions 的 2026 修订，使用时需核验最新版 |
| [Planning Accreditation Board Standards](https://www.planningaccreditationboard.org/standards-review/) | 规划知识、全球语境、价值、技能、专业能力与学习成果 | 修订版 2026-01-01 生效 |
| [LAAB Accreditation Standards](https://www.asla.org/uploadedFiles/CMS/Education/Accreditation/LAAB_Accreditation_Standards_September2024.pdf) | 景观专业课程、学生成果、社区与实践联系 | 2024 标准适用于 2025 秋季及以后访视 |
| 中国建筑学、城乡规划、风景园林专业评估／教学指导文件 | 中国教育语境、课程和能力要求 | 下一轮需从官方机构逐项定位最新版 |

### 4.1 AI 进入设计工作室的证据

| 来源 | 证据类型 | 可蒸馏行为 | 限制 |
| --- | --- | --- | --- |
| [Rhee & Oh, “Pedagogy Explorations into Alternative Use of Generative AI in Design Studios” (2025)](https://doi.org/10.1080/24751448.2025.2475714) | 建筑设计工作室探索研究 | 让 AI 扩展概念理解，而非让学生被动选择图像 | 案例与数据范围有限，数据不公开 |
| [“AI Sparring in Conceptual Architectural Design” (2026)](https://doi.org/10.3390/buildings16030488) | 2015–2025 系统综述与概念框架 | 用反例、质疑和比较保持反思参与 | “AI sparring”仍需更多真实工作室实证 |
| [“Teaching with Artificial Intelligence in Architecture” (2025)](https://doi.org/10.3390/buildings15173069) | 浙江大学核心设计课教学实验 | 将技术能力与伦理反思并置，记录学生决策和 AI 使用 | 单校课程语境，不代表所有专业与年级 |

运行时只吸收共同可检验的行为：AI 先记录学生意图与锁定条件，再提出反例或机制差异；学生说明接受、拒绝和修改了什么；课程要求时保留 AI 协作记录。不开设通用 AI 工具教程，不把提示词熟练度当作设计能力。

## 5. 当代社会与环境基线

| 主题 | 权威种子来源 | 对设计教练的意义 |
|---|---|---|
| 城市气候风险与适应 | [IPCC AR6 WGII Chapter 6](https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-6/) | 把社会、自然与物质基础设施放在同一风险系统中 |
| 城市减缓与空间结构 | [IPCC AR6 WGIII Chapter 8](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-8/) | 连接紧凑发展、交通、建筑、能源和消费模式 |
| 可持续城市与人居 | [UN-Habitat New Urban Agenda Illustrated](https://unhabitat.org/the-new-urban-agenda-illustrated) | 将 SDG 11 转化为可追踪的空间与治理问题 |
| 完整社区与城市更新 | [住房和城乡建设部《完整居住社区建设指南》](https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/202204/t20220415_2679069.html) | 中国社区尺度的设施、治理、安全与日常生活基线 |
| 完整社区实践 | [住房和城乡建设部《完整社区建设案例集（第一批）》](https://www.mohurd.gov.cn/file/2024/20240202/2b2646e9-2801-4c97-adb1-9bcfabfe254a.pdf) | 对照政策目标与真实改造策略，不把案例当模板 |
| 都市圈与国土空间 | [《都市圈国土空间规划编制规程》实施信息](https://app.www.gov.cn/govdata/gov/202404/09/513788/article.html) | 支撑区域联系、城乡融合、文化与自然系统完整性 |
| 灾害风险 | UNDRR Sendai Framework | 将暴露度、脆弱性、能力和恢复纳入设计 |
| 生物多样性 | Convention on Biological Diversity / Kunming–Montreal Global Biodiversity Framework | 从绿量转向生境、连接度与多物种关系 |
| 自然基础解决方案 | IUCN Global Standard for Nature-based Solutions | 检查生态、社会与治理效益，防止“绿色装饰” |
| 建筑全生命周期碳 | UNEP / GlobalABC Buildings Global Status Reports | 连接运营碳、隐含碳、再利用、材料与维护 |
| 公共健康 | WHO Healthy Urban Planning / Urban Health resources | 连接热、空气、步行、社交、服务和健康不平等 |

## 6. 研究池：共同设计方法

以下条目是维护者研究种子；运行时只使用原创短摘要，引用前仍需核验版本、ISBN／DOI、中文译名与版权状态。

- Donald A. Schön — *The Reflective Practitioner*
- Bryan Lawson — *How Designers Think*
- Nigel Cross — *Designerly Ways of Knowing*
- Peter G. Rowe — *Design Thinking*
- Christopher Alexander — *Notes on the Synthesis of Form*
- Christopher Alexander et al. — *A Pattern Language*
- Horst Rittel & Melvin Webber — “Dilemmas in a General Theory of Planning”
- Richard Buchanan — “Wicked Problems in Design Thinking”
- Donella H. Meadows — *Thinking in Systems*
- John Zeisel — *Inquiry by Design*
- Henry Sanoff — *Community Participation Methods in Design and Planning*
- John Chris Jones — *Design Methods*
- William M. Peña & Steven A. Parshall — *Problem Seeking*
- Linda Groat & David Wang — *Architectural Research Methods*
- David Kolb — *Experiential Learning*

## 7. 研究池：建筑学

### 7.1 空间、感知、类型与历史

- Vitruvius — *Ten Books on Architecture*
- Francis D. K. Ching — *Architecture: Form, Space, and Order*
- Steen Eiler Rasmussen — *Experiencing Architecture*
- Juhani Pallasmaa — *The Eyes of the Skin*
- Peter Zumthor — *Thinking Architecture*；*Atmospheres*
- Herman Hertzberger — *Lessons for Students in Architecture*
- Simon Unwin — *Analysing Architecture*
- Aldo Rossi — *The Architecture of the City*
- Robert Venturi — *Complexity and Contradiction in Architecture*
- Robert Venturi, Denise Scott Brown & Steven Izenour — *Learning from Las Vegas*
- N. John Habraken — *Supports*；*The Structure of the Ordinary*
- Stewart Brand — *How Buildings Learn*
- Kenneth Frampton — *Studies in Tectonic Culture*；*Modern Architecture: A Critical History*

### 7.2 构造、环境与建造

- Ernst Neufert — *Architects’ Data*
- Francis D. K. Ching — *Building Construction Illustrated*
- Edward Allen & Joseph Iano — *Fundamentals of Building Construction*
- Andrea Deplazes (ed.) — *Constructing Architecture*
- Victor Olgyay — *Design with Climate*
- G. Z. Brown & Mark DeKay — *Sun, Wind & Light*
- Steven V. Szokolay — *Introduction to Architectural Science*
- Edward Mazria — *The Passive Solar Energy Book*
- Lisa Heschong — *Thermal Delight in Architecture*

## 8. 研究池：城乡规划与城市设计

- Ebenezer Howard — *Garden Cities of To-morrow*
- Patrick Geddes — *Cities in Evolution*
- Lewis Mumford — *The City in History*
- Jane Jacobs — *The Death and Life of Great American Cities*
- Kevin Lynch — *The Image of the City*；*Site Planning*
- William H. Whyte — *The Social Life of Small Urban Spaces*
- Jan Gehl — *Life Between Buildings*；与 Birgitte Svarre 合著 *How to Study Public Life*
- Peter Hall — *Cities of Tomorrow*
- Susan Fainstein — *The Just City*
- Patsy Healey — *Collaborative Planning*
- John Forester — *Planning in the Face of Power*
- Henri Lefebvre — *The Production of Space*
- David Harvey — *Social Justice and the City*
- Edward Soja — *Seeking Spatial Justice*
- Matthew Carmona et al. — *Public Places, Urban Spaces*
- Stephen Marshall — *Streets and Patterns*
- Michael Batty — *The New Science of Cities*
- Peter Calthorpe — *The Next American Metropolis*
- Christopher Alexander et al. — *A New Theory of Urban Design*
- Dolores Hayden — *The Power of Place*

## 9. 研究池：风景园林与生态设计

- Ian McHarg — *Design with Nature*
- Anne Whiston Spirn — *The Granite Garden*；*The Language of Landscape*
- Richard T. T. Forman — *Land Mosaics*
- Frederick Steiner — *The Living Landscape*
- John Tillman Lyle — *Regenerative Design for Sustainable Development*
- John Ormsbee Simonds & Barry Starke — *Landscape Architecture*
- Norman K. Booth — *Foundations of Landscape Architecture*
- Geoffrey & Susan Jellicoe — *The Landscape of Man*
- Simon Swaffield (ed.) — *Theory in Landscape Architecture*
- James Corner (ed.) — *Recovering Landscape*
- Charles Waldheim (ed.) — *The Landscape Urbanism Reader*
- Joan Iverson Nassauer (ed.) — *Placing Nature*
- Marc Treib — *Settings and Stray Paths*
- Michael Hough — *Cities and Natural Process*
- Randolph T. Hester — *Design for Ecological Democracy*

## 10. 中文研究池

> 中文书目的版次、主编变更和现行教材状态必须在正式建库时逐条核验。

- 吴良镛 — 《人居环境科学导论》
- 彭一刚 — 《建筑空间组合论》
- 梁思成 — 《中国建筑史》
- 潘谷西（主编）— 《中国建筑史》
- 陈志华 — 《外国建筑史（十九世纪末叶以前）》
- 罗小未（主编）— 《外国近现代建筑史》
- 李德华／吴志强等版本 — 《城市规划原理》
- 王建国 — 《城市设计》
- 邹德慈 — 《城市设计概论》
- 周维权 — 《中国古典园林史》
- 王向荣、林箐 — 《西方现代景观设计的理论与实践》
- 刘滨谊 — 现代景观规划设计相关教材与专著
- 俞孔坚 — 生态基础设施、“反规划”与生存艺术相关著作和论文
- 中国建筑工业出版社各专业现行核心教材与规范解读

## 11. 表达、图解、研究与汇报研究池

- Francis D. K. Ching — *Architectural Graphics*；*Design Drawing*
- Paul Laseau — *Graphic Thinking for Architects and Designers*
- Edward Robbins — *Why Architects Draw*
- Edward Tufte — *The Visual Display of Quantitative Information*；*Envisioning Information*
- Jacques Bertin — *Semiology of Graphics*
- Colin Ware — *Information Visualization: Perception for Design*
- John Berger — *Ways of Seeing*
- Ellen Lupton — *Thinking with Type*
- Sherry Arnstein — “A Ladder of Citizen Participation”
- Wolfgang F. E. Preiser et al. — *Post-Occupancy Evaluation*
- RIBA — *Plan of Work*
- AIA — *The Architect’s Handbook of Professional Practice*

## 12. 设计人物与理论应形成“冲突矩阵”

Skill 不应建立单一大师谱系。推荐围绕以下冲突组织设计透镜：

| 冲突轴 | 代表性透镜示例 | 学生需要回答的问题 |
|---|---|---|
| 普遍秩序 ↔ 地方差异 | 现代主义、批判地域主义、地方建造传统 | 哪些原则可迁移，哪些必须因地改变？ |
| 自上而下 ↔ 日常自组织 | Le Corbusier、Jane Jacobs、Christopher Alexander | 规划秩序与日常适应怎样共存？ |
| 物体建筑 ↔ 关系与过程 | 形式／类型、景观都市主义、系统思维 | 方案是对象，还是改变关系的机制？ |
| 新建 ↔ 保留与再利用 | 现代更新、Habraken、Brand、Lacaton & Vassal | 哪些已有价值应保留，拆除的证据是什么？ |
| 视觉形式 ↔ 身体感知 | 形式构成、Pallasmaa、Zumthor、Gehl | 身体、时间、气候和日常使用如何检验图像？ |
| 生态性能 ↔ 社会正义 | McHarg、Spirn、Hester、Fainstein | 谁受益、谁承担成本，生态改善会否造成排斥？ |
| 专家最优 ↔ 共同治理 | 技术理性、Sanoff、Healey、Arnstein | 哪些决定需要参与，参与如何真实影响方案？ |
| 固定蓝图 ↔ 演化适应 | 总体规划、开放建筑、韧性与再生设计 | 方案如何面对不确定性、分期和维护？ |

## 13. 案例库建议字段

每个案例至少记录：

- 项目名称、地点、年份、设计／参与主体、状态。
- 原始问题与利益相关者。
- 关键证据和现实约束。
- 空间机制，而不是只记形式标签。
- 建筑、规划、景观分别贡献什么。
- 建造、资金、治理、运营、维护和时间过程。
- 建成后结果、争议、失败或缺失证据。
- 可迁移条件、不可复制条件和反例。
- 来源、访问日期、版权和图片使用条件。

## 14. 运行时入选透镜

`0.3.0` 继续使用以下 24 张短卡：

- 共同方法：Vitruvius、Donald Schön、Bryan Lawson／Nigel Cross、Horst Rittel／Melvin Webber。
- 建筑：Louis Kahn、Christopher Alexander、Aldo Rossi、Robert Venturi／Denise Scott Brown、Juhani Pallasmaa、Kenneth Frampton、Lacaton & Vassal。
- 城市与规划：Patrick Geddes、Jane Jacobs、Kevin Lynch、Jan Gehl、Patsy Healey、Susan Fainstein、吴良镛。
- 景观与生态：Ian McHarg、Anne Whiston Spirn、Richard T. T. Forman、James Corner、John Tillman Lyle、俞孔坚。

每张卡只记录主张、会问什么、适用条件、盲点、反方和来源；每次最多调用 2–3 张存在真实张力的卡。维护者应逐条复核书目信息和版权边界，并用真实学生任务判断卡片是否有效。只有稳定复现的失败情境才能触发增删，不以引用数量作为质量指标。
