# MCP tool recovery evaluation record

## Configuration

Current Terminal-Bench checkout: 209679e34327a78ce8e9bf5300b2f317992863c9, fetched 2026-10-10. Harbor version: 0.23.1.dev202609170426. The current CI defaults specify three standard trials per agent: codex with openai/gpt-6-astra and reasoning_effort=xhigh, plus claude-code with anthropic/claude-fable-5-1 and reasoning_effort=max. Claude also sets CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000. The /cheat workflow runs one adversarial trial per agent with docs/prompts/hack-trial-prompt.md as extra instructions.

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Static scripts | Run every /private/tmp/tb3-current/scripts/checks/check-*.sh on tasks/mcp-tool-recovery with dockerfile-pin v1.5.0 on PATH | PASS, 2026-10-10 |
| Local reference tests | TB3_PROGRAM="$PWD/tasks/mcp-tool-recovery/solution/gateway.py" python3 -m pytest -q tasks/mcp-tool-recovery/tests/test_gateway.py | PASS, 4/4, 2026-10-10; localhost binding required an unsandboxed local run |
| Docker oracle | harbor run -p tasks/mcp-tool-recovery --agent oracle --env docker --yes | PASS, reward 1.0, no exceptions, jobs/2026-10-10__12-46-07 |
| Docker nop | harbor run -p tasks/mcp-tool-recovery --agent nop --env docker --yes | PASS, reward 0.0, no exceptions, jobs/2026-10-10__12-46-09 |
| Implementation rubric | harbor check tasks/mcp-tool-recovery -r /private/tmp/tb3-current/docs/prompts/task-implementation.toml --agent claude-code --model anthropic/claude-sonnet-5 | Pending Claude authentication and author-written README sections |

## Standard agent trials

The checked-in [evidence](evidence/mcp-tool-recovery/) contains static-check output, Harbor result summaries, and per-test CTRF reports for Docker oracle and nop validation. Full local jobs are omitted because agent transcripts may contain credentials.

The following commands must each produce three completed verifier failures. Agent crashes or infrastructure errors do not count:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --n-attempts 3
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --n-attempts 3
```

Results: 0/3 countable Codex failures and 0/3 countable Claude failures. The first Codex attempt on this task, jobs/2026-10-10__12-47-46, ended in NonZeroAgentExitCodeError. A repeat using the exact current CI Codex configuration and `--n-attempts 3` (jobs/2026-10-10__13-05-05) produced three more NonZeroAgentExitCodeError exceptions. Each agent log ends with "workspace routing discovery failed" before the agent wrote a solution. Their 0.0 rewards are infrastructure failures and do not count as model failures. Harbor summaries are saved in evidence/mcp-tool-recovery/codex-infrastructure-result.json and codex-three-trials-infrastructure-result.json. The repository was published on GitHub; Claude Docker authentication and author-written README sections are pending.

## Adversarial trials

The local equivalent of the current /cheat wrapper adds the upstream prompt as extra instructions. One run per agent is required, with reward exactly 0.0:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
```

Results: pending for both agents. No model-failure analysis is possible until completed trajectories exist.
