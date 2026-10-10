# Evaluation record

## Upstream basis

- Terminal-Bench 3 commit: `209679e34327a78ce8e9bf5300b2f317992863c9` (checked out 2026-10-10). Previous validation used `1dcda8716784493721921c23e4bc7f7d988b4494` (2026-10-03).
- The checkout pins Harbor `0.23.1.dev202609170426` in `.github/harbor-version`. The first local validations used `0.23.0`; final validation and trials use the pinned version.
- The checked-in `.github/harbor-run-defaults.yml` sets three `/run` trials per agent: `claude-code` with `anthropic/claude-fable-5-1` and `reasoning_effort=max`, plus `codex` with `openai/gpt-6-astra` and `reasoning_effort=xhigh`. The Claude environment sets `CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000`.
- This differs from the model names in the hiring email; the email says current TB3 CI is authoritative, so the checked-in defaults are used here.
- `/cheat` is a distinct adversarial run using the prompt in `docs/prompts/hack-trial-prompt.md`. It uses one trial per configured agent.

## Validation

Reviewable local artifacts are in [`evidence/`](evidence/): the complete static-check output, Harbor result JSON for final oracle and nop runs, their per-test CTRF reports, and the errored Codex run summary. Harbor's full `jobs/` directories are local and omitted from Git because they may contain agent transcripts or credentials.

| Check | Command | Result |
| --- | --- | --- |
| Static checks | `PATH="/private/tmp:$PATH"; for check in /private/tmp/tb3-current/scripts/checks/check-*.sh; do bash "$check" tasks/causal-outbox || exit 1; done` against upstream commit above; `dockerfile-pin` v1.5.0 placed in `/private/tmp` | PASS, all scripts, 2026-10-10 |
| Docker build + oracle, initial image | `harbor run -p tasks/causal-outbox --agent oracle --env docker --yes` | PASS, reward 1.0, `jobs/2026-10-03__12-33-36` |
| Nop, initial image | `harbor run -p tasks/causal-outbox --agent nop --env docker --yes` | PASS, reward 0.0, `jobs/2026-10-03__12-34-11` |
| Docker build + oracle, preinstalled agent image | Same command | PASS, reward 1.0, `jobs/2026-10-03__12-42-09` (Harbor 0.23.0) |
| Docker build + oracle, CI-pinned Harbor | Same command | PASS, reward 1.0, `jobs/2026-10-03__12-48-20` (prior Codex CLI image) |
| Nop, CI-pinned Harbor | Same command with `--agent nop` | PASS, reward 0.0, `jobs/2026-10-03__12-49-03` (prior Codex CLI image) |
| Docker build + oracle, current digest-pinned image | Same oracle command | PASS, reward 1.0, `jobs/2026-10-10__12-21-24` |
| Nop, current digest-pinned image | Same command with `--agent nop` | PASS, reward 0.0, `jobs/2026-10-10__12-23-50` |
| Oracle after adding dependency-set/JSON-value coverage | Same oracle command | PASS, reward 1.0, `jobs/2026-10-10__12-26-11` |
| Nop after adding dependency-set/JSON-value coverage | Same nop command | PASS, reward 0.0, `jobs/2026-10-10__12-26-16` |
| Implementation rubric | `harbor check tasks/causal-outbox -r docs/prompts/task-implementation.toml` | Pending; Claude Code is not yet authenticated and author-written README prose is pending. |

The first oracle build on 2026-10-03 produced reward 0 because a test incorrectly expected `ack` at the subscription's existing cursor to be invalid. The instruction explicitly says it must return `already`. The test was corrected. The final 2026-10-10 test set has four local passing tests, Docker oracle reward 1.0, and nop reward 0.0.

## Standard `/run` trials

Only a completed verifier run with reward below 1.0 counts as a genuine model failure. Agent or infrastructure exceptions are recorded separately and rerun. Three completed failures are required per configuration.

| Agent | Model | Reasoning | Trial 1 | Trial 2 | Trial 3 |
| --- | --- | --- | --- | --- | --- |
| codex | `openai/gpt-6-astra` | xhigh | 0/3 countable failures; three infrastructure errors recorded below | Pending | Pending |
| claude-code | `anthropic/claude-fable-5-1` | max | Pending authentication | Pending | Pending |

Codex command, repeated three times:

```bash
harbor run -p tasks/causal-outbox --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh
```

An initial Codex attempt at `jobs/2026-10-03__12-34-59` ended with `AgentSetupTimeoutError` after 360 seconds while Harbor installed Node and Codex. Its reward summary is **not** a model failure. The agent image was changed to preinstall pinned Codex and Claude Code CLIs; all validation and trials must be rerun against that image.

The next attempt at `jobs/2026-10-03__12-50-03` had `NonZeroAgentExitCodeError` and no model solution: Codex reported TLS `UnknownIssuer` and failed to reach its response endpoint. A host diagnostic also showed Codex CLI 0.147.0 was too old for `gpt-6-astra`; the image was updated to CLI 0.160.0 before the October 10 retry. This attempt likewise does **not** count as a model failure.

On 2026-10-10, `jobs/2026-10-10__12-24-02` used the current digest-pinned image and Codex CLI 0.160.0. It again ended in `NonZeroAgentExitCodeError` before a model solution: the agent log ends with `workspace routing discovery failed`. A credential-free request from both the host and the Docker image to `https://chatgpt.com/backend-api/ps/mcp` returned HTTP 451 (`no_biscuit_no_service`). The recorded 0.0 reward is an infrastructure failure and **does not count** toward the three required model failures. It ran before the last verifier test was added, so a successful retry must use the final task version.

Claude Code command, repeated three times after `claude setup-token` or equivalent login:

```bash
harbor run -p tasks/causal-outbox --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN=<token> --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max
```

## Adversarial `/cheat` trials

The exact upstream adversarial prompt and CI wrapper must be used once for each agent. Both runs must receive reward 0.0. Results: pending; neither agent has completed a standard trial on this machine.

The current CI wrapper passes `docs/prompts/hack-trial-prompt.md` as Harbor `extra_instructions`; the local CLI equivalent is `--extra-instruction-path`. Run each command once from this repository after cloning the current upstream commit to `/private/tmp/tb3-current` and establishing agent credentials:

```bash
harbor run -p tasks/causal-outbox --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
harbor run -p tasks/causal-outbox --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
```

## Failure analysis

No completed model trajectory exists yet, so there is no honest model failure analysis. The recorded Codex failures are execution/network failures, not verifier failures caused by model code. The task design aims to expose mistakes in causal ordering, durable pending events, replay, and acknowledgement validation; that hypothesis still requires the mandated trials to test it.
