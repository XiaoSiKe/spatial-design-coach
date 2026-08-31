# Student Project State

Read this reference when material first arrives, a sandbox starts or resumes, a pivotal decision changes, rescue mode begins, an external capability returns, or the student asks to save or resume progress.

## Select file-backed or chat-only state

In a writable assignment sandbox, run `scripts/init_project.py` and use `studio/PROJECT.md` as the only project-state file. Update it in place after meaningful events. Keep the student's original files outside `studio/` untouched; derived files belong in `studio/outputs/working/`, and only verified submission files belong in `studio/outputs/final/`.

If the workspace is read-only or the user prohibits writes, maintain the same fields in conversation and export a continuation snapshot on request. Do not create another state file as a workaround.

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
| Standards | Brief or rubric criterion, responsible Artifact, observable pass condition |
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
- a required Artifact changes status, dependency, version or QA result;
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

When the student selects one alternative, keep every other compared family as a rejected direction with its mechanism, evidence and rejection reason. Do not delete alternatives merely because the current design has moved on.

When the student says “I decide,” “I choose,” or an equivalent confirmation, record it visibly as **student confirmed** and name both the affected overall plan/masterplan and the affected focus-area plan, section or equivalent downstream Artifact.

## Preserve files and versions

- Treat original material as read-only even when the sandbox is writable.
- Never update an Artifact status from a filename alone; inspect the file or label it unverified.
- Record which project version each Artifact represents.
- When a derived target already exists, create the next `-vN` output instead of overwriting it.
- Move or copy a file into `studio/outputs/final/` only after its requirement, project version and QA are confirmed.

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
