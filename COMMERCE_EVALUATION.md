# Commerce reconciliation evaluation

This third independent candidate was implemented and validated, then rejected as too easy for the hiring-email configurations: GPT-6.1 Sol and Opus 5.5 both completed and passed their first trials. Earlier candidates are preserved.

## Dataset and design

The bundled sample adapts UCI Online Retail (Chen, 2015), licensed CC BY 4.0. [Attribution and transformations](tasks/commerce-reconciliation/environment/data/ATTRIBUTION.md) include the source hash and describe the synthetic connector deliveries. All data needed at trial time is baked into the images. No Kaggle account or external service is needed.

To reproduce the sample during development (not during a trial):

```bash
curl -L --fail https://archive.ics.uci.edu/static/public/352/online+retail.zip -o /private/tmp/online-retail.zip
python3 tools/prepare_retail_sample.py /private/tmp/online-retail.zip /private/tmp/retail-sample.ndjson
cmp /private/tmp/retail-sample.ndjson tasks/commerce-reconciliation/environment/data/retail-sample.ndjson
```

The reproduction was checked byte for byte. Development checks also confirmed that the verifier rejects feasible allocations with inferior price and age objectives.

The task repairs a connector reconciliation pipeline. Revision resolution determines the active ledger; globally optimal capacitated matching allocates partial returns. The objectives are lexicographic: maximum quantity, minimum total price distance, then minimum total age. Tied optimal allocations are accepted.

The reference uses successive shortest augmenting paths. The verifier checks output feasibility, absence of residual augmenting paths, and absence of residual negative-cost cycles. Tiny generated histories are additionally checked by exhaustive unit allocation. The verifier does not import the reference solver. This reduces the risk that solution and verifier share a greedy-matching error.

## Checks

Upstream basis: Terminal-Bench commit `209679e34327a78ce8e9bf5300b2f317992863c9`, Harbor `0.23.1.dev202609170426`. Task image pins Codex CLI 0.162.1 and Claude Code 2.1.282 and installs CA certificates.

| Check | Command | Result |
| --- | --- | --- |
| Static scripts | Every `/private/tmp/tb3-current/scripts/checks/check-*.sh` against `tasks/commerce-reconciliation`, with dockerfile-pin v1.5.0 on PATH | PASS; `evidence/commerce-reconciliation/static-checks.txt` |
| Local reference | `TB3_PROGRAM="$PWD/tasks/commerce-reconciliation/solution/reconcile.py" python3 -m pytest -q tasks/commerce-reconciliation/tests/test_reconcile.py` | PASS, five test groups, 2026-10-10 |
| Local starter | Same command with `TB3_PROGRAM` pointing to `environment/reconcile.py` | Four groups fail and one passes, including a demonstrated greedy allocation failure |
| Docker build and oracle | `harbor run -p tasks/commerce-reconciliation --agent oracle --env docker --yes` | PASS, reward 1.0, no exceptions, `jobs/2026-10-10__19-08-17` on the final verifier after correcting tied-allocation acceptance and enforcing integer audit fields |
| Docker nop | Same command with `--agent nop` | PASS, reward 0.0, no exceptions, `jobs/2026-10-10__19-08-30` on the final verifier |
| Implementation rubric | `harbor check tasks/commerce-reconciliation -r /private/tmp/tb3-current/docs/prompts/task-implementation.toml --agent claude-code --model anthropic/claude-sonnet-5 --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN"` | 29 pass, 5 fail, 1 not applicable in `jobs/2026-10-10__18-58-35`. Failures: reviewable, difficulty_explanation_quality, solution_explanation_quality, verification_explanation_quality, task_readme. All concern blank README sections or absent reviewer explanations. A technical design note was subsequently added; the rubric must be rerun after the author writes the required sections. |

The instruction is an AI-assisted draft. The current rubric's `instruction_concision` criterion calls for human-written instructions and flags LLM-generated prose. The author must rewrite it in their own words while retaining the exact contract, in addition to writing the four required README explanation sections. No claim of full rubric compliance is made.

## Standard trials

The hiring email names GPT-6.1 Sol xhigh and Opus 5.5 max. The upstream defaults at the recorded commit name Astra xhigh and Fable 5.1 max, with three standard trials each. This mismatch remains documented in the other evaluation records. Fable previously required usage credits on this account; that access failure is not a model failure. Neither configuration is claimed complete here.

| Configuration | Trial 1 | Trial 2 | Trial 3 |
| --- | --- | --- | --- |
| Email: Codex / GPT-6.1 Sol / xhigh | PASS, reward 1.0, no exception | Not run; the first pass rejects this revision for the all-fail criterion | Not run |
| Email: Claude Code / Opus 5.5 / max | PASS, reward 1.0, no exception | Not run; the first pass rejects this revision for the all-fail criterion | Not run |
| Upstream CI: Codex / Astra / xhigh | Not run on this candidate | Pending | Pending |
| Upstream CI: Claude Code / Fable 5.1 / max | Not run on this candidate; previous tasks encountered account access errors | Pending | Pending |

Initial email-configuration trials use:

```bash
harbor run -p tasks/commerce-reconciliation --agent codex --model openai/gpt-6.1-sol --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh
harbor run -p tasks/commerce-reconciliation --agent claude-code --model anthropic/claude-opus-5-5 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ak reasoning_effort=max
```

Anthropic's documented Opus model ID uses `claude-opus-5-5`; the dotted email ID failed in earlier setup attempts. Credentials are kept outside Git. Full local jobs are ignored because transcripts may contain credentials; safe result summaries will be copied to evidence.

The full standard commands for the recorded upstream CI defaults are:

```bash
harbor run -p tasks/commerce-reconciliation --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --n-attempts 3
harbor run -p tasks/commerce-reconciliation --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --n-attempts 3
```

Required completed failures: three per required configuration. Count: zero. GPT-6.1 Sol's first trial (`jobs/2026-10-10__18-56-23`) completed normally and passed with reward 1.0 and no exceptions. Opus 5.5's first trial (`jobs/2026-10-10__18-56-22`) also completed normally and passed with reward 1.0 and no exceptions. This candidate fails the hiring-email all-fail requirement for both configurations. No subsequent standard trials or adversarial trials were run on this rejected candidate. This is not a completed assignment evaluation.

## Analysis of the unsuccessful design

The intended difficulty was a shared greedy-matching blind spot. Both models instead recognized the global transportation/minimum-cost flow structure. Sol implemented minimum-cost maximum-flow with integer costs and resolved conflicting and superseded revisions. Opus implemented a transportation optimization routine and tested its result on generated and stress histories. Review found no obvious stated requirement missing from the passing Sol implementation. The data's revision and provenance rules added work but did not defeat either model. This was a solvable benchmark prototype, not evidence of a model capability gap. More cases built around the same algorithm would not justify claiming the task is beyond the frontier without fresh failures.

The outcome is recorded as two model passes, not model failures. Crashes, timeouts, API errors, and container errors are excluded from model-failure counts.

## Adversarial trials

Not run on this rejected candidate. The local equivalent of the current `/cheat` workflow adds `--extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md` to each agent command, once per required configuration. Zero reward is required; an access error or refusal must be documented explicitly and cannot be presented as proof of verifier resistance. The commands below are documented for a future qualifying revision; they are not claimed as executed here.

```bash
harbor run -p tasks/commerce-reconciliation --agent codex --model openai/gpt-6-astra --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
harbor run -p tasks/commerce-reconciliation --agent claude-code --model anthropic/claude-fable-5-1 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ae CLAUDE_CODE_MAX_OUTPUT_TOKENS=128000 --ak reasoning_effort=max --extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md
```
