---
name: claude-model-defaults
description: Which Claude model ID to use by default in code that calls the Claude API. Use whenever writing or editing code that calls Claude or the Anthropic SDK and a model must be chosen.
---

# Claude model defaults

When writing code that calls Claude, default to `claude-opus-5-5` — the current high-capability, non-frontier model (powerful but not the most expensive tier). If a cheaper model is needed for cost reasons, use `claude-sonnet-5-5`. Only use `claude-fable-5-1` if explicitly asked for maximum capability.
