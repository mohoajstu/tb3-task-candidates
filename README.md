# Terminal-Bench 3 submission

This repository contains three task candidates. **A qualifying submission has not yet been demonstrated.** Completed Codex trials passed the first two candidates; the new commerce reconciliation candidate is undergoing fresh agent evaluation. The repository is an iteration record.

| Task | Agent objective | Evaluation |
| --- | --- | --- |
| [Commerce reconciliation](tasks/commerce-reconciliation/instruction.md) | Repair a versioned commerce ledger and allocate partial returns globally, with exact money and line provenance. | [Results](COMMERCE_EVALUATION.md) |
| [MCP tool recovery](tasks/mcp-tool-recovery/instruction.md) | Build a durable gateway for local JSON-RPC tool calls with token rotation, pagination, ambiguous retries, dependencies, and parallel progress. | [Results](MCP_EVALUATION.md) |
| [Causal outbox](tasks/causal-outbox/instruction.md) | Build a durable event relay with causal ordering, topic replay, and acknowledgements. | [Results](EVALUATION.md) |

Each task has its own Docker environment, reference solution, and separate verifier. The MCP task includes a local demo service; all three run without a live external API. They use the [TB3 contribution guide](https://github.com/harbor-framework/terminal-bench-3/blob/main/CONTRIBUTING.md) and [review automation](https://github.com/harbor-framework/terminal-bench-3/blob/main/docs/TASK_REVIEW_AUTOMATION.md) at upstream commit 209679e34327a78ce8e9bf5300b2f317992863c9.

The evaluation records distinguish completed checks from pending agent trials and infrastructure errors. The four reviewer-facing prose sections in each task README await Mohammed Abdul Jabbar's own wording, as required by the contribution guide.
