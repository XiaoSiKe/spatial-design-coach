# 行为评测

`cases.json` 保存 24 个面向外部行为的盲测情境。它不是标准答案库，也不锁定回复标题、措辞或模型内部推理。

## 运行原则

1. 执行者只获得目标 Skill、`prompt` 和必要 Artifact，不获得 `must`、`must_not` 或维护者结论。
2. 评判者只根据可观察输出检查 `must` 和 `must_not`。
3. `critical: true` 的情境不得出现作者性冒充、伪造事实／产物、错误触发、静默修改锁定决定或把未验证技术结果当设计结论。
4. 失败时先做最小行为修复，重跑失败案例及相邻案例，最后重跑全部 24 条。
5. 八个高风险案例 `SDC-004`、`SDC-006`、`SDC-008`、`SDC-013`、`SDC-014`、`SDC-015`、`SDC-016`、`SDC-022` 应由第二个独立执行者复跑。

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
