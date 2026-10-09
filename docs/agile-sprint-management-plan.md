# HazardLens Agile and Sprint Management Plan

**Status:** Proposed team working agreement; whole-team approval pending  
**Applies to:** Five-student HazardLens team  
**Planning horizon:** Approximately eight weeks, subject to confirmation of the course deadline and each student's availability  
**Project controls:** Gate 0 and technical delivery gates remain mandatory and are not replaced by sprint ceremonies.

## 1. Purpose and method

HazardLens will use a **lightweight Scrum-based Agile workflow with GitHub Flow**. This is the proposed operating method, not a claim that the team is already fully practicing Scrum. The team must review and accept this agreement at kickoff before it becomes the team baseline.

Use Scrum's core structure: a Product Goal, a Product Backlog, time-boxed Sprints, a Sprint Goal, a Sprint Backlog, a usable Increment that meets the Definition of Done, and recurring inspection/adaptation. Keep the process proportionate to a five-student academic project; do not add ceremonies or reports that do not help the team coordinate, inspect evidence, or improve delivery.

**Important distinction:** Gate 0 and Gates A–E are governance and dependency/acceptance gates. They are not Sprints. Sprints are time-boxed planning and delivery cycles that may complete work within a gate. A gate only closes when its documented exit criteria are met.

## 2. Scrum accountabilities — proposed mapping

The Scrum Guide defines Product Owner, Scrum Master, and Developers as accountabilities. The following assignments are proposals until the whole team confirms them:

| Accountability / function | Proposed assignment | Responsibility |
|---|---|---|
| Product Owner | Project lead, `@markalvincadangin` (team confirmation required) | Maintain the Product Goal and backlog ordering; clarify value, scope, and acceptance expectations; bring unresolved scope choices to the team. |
| Scrum Master / facilitator | To be confirmed at kickoff; may be a rotating facilitator if the team agrees | Help the team use the process effectively, facilitate events, surface impediments, and improve the workflow. This role is not a task supervisor. |
| Developers | All five students | Plan and perform the work needed for a Done Increment, maintain quality, update the Sprint Backlog, and hold one another accountable. |
| Technical / peer reviewers | Named per issue or PR; reviewer must differ from author | Review implementation and verification evidence. Reviewer assignment is a quality-control function, not a substitute for team ownership. |

The existing three specialization tracks (Data & AI Infrastructure, Interactive GIS & Geolocation, Product UI/UX & QA) are collaboration areas, not Scrum subteams. Each issue still needs one accountable lead implementer and a different reviewer. Confirm availability before treating proposed track allocations as final.

## 3. Sprint length and planning cadence

**Recommendation:** Start with one-week Sprints because the academic project is short and source/API work has uncertainty. The team must confirm the Sprint length, real deadline, weekly availability, and any class/exam constraints at kickoff. Do not create calendar due dates until those facts are recorded.

Each Sprint should include:

1. **Sprint Planning** at the start: establish why the Sprint matters (Sprint Goal), choose feasible Product Backlog items, and plan how to deliver them.
2. **Daily Scrum / progress inspection:** Developers inspect progress toward the Sprint Goal and adapt the plan. If schedules do not permit a live 15-minute meeting every day, the team may agree on an asynchronous daily check-in, but it should still be regular, brief, focused on the Sprint Goal, and followed by direct coordination when blocked. Do not turn it into a status report to the project lead.
3. **Sprint Review** near the end: demonstrate completed work to the team, inspect it against acceptance criteria and the Product Goal, capture feedback, and update the Product Backlog.
4. **Sprint Retrospective** after the review and before the next Sprint: inspect collaboration, tooling, quality, and process; select one or two actionable improvements for the next Sprint.

Planning, review, and retrospective durations should be proportionate to the one-week Sprint. Record decisions and resulting backlog changes in GitHub, not only in chat.

## 4. Backlog and issue workflow

GitHub Issues are the work-item record; the linked GitHub Project is the team's visual status board. The board and issue state must not become competing sources of truth. Delivery-gate milestones group dependency/acceptance phases; they do not represent weekly Sprints. Once the team confirms cadence and dates, use a clear Sprint field or Sprint-specific milestones for iteration planning rather than relabelling gate milestones as Sprints.

### Minimum issue fields

Every implementation issue must state:

- Purpose and user/system outcome.
- Included and excluded scope.
- SRS requirement IDs, where applicable.
- Dependencies and blockers.
- One accountable lead implementer.
- A distinct independent reviewer (`Author != Reviewer`).
- Testable acceptance criteria.
- Verification evidence expected (tests, fixture, screenshot, live-source record, or other reproducible artifact).
- Completion rule and target gate / planned Sprint when known.

Keep issues small enough to review. Split work that cannot reasonably be completed and verified in one Sprint. Do not start work with unresolved scope or source-contract assumptions that could change its meaning.

## 5. Definition of Ready (team working agreement)

Definition of Ready is a local backlog-quality checklist, not an official Scrum artifact. An item is ready for Sprint Planning when:

