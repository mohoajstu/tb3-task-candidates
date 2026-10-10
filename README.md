# Terminal-Bench 3 task candidates

This repository contains two independent task candidates:

| Task | Agent objective | Evaluation |
| --- | --- | --- |
| [Causal outbox](tasks/causal-outbox/instruction.md) | Build a durable event relay with causal ordering, topic replay, and acknowledgements. | [Results](EVALUATION.md) |
| [MCP tool recovery](tasks/mcp-tool-recovery/instruction.md) | Build a durable gateway for local JSON-RPC tool calls with token rotation, pagination, ambiguous retries, and dependencies. | [Results](MCP_EVALUATION.md) |

Each task has its own Docker environment, reference solution, and separate verifier. The MCP task includes a local demo service; neither task needs a live external API. Both are based on the [TB3 contribution guide](https://github.com/harbor-framework/terminal-bench-3/blob/main/CONTRIBUTING.md) and [review automation](https://github.com/harbor-framework/terminal-bench-3/blob/main/docs/TASK_REVIEW_AUTOMATION.md) at upstream commit 209679e34327a78ce8e9bf5300b2f317992863c9.

The evaluation records distinguish completed checks from pending agent trials and infrastructure errors. The four reviewer-facing prose sections in each task README await Mohammed Abdul Jabbar's own wording, as required by the contribution guide.
