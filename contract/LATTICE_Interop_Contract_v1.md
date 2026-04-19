# SELARIX Lattice Interoperability Contract v1

Every project in the Lattice must produce and consume three file types in the same format. This contract is the non-negotiable foundation — without it, the Reporter cannot roll up status and the agent pool cannot work across projects.

## The three file types

1. **Status files** — written nightly by project agents, consumed by Reporter
   Location: `/projects/{project_name}/status/{YYYY-MM-DD}.json`
   Schema: status_schema.json

2. **Manifest files** — describe each project to the Lattice
   Location: `/projects/{project_name}/manifest.json`
   Schema: manifest_schema.json

3. **Inbox directives** — Mike's Telegram replies routed back to projects
   Location: `/projects/{project_name}/inbox/{directive_id}.json`
   Schema: inbox_schema.json

See the corresponding *_schema.json files in this directory for field specifications.

## Contract enforcement

- Projects that do not emit valid status files are invisible to the Reporter
- Projects that do not have a valid manifest are not watched by the Coordinator
- Malformed inbox directives are logged and skipped, not silently dropped

Version: 1.0
Date: 2026-04-19
Status: Canonical — update with care
