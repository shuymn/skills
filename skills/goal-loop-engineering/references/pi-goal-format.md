# pi Goal Format

Applies to the `goal` command and tool from `shuymn/pi-extensions`, not a built-in pi or Codex command. When its source is available, check `extensions/compact/goal.ts` (`parseGoalStart`, `goalContext`) and `extensions/compact/runtime.ts` (command handler) for contract changes.

## Copyable command

Return one single-line command:

```text
/goal start <objective and necessary execution context> | <final condition 1> | <final condition 2>
```

The first segment becomes `objective`; every subsequent segment becomes a separate `doneWhen` item. At least one nonempty final condition is required. Each must describe a verifiable final state, not a checkpoint instruction.

All ASCII `|` characters are separators, including those inside quotes, backticks, shell pipelines, or Markdown tables. There is no escaping. Rephrase literal pipes in prose or refer to an existing file containing the exact material. Keep every segment nonempty; omit trailing separators.

Put essential scope, checkpoint guidance, and source or progress-record paths in the objective segment, before the first separator. The parser has no separate context field and collapses whitespace: appended paragraphs would become part of the last completion condition. Keep the command self-contained; explanation outside the code block is not submitted with it. Reference an existing plan for lengthy details rather than creating a file just to format the prompt.

Example:

```text
/goal start 設定保存後も選択テーマを保持する不具合を修正する。再現と保存・復元の経路を検証可能な単位で進め、失敗は範囲内で修正する。 | テーマ変更後に再起動したとき、選択したテーマが復元されることを回帰テストで確認できる | リポジトリで要求される変更対象の検証がすべて成功し、結果が報告されている
```

## Execution semantics

The user submits `/goal start` to authorize execution. Bare `/goal` shows status; `/goal <free-form objective>` does not start work. The LLM-facing `goal` tool cannot start or resume a Goal.

The extension supplies authoritative structured Goal state and tool instructions to the executing agent: `complete` requires evidence for all `doneWhen` conditions; `wait` precedes required human input or approval; `stop` pauses. Rely on those instructions rather than copying the tool protocol into every task prompt.

Paused, waiting, or continuation-limited Goals require the user's `/goal resume`. Prompt wording cannot grant automatic resumption or bypass the continuation limit. Goal status is not an editable checkpoint log; use an existing progress record when checkpoint details need to survive compaction, while leaving execution authority in the structured session state.

For an unresolved decision, return a plain planning-only prompt unless a planning command is confirmed in the target environment.
