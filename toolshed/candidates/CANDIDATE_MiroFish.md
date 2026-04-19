# MiroFish — Multi-agent prediction simulation engine

**Repo:** github.com/mbennett-labs/MiroFish (forked from 666ghj/MiroFish)
**Status:** Filed, not active. Forked April 2026.
**Category:** Prediction / scenario simulation
**Stack:** Python + Vue, Docker, OASIS engine (CAMEL-AI), GraphRAG, multi-agent LLM personas

## What it does
Multi-agent social simulation for prediction. Seed material in → thousands of LLM agents simulate reactions/evolution → prediction report out. Recommends Alibaba Qwen, swappable to any OpenAI-SDK-compatible model.

## Why it's filed here, not deployed
- No falsifiable track record published (no Brier scores, no Polymarket backtest)
- Expensive to run (40+ rounds × thousands of agents × LLM calls)
- General-purpose simulation has no specific edge vs. narrow Polymarket strategies (e.g., healthcare regulatory latency arbitrage already in production)
- Active research area, not proven product

## When to revisit
- After TheBinMap is generating real revenue signal (2-3+ weeks out)
- Test scenario: pick 10 already-resolved Polymarket questions, run MiroFish retroactively, score predictions vs. actual outcomes. If meaningfully better than chance, escalate.

## Possible non-prediction uses worth exploring
- Test TheBinMap UX features against simulated user personas before building
- Stress-test SELARIX Lattice agent personas in adversarial scenarios
- Run simulated outreach negotiations to refine messaging
- Explore "what if" scenarios for SaaS product decisions

## Underlying tech worth knowing
OASIS (Open Agent Social Interaction Simulations) by CAMEL-AI is the actual simulation engine. Open source. If MiroFish itself doesn't pan out, OASIS is the deeper layer worth building on directly for narrow specific applications.

---
*Filed April 19, 2026. Not chased. Not forgotten.*
