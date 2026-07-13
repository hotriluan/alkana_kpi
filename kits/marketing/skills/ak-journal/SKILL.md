---
name: ak:journal
description: "Write technical journal entries analyzing recent changes. Use for session reflections, change analysis, decision documentation."
user-invocable: true
when_to_use: "Invoke for technical session reflection or decision records."
category: utilities
keywords: [journal, reflection, changes, session]
argument-hint: "[topic or reflection]"
metadata:
  author: agentkit
  version: "1.0.0"
---

# Journal

Use the `journal-writer` subagent to explore the memories and recent code changes, and write some journal entries.
Journal entries should be concise and focused on the most important events, key changes, impacts, and decisions.
Keep journal entries in the `./docs/journals/` directory.
After the local entry is created, have `journal-writer` publish/share it through AgentWiki CLI or MCP when available; otherwise report that AgentWiki publishing was skipped.

**IMPORTANT:** Invoke "the engineer project-organization skill" skill to organize the outputs.

## Workflow Position

**Typically follows:** `the engineer ship skill` (journal after shipping), `/ak:cook` (journal after implementation), `/ak:fix` (journal after bug fix)
**Terminal skill** — no typical successor.
