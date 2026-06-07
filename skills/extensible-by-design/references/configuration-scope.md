# Configuration Scope: Fit the Application

Configuration boundaries are not universal. Do **not** require every system to support local / project / global / org settings. First identify who owns variation in this application, then design the smallest scope model that preserves safety and useful customization.

## Start With Ownership, Not a Hierarchy

Ask:

1. Who needs to change this behavior independently?
2. Does the change affect only one user, one workspace/project, one team/org, one deployment, or all users?
3. What happens if two owners disagree?
4. Does the system need runtime overrides, install-time defaults, or only explicit parameters?
5. Is provenance needed for audit/debugging, or is a single effective value enough?

Only introduce a scope when it corresponds to a real owner or lifecycle boundary.

## Common Scope Models

| Application shape | Often enough | Add more scopes only if... |
|-------------------|--------------|----------------------------|
| Single-user CLI | Flags + one user config | Projects need committed shared behavior |
| Repo-based developer tool | Defaults + repo config + optional user overrides | Organizations enforce policy across repos |
| SaaS workspace app | Workspace config | Individual preferences or enterprise policy differ |
| Enterprise platform | Tenant/org policy + workspace/project overrides | Personal overrides are safe and expected |
| Library/framework | Constructor/options + environment defaults | Consumers need plugin/package composition |
| Embedded appliance | Build/deployment config | Operators can safely change behavior post-deploy |

These are illustrative, not prescriptions. Translate the boundary names to the user's domain.

## When Multi-Scope Composition Is Justified

Use multiple scopes when at least two are true:

- Different owners legitimately customize the same behavior.
- Settings need different lifecycles (committed with project vs private per user vs centrally managed).
- Conflict resolution can be explained in one precedence table.
- Users or agents must inspect where an effective value came from.
- Safety or compliance requires non-bypassable higher-level policy.

If only one actor changes the value, prefer one config surface.

## Provenance and Precedence

When multiple scopes exist, document:

- Scope names in the application's own language
- Precedence order and whether higher scopes can lock values
- Merge semantics: replace, deep merge, append, or deny-on-conflict
- How to inspect the effective config and its source
- Failure mode for invalid or conflicting config

Avoid generic defaults like `global > project > local` unless those boundaries are real in the product.

## Anti-Patterns

| Anti-pattern | Problem | Better |
|--------------|---------|--------|
| Universal local/project/global stack | Adds ceremony to apps without those ownership layers | Derive scopes from actual owners |
| Scope for every directory or object | Debugging effective values becomes impossible | Put boundaries at stable lifecycle points |
| Hidden overrides | Users cannot explain behavior | Show effective config with provenance |
| Precedence copied from another tool | Wrong mental model for this domain | Name scopes after domain concepts |
| Org policy as ordinary lower-precedence config | Compliance can be bypassed accidentally | Separate enforceable policy from preferences |

## Review Prompt

When reviewing a design, say:

> "This system needs <scope list> because <owners/lifecycles>. It does **not** need <omitted scope> because <reason>. Conflict resolution is <rule>, and users can inspect provenance via <mechanism>."

If that sentence cannot be completed concretely, the scope model is probably speculative.
