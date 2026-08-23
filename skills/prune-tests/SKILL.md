---
name: prune-tests
description: "Prunes test-suite sediment without discarding regression protection. Use when the user wants to audit or remove meaningless, vacuous, obsolete, duplicate, brittle, or coding-agent-generated tests, consolidate a test suite, or decide whether tests for removed behavior still protect a current contract."
allowed-tools: [Bash, Read, Edit, Write, Grep, Glob, AskUserQuestion]
---

# Prune Tests by Protection

A smaller suite is useful only when it protects the same current contracts. Build a **protection map** from each targeted test to:

1. a current contract,
2. an observable outcome, and
3. a realistic production break that would make the test fail.

Authorship, generated-looking style, coverage, and a green run are discovery signals, not verdicts. Judge human- and agent-written tests by the same evidence. A green run after deleting a test proves only that the remaining tests pass; it does not prove that the deleted protection was redundant.

## Boundaries

- Change tests, test data, and test-only helpers. Preserve production behavior and public APIs.
- When a test file is generated, edit its test-only generator or source template and regenerate it. Treat an unknown generator as `ESCALATE`; changing a generator shared with production artifacts requires explicit scope approval.
- Keep unrelated working-tree changes intact. Use disposable copies or the project's mutation tool for fault probes rather than mutating production files in the caller's worktree.
- Use `--report-only` when supplied or when the user asked to audit, explain, or propose rather than edit.
- Commits, pushes, PRs, and public comments remain separate, explicitly requested actions.

## 1. Resolve the Scope

Read repository instructions first. Resolve targets in this order:

1. Explicit test files or directories from the user.
2. Tests changed by `--base=<ref>`.
3. Staged tests for `--staged` / `--cached`.
4. Tests in the working-tree change set, including untracked tests.
5. The whole tracked test suite only when the user explicitly requested repository-wide cleanup or passed `--all`.

Pasted tests without a repository path are direct-input, report-only targets: classify only from the supplied contract and context, and return proposed edits without changing unrelated files. Use the repository's test configuration and naming conventions to distinguish tests from fixtures and helpers. Include a helper only when a targeted test depends on it or the helper itself is being consolidated.

Capture `git status` and the relevant diff before editing. In a non-Git workspace, record target paths and content hashes instead; missing history is an evidence gap only when a verdict depends on it. For a test already deleted in the target diff, inspect its base version and treat the deletion as a `DELETE` candidate subject to the same gate.

If the resolved scope is empty, report that fact and stop. If no scope can be inferred and repository-wide work was not requested, ask the user to choose changed tests or the full suite. Scope resolution is complete when every target and any pre-existing local modification to it is listed.

## 2. Establish the Baseline and Protection Map

Discover the narrowest supported test command and run the targeted tests before editing. Also inspect nearby production boundaries, callers, current requirements, and history needed to understand the tests.

Use this evidence order for a test's contract:

1. Product behavior explicitly stated in the user's current request; maintained acceptance criteria, ADRs, schemas, public API contracts, security/privacy/legal rules, and explicit compatibility policy.
2. Maintained product documentation, issue or incident records, changelogs, consumer behavior, and tests at a public boundary.
3. Current implementation and git history as clues only.
4. The test's name or body as a hypothesis only.

The implementation may already be wrong, and an agent can copy that wrong behavior into an oracle. Derive expected behavior independently of the code under test. When implementation and stronger contract evidence disagree, report a product issue and stop pruning that protection.

Inventory every targeted test. Data-driven rows may share one entry only when they protect the same contract and their equivalence partitions and boundaries are explicit. Record:

| Field | Required evidence |
| --- | --- |
| Test | Path and test or row name |
| Contract | Current source, or `unknown` |
| Observer | User/API/state/output/side effect that the assertion observes |
| Break | Specific realistic defect or regression that should fail it |
| Overlap | Other tests that catch that same break, including their layer |
| Risk | Security, privacy, money, data loss, compatibility, migration, incident history, or ordinary |
| Cost/smell | Brittleness, flakiness, runtime, setup, duplication, or weak oracle |

Candidate searches are triage, never automatic deletion. Look for:

- tautologies, unconditional assertions, mirrored expectations, unreachable assertions, and over-filtered property tests;
- calls with no visible assertion, type-only checks, or no-crash checks;
- assertions on private methods, source text, internal call order, mock setup, constants, or broad snapshots;
- names and assertions about removed features, absent symbols, old routes, compatibility, or deprecation;
- repeated inputs and observers, overlapping parameter rows, and the same fixture copied across layers;
- skipped tests, fixed sleeps, order/time/random dependencies, and retry-only stabilization;
- tests of framework behavior without a project-owned boundary contract.

