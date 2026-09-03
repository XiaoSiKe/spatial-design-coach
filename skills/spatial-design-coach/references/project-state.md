# Student Project State

Read this reference when material first arrives, a sandbox starts or resumes, a pivotal decision changes, rescue mode begins, an external capability returns, or the student asks to save or resume progress.

## Keep Skill and project versions separate

`SKILL.md` `metadata.version` identifies the installed coaching instructions. `studio/PROJECT.md` records both the last applied Skill version and an independent project-state schema. A Skill update must not silently change project state.

Before editing an existing file after update, run `scripts/migrate_project.py --root <workspace> --check --json`. Treat `legacy`, `schema-migration-required`, or `skill-version-update-required` as a visible compatibility notice. Continue read-only analysis when safe, but run `--apply` only after the user explicitly requests migration. An apply must create a backup and preserve all project decisions, evidence, Artifacts, and student-authored content. If the project uses a future schema, stop state writes and update the Skill first.

## Select file-backed or chat-only state

When the user asks to start or manage the assignment in the current writable sandbox, run `scripts/init_project.py` and use `studio/PROJECT.md` as the only project-state file. Update it in place after meaningful events. Keep the student's original files outside `studio/` untouched; derived files belong in `studio/outputs/working/`, and only verified submission files belong in `studio/outputs/final/`.

If the user has not asked for workspace state, the workspace is read-only, or the user prohibits writes, maintain the same fields in conversation and export a continuation snapshot on request. A writable directory alone is not permission to initialize it. Do not create another state file as a workaround.

## Keep one shared state

Maintain one student-visible source of truth for the current project. Do not create parallel project cards, decision logs, deliverable lists, and handoff states that can drift apart.

| State area | Keep |
| --- | --- |
| Scope | Discipline, assignment, site, boundary, scale, people, program, constraints |
| Delivery | Deadline, interim reviews, required artifacts, scales, formats, current source files |
| Position | Mode, current stage, dominant conflict, proposition, selected alternative |
| Decisions | Open, provisional, locked, or superseded choices; rejected alternatives; reason and trade-off |
| Evidence | Supplied facts, inspected evidence, inferences, assumptions, pending verification |
| Artifacts | Current project version, completed/provisional/missing status, blocking dependency |
| Standards | Brief or rubric criterion, responsible Artifact, observable pass condition |
| Forward motion | Next 1–3 actions, next smallest artifact, pass condition |

Keep the state proportional. Omit irrelevant fields rather than printing `unknown` repeatedly.

Do not turn temporary distress, confidence, personality, teacher tone, or inferred ability into project-state fields or a student profile. Record only project-relevant feedback criteria, requested support preferences, decisions, and next actions that the student wants preserved.

A student-confirmed philosophical value belongs in the existing proposition or decision rationale, together with the trade-off, source status, affected Artifact, and next test. Record the project choice rather than a life story or belief profile. Declining reflection does not prevent ordinary project work and does not authorize any schema migration.

## Control decision maturity

- **Open:** a choice is still being framed or compared.
- **Provisional:** a reversible working direction with stated assumptions or pending evidence.
- **Locked:** a pivotal choice the student confirmed with its basis and accepted trade-off.
- **Superseded:** a previous direction retained with the evidence or decision that replaced it.

Do not upgrade a decision because it appears repeatedly in drawings or external output. Match commitment to evidence: keep uncertain moves reversible, and require stronger evidence plus student confirmation before a costly or hard-to-reverse move becomes locked.

Keep three questions separate: what the brief requires, what the student has decided, and what the available evidence verifies. A confirmed flood-performance requirement is not a verified flood-performance result. A confirmed retention choice can have an unfinished section. A mode change changes priorities, not these evidence or authority states; report each confirmed item's kind explicitly.

Carry the evidence status through every summary and state update: a hypothesis does not become a finding because it was written into PROJECT.md, and a known source version does not become provisional without new evidence. A work-time report is progress information, not proof of completed or inspected files.

Attach each status to its actual object. A locked spatial choice and its missing or provisional drawing can coexist; label the drawing with its Artifact name rather than placing the choice itself in an Artifact-readiness bucket. The final state update must use the same distinction as the opening status summary.

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

Apply partial choices as an explicit old → new change before summarizing the state. If one component of a bundled proposal is rejected or deferred, split the bundle: state the current retained components and move the paused part into the existing rejected/deferred history with its reason and reopening condition. Do not repeat the old bundle as an active provisional scheme after describing the new choice. Preserve unaffected decisions without reinstating the rejected component.

Keep the latest design decision distinct from the last inspected drawing. That old file may still contain the superseded layout and serve as a base to edit; label the discrepancy and affected Artifacts as pending revision rather than claiming the drawing already changed or treating its old contents as the current decision. Check the opening recommendation, decision row and next-work summary against the same updated state.

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

> 这是供学生审阅的工作记录；各项仍以所标明的证据状态为准，快照本身不作事实核验或成果完成证明。

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

Fill only useful fields. Keep the evidence-limit sentence inside the copyable snapshot so it survives the move to another conversation. For a chat-only export, the snapshot itself is the handoff; do not append a duplicate proposal to write PROJECT.md. Do not write to disk or create a persistent student profile unless the user explicitly asks.
