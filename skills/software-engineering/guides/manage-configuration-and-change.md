# Manage Configuration and Change

## Use When
- Versioning code, data, assets, documents, dependencies, environments, or releases.
- Evaluating and implementing change requests.
- Establishing continuous integration, audit, and status reporting.

## Required Context
- Configuration items, repository, branches/versions, build/deployment process, and access needs.
- Baselines, release policy, dependency graph, approval authority, and change priorities.
- Required traceability, audit, rollback, and regulatory evidence.

## Instructions
1. Identify software configuration items: source, data, models, tests, build scripts, dependencies, environment definitions, documentation, and release artifacts needed for reproducibility.
2. Establish naming, versioning, storage, access, backup, integrity, and retrieval rules in the repository.
3. Create baselines only after defined review and acceptance; change them through controlled procedure.
4. For each change request:
   - Record rationale, requester, urgency, affected requirement, and desired outcome.
   - Perform impact analysis across requirements, architecture, components, interfaces, data, tests, documentation, schedule, cost, and risk.
   - Approve, reject, defer, or request clarification through defined authority.
   - Assign implementation and verification.
   - Update linked configuration items and status.
5. Integrate frequently enough to expose conflicts and dependency problems; use automated build and tests where practical.
6. Audit configuration before release: correct versions, approved changes, completed tests, documentation, dependencies, and reproducible build.
7. Report status of baselines, changes, versions, builds, audits, and unresolved deviations.
8. For content-heavy/mobile/web systems, control content, publishing, environment, and platform variants with the same rigor as code.
9. Preserve rollback or recovery paths for releases and migrations.

## Decision Rules
- If an artifact can change product behavior or release reproducibility, place it under configuration control.
- If a change crosses a baseline, require impact analysis and authorization proportional to risk.
- If branches remain divergent long enough to hide integration risk, integrate smaller changes more frequently.
- If emergency change bypasses normal flow, require retrospective review, tests, documentation, and baseline correction immediately afterward.
- If generated artifacts are reproducible from controlled sources, version the sources and generation procedure; store generated output only when release or audit needs justify it.

## Constraints
- Never rewrite shared history or destroy recoverability without explicit authorization and backup.
- Do not mix unrelated logical changes in one change set.
- A passing build does not prove the correct configuration was built; audit inputs and versions.
- Secrets and private raw evidence must not enter normal repositories.
- Configuration records must identify who changed what, why, when, and with what verification.

## Failure Modes
- **Cannot reproduce release** — Cause: missing dependency, environment, data, or build control. Correction: inventory and baseline all behavioral inputs.
- **Approved change causes unrelated failure** — Cause: incomplete impact analysis. Correction: inspect dependency and regression scope.
- **Merge crisis** — Cause: long-lived divergent work. Correction: reduce change size and integrate continuously.
- **Status reports disagree with repository** — Cause: manual parallel records. Correction: derive status from controlled workflow and audit discrepancies.

## Verification
- Configuration items and baselines are identifiable and retrievable.
- Change decisions and impact analyses are recorded.
- Builds and releases are reproducible from controlled inputs.
- Required regression and audits pass for the exact release candidate.
- Rollback/recovery has been tested where failure impact warrants it.

## Required Terms
- [Baseline](../glossary.md#baseline) — defines when ordinary edits become controlled changes.
- [Software configuration item](../glossary.md#software-configuration-item) — determines what belongs under SCM.

## Source Locators
- Ch 22 §§22.1–22.7, pp. 438–458.
- Ch 27 §27.2.2, pp. 554–555.
