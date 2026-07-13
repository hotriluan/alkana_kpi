# Skill Workflow Routing

When orchestrating multi-step tasks, consider these workflow sequences. Skills are listed in typical execution order.

## Core Development Workflow

```
/ak:plan → /ak:cook → /ak:test → /ak:code-review → /ak:ship → /ak:journal
```

| User Intent | Suggested Start |
|-------------|----------------|
| "implement feature X", "build X", "add X" | `/ak:plan` then `/ak:cook` |
| "execute this plan" | `/ak:cook <plan-path>` |
| "quick implementation" | `/ak:cook --fast` |

## Bugfix Workflow

```
/ak:scout → /ak:debug → /ak:fix → /ak:test → /ak:code-review
```

| User Intent | Suggested Start |
|-------------|----------------|
| "X is broken", "error in X", "bug in X" | `/ak:fix` (auto-scouts internally) |
| "CI is failing", "tests broken" | `/ak:fix --auto` |
| "investigate why X happens" | `/ak:scout` then `/ak:debug` |

## Investigation Workflow

```
/ak:scout → /ak:debug → /ak:brainstorm → /ak:plan
```

| User Intent | Suggested Start |
|-------------|----------------|
| "understand how X works" | `/ak:scout` |
| "why is X happening" | `/ak:debug` |
| "explore options for X" | `/ak:brainstorm` then `/ak:plan` |

## Post-Implementation Checklist

After completing implementation work, consider:
- `/ak:code-review` — review changes before merging
- `/ak:ship` — run full shipping pipeline (tests, review, version, PR)
- `/ak:journal` — document decisions and lessons learned

## Setup Skills

Before starting implementation in a shared codebase:
- `/ak:worktree` — create isolated worktree for the feature/fix
- `/ak:scout` — discover relevant files and code patterns
