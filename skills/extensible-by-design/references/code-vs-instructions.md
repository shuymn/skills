# Code vs Instructions: Two Planes of Extension

The same word "extension" hides two different things. Mixing them creates unmaintainable systems — code that encodes policy, or prose that pretends to execute.

## The Two Planes

| Plane | What it is | Typical author | Change frequency | Verification |
|-------|------------|----------------|------------------|--------------|
| **Code** | Typed, executable, side effects | Engineers, generated code | Low–medium | Tests, types, runtime errors |
| **Instructions** | Natural language, declarative guidance | Domain experts, operators, AI | High | Outcomes, spot checks, evals |

**Code plane** answers: *How does something run?* API calls, auth, file I/O, event handlers, data transforms.

**Instruction plane** answers: *What should happen and under what criteria?* Policies, checklists, tone, escalation rules, analysis frameworks.

## Decision Tree

```
Is the change primarily about HOW something executes?
  YES → Code plane (plugin, hook handler, adapter, script)
  NO  ↓

Is the change primarily about WHAT to decide or prioritize?
  YES → Instruction plane (playbook, skill, prompt template, policy doc)
  NO  ↓

Does it need both?
  YES → Split: thin code shell + instruction artifact the shell loads
  NO  → Re-examine; one plane usually dominates
```

## Split Pattern (recommended default)

When a feature needs both:

1. **Code** provides: invocation entry point, I/O, safety boundaries, provenance metadata
2. **Instructions** provide: domain rules, examples, edge-case handling prose
3. **Contract**: code loads instructions by reference; instructions never call APIs directly

Examples across domains:

| Domain | Code plane | Instruction plane |
|--------|------------|-------------------|
| Support bot | Ticket API, auth, tool routing | Escalation policy, brand voice |
| Data pipeline | Connectors, schema validation | Column mapping rules, quality thresholds |
| Code review agent | Git integration, diff parser | Review checklist, severity rubric |
| CMS | Publish workflow, permissions | Editorial guidelines, SEO checklist |

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| Policy encoded in `if` chains | Every policy change needs a deploy | Extract conditions to instruction or config layer |
| "Smart" prompts that perform I/O | No type safety, hard to test, opaque failures | Move I/O to code; prompt receives structured input |
| Giant plugin with embedded copy | Marketing text in TypeScript | Plugin loads markdown at runtime |
| Instruction-only "integrations" | Agent hallucinates API behavior | Code plane owns the actual integration |

## Progressive Disclosure for Instructions

Instruction-plane artifacts should follow:

- **Resident**: name + one-line purpose (what it does, when to use)
- **On demand**: full body, examples, edge cases (loaded when task matches)

This mirrors how agents should treat skills, playbooks, and runbooks — not how core should treat configuration.

## Review Questions

Ask when evaluating a proposed extension:

1. If the domain expert rewrites this tomorrow, is that a code change or a doc change?
2. Can two teams fork the guidance without forking the runtime?
3. Does the code layer stay stable when policies churn weekly?
4. Can an AI agent author and hot-reload the instruction layer safely?

If answers skew toward "doc change" and "yes to fork," keep judgment out of core code.
