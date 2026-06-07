---
name: extensible-by-design
description: Design philosophy for AI-native software that agents and humans can extend without bloating core. Use when designing new products, reviewing architecture for extensibility, deciding what belongs in core vs extensions, choosing between code and instruction layers, or when the user asks to make software self-extensible, avoid feature bloat, or apply extensibility-by-design principles.
allowed-tools: [Read, Grep, Glob]
---

# Extensible by Design

Software is not a finished artifact — it is a platform that AI and humans extend over time. The design question shifts from "what features to build" to **what to leave out of core and where to expose extension surfaces**.

This skill is **application-agnostic**. It captures transferable design philosophy, not any single harness or framework.

## When to Apply

- Greenfield product or subsystem design
- Architecture review: "Is core too fat? Are extension points missing?"
- Choosing how to add a capability (core, plugin, config, playbook, hook)
- Evaluating whether AI self-modification loops are possible

## Quick start

User: "Review our order API for extensibility."

1. **Frame** — core = order CRUD + auth; extensions = none; discounts hardcoded in service layer.
2. **Score** — rate all eight principles STRONG / PARTIAL / MISSING with one sentence each.
3. **Lens** — load a reference only when needed (e.g. [intervention-points.md](references/intervention-points.md) for hook placement).
4. **Deliver** — scorecard + prioritized recommendations using [review-output-format.md](references/review-output-format.md).

## Eight Principles

| # | Principle | One-line test |
|---|-----------|---------------|
| 1 | **Minimal core, maximal extension surface** | Core runs with zero extensions; extensions add depth, not prerequisites |
| 2 | **Negative space defines the contract** | "We do not build X in core" is an explicit design decision |
| 3 | **Separate what runs from what guides** | Execution (code) and judgment (instructions) live on different planes |
| 4 | **Context is a budget** | Only summaries stay resident; details load on demand |
| 5 | **Hooks, not hooks everywhere** | Named pipeline stages with clear precedence — not arbitrary interception |
| 6 | **Multi-scope composition with provenance** | Personal, team, org, and package extensions compose; origin resolves conflicts |
| 7 | **Self-modification loop** | An agent can author an extension, apply it, and verify without a release cycle |
| 8 | **Exploration over linearity** | Branching, retry, and alternate paths are first-class state |

## Workflows

Run when the user asks for an extensibility review or during design discussions.

### Step 1 — Frame the system

Identify: core runtime, primary user/agent loop, existing extension mechanisms (if any), and what is currently hardcoded.

### Step 2 — Score each principle

For each principle, assign **STRONG**, **PARTIAL**, or **MISSING** with one sentence of evidence.

### Step 3 — Apply decision lenses

Load reference files only when a lens needs depth.

| Lens | Question | Reference |
|------|----------|-----------|
| Negative space | What should explicitly *not* live in core? | [negative-space-checklist.md](references/negative-space-checklist.md) |
| Two planes | Is this execution logic or judgment guidance? | [code-vs-instructions.md](references/code-vs-instructions.md) |
| Intervention | At which pipeline stage should extensions act? | [intervention-points.md](references/intervention-points.md) |

### Step 4 — Recommend

For each PARTIAL or MISSING principle, propose one concrete change. Prefer:

- Declaring negative space over adding core features
- A new hook or scope over a hardcoded branch
- An instruction-plane artifact over code when judgment changes often

Format output per [review-output-format.md](references/review-output-format.md). Do not recommend copying any specific product's API — translate principles to the user's domain.

## Quick Decision Guide

**Put in core only when ALL are true:**

- Required for every session with no extension installed
- Wrong or unsafe if left to third parties without guardrails
- Stable contract unlikely to need per-user or per-team variation

**Prefer extension surface when ANY are true:**

- Domain teams or AI agents will customize behavior
- The capability is optional or competes with alternatives (MCP vs native plugin vs script)
- Judgment rules change faster than execution infrastructure
- Users need to fork, branch, or experiment without breaking others
