# Capability Routing

Read this reference when a design decision requires specialist research, analysis, modeling, visualization, or document production beyond the lightweight coaching core.

## Route by capability, not vendor

Use one of five stable capability types:

| Capability | Route when the decision requires | Typical return |
| --- | --- | --- |
| `research-current` | Current regulations, policy, datasets, social context, recent precedents, or verifiable sources | Source-backed finding with jurisdiction, date, uncertainty, and design consequence |
| `geospatial` | GIS data, mapping, network or terrain analysis, remote sensing, spatial statistics, or cartographic production | Reproducible analysis, editable project or data, map export, CRS and method record |
| `cad-modeling` | CAD/BIM geometry, parametric tests, quantities, interoperability, fabrication, or model validation | Editable geometry or model, units and origin, parameters, views, and validation record |
| `visual` | A diagram, sketch, atmosphere study, reference-image variation, or other visual test | Image or editable visual with prompt or method, resolution, limitations, and design-state match |
| `presentation-document` | Boards, slides, reports, PDFs, layout, export, or file-level QA | Editable source, final export, dimensions, fonts or links, and visual verification |

Do not route ordinary design reasoning just because a specialist tool exists. Route only when an operation or current external fact is necessary for the next decision or deliverable.

## Discover and delegate

1. State the design decision the external work must inform.
2. Identify locked decisions the specialist must not silently redesign.
3. Inspect available Skills, MCPs, connectors, and tools for the capability.
4. Prefer the most specific already installed capability; do not hard-code a repository as the only provider.
5. Read and follow the selected capability's own instructions before using it.
6. Pass a bounded handoff contract and required source artifacts.
7. Inspect the returned artifact and provenance before accepting it.
8. Reconcile the result with the shared project state, then explain the design consequence and next evidence.

Do not automatically install a missing dependency, vendor another repository, or make the student choose among implementation tools when the design need is already clear.

## Use the handoff contract

Keep this structure when delegating internally or giving the student a copyable brief:

```markdown
## 能力移交

- 能力：
- 设计目的：
- 当前阶段：
- 项目状态摘要：
- 输入与文件：
- 明确任务：
- 已锁定、不得改变的设计决定：
- 依赖的待验证项：
- 验收标准：
- 返回：产物路径、方法与工具、数据来源、验证证据、限制、需人工复核项
```

In a writable assignment sandbox, add the assigned output directory and require a `RESULT.md`. The return record must contain:

```markdown
# Capability Result

- Capability and task:
- Inputs and authoritative project version:
- Data provenance (owner/source, date/version, transformations):
- Method and tools:
- Returned files:
- Verification evidence:
- Limitations and pending checks:
- Locked-decision conflicts:
- Proposed project-state changes:
```

Do not let an adapter write outside its assigned directory or overwrite an existing return. A returned file without this record remains provisional.

Every initial handoff and every rework request must spell the exact relative output directory, such as `studio/outputs/working/geospatial/public-axis/` or its next unused `-vN`; never refer only to “the previous” or “the specified” directory.

Make the **design purpose** decision-specific. “Create a GIS map” is too weak; “test whether the proposed east–west public spine connects the three 10-minute walking catchments without crossing the flood exclusion zone” is actionable.

Locked decisions protect authorship and consistency. They may include site boundary, selected alternative, program quantities, datum, project north, level system, material logic, graphic conventions, or claims that require verification rather than invention.

Acceptance criteria should be observable: file type, scale, units, coordinate system, required layers, viewpoint, editable structure, comparison set, source date, export size, or the question the artifact must answer.

Every handoff must also state how the return will be translated into a concrete spatial or deliverable consequence; do not postpone that responsibility until after the tool runs.

## Apply capability-specific checks

### `research-current`

- Prefer primary and authoritative sources for regulations, standards, policy, data, and product or platform behavior.
- Record source title, link, publisher, publication or update date, event date when different, jurisdiction, and access date.
- Separate mandatory requirement, guidance, reported practice, and inference.
- Check that the source applies to the project's place, date, scale, and student use.
- Return the design decision affected; do not hand back an undigested bibliography.

### `geospatial`

- Record data owner, vintage, coverage, resolution, license, missing values, and known bias.
- State CRS, units, datum, transformations, analysis extent, method, parameters, and classification choices.
- Keep input data and computed outputs distinguishable.
- Verify a sample against an authoritative map, field evidence, or known control where possible.
- Return an editable source plus a readable export; explain which design hypothesis the result supports or weakens.

### `cad-modeling`

