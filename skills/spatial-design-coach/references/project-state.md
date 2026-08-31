# Student Project State

Read this reference when material first arrives, a pivotal decision changes, rescue mode begins, an external capability returns, or the student asks to save or resume progress.

## Keep one shared state

Maintain one student-visible source of truth for the current project. Do not create parallel project cards, decision logs, deliverable lists, and handoff states that can drift apart.

| State area | Keep |
| --- | --- |
| Scope | Discipline, assignment, site, boundary, scale, people, program, constraints |
| Delivery | Deadline, interim reviews, required artifacts, scales, formats, current source files |
| Position | Mode, current stage, dominant conflict, proposition, selected alternative |
| Decisions | Locked student-confirmed choices, rejected alternatives, reason and trade-off |
| Evidence | Supplied facts, inspected evidence, inferences, assumptions, pending verification |
| Artifacts | Current project version, completed/provisional/missing status, blocking dependency |
| Forward motion | Next 1–3 actions, next smallest artifact, pass condition |

Keep the state proportional. Omit irrelevant fields rather than printing `unknown` repeatedly.

## Update at meaningful events

Create or substantially refresh the state when:

- a brief or meaningful artifact is first inspected;
- the mode, stage, proposition, selected alternative, or dominant conflict changes;
- the student confirms or rejects a pivotal design choice;
- a new fact invalidates an assumption;
- rescue mode establishes a minimum complete submission;
- an external capability returns an artifact or finding;
- the student asks to save, hand off, or resume the project.

During ordinary turns, show only the changed decisions, assumptions, artifact status, and next evidence. Do not repeat the full state in every response.

## Resolve conflicts before updating

When new information conflicts with the state:

1. name the old item and its evidence status;
2. name the new evidence and its source;
3. explain which downstream decisions or artifacts would change;
4. ask the student to confirm a pivotal value choice when needed;
5. update the state and mark superseded items rather than silently deleting their history.

An external capability return is evidence, not an automatic state change. If it conflicts with a locked decision, surface the conflict before merging it.

## Export a continuation snapshot

When the student asks to save progress or continue in another conversation, return this compact Markdown snapshot:

```markdown
# 项目续航快照

- 项目与截止时间：
- 当前模式／阶段：
- 当前主导矛盾：
- 设计命题：
- 已锁定决定：
- 被否决方向与原因：
- 已确认事实／当前假设：
- 待验证项：
- 成果状态：
- 下一步 1–3 项：
- 下一轮带回与通过条件：
```

Fill only useful fields. State that the snapshot is student-reviewable working memory, not proof of facts or completed work. Do not write it to disk or create a persistent student profile unless the user explicitly asks.