These shapes have legitimate exceptions: expected exceptions and compile/type tests may need no assertion; no-crash may be a contract; an outbound interaction may itself be the contract; and a focused characterization test may protect an upstream assumption.

If the targeted baseline fails, separate pre-existing failures from the requested cleanup. An unexplained failure in the affected scope blocks edits there; produce the protection map and classify as `ESCALATE` rather than making deletion the way to green. If test discovery or execution is unavailable, use the repository's documented non-destructive setup once; missing dependencies, credentials, services, unsupported platforms, hangs, and timeouts then become explicit blockers. Static inspection may still produce candidates, but it cannot support an edit whose gate requires runtime evidence. This step is complete when each targeted test has a filled protection entry or an explicit evidence gap.

## 3. Classify Each Test

Assign exactly one verdict:

| Verdict | Use when |
| --- | --- |
| `KEEP` | It protects a current contract from a distinct realistic break at a useful layer, and its cost is justified. |
| `REWRITE` | The contract is valuable, but the oracle, boundary, setup, or determinism is weak or implementation-coupled. |
| `MERGE` | Another retained test protects the same contract from the same break at the same useful layer, while all meaningful partitions and boundaries remain explicit. |
| `DELETE` | The deletion gate below is fully satisfied. |
| `ESCALATE` | Contract ownership, intended absence, risk, generator source, baseline, or unique protection is ambiguous. |

### Deletion gate

Use `DELETE` only when all four statements are supported:

1. **Contract:** no current contract requires this check, or a named retained test covers that contract.
2. **Sensitivity:** the test catches no unique realistic break, or the retained test catches the same break.
3. **Risk:** no unresolved security, privacy, legal, financial, data-loss, compatibility, migration, or incident-regression reason requires independent protection.
4. **Proof:** a fault probe, direct vacuity proof, exact semantic-overlap proof, or authoritative contract-retirement record supports removal; coverage equality and a green post-deletion run do not stand alone.

An evidence gap changes the verdict to `ESCALATE`, not `DELETE`. Batch material `ESCALATE` questions for the user or contract owner after completing the map; do not interrupt once per test. An explicit request to reduce test count supplies intent, not missing contract or risk evidence.

### Changed and removed contracts

Separate three evolution cases:

- A test that still demands deliberately removed behavior is stale. Once the current removal decision and replacement behavior are independently established, delete it or rewrite it around the replacement; account for any incident, migration, or compatibility protection first.
- A test that demands the removed behavior remain unavailable is a negative-space test; apply the rules below.
- A test that disagrees with current implementation but has no authoritative change decision is an unresolved product-contract conflict. Use `ESCALATE` rather than treating the implementation as proof that the test is obsolete.

### Negative-space tests

A negative-space test says that something is absent. Classify the *absence contract*, not the old feature:

- `KEEP` or `REWRITE` when a current public contract forbids access, disclosure, rendering, routing, side effects, or compatibility behavior. Security/privacy rules, a public endpoint's required `404`/`410`, a migration tombstone, and a recorded regression are concrete reasons.
- Prefer an observable boundary check over grepping source text or naming a private symbol. For example, “unauthorized callers receive no data” protects a contract; “`legacyHandler` is not in this file” usually protects an implementation detail.
- `DELETE` an assertion whose only source is old implementation or prompt history and whose only failure is reintroducing a private name, comment, file, or exact internal shape—after the deletion gate passes.
- `ESCALATE` when the removed capability might be a live deprecation, threat-control, legal requirement, or externally consumed API.

A removed feature does not make every negative test useless, and prior existence does not make absence a permanent requirement.

### Duplication and layers

Syntactic similarity is insufficient for `MERGE`. Compare contract, input partition, observer, break, and layer. Boundary values remain distinct even when bodies look alike. Unit and integration tests for the same behavior may be intentional defense in depth: one localizes logic faults while the other verifies wiring. Consolidate only when the retained protection is demonstrably equivalent and the diagnostic or boundary value of the second test is negligible.

### Oracles, doubles, snapshots, and frameworks

