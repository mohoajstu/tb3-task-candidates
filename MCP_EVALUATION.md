# MCP tool recovery evaluation record

## Configuration

Current Terminal-Bench checkout: 209679e34327a78ce8e9bf5300b2f317992863c9, fetched 2026-10-10. Harbor version: 0.23.1.dev202609170426. The current CI defaults specify three standard trials per agent: codex with openai/gpt-6-astra and reasoning_effort=xhigh, plus claude-code with anthropic/claude-fable-5-1 and reasoning_effort=max. Claude also sets CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000. The /cheat workflow runs one adversarial trial per agent with docs/prompts/hack-trial-prompt.md as extra instructions.

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Static scripts | Run every /private/tmp/tb3-current/scripts/checks/check-*.sh on tasks/mcp-tool-recovery with dockerfile-pin v1.5.0 on PATH | PASS, 2026-10-10 |
| Local reference tests | TB3_PROGRAM="$PWD/tasks/mcp-tool-recovery/solution/gateway.py" python3 -m pytest -q tasks/mcp-tool-recovery/tests/test_gateway.py | PASS, 7/7 after adding independent parallel progress, 2026-10-10; localhost binding required an unsandboxed local run |
| Docker oracle | harbor run -p tasks/mcp-tool-recovery --agent oracle --env docker --yes | PASS, reward 1.0, no exceptions, jobs/2026-10-10__17-59-05 on the seven-test revision |
| Docker nop | harbor run -p tasks/mcp-tool-recovery --agent nop --env docker --yes | PASS, reward 0.0, no exceptions, jobs/2026-10-10__17-59-53 on the seven-test revision |
| Implementation rubric | harbor check tasks/mcp-tool-recovery -r /private/tmp/tb3-current/docs/prompts/task-implementation.toml --agent claude-code --model anthropic/claude-sonnet-5 --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="(private token)" | 29 pass, 5 fail, 1 not applicable, jobs/2026-10-10__13-14-50; four failures are empty human-written README sections and one was local ignored Python bytecode caches, now removed. Must rerun after author prose is added. |

## Standard agent trials

The checked-in [evidence](evidence/mcp-tool-recovery/) contains static-check output, Harbor result summaries, and per-test CTRF reports for Docker oracle and nop validation. Full local jobs are omitted because agent transcripts may contain credentials.