- [ ] The outcome and scope are understandable; exclusions are explicit where useful.
- [ ] Relevant SRS requirements and dependencies are linked.
- [ ] Acceptance criteria are observable and testable.
- [ ] Required source/API/data contracts and safety constraints are identified; unknowns are tracked as blockers or research tasks rather than hidden assumptions.
- [ ] The lead implementer and a different reviewer are named and have confirmed availability.
- [ ] The item is sized sufficiently for the team's capacity; it can be split if too large.
- [ ] Required test/verification evidence is clear.
- [ ] It does not violate Gate 0 or another prerequisite gate.

Items that fail this checklist stay in the Product Backlog for clarification; they must not be silently treated as Sprint commitments.

## 6. Definition of Done

A backlog item is Done only when all applicable conditions are met:

- [ ] Acceptance criteria are satisfied and evidence is linked in the issue or PR.
- [ ] Relevant automated tests pass; lint, type checks, and builds pass where applicable.
- [ ] CI passes on the PR head commit.
- [ ] A teammate other than the author reviewed the diff and approved it; review conversations are resolved.
- [ ] API contracts, migrations, documentation, attribution, and configuration are updated when affected.
- [ ] Security, privacy, accessibility, and failure-isolation expectations relevant to the change are verified.
- [ ] No known critical regression is introduced; the change is reproducible in the agreed environment.
- [ ] Requirement traceability and issue status reflect the actual delivered scope.
- [ ] Any live-source verification is distinguished from fixture/mock tests; unknown source semantics remain `UNAVAILABLE`, not guessed.
- [ ] The change complies with the active delivery gate and approved scope.

A green CI run alone does not mean a feature is Done, and closing an issue does not itself close a delivery gate. Gate closure requires its own exit evidence and approval.

## 7. HazardLens-specific planning and quality rules

- Keep **evidence before AI**: do not start AI/provider work until the first evidence vertical slice and all four required hazard sources are verified, per the current working scope.
- Preserve the five evidence states and their semantics: `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, `UNSUPPORTED`.
- Do not claim live-source reliability based on recorded fixtures or mocks.
- Keep FR-02 persistence/history in the MVP release scope even though it is not required in the first vertical slice.
- FR-11 comparison, FR-12 printable report, and FR-20 polygon/area investigation remain post-MVP in the project-lead working direction until the team formally confirms or changes that scope.
- Keep the weather card (FR-13) separate from hazard evidence and implement FR-21 failure isolation if retained in MVP scope.
- Do not begin additional feature implementation until Gate 0 is formally closed.
- A scope, architecture, source, schema, or requirement change must be reviewed and recorded in the decision log, with SRS and traceability updates made in the same review cycle where relevant.

## 8. Sprint health and reporting

At Sprint Planning, record the Sprint Goal, selected issues, owners/reviewers, dependencies, and capacity assumptions. During the Sprint, keep issue status current and flag blockers early. At review, report:

- Sprint Goal: met / partially met / not met, with reasons.
- Issues accepted as Done and links to their evidence.
- Work not Done, why it remains incomplete, and its updated backlog state.
- New risks, source/API findings, and decisions required.
- Whether any scope or dependency assumption changed.

Do not use story points or velocity as individual performance measures. For this small team, forecast using available student time, issue size, dependencies, and observed completion history. Avoid carrying unfinished work forward automatically; re-plan it explicitly.

At the Retrospective, record one or two process improvements with an owner and a check-in point. Review the risk register at kickoff and at least once per Sprint.

## 9. Gate 0 approval checklist

Before Gate 0 can close, the team must:

- [ ] Review and accept or amend this Agile/Sprint working agreement.
- [ ] Confirm the Product Goal, Product Owner, Sprint facilitator, Sprint length, real deadline, and availability/capacity.
- [ ] Confirm all issue lead/reviewer pairings and ensure reviewers differ from authors.
- [ ] Confirm the SRS, release scope, task matrix, traceability, schema strategy, and source contracts are internally consistent.
- [ ] Verify repository branch protection / required CI and review rules rather than relying on documentation alone.
- [ ] Verify clean-checkout setup and required local checks.
- [ ] Resolve the two remaining organization invitations, according to the project lead's latest confirmation, and ensure the delegation matrix uses current GitHub identities.
- [ ] Record whole-team approval and any amendments in GitHub / the decision log.

Until these conditions are evidenced and Gate 0 is explicitly closed, additional feature implementation remains paused.

## 10. Reference

- [The Scrum Guide](https://scrumguides.org/scrum-guide.html) — framework accountabilities, events, artifacts, and commitments.
- [HazardLens Project Execution Plan](project-execution-plan.md)
- [Project Readiness Checklist](project-readiness-checklist.md)
- [Release Scope and Dependency-Aware Task Matrix](release-scope-and-task-matrix.md)
- [Decision Log](decision-log.md)
- [Contributing Guide](../CONTRIBUTING.md)
