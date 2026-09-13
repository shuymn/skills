---
name: adversarial-verify
description: "Stress-test implementation changes with concrete edge-case, failure-path, security, and concurrency probes. Report vulnerabilities without fixing production code."
allowed-tools: [Read, Bash, Grep, Glob, Write]
---

# Adversarial Verify

Verify target files against a change description and its impact. Accept repository-relative target paths and a risk tier: Critical, Sensitive (default), or Standard. Infer missing context from the repository when reliable; ask only for material gaps.

## Boundaries

- Do not modify implementation code. Write only attack tests and `adversarial-report.md`; keep tests separate from production tests (`*_adversarial_test.*` or a dedicated directory).
- Run destructive fault simulations only in isolated disposable environments. External systems and data require explicit authorization.
- Missing target files, required references, or essential probe runtime are `BLOCKED`, not a passing verification. Optional analysis tools may be unavailable without blocking executable probes.
- Do not repair vulnerabilities or edit this skill's vectors during verification. Include reusable new vectors as separate maintenance suggestions in the report.

## Select and probe

Read the target files and [attack vectors](references/attack-vectors.md), including matching maintainer extensions. Select categories from actual attack surfaces and defect impact, not labels alone. Read [coverage and verdict rules](references/coverage.md) for the chosen tier before executing probes.

Design concrete probes that can distinguish defended behavior from a violation. Execute them and retain reproducible evidence: vector, test path, command, exit code, observed result, and why it demonstrates `DEFENDED` or `VULNERABLE`. A zero exit code alone is not proof of defense. Test unrelated surfaces independently where useful; choose delegation depth by risk and uncertainty, not a fixed reviewer count.

Required coverage is a floor, not a substitute for probing relevant non-required vectors. Do not claim success for unexecuted or inconclusive probes.

## Report

Write `adversarial-report.md` using repository-relative artifact paths and actual reproducible commands. Include:

- Metadata: mode `adversarial-verify`, target files, change scope, risk tier, UTC verification timestamp, overall `PASS` / `FAIL` / `BLOCKED`.
- Attack summary: category/vector, required status, test path, command, exit code, `DEFENDED` / `VULNERABLE` / `BLOCKED`, and evidence. Include N/A coverage rationales.
- Vulnerabilities: severity, reproduction steps, and suggested fix; do not conflate a tooling failure or coverage gap with a demonstrated vulnerability.
- Decision: coverage assessment, verdict rationale, untested surfaces and blockers, and specific next action. `PASS` means the executed probes were defended and required coverage was satisfied, not that no vulnerability exists.
