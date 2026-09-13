# Research Basis for Protection-First Test Pruning

Last source check: **2026-07-28**.

Use this reference for disputed verdicts or research rationale. Operational gates live in `../SKILL.md`; practical edge cases live in [decision cases](decision-cases.md). Source dates below are the existing research record, not a claim that sources were rechecked during an instruction-only revision.

## Synthesis

The available evidence does **not** support a universal detector for “meaningless tests.” The defensible unit of analysis is the protection a test supplies: a current contract, an observable outcome, and a realistic fault it can detect.

The skill therefore combines these practices:

1. **Trace tests to current contracts and risks.** A test body is not authoritative evidence of the intended product. Requirements, public contracts, incidents, and risk controls outrank current implementation.
2. **Treat smells and authorship as candidate generators.** Tautologies, mock-only assertions, broad snapshots, duplication, flakiness, removed-feature vocabulary, and AI authorship justify inspection, not deletion.
3. **Test behavior at stable boundaries.** Public behavior and state usually survive harmless refactoring better than private calls, source text, and interaction order.
4. **Prove semantic redundancy, not visual similarity.** Equal coverage or similar code cannot show that two tests detect the same faults. Input partitions, observers, layers, and diagnostic value also matter.
5. **Use fault sensitivity as evidence, with limits.** Mutation testing or a controlled fault probe can show whether a test reacts to a plausible semantic break. Equivalent/irrelevant mutants and incomplete mutation operators prevent mutation score from being an oracle of product correctness.
6. **Classify negative space by its current contract.** “The user cannot access X” may be a durable security or API contract. “Private symbol X is absent” is usually implementation history. The word “removed” alone decides neither case.
7. **Make deletion a gated, incremental change.** Test-suite reduction can lose fault-detection capability. Baselines, narrow batches, retained replacements, fault probes, and broader regression checks limit that risk.
8. **Counter implementation anchoring in agent-written tests.** An LLM shown buggy code can reproduce its behavior in the expected result. Deriving the oracle from an independent specification is more important than whether an agent or human wrote the test.

## Authoritative and Primary Sources

### Testing principles and maintenance

