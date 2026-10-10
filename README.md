# Terminal-Bench 3 candidate: causal outbox

This repository contains one original task at [`tasks/causal-outbox`](tasks/causal-outbox). The agent must implement a durable event relay that releases events in causal order and replays them to subscribers until acknowledged. The task includes an isolated Docker environment, a reference solution, and a separate verifier.

The task follows Terminal-Bench 3's [contribution guide](https://github.com/harbor-framework/terminal-bench-3/blob/main/CONTRIBUTING.md) and [review automation](https://github.com/harbor-framework/terminal-bench-3/blob/main/docs/TASK_REVIEW_AUTOMATION.md). The current defaults were read at upstream commit `209679e34327a78ce8e9bf5300b2f317992863c9` (2026-10-10); see [evaluation notes](EVALUATION.md) for the exact commands and results.

## Task layout

- [`instruction.md`](tasks/causal-outbox/instruction.md): agent-facing contract.
- [`environment/`](tasks/causal-outbox/environment): agent image and starting stub.
- [`solution/`](tasks/causal-outbox/solution): reference implementation used by the oracle.
- [`tests/`](tasks/causal-outbox/tests): isolated verifier image and behavioral tests.
- [`README.md`](tasks/causal-outbox/README.md): reviewer-facing task explanation; the four required prose sections await the author's own wording, as required by the contribution guide.

## Submission status

See [EVALUATION.md](EVALUATION.md) for the live check and trial record. Results are recorded as completed, not inferred from local code inspection.

The current task passes all static checks, Docker oracle validation, and nop validation. Required standard and adversarial agent trials and the automated implementation-rubric review remain incomplete; the evaluation record distinguishes infrastructure errors from genuine model failures.
