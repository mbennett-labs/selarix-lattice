# Default Model Configuration
Kind: context
Status: active
What it does: Defines default LLM routing for SELARIX agents.
When to use it: Loaded by every agent persona unless overridden in that project manifest.
When not to use it: Override per project when a specialized model is justified (e.g., long-context work on Qwen 3.6 Plus).
Dependencies: toolshed/adapters/openrouter.md (TBD — wrap on first use)
Model compatibility: all
Last updated: 2026-04-24 by Mike Bennett

---

## Primary
```
provider: openrouter
model: deepseek/deepseek-chat
context_window: 164000
notes: V3.2 sparse-attention workhorse. ~$0.26/$0.39 per Mtok in/out as of Apr 2026.
```

## Fallback chain (on primary failure or quota)
```
1. z-ai/glm-4.7         — strong coding + agentic, 200K context
2. qwen/qwen-3.6-plus    — 1M context, 78.8% SWE-Bench Verified, long-form work
3. minimax/minimax-m2.7  — cheap parallel workers, 56% SWE-Pro
```

## Strategic layer (human-driven only)
```
Claude Opus 4.7 via Max subscription — used by Mike in chat for planning, architecture, pressure-testing. NOT called by swarm agents.
```

## What this is NOT
- Not a hard constraint. Project manifests override via `model_override`.
- Not a Claude/Anthropic defender for swarm inference. Anthropic keys are for Mike's Claude Code / Claude Chat — NOT swarm agents.
- Not frozen. When a better model ships, this file updates and all agents pick it up on next manifest sync.

## Change log
- 2026-04-24: created during Phase 1 from research doc recommendation (Category 1, Category 6c)
