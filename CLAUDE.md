# kronobot-backend

Backend application for Kronobot.

## Workflow: spec-driven development

Work is planned before it is implemented. Every task starts as a plan file in [plans/](plans/) before any code is written.

### Plan files

- Location: `plans/`
- Naming: `<ticket-number>_description-of-the-task.md` (e.g. `1_setup-project-skeleton.md`)
- One file per ticket/task. Use the template at [plans/_TEMPLATE.md](plans/_TEMPLATE.md) as the starting structure.

### Process

1. Before implementing a task, create or update its plan file in `plans/` describing the approach.
2. Get the plan reviewed/approved before writing code.
3. Implement according to the approved plan.
4. Keep the plan file up to date if the approach changes materially during implementation.

## Notes for Claude

- This repo is currently a skeleton — no framework/stack has been chosen yet. Do not assume a language or framework; confirm with the user before scaffolding.
- Always check `plans/` for an existing plan matching the ticket before starting new work.
- **Do not confuse Claude Code's built-in plan mode with this repo's `plans/` convention.** When plan mode is active, it drafts to a scratch file under `~/.claude/plans/` purely for interactive approval — that file is never the deliverable. Once a plan (whether drafted via plan mode or written directly) is finalized, its content must be written into `plans/<n>_description-of-the-task.md` in this repo. That is the only place a plan is considered "stored."
- When the user asks to "create a plan" for a ticket, the end state to aim for is always a file under `plans/` — if plan mode's approval flow is used along the way, treat that as a review step, not the destination.
