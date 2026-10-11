# MCP tool recovery evaluation record

## Configuration

Current Terminal-Bench checkout: 209679e34327a78ce8e9bf5300b2f317992863c9, fetched 2026-10-10. Harbor version: 0.23.1.dev202609170426. The current CI defaults specify three standard trials per agent: codex with openai/gpt-6-astra and reasoning_effort=xhigh, plus claude-code with anthropic/claude-fable-5-1 and reasoning_effort=max. Claude also sets CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000. The /cheat workflow runs one adversarial trial per agent with docs/prompts/hack-trial-prompt.md as extra instructions.

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Static scripts | Run every /private/tmp/tb3-current/scripts/checks/check-*.sh on tasks/mcp-tool-recovery with dockerfile-pin v1.5.0 on PATH | PASS, 2026-10-10 |
| Local reference tests | TB3_PROGRAM="$PWD/tasks/mcp-tool-recovery/solution/gateway.py" python3 -m pytest -q tasks/mcp-tool-recovery/tests/test_gateway.py | PASS, 5/5 after adding concurrent process coverage, 2026-10-10; localhost binding required an unsandboxed local run |
| Docker oracle | harbor run -p tasks/mcp-tool-recovery --agent oracle --env docker --yes | PASS, reward 1.0, no exceptions, jobs/2026-10-10__17-35-46 on the revised task |
| Docker nop | harbor run -p tasks/mcp-tool-recovery --agent nop --env docker --yes | PASS, reward 0.0, no exceptions, jobs/2026-10-10__17-36-40 on the revised task |
| Implementation rubric | harbor check tasks/mcp-tool-recovery -r /private/tmp/tb3-current/docs/prompts/task-implementation.toml --agent claude-code --model anthropic/claude-sonnet-5 --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="(private token)" | 29 pass, 5 fail, 1 not applicable, jobs/2026-10-10__13-14-50; four failures are empty human-written README sections and one was local ignored Python bytecode caches, now removed. Must rerun after author prose is added. |

## Standard agent trials

The checked-in [evidence](evidence/mcp-tool-recovery/) contains static-check output, Harbor result summaries, and per-test CTRF reports for Docker oracle and nop validation. Full local jobs are omitted because agent transcripts may contain credentials.

The following commands must each produce three completed verifier failures. Agent crashes or infrastructure errors do not count:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --n-attempts 3
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --n-attempts 3
```

Results: 0/3 countable Codex failures and 0/3 countable Claude failures. The first Codex attempt on this task, jobs/2026-10-10__12-47-46, ended in NonZeroAgentExitCodeError. A repeat using the exact current CI Codex configuration and `--n-attempts 3` (jobs/2026-10-10__13-05-05) produced three more NonZeroAgentExitCodeError exceptions. Each agent log ends with "workspace routing discovery failed" before the agent wrote a solution. Their 0.0 rewards are infrastructure failures and do not count as model failures. The exact current CI Claude configuration was run three times in jobs/2026-10-10__13-09-03. All three ended in ApiRateLimitError before coding; the model response said "Fable 5.1 requires usage credits. Switch to another model to continue." These 0.0 rewards are access failures and do not count as model failures. Harbor summaries are saved in evidence/mcp-tool-recovery/codex-infrastructure-result.json, codex-three-trials-infrastructure-result.json, and claude-three-trials-access-result.json. The repository was published on GitHub; author-written README sections are pending.

## Email-model setup and task iteration

The hiring email names GPT-6.1 Sol and Claude Opus 5.5, whereas the upstream CI configuration above names Astra and Fable. Host CLI smoke tests succeeded for both email models after upgrading Codex CLI to 0.162.1 and using Anthropic's documented `claude-opus-5-5` model ID. The task image now pins the newer Codex CLI and installs CA certificates; an isolated Codex Docker trial on that image is in progress. The first Codex Docker trial before the CA fix (jobs/2026-10-10__17-31-23) failed during workspace routing discovery and is not countable.

Three Opus 5.5 trials on the first task revision (jobs/2026-10-10__13-59-07) produced one completed verifier pass and two API rate-limit exceptions. The pass proves that revision was too easy for the assignment. The task now includes concurrent use of the same SQLite database by multiple gateway processes and a fifth verifier test for duplicate execution under overlap. A subsequent three-trial Opus run (jobs/2026-10-10__17-33-37) encountered the subscription session limit before coding in all three attempts; the limit resets at 6:10 pm America/Vancouver. The summary of the first Opus run is in evidence/mcp-tool-recovery/opus-5-5-initial-result.json. Fresh completed agent trials are required for the revised task.

## Adversarial trials

The local equivalent of the current /cheat wrapper adds the upstream prompt as extra instructions. One run per agent is required, with reward exactly 0.0:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
```

Results: both adversarial commands were attempted. Claude (jobs/2026-10-10__13-10-59) returned reward 0.0 with ApiRateLimitError because Fable 5.1 requires usage credits. Codex (jobs/2026-10-10__13-11-03) returned reward 0.0 with NonZeroAgentExitCodeError after workspace routing discovery failed. Neither agent reached the task, so neither result demonstrates verifier resistance to an adversarial model. Their Harbor summaries are in evidence/mcp-tool-recovery/claude-cheat-access-result.json and codex-cheat-infrastructure-result.json. No completed model trajectory exists for failure analysis.
