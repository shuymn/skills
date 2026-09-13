---
name: prune-tests
description: "Audit or remove obsolete, weak, duplicate, or brittle tests while preserving current contract and regression protection."
allowed-tools: [Bash, Read, Edit, Write, Grep, Glob, AskUserQuestion]
---

# Prune Tests by Protection

Optimize distinct protection and maintenance clarity, not deletion count. Judge each test by its **current contract, observable outcome, and realistic production break**. Authorship, smells, coverage, and a green run are discovery signals—not deletion proof.

## Mode and scope

- `--report-only`, audit/explanation/proposal requests, and pasted tests without a repository path are report-only. An explicit cleanup request authorizes in-scope local edits without a second approval.
- Select targets in order: explicit paths; tests changed by `--base=<ref>`; staged tests for `--staged`/`--cached`; changed and untracked tests. Use the full tracked suite only for `--all` or an explicit repository-wide request. Ask when no scope can be inferred; stop if a resolved scope is empty.
- Include only dependent or explicitly targeted fixtures/helpers. Review already-deleted tests from their base version against the same deletion gate.
- Change only tests, test data, and test-only helpers; preserve production behavior and APIs. Edit generated tests through their generator/template. Escalate an unknown generator; production-shared generators require explicit scope approval.
- Preserve existing edits and record the initial diff/status (or paths and hashes outside Git). Fault probes belong in disposable copies or configured mutation tooling, not production files in the caller's worktree. Commits, pushes, and PRs require separate requests.

## Evidence and decisions

Run the narrowest targeted baseline and inspect the contract at the relevant production boundary. Rank current user requirements, maintained acceptance criteria, ADRs, public schemas/APIs, and security/legal/compatibility rules above documentation and consumer/incident evidence; implementation/history are clues, test bodies are hypotheses. Derive expected outcomes independently of the implementation. A conflict with stronger contract evidence blocks pruning that protection.

Map every target (including meaningful parameter partitions) to contract source, observer, realistic break, overlapping retained tests and layer, risk, and maintenance cost. Record unknowns rather than inventing evidence.

| Verdict | Requirement |
| --- | --- |
| `KEEP` | Distinct current protection at a useful layer. |
| `REWRITE` | Valuable contract with a weak oracle, boundary, setup, or determinism. Replacement must pass current behavior and fail a realistic contract violation. |
| `MERGE` | Named retained test demonstrably covers the same contract, break, partitions, and useful layer; no meaningful diagnostic or defense-in-depth value is lost. |
| `DELETE` | All deletion gates below pass. |
| `ESCALATE` | Contract, risk, baseline, generator, or unique protection remains uncertain. Do not edit that candidate. |

### Deletion gate

Every deletion, including a merge's removed protection, needs all four:

1. No current contract requires the check, or a named retained test covers it.
2. No unique realistic break is lost; retained protection detects the same break where applicable.
3. No unresolved security, privacy, legal, financial, data-loss, compatibility, migration, or incident-regression obligation requires independent protection.
4. Reproducible proof: a realistic fault probe, direct vacuity proof, exact semantic-overlap proof, or authoritative contract-retirement record. Green runs and equal coverage do not suffice.

For overlap proof, account for boundary partitions and run retained tests independently. For runtime comparison, probe candidate and retained sets with the same contract-violating defect. Mutation scores never establish that an oracle is correct; equivalent/irrelevant mutants need no test. An evidence gap means `ESCALATE`, even when the user requested fewer tests.

## Conditional guidance

- For removed behavior, absence assertions, cross-layer duplication, mirrored oracles, snapshots, no-assertion tests, flakes, or framework checks, read [decision cases](references/decision-cases.md) before classifying them.
- For disputed/unusual verdicts or research questions, read [research basis and caveats](references/research-basis.md). Operational decisions do not require loading the bibliography.

## Apply and verify

In edit mode, establish replacement protection before removal. Use small contract-focused batches and validate affected tests and the nearest suite, plus repository-required checks appropriate to scope. Preserve independent expectations, meaningful boundaries, clear names, and useful failure diagnostics. Keep production fixes and unrelated additions out of this pass.

Unexplained baseline failures block edits in the affected scope; deleting a failing test is not a repair. If execution is unavailable, try documented non-destructive setup within authorization, then report blockers. Adding dependencies or persistent mutation configuration needs approval. Retain/escalate candidates whose proof requires unavailable runtime evidence; static candidates remain reportable.

Inspect the final diff for unrelated/production changes and whitespace errors. Compare validation with the baseline; run relevant fault probes on the retained/replacement set and repeat repaired flaky tests. Do not repeat equivalent checks without new changes or uncertainty. Completion requires no new failures, evidence for every applied verdict, preserved high-risk/boundary protection, and no edits to ambiguous candidates.

## Report

Report scope and verdict counts; a table of test, verdict, contract/break, evidence, and change; high-risk and negative-space protection retained; validation commands/results and fault-probe evidence; and blockers or owner questions with the safest next step. Batch material questions rather than interrupting per test. Distinguish proposed decisions from applied edits and unverified claims from proven equivalence.
