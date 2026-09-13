# Coverage and verdict rules

An implementation target contains runtime implementation code rather than only documentation or test scaffolding.

| Tier | Category selection | Executed probe minimum | Required-vector coverage |
| --- | --- | --- | --- |
| Critical | All applicable categories | 3 | Every `[required]` vector in selected categories: execute or document specific N/A rationale. |
| Sensitive | Input Boundary plus the most relevant additional category; add others when relevant | 2 | Every `[required]` vector in selected categories: execute or document specific N/A rationale. |
| Standard, implementation | Most relevant category | 1 | Cover the most relevant applicable `[required]` vector in the selected category; explain if none applies. |
| Standard, non-implementation | User-selected; invocation optional | None | No mandatory required-vector coverage. |

Where a parent workflow uses risk-tier invocation gates, verification is mandatory for Critical and Sensitive, conditionally mandatory for Standard implementation work, and optional for Standard non-implementation work. This skill does not independently launch itself on unrelated tasks.

If no category appears applicable, use Input Boundary and Error Handling as baselines for Critical/Sensitive, Input Boundary for Standard implementation, and document limited applicability. Never manufacture irrelevant probes to satisfy a count: if meaningful minimum coverage cannot be achieved, report the gap rather than PASS.

Matching maintainer extension vectors are additional probe targets. Non-required vectors still warrant probes when relevant. Expand probing where new evidence reveals attack paths; stop when relevant risks are covered or report remaining uncertainty and resource limits. No numeric cap overrides coverage obligations.

Cross-reference the attack summary against required vectors before deciding:

- **FAIL:** a demonstrated vulnerability or an unexplained required-coverage omission. Report coverage failures separately from vulnerabilities.
- **BLOCKED:** required inputs/runtime are unavailable or probes remain inconclusive for an identified blocker, with no demonstrated failure. Explain the missing evidence and next action. A blocker does not erase an already demonstrated FAIL.
- **PASS:** minimum probe counts and required coverage are satisfied, all executed probes are DEFENDED, and no required execution is blocked. N/A requires a concrete applicability rationale, not lack of tools or budget.
