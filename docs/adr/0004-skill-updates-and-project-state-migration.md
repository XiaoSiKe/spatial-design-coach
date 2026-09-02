# ADR-0004：Skill 更新与项目状态迁移

- 状态：已接受
- 日期：2026-09-02
- 适用版本：`0.5.0` 起
- 补充：[ADR-0003](./0003-assignment-sandbox-and-file-backed-state.md)

## 背景

GitHub 中的 Skill 更新不会自动改变用户已经安装的本地副本，已经打开的任务也可能继续使用更新前加载的 instructions。与此同时，设计作业会跨越数周；更新教练能力不能覆盖学生已有的 `studio/PROJECT.md`，但项目状态结构未来确实可能需要演进。

[OpenAI 托管 Skills API](https://developers.openai.com/api/reference/go/resources/skills) 提供不可变版本与默认版本指针，但本项目当前主要通过 GitHub 和 `npx skills` 分发本地 Skill，因此不能把托管 API 的版本行为当成本地自动更新承诺。

## 决策

采用四层版本边界：

1. **发布源：** GitHub tag／Release 标识已验证版本。
2. **安装副本：** 用户通过 `npx skills update` 显式更新；手动复制安装需要替换完整目录。
3. **活动任务：** 更新或 Plugin 重装后用新任务加载新版；不承诺旧任务热更新。
4. **项目状态：** `PROJECT.md` 使用独立 schema，不随每次 Skill 发布自动迁移。

`SKILL.md` 的 `metadata.version` 是运行时版本源，与 Plugin manifest、产品基线和新项目模板保持一致。版本遵循语义化版本：修复使用 patch，向后兼容能力使用 minor，不兼容行为或状态变化使用 major；项目 schema 只在 `PROJECT.md` 结构不兼容时递增。

新增 `scripts/migrate_project.py`：

- 默认或 `--check` 只读检查；
- `--apply` 必须由用户明确要求；
- 写入前创建不覆盖的备份；
- 只迁移 `studio/PROJECT.md`，保留学生内容；
- 不修改原始任务书、图纸、模型、照片或数据；
- 遇到未来 schema 时拒绝写入，要求先更新 Skill。

## 备选方案

### 每次调用都联网检查并自动更新

可以更快分发，但会引入网络依赖、不可复现行为、隐私与供应链风险，也可能在作业中途改变辅导规则，因此拒绝。

### Skill 更新时自动重写旧项目状态

操作简单，但会混淆教练版本与学生项目，扩大误删和状态漂移风险，因此拒绝。

### 永不迁移旧项目

最安全但会阻止必要的结构演进。采用只读检查、显式授权、备份和幂等迁移作为折中。

## 影响

- 用户需要主动更新并新建任务，升级不是完全无感。
- 维护者必须同步版本元数据并提供中文 Release 说明。
- 旧项目继续可读；只有项目 schema 不兼容时才需要迁移。
- 发布验证会阻止 Skill、Plugin、产品基线和模板版本漂移。