- Rewrite expectations computed with the production algorithm or its helper into independently derived literals, fixtures, properties, or a trusted external oracle.
- Prefer public behavior and state over private calls and interaction order. Keep an interaction assertion when the interaction is observable policy, such as charging once, emitting an event, or making no external call.
- Narrow broad snapshots to intentional consumer-visible contracts. Keep a reviewed golden file when exact serialized output is the contract. Exact messages, ordering, and duplicate outputs also remain when consumers or protocols observe them.
- Replace framework-mechanics tests with a project-owned boundary check. Keep one narrow characterization test when the project depends on an undocumented or historically surprising upstream behavior.

### Flakiness

Run a suspected flaky test repeatedly on the same revision and distinguish a test defect from nondeterminism in production. Repair the synchronization, isolation, data, or oracle; quarantine only under the repository's policy and with an owner. Flakiness alone never satisfies the deletion gate.

### Coverage and mutation

Use coverage to find code that was not executed, not to certify test quality or redundancy. Use an already configured mutation tool or a manual fault probe to ask whether tests detect a plausible semantic break; adding project dependencies or persistent mutation configuration requires separate user approval. Review surviving and killed mutants against the current contract: equivalent or irrelevant mutants need no test, and killing a mutant does not prove the oracle is correct.

## 4. Challenge Every Proposed Change

For each `MERGE` or `DELETE` candidate:

1. State the protection claimed by the candidate.
2. Name the retained test, if any, that replaces it.
3. Choose the strongest feasible proof:
   - run an installed mutation tool narrowly against the relevant production boundary;
   - in a disposable copy, introduce one realistic contract-violating defect and compare the candidate with the retained set;
   - prove vacuity directly (for example, a tautology, impossible generator domain, or an assertion that only repeats behavior configured into a double without observing a project-owned contract);
   - prove exact semantic overlap, including boundary partitions, then run the retained test independently.
4. Recheck the high-risk categories in the deletion gate.

For each `REWRITE`, demonstrate that the replacement passes on current behavior and fails on a realistic contract violation. A test that cannot be made red for the claimed break needs a new classification.

Use current specifications to choose probes. If the code may already contain the bug, mutation and coverage scores are not reliable substitutes for a correct oracle. Challenge is complete only when every proposed edit has reproducible evidence; otherwise move it to `ESCALATE`.

## 5. Apply the Smallest Safe Batches

Skip edits in report-only mode. Otherwise:

1. Apply `REWRITE` and the retained side of `MERGE` before deleting protection.
2. Change one contract cluster at a time.
3. Preserve clear test names, independently derived expectations, boundary partitions, and useful failure diagnostics.
4. Run the targeted test after each cluster and inspect the diff before continuing.
5. Keep production fixes, broad refactors, and unrelated test additions outside this pruning pass; report them separately.

A test may be short or trivial and still valuable. Optimize for distinct protection and maintenance clarity, not deletion count.

## 6. Verify the Result

Run, in order:

1. every changed test file or narrow target;
2. the nearest affected package/module suite;
3. repository-mandated test, type, lint, formatting, and build checks appropriate to the changed scope;
4. the selected mutation or disposable fault probes for every applied `MERGE`/`DELETE` where direct vacuity proof was not sufficient;
5. repeated runs for any flaky test that was repaired;
6. `git diff --check`, then inspect the complete diff and status for unintended production or unrelated changes.

Compare results with the baseline and report pre-existing failures separately. Missing or prohibitively expensive tooling is an explicit limitation, not a reason to claim equivalence; retain or escalate candidates whose deletion depends on that evidence.

The pass is complete when there are no new failures, every applied verdict satisfies its gate, all current high-risk and boundary contracts remain mapped to tests, and no ambiguous candidate was edited.

## Report

Use the user's language and lead with the result:

```markdown
## Test-pruning report

### Summary
- Scope: ...
- Targeted tests: N
- Kept / rewritten / merged / deleted / escalated: ...
- Baseline: ...

### Protection decisions
| Test | Verdict | Current contract and break | Evidence | Change |
| --- | --- | --- | --- | --- |

### Negative-space and high-risk checks
- ...

### Escalations
- Missing evidence, owner question, and safest next step

### Verification
- `command` — PASS/FAIL/BLOCKED
- Fault probe or mutation evidence: ...

### Residual risk
- Unrun suites, unavailable tools, equivalent-mutant uncertainty, or none
```

Report contracts retained, not just lines or tests removed. When the user asks for the research rationale, an unusual verdict needs calibration, or this skill is being updated, consult [the research basis and source caveats](references/research-basis.md).
