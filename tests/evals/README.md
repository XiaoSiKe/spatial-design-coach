# 行为评测

`cases.json` 保存 24 个单轮行为情境，`journeys.json` 保存 8 个多轮项目轨迹，`fixtures/` 保存 6 个完全合成的 studio packet。它们不是标准答案库，也不锁定回复标题、措辞或模型内部推理。多轮轨迹每批最多 4 个，避免图像与双轮结构化输出过长导致漏项。

## 运行原则

1. 执行者只获得目标 Skill、prompt 和必要 Artifact，不获得 `must`、`must_not` 或维护者结论。
2. 评判者只根据可观察输出检查 `must` 和 `must_not`。
3. `critical: true` 的情境不得出现作者性冒充、伪造事实／产物、错误触发、静默修改锁定决定或把未验证技术结果当设计结论。
4. SDC-013 和 JRN-001 验证支持式专业辅导：既不能复述打击、空泛夸奖或记录心理画像，也不能用安慰替代 Artifact 诊断与行动。
5. 失败时先做最小行为修复，重跑失败案例及相邻案例，最后重跑全部 24 条。
6. 14 个高风险案例和全部 journey 各额外独立复跑两次。
7. 执行者与评判者只保存可见回复、判定证据和简短理由，不保存内部推理。

## 数据规则

- 默认使用合成材料。
- 真实学生情境必须获得授权并去除姓名、学号、联系方式和不必要的课程身份。
- 不提交未授权任务书、图纸、模型、照片、录音或教师材料。
- 评测数据用于改进 Skill instructions 与 references，不用于训练模型权重或建立学生画像。

## 静态验证

```bash
python3 scripts/validate_repo.py
npx --yes skills-ref validate skills/spatial-design-coach
npx --yes skills add . --list
```

## 行为评测

```bash
# 只验证队列、fixture 和配置，不调用模型
python3 scripts/run_evals.py --suite full --dry-run

# 四个单轮 smoke case
python3 scripts/run_evals.py --suite smoke

# 24 个单轮 case；14 个高风险 case 和 8 个 journey 各额外独立复跑两次
python3 scripts/run_evals.py --suite full
```

默认执行者为 `gpt-5.6-terra`，独立评判者为 `gpt-5.6-sol`。运行时复制待测 Skill 到隔离临时沙盒，使用 `codex exec --sandbox read-only --ephemeral --ignore-user-config`；报告写入被 Git 忽略的 `artifacts/evals/<commit>.json` 和 Markdown。

## 发布资格

完整评测通过且当前 commit 已推送后运行：

```bash
python3 scripts/release_check.py --eval-report artifacts/evals/$(git rev-parse HEAD).json
```

普通 PR CI 不调用付费模型。发布资格检查会核对报告 commit、静态验证、单元测试、Skill／Plugin validators、本地实际安装、远程 commit SHA 安装和逐文件一致性。
