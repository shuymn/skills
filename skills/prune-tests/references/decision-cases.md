# Test-pruning decision cases

These cases refine the protection map and deletion gate in `../SKILL.md`; none is an automatic deletion rule.

## Changed contracts and negative space

- A test demanding deliberately removed behavior is stale only when an authoritative current removal decision and replacement behavior are independently established. Account for incident, migration, and compatibility obligations before deleting or rewriting it.
- A test disagreeing with implementation without an authoritative change decision is a product-contract conflict: `ESCALATE`.
- A test requiring something to remain absent protects an **absence contract**, not necessarily an obsolete feature. Keep/rewrite current requirements forbidding access, disclosure, rendering, routes, side effects, or compatibility behavior. Required public `404`/`410` responses, migration tombstones, and incident regressions may remain valuable.
- Prefer observable absence (unauthorized callers receive no data) over private shape (`legacyHandler` is not in a source file). A private-name/comment/file assertion supported only by old implementation or prompt history is a deletion candidate, subject to every gate. Build/artifact or scanner contracts can justify an apparent exception.
- Escalate uncertain deprecation, threat-control, legal, or external-consumer obligations. Neither removal nor prior existence decides whether absence is a permanent requirement.

## Duplication and layers

Compare contract, input partition, observer, realistic break, and test layer—not syntax. Boundary values and incident provenance can make similar rows distinct. Unit and integration coverage may intentionally protect logic and wiring separately. Merge only with equivalent retained protection and negligible lost diagnostic or boundary value.

## Weak or unusual oracles

Tautologies, unreachable assertions, over-filtered properties, assertions that repeat mock setup, source mirrors, and broad snapshots warrant investigation. Even a vacuous test tied to a live unprotected high-risk contract should be rewritten rather than simply removed.

- Replace expectations computed by the production algorithm/helper with independently derived literals, fixtures, properties, or a trusted external oracle.
- Expected exceptions, compile/type tests, and contractual no-crash checks may validly lack ordinary assertions.
- Prefer public behavior/state over private calls or order. Retain observable interaction policies such as charging once, emitting an event, or making no external call.
- Narrow snapshots to intentional consumer-visible contracts. Reviewed goldens, exact messages, ordering, and duplicate outputs remain valuable when protocols or consumers observe them.
- Framework-mechanics tests usually need a project-owned boundary instead. A narrow characterization test can protect an undocumented or historically surprising upstream dependency.

## Flakiness

Repeat on the same revision and distinguish faulty synchronization/isolation/data/oracles from production nondeterminism. Repair the cause; quarantine only under repository policy with an owner. Fixed sleeps, skipped tests, order dependencies, and retries are investigation signals. Flakiness alone never passes the deletion gate.

## Fault evidence

Prefer an already configured mutation tool or a disposable-copy fault probe targeting a plausible contract violation. Compare the candidate and retained set, or show a rewrite passes current behavior and fails the violation. Direct vacuity and exact semantic-overlap proofs are alternatives, not excuses to omit independent contract evidence. Authoritative retirement records can establish that a check is no longer required.

Coverage only tells which code executed. Review killed and surviving mutants against the current contract: equivalent or irrelevant mutants need no new tests, and a killed mutant does not validate an implementation-derived oracle. If the implementation may already be wrong, settle the contract before trusting proxy scores.