- Enumerate the selected design scheme and authoritative version as locked decisions alongside boundary, north, datum and levels; define how the returned model version will be named and compared.
- Define a usable exchange rule in the handoff: inherit the authoritative file's unit, origin/control point, axes, north and vertical datum unchanged; identify that file/version and the point's coordinates. If any value is unavailable, explicitly mark it **pending confirmation before modeling**, request the source metadata/control-point record in one bundle, and limit current work to preparation. Never silently choose metres, millimetres, `(0,0,0)`, or a scheme name.
- Record any necessary conversion as a proposed scale/rotation/translation, verify it against a known dimension/control point, and obtain confirmation before exchange. Lock levels, tolerances, naming and file version at the same gate; merely asking the return to “explain units and origin” is insufficient.
- State which geometry is authoritative and which is exploratory.
- Keep parameters and layers legible; avoid unexplained destructive conversion.
- Check open edges, overlaps, normals, solids, dimensions, quantities, or interoperability as relevant.
- Return representative views and the editable model; a screenshot alone is not a model result.

### `visual`

- State the design facts that must remain unchanged and the uncertainty the image is allowed to explore.
- Use visual output to test atmosphere, sequence, material, light, occupation, or communication—not to fabricate evidence.
- Check people, access, scale, season, vegetation, water, structure, and context against current drawings.
- Label speculative imagery. Do not present generated users, site conditions, or performance as observed fact.
- Return generation or editing method, references used, resolution, editability, and inconsistencies requiring manual correction.

### `presentation-document`

- State final page or board size, orientation, count, export format, delivery channel, and deadline.
- Preserve the selected project state, narrative order, terminology, units, captions, and source credits.
- Prefer editable sources; package fonts, links, or assets only when licensing permits.
- Render and inspect the final output at delivery size for clipping, substitutions, broken links, line weight, contrast, and raster quality.
- Return source and export paths plus a brief visual QA result.

## Reinterpret every return

Before presenting an external result to the student, answer:

1. Which design assumption did it support, weaken, or fail to test?
2. What specific part of the proposal or deliverable should now change?
3. Which parts remain technical artifacts rather than design conclusions?
4. Did it alter a locked decision, project version, datum, terminology, quantity, or visual convention?
5. Which project-state fields can be updated, and which still require the student's confirmation?

Use a visible return-audit checklist: **actual files inspected → method → source/data → verification → limitations → design consequence → student confirmation**. A hypothetical or merely promised return cannot be marked accepted.

For a reported return without inspectable content, state the current gaps separately: **files not inspected; method unknown; data provenance unknown; validation evidence unavailable; scope/limitations unassessed**. Source provenance means where the input data came from, its owner and date/version; unknown north or elevation alone is not a source audit. Name the affected hypothesis as untested and a conditional spatial consequence, without asserting that a merely reported file actually exists or passed.

Complete one result-to-action branch now; a menu of possible design questions or a request for files is not that branch. For an explicitly hypothetical sunlight question: **if a validated result shows a daily-use area shaded during its intended use**, compare relocating the activity or changing its schedule with adjusting the shading mass; **if it supports the intended condition**, retain the arrangement and carry the evidence into the indexed plan/section; **if provenance or validation is missing**, keep the hypothesis untested, add the missing evidence/location record and retain the current decision. The current return remains uninspected; any change to a locked choice still needs student confirmation.

State at least one concrete spatial or deliverable consequence, even when the technical result passes. Technical consistency alone is not a design conclusion. Before proposing any locked-decision update, say explicitly that the current locked state remains authoritative until the student confirms the change.

For every inspected return, include at least one visible row:

| Design assumption | Supported / weakened / untested | Return evidence and limitation | Affected Artifact |
| --- | --- | --- | --- |

Do not leave the assumption-status column implicit in surrounding prose.

If the result conflicts with locked decisions, do not silently merge it. Surface the conflict and consequence, name exactly the smallest locked decision that could be reopened, and explicitly ask the student whether to reopen it. Keep the old state until the student confirms the change.

## Degrade honestly when no capability exists

Lead with the operation's actual status, for example: **“本次尚未运行日照模拟，未生成或核查模拟结果；依赖模拟的判断仍待验证。”** Use the true operation and distinguish any prior user-supplied results. A future handoff, manual approximation, or “if untested” branch does not report what happened in this session.

Return three things:

1. the full completed handoff contract from this reference, not a prose summary;
2. a short manual workflow using tools the student actually has;
3. an acceptance and verification checklist.

Render them under the visible headings **能力移交**, **人工路径**, and **验收清单** so a missing capability cannot collapse into generic advice.

Continue with reversible design reasoning while the specialist result is absent. Mark dependent claims as pending. Never claim to have searched, measured, mapped, modeled, rendered, calculated, exported, or verified something that was not actually produced and inspected.
