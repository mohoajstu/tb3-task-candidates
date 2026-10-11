# Commerce reconciliation evaluation

This is a third independent candidate. Its difficulty is unproven until completed agent trials produce verifier failures. Earlier candidates are preserved.

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
| Docker build and oracle | `harbor run -p tasks/commerce-reconciliation --agent oracle --env docker --yes` | PASS, reward 1.0, no exceptions, `jobs/2026-10-10__18-53-50` |
| Docker nop | Same command with `--agent nop` | PASS, reward 0.0, no exceptions, `jobs/2026-10-10__18-54-14` |
| Implementation rubric | Current upstream implementation rubric | Pending; author-written README sections remain empty |

## Standard trials

The hiring email names GPT-6.1 Sol xhigh and Opus 5.5 max. The upstream defaults at the recorded commit name Astra xhigh and Fable 5.1 max, with three standard trials each. This mismatch remains documented in the other evaluation records. Fable previously required usage credits on this account; that access failure is not a model failure. Neither configuration is claimed complete here.

Initial email-configuration trials are running with:

```bash
harbor run -p tasks/commerce-reconciliation --agent codex --model openai/gpt-6.1-sol --env docker --yes --ae CODEX_FORCE_AUTH_JSON=1 --ak reasoning_effort=xhigh
harbor run -p tasks/commerce-reconciliation --agent claude-code --model anthropic/claude-opus-5-5 --env docker --yes --ae CLAUDE_FORCE_OAUTH=1 --ae CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN" --ak reasoning_effort=max
```

Anthropic's documented Opus model ID uses `claude-opus-5-5`; the dotted email ID failed in earlier setup attempts. Credentials are kept outside Git. Full local jobs are ignored because transcripts may contain credentials; safe result summaries will be copied to evidence.

Required completed failures: three per required configuration. Count so far: zero. Trial outcome and failure analysis are pending. Crashes, timeouts, API errors, and container errors will be excluded.

## Adversarial trials

Pending. The local equivalent of the current `/cheat` workflow adds `--extra-instruction-path /private/tmp/tb3-current/docs/prompts/hack-trial-prompt.md` to each agent command, once per required configuration. Zero reward is required; an access error or refusal will be documented explicitly and will not be presented as proof of verifier resistance.
