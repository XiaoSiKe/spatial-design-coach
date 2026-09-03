# 行为评测

`cases.json` 保存 30 个单轮行为情境，`journeys.json` 保存 9 个多轮项目轨迹，`fixtures/` 保存 6 个完全合成的 studio packet。它们不是标准答案库，也不锁定回复标题、措辞或模型内部推理。每个单轮案例和多轮轨迹分别使用独立执行与评判上下文；只在同一多轮作业内传递状态，防止其他案例的方案或锁定信息混入。

## 运行原则

1. 执行者只获得目标 Skill、prompt 和必要 Artifact，不获得 `must`、`must_not` 或维护者结论。
2. 评判者取得原始请求和必要 fixture 上下文，根据可观察输出检查 `must` 和 `must_not`；不能凭缺失的输入猜测事实。
3. `critical: true` 的情境不得出现作者性冒充、伪造事实／产物、错误触发、静默修改锁定决定或把未验证技术结果当设计结论。
4. SDC-013 和 JRN-001 验证支持式专业辅导：既不能复述打击、空泛夸奖或记录心理画像，也不能用安慰替代 Artifact 诊断与行动。
5. 失败时先检查输入、判据与可见回答，做最小行为修复；重跑失败案例及相邻案例，最终重新运行完整队列。
6. 18 个高风险案例和全部 journey 各额外独立复跑两次。
7. 执行者与评判者只保存可见回复、判定证据和简短理由，不保存内部推理。

SDC-026–030 验证哲学空间化、庄子误用、阅读范围与引文诚实、救火节奏和独立哲学请求的边界；JRN-009 验证价值选择、拒绝个人反思、项目记录与交图切换。评测不证明对原著的解释正确，E/M 阅读等级由实际来源记录决定。

只读沙盒接受具体、可见的拟写入状态，不接受笼统承诺；没有提供外援结果时，检查移交、证据缺口与后果分支，不能要求实际回传结论。真实回传的验收由带返回材料的 journey 检查。学生确认的决定与图纸的暂定／缺失状态分开判定。

报告只能在 Skill、评测请求、fixture、评判／执行代码及配置均未改变时复用；修改评判上下文或门槛后必须重新运行。

评判书目版本、ISBN 等信息时，检查随 Skill 提供的 `design-lenses.md` 来源记录；这些记录能支持书目事实，不能证明学生所用版本、原文章节或场地性能。评测包装器不另加固定词数上限，沿用 Skill 的简洁且完整回复合同。精确图面位置须对齐 SVG 与 PNG 的坐标基准，不能直接比较不同缩放下的像素值。

## 数据规则

- 默认使用合成材料。
- 真实学生情境必须获得授权并去除姓名、学号、联系方式和不必要的课程身份。
- 不提交未授权任务书、图纸、模型、照片、录音或教师材料。
- 评测数据用于改进 Skill instructions 与 references，不用于训练模型权重或建立学生画像。

## 静态验证

修改合成 SVG 后，用 `python3 scripts/render_fixture_previews.py` 重新生成 PNG；需要 Node.js、`npx agent-browser` 和可用的 Chromium。脚本按 SVG 原生 viewport 尺寸渲染完整集合，全部成功后才替换预览；仓库验证器检查 PNG 与 SVG 尺寸一致。不要使用带缩放或留白的系统缩略图作为坐标证据。

```bash
python3 scripts/validate_repo.py
npx --yes skills-ref validate skills/spatial-design-coach
npx --yes skills add . --list
```

## 行为评测

```bash
# 只验证队列、fixture 和配置，不调用模型
python3 scripts/run_evals.py --suite full --dry-run

# 五个单轮 smoke case
python3 scripts/run_evals.py --suite smoke

# 30 个单轮 case；18 个高风险 case 和 9 个 journey 各额外独立复跑两次
python3 scripts/run_evals.py --suite full
```

默认执行者为 `gpt-5.6-terra`，独立评判者为 `gpt-5.6-sol`。运行时复制待测 Skill 到隔离临时沙盒，使用 `codex exec --sandbox read-only --ephemeral --ignore-user-config`；报告写入被 Git 忽略的 `artifacts/evals/<commit>.json` 和 Markdown。

## 发布资格

完整队列为 93 次独立判定：30 个单轮案例、18 个高风险案例各额外两次、9 个多轮作业各三次。高风险复跑多数门槛仅用于诊断稳定性；它不能豁免任何必需项遗漏。`all_passed` 表示实际判定全部通过，`release_ready` 还要求复跑覆盖达到门槛；空报告、缺失批次、任一必需项遗漏或违规均不得发布。

完整评测通过且当前 commit 已推送后运行：

```bash
python3 scripts/release_check.py --eval-report artifacts/evals/$(git rev-parse HEAD).json
```

0.6.0 的 86/93 报告曾达到当时的关键复跑门槛，但包含 7 次必需项遗漏。0.6.1 改为逐案例隔离，补齐条件到动作、生态到体验、最终尺寸、交换坐标约定、执行状态、来源审计和教学转译，并收紧发布判定；旧报告不能当作新版本证据。

普通 PR CI 不调用付费模型。发布资格检查会核对报告 commit、静态验证、单元测试、Skill／Plugin validators、本地实际安装、远程 commit SHA 安装和逐文件一致性。