The following commands must each produce three completed verifier failures. Agent crashes or infrastructure errors do not count:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --n-attempts 3
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --n-attempts 3
```

Results: 0/3 countable Codex failures and 0/3 countable Claude failures. The first Codex attempt on this task, jobs/2026-10-10__12-47-46, ended in NonZeroAgentExitCodeError. A repeat using the exact current CI Codex configuration and `--n-attempts 3` (jobs/2026-10-10__13-05-05) produced three more NonZeroAgentExitCodeError exceptions. Each agent log ends with "workspace routing discovery failed" before the agent wrote a solution. Their 0.0 rewards are infrastructure failures and do not count as model failures. After CA certificates and Codex CLI were fixed, one `openai/gpt-6-astra` xhigh trial on the five-test revision (jobs/2026-10-10__17-44-53) completed normally and **passed with reward 1.0**. Its result summary is `evidence/mcp-tool-recovery/codex-astra-concurrency-pass.json`. The exact current CI Claude configuration was run three times in jobs/2026-10-10__13-09-03. All three ended in ApiRateLimitError before coding; the model response said "Fable 5.1 requires usage credits. Switch to another model to continue." These 0.0 rewards are access failures and do not count as model failures. Harbor summaries are saved in evidence/mcp-tool-recovery/codex-infrastructure-result.json, codex-three-trials-infrastructure-result.json, and claude-three-trials-access-result.json. The repository was published on GitHub; author-written README sections are pending.

## Email-model setup and task iteration

The hiring email names GPT-6.1 Sol and Claude Opus 5.5, whereas the upstream CI configuration above names Astra and Fable. Host CLI smoke tests succeeded for both email models after upgrading Codex CLI to 0.162.1 and using Anthropic's documented `claude-opus-5-5` model ID. The task image now pins the newer Codex CLI and installs CA certificates. The first Codex Docker trial before the CA fix (jobs/2026-10-10__17-31-23) failed during workspace routing discovery and is not countable. A subsequent isolated GPT-6.1 Sol Docker trial on the revised task and fixed image (jobs/2026-10-10__17-34-15) completed normally and **passed the verifier with reward 1.0**. This is a valid agent pass, so the revised task does not satisfy the assignment's required model-failure criterion. Its Harbor summary is in evidence/mcp-tool-recovery/codex-6-1-sol-concurrency-pass.json.

Three Opus 5.5 trials on the first task revision (jobs/2026-10-10__13-59-07) produced one completed verifier pass and two API rate-limit exceptions. The pass proves that revision was too easy for the assignment. The task now includes concurrent use of the same SQLite database by multiple gateway processes and a fifth verifier test for duplicate execution under overlap. The earlier Opus solution, replayed against the revised verifier, fails this new test because both processes claim completion of the same call; this is retrospective analysis, not a fresh countable trial. A subsequent three-trial Opus run (jobs/2026-10-10__17-33-37) encountered the subscription session limit before coding in all three attempts; the limit resets at 6:10 pm America/Vancouver. The summary of the first Opus run is in evidence/mcp-tool-recovery/opus-5-5-initial-result.json. Fresh completed agent trials are required for the revised task.

The six-test revision adds a verifier case that kills a process after the service creates a note but before the response reaches the gateway, then checks that another process retries the same call and the service records one effect. The reference solution passed all six local tests and Docker oracle/nop validation. The saved Astra solution from the five-test trial also passed all six tests when replayed as a Docker oracle (`jobs/2026-10-10__17-53-52`); this retrospective replay is not a new agent trial and gives no evidence of a model failure. The macOS replay stalled because of platform-specific file locking, so only the Linux Docker replay is used for this analysis.

The seven-test revision adds a real parallel-progress requirement: a process blocked on call A must not stop another process from finishing independent call B. The reference uses per-call OS locks and coordinates token refresh; local tests and Docker oracle/nop passed. Both saved Codex solutions from earlier revisions fail only the new parallel test when replayed in Docker (Astra `jobs/2026-10-10__17-58-58`, GPT-6.1 Sol `jobs/2026-10-10__17-59-48`). These are retrospective replays, not fresh model trials. A fresh Astra trial on the seven-test revision (`jobs/2026-10-10__18-00-02`) completed normally and **passed with reward 1.0**, so this revision also fails the assignment's all-fail criterion for the upstream CI Codex configuration. Its result summary is `evidence/mcp-tool-recovery/codex-astra-parallel-pass.json`.

## Adversarial trials

The local equivalent of the current /cheat wrapper adds the upstream prompt as extra instructions. One run per agent is required, with reward exactly 0.0:

```bash
harbor run -p tasks/mcp-tool-recovery --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
harbor run -p tasks/mcp-tool-recovery --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
```

Results: both adversarial commands were attempted. Claude (jobs/2026-10-10__13-10-59) returned reward 0.0 with ApiRateLimitError because Fable 5.1 requires usage credits. Codex (jobs/2026-10-10__13-11-03) returned reward 0.0 with NonZeroAgentExitCodeError after workspace routing discovery failed. After Docker connectivity was fixed, the Codex adversarial command on the six-test revision (jobs/2026-10-10__17-55-32) returned reward 0.0 with AgentSafetyRefusalError: the model endpoint flagged the upstream hack prompt before the agent touched the task. None of these attempts demonstrates verifier resistance to an adversarial model. Their Harbor summaries are in evidence/mcp-tool-recovery/claude-cheat-access-result.json, codex-cheat-infrastructure-result.json, and codex-cheat-safety-refusal-result.json. No completed adversarial model trajectory exists for failure analysis.