- **JSTQB, Foundation Level Syllabus v4.0, official Japanese translation** (syllabus dated 2023-04-12; current official download checked 2026-07-28): [PDF](https://www.jstqb.jp/wordpress/wp-content/uploads/2026/02/CORE-FOUNDATION-FL%E3%82%B7%E3%83%A9%E3%83%90%E3%82%B9CTFL.pdf).
  - Testing can reveal defects but cannot prove their absence.
  - Exhaustive testing is infeasible; techniques, prioritization, and risk-based testing focus effort.
  - Repeating the same tests can lose defect-finding effectiveness, while repeated regression tests can still be useful.
  - Testing is context-dependent.
  - Traceability supports coverage evaluation and change-impact analysis.
  - Maintenance-test scope depends on change risk, system size, and change size.
  - **Skill consequence:** neither “green” nor “old/repeated” is a deletion verdict; traceability and risk are explicit gates.

- **Software Engineering at Google, Chapter 12: Unit Testing** (Google/Abseil, 2020): [chapter](https://abseil.io/resources/swe-book/html/ch12.html).
  - Recommends testing through public APIs, testing state rather than implementation interactions, and organizing tests around behaviors rather than methods.
  - Notes that some redundancy across a support library and its consumers can be valuable.
  - **Skill consequence:** implementation coupling is normally rewritten, while cross-layer duplication is evaluated rather than automatically collapsed.

- **Google Testing Blog**:
  - [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html) (2013-08).
  - [Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html) (2015-01).
  - [Don't Put Logic in Tests](https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html) (2014-07).
  - [Flaky Tests at Google and How We Mitigate Them](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) (2016-05) and [Where do our flaky tests come from?](https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html) (2017-04).
  - **Skill consequence:** source mirrors, test logic, and nondeterminism are investigation targets; a flaky failure can expose either a test defect or a real production race, so flakiness alone never licenses deletion.

### Coverage, mutation, and reduction

- **Martin Fowler, “Test Coverage”** (2012-04-17): [article](https://martinfowler.com/bliki/TestCoverage.html).
  - Coverage is useful for finding untested code but weak as a numerical statement of test quality; targets can incentivize low-quality tests.
  - **Skill consequence:** coverage is a discovery signal and cannot prove redundancy.

- **PIT, official mutation-testing documentation**: [overview](https://pitest.org/) and [FAQ](https://pitest.org/faq/).
  - Line/branch coverage says code executed; mutation asks whether tests detect injected behavior changes.
  - **Stryker, official documentation**: [overview](https://stryker-mutator.io/docs/) and [equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/).
  - Equivalent mutants cannot be killed because they preserve observable behavior.
  - **Skill consequence:** use narrow realistic mutants as evidence, review surviving mutants, and avoid a “kill every mutant” target.

- **Rothermel, Harrold, von Ronne, and Hong, “Empirical studies of test-suite reduction”** (Software Testing, Verification and Reliability 12(4), 2002): [DOI 10.1002/stvr.256](https://doi.org/10.1002/stvr.256).
  - The reported studies found that reduction can severely compromise fault-detection capability, contrary to earlier results on narrower subjects.
  - **Skill consequence:** deleting a test because the reduced suite remains green or keeps structural coverage is insufficient.

- **Just et al., “Are mutants a valid substitute for real faults in software testing?”** (FSE 2014): [DOI 10.1145/2635868.2635929](https://doi.org/10.1145/2635868.2635929), [author-hosted PDF](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014.pdf).
  - Found a statistically significant relationship between mutant and real-fault detection in its subjects, while also finding uncoupled real faults and limitations in common mutation operators.
  - **Skill consequence:** mutation is stronger evidence than structural coverage for a chosen fault class, but it is not proof of complete real-world protection.

## Current LLM-Test Evidence

These 2026 papers were available as **arXiv preprints** at the source-check date. They are timely but not treated as settled, peer-reviewed fact; the skill uses their shared direction only as a conservative guardrail.

- **Zhao, Zhou, and Cohen, “Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests”** (2026-07-24): [arXiv:2607.22883](https://arxiv.org/abs/2607.22883).
  - Reports that buggy code can steer generated tests toward asserting the bug and that specification-based prompting mitigated this effect in the study.
  - **Adopted guardrail:** rank independent current specifications above implementation-derived expectations.

- **Zhao, Zhou, and Cohen, “Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness?”** (replicability study, 2026-07-24): [arXiv:2607.22880](https://arxiv.org/abs/2607.22880).
  - Reports context-dependent usefulness for coverage and mutation: more informative in regression-style settings with reasonably bug-free code, unreliable as indicators when the supplied code may already contain the target bug.
  - **Adopted guardrail:** never let proxy metrics override uncertainty about the oracle.

- **Haroon, Khan, and Gulzar, “Evaluating LLM-Based Test Generation Under Software Evolution”** (2026-03-24): [arXiv:2603.23443](https://arxiv.org/abs/2603.23443).
  - Reports sensitivity to semantic-preserving syntactic change and residual alignment with old behavior under semantic change.
  - **Adopted guardrail:** inspect evolution history and current contract; do not infer obsolescence from surface vocabulary alone.

- **Berndt et al., “On the Flakiness of LLM-Generated Tests for Industrial and Open-Source Database Management Systems”** (2026-01-13): [arXiv:2601.08998](https://arxiv.org/abs/2601.08998).
  - Reports slightly more flakiness in generated tests in the studied systems, frequent reliance on unspecified order, and transfer of flakiness from prompt examples.
  - **Adopted guardrail:** repeat suspected flakes, inspect ordering and shared context, and repair rather than delete by origin.

- **Bruches et al., “TAM-Eval: Evaluating LLMs for Automated Unit Test Maintenance”** (2026-01-26): [arXiv:2601.18241](https://arxiv.org/abs/2601.18241), [benchmark repository](https://github.com/trndcenter/TAM-Eval).
  - Reports limited capability and marginal test-effectiveness improvements in realistic file-level creation, repair, and update scenarios.

- **Sun et al., “SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?”** (2026-05-21): [arXiv:2605.22175](https://arxiv.org/abs/2605.22175).
  - Uses mutated solutions to expose superficial, weakly discriminating generated test suites.
  - **Shared consequence:** agent output still needs repository context, an independent oracle, and executable challenge evidence.

## Japanese Practitioner Evidence

These sources establish local practice and workflow patterns, not universal empirical results.

- **NewsPicks QA Engineering, “あれほど頼れるAIが、しょっぱいテストケースを作ってくる理由を考えた”** (2026-05-21; updated 2026-06-09): [Qiita](https://qiita.com/yurizono/items/43a93d8ff3f7046b31e3).
  - Reports that project documents alone missed existing-feature, user-type, and incident context; a maintained product-specific specification database improved AI-assisted test design.
  - **Skill consequence:** search beyond the focal implementation and escalate when current product context is unavailable.

- **COMPASS/Qubena, “退屈なことはAIにやらせよう（ミューテーションテスト編）”** (2025-07-14): [Zenn](https://zenn.dev/qubena/articles/8a5182abae2b46).
  - Describes an agent parsing mutation reports, relating surviving mutants to proposed table-driven cases, and leaving review to developers; also reports runtime and operational cost.
  - **Skill consequence:** use mutation as structured evidence and preserve a human-reviewable relationship between fault and test. Tool-specific or anecdotal claims were not generalized.

## Public Agent Instructions Surveyed

These are implementation examples, not research evidence.

- **obra/superpowers, `writing-good-tests.md`** (snapshot `3dcbd5c4`, 2026-07-23): [permalink](https://github.com/obra/superpowers/blob/3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9/skills/test-driven-development/writing-good-tests.md).
  - Useful pattern: require a test to name the production break it catches, prefer real behavior, and perform a mental mutation check.

- **Trail of Bits skills, property-based test reviewing** (snapshot `cfe5d7b1`, 2026-06-30): [permalink](https://github.com/trailofbits/skills/blob/cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af/plugins/property-based-testing/skills/property-based-testing/references/reviewing.md).
  - Useful candidate taxonomy: tautological, vacuous/over-filtered, weak, and reimplemented properties, followed by mutation-oriented challenge examples.

- **GitHub Awesome Copilot, Universal Janitor** (snapshot `b94ae92a`, 2026-07-28): [permalink](https://github.com/github/awesome-copilot/blob/b94ae92ab0a6fa695803f1b79b2e41a904a237db/agents/janitor.agent.md).
  - It recommends deleting obsolete, duplicate, flaky, or meaningless tests and validating removals. It does not define enough contract, risk, or equivalence evidence for safe deletion.
  - **Rejected pattern:** an aggressive deletion objective plus a green suite. The protection map and deletion gate replace it.

## Limits

- No static smell, score threshold, or provenance label can establish meaninglessness in every repository.
- Mutation operators model selected fault classes; equivalent mutants and unmodeled faults remain.
- Product risk and contract ownership are repository-specific and may require a human decision.
- The current LLM evidence is fast-moving and several cited results are preprints; rerun the source check when revising policy, claiming numerical thresholds, or applying this skill in regulated/high-assurance systems.
