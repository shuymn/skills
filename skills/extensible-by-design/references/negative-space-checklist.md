# Negative Space Checklist

**Negative space** is what you deliberately do *not* build into core. Declaring it early turns "missing features" into a designed extension contract instead of product debt.

## Core Question

> If we put this in core, can users (or AI agents) no longer add or replace it themselves?

If yes — or if core would need constant churn to satisfy variants — it belongs outside core.

## Checklist: Candidates for Negative Space

For each capability under consideration, mark **Core**, **Extension**, or **External**.

### Workflow and orchestration

- [ ] Multi-step approval flows
- [ ] Plan / explore / review modes
- [ ] Background job scheduling semantics
- [ ] Sub-agent or delegation orchestration

*Typical negative space:* provide hooks and spawn primitives; let extensions or external tools (tmux, queue workers) compose workflows.

### Integration protocols

- [ ] Specific third-party protocol implementations (MCP, A2A, proprietary)
- [ ] Vendor-specific auth flows beyond one generic adapter interface
- [ ] Opinionated tool catalogs tied to one ecosystem

*Typical negative space:* one minimal adapter interface; protocol packs as extensions or packages.

### User-facing policy

- [ ] Permission prompts and consent UX variants
- [ ] Team-specific lint / compliance rules
- [ ] Domain playbooks and checklists

*Typical negative space:* safe defaults + override points; policy as instruction-plane artifacts.

### Productivity features

- [ ] Built-in todo / task systems
- [ ] Note-taking or knowledge bases
- [ ] Dashboards and analytics views

*Typical negative space:* file-based or API-backed conventions extensions can adopt (e.g., TODO.md pattern).

### Presentation

- [ ] Themes, layouts, rich custom UI beyond a component API
- [ ] Report templates for every domain

*Typical negative space:* theming API + template slot; domain templates as extensions.

## What Usually Stays in Core

Keep in core only capabilities that are:

1. **Safety-critical** — auth boundaries, sandbox enforcement, audit logging hooks
2. **Universal** — required on every run (session identity, basic I/O, error propagation)
3. **Stable** — contract changes rarely and affects all extensions equally
4. **Non-delegable** — incorrect behavior if left to unreviewed third parties

When in doubt, start in negative space. Moving from extension → core is easier to justify with usage data than removing from core later.

## Declaring Negative Space (template)

Document explicitly in design docs or README:

```markdown
## Intentionally not in core

| Capability | Why not core | Extension path |
|------------|--------------|----------------|
| <X> | <reason> | <plugin / hook / skill / external tool> |
```

This table is the extension contract's table of contents.

## Review Signals

**Core is too fat when:**

- Feature flags multiply to handle team variants
- "Just one more mode" requests arrive every sprint
- AI agents duplicate logic because they cannot inject at the right layer
- Releases block on optional integrations

**Negative space is working when:**

- New capabilities ship as extensions without core changes
- Teams compose personal + org rules without merge conflicts in core
- AI can scaffold an extension, reload, and test in one session

## Domain Examples (illustrative)

| Application type | Often negative space | Often core |
|------------------|---------------------|------------|
| CRM | Industry-specific pipelines | Contact model, audit trail |
| BI tool | Chart types, domain metrics | Query engine, access control |
| Internal portal | Department homepages | SSO, navigation shell |
| CI platform | Language-specific steps | Job runner, secrets injection |
| Agent harness | Plan mode, MCP, todos | Agent loop, tool contract, session I/O |

These are patterns, not rules — run the checklist against the specific system.
