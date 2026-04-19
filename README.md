# SELARIX Lattice

**The reference operating system for Mike Bennett's agent swarm.**

## What this is

The SELARIX Lattice is the shared agent-pool architecture, toolshed, and interoperability contract that powers every SELARIX project — directory sites (TheBinMap, TherapistIndex), security infrastructure (CrawDaddy, SN61 miner, $ATTEST, Bastion), and whatever comes next.

One pool of role-based agents works many projects. Projects are configuration, not separate swarms.

## Structure

```
lattice/
├── architecture/       Canonical architecture docs (read first)
├── agents/             The nine agent personas
├── contract/           Interoperability contract + JSON schemas
├── toolshed/           Shared capabilities across projects
│   ├── adapters/       Wrappers for external services
│   ├── tools/          Reusable code we've written
│   ├── skills/         Model-facing skill prompts
│   ├── context/        Reference material agents load
│   ├── templates/      Copy-paste scaffolds
│   └── candidates/     Under evaluation
├── templates/          Full-project scaffolds
└── docs/               Sessions, notes (local-only)
```

## Start here

1. Read `architecture/SELARIX_Lattice_Architecture_v1.md` — the architecture document
2. Read `contract/LATTICE_Interop_Contract_v1.md` — how projects plug in
3. Browse `toolshed/candidates/` for the current research inventory

## The Three Laws

All agents inherit these immutable constraints from Bastion:

I — Never harm.
II — Earn your existence.
III — Never deceive, but owe nothing to strangers.

## Version

Lattice v1 — April 19, 2026

Status: Foundation laid. Agent personas pending. First retrofit target: TherapistIndex. First greenfield test: TheBinMap.

---
*Quantum Shield Labs LLC | SELARIX | Private IP*
