# Matched topology results

**Public snapshot adaptation.** This describes the historical study; it is not a new preregistration or an execution instruction. Private Git ancestry, original locks and raw evidence are absent. Source commit/file hashes in [provenance](../provenance.json) identify the supplied bytes but do not independently establish when the design was fixed. See [evidence limits](evidence-availability.md). Operational coordination text is omitted; the original remains preserved privately.

## Scope and result

On 96 fresh independent families, the matched chain and AND fork/join used the same 32 opaque IDs, required records (k=4 or 8), labels and payload budgets (B=4,8,12). Intact frontier retrieval was complete exactly where B≥k, as predicted. At k=4/B=12, null-anchor faults gave fork/join 21/96 completions versus chain 3/96, a paired +18.75 pp [11.46,27.08]; false-leaf faults gave 20/96 versus 2/96 with the same difference. At k=8/B=12, null faults gave 2/96 versus 0/96, +2.08 pp [0.00,5.21], and false-leaf faults gave zero for both. All 18 blind fork-minus-chain completion differences were exactly zero; this does not mean every blind completion count is zero. These are conditional descriptive differences under a specific anchor-fault intervention, without multiplicity adjustment or an overall mixture headline.

The smaller fork branch cut preserves more reachable true records; target edge counts and fault cut sizes differ despite matched cardinality. Much of the behavior is predictable combinatorially. Complete private-set recovery does not authenticate asserted edges or guarantee checker agreement. The oracle bounds retrieval only. In this frozen model all damaged-reference oracle views abstain, and it has zero false-normal/false-violation outcomes. Full-catalog evidence can produce false verdicts. No agent strategy, model/API, real data, identification capability or operational safety was tested.

## Evidence scope

The [adapted protocol](swarm-018-topology-protocol-v1.md), [design counterexamples](swarm-018-acceptance-v1.md), [aggregate summary](../reports/swarm-018-summary.json), and [timing groups](../reports/swarm-018-timing-summary.json) are included. [Research history](research-history.md) reports the original chronology without claiming publicly verifiable preregistration. Original raw rows, keys, locks, audit inputs and Git history are excluded.

## All 18 primary topology contrasts

Counts are complete families out of96, identical across the two label views; contrasts average those views within each family. Delta is fork/join minus chain, in percentage points, with the frozen shared-family percentile interval. W/L/T uses96 paired families, not192 independent label rows.

| k | B | Condition | Chain /96 | Fork /96 | Delta pp [95%] | W/L/T |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | Intact | 96 | 96 | 0.00 [0.00, 0.00] | 0/0/96 |
| 4 | 4 | Null | 0 | 1 | 1.04 [0.00, 3.12] | 1/0/95 |
| 4 | 4 | False leaf | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 4 | 8 | Intact | 96 | 96 | 0.00 [0.00, 0.00] | 0/0/96 |
| 4 | 8 | Null | 0 | 13 | 13.54 [7.29, 20.83] | 13/0/83 |
| 4 | 8 | False leaf | 0 | 10 | 10.42 [4.17, 16.67] | 10/0/86 |
| 4 | 12 | Intact | 96 | 96 | 0.00 [0.00, 0.00] | 0/0/96 |
| 4 | 12 | Null | 3 | 21 | 18.75 [11.46, 27.08] | 18/0/78 |
| 4 | 12 | False leaf | 2 | 20 | 18.75 [11.46, 27.08] | 18/0/78 |
| 8 | 4 | Intact | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 4 | Null | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 4 | False leaf | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 8 | Intact | 96 | 96 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 8 | Null | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 8 | False leaf | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 12 | Intact | 96 | 96 | 0.00 [0.00, 0.00] | 0/0/96 |
| 8 | 12 | Null | 0 | 2 | 2.08 [0.00, 5.21] | 2/0/94 |
| 8 | 12 | False leaf | 0 | 0 | 0.00 [0.00, 0.00] | 0/0/96 |

## All 18 blind topology negative controls

| Topology | k | B | Condition | Delta pp [95%] | W/L/T |
| --- | --- | --- | --- | --- | --- |
| Fork minus chain | 4 | 4 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 4 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 8 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 8 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 8 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 12 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 12 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 4 | 12 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 4 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 4 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 8 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 8 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 8 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 12 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 12 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork minus chain | 8 | 12 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |

## All 36 frontier minus blind contrasts

| Topology | k | B | Condition | Delta pp [95%] | W/L/T |
| --- | --- | --- | --- | --- | --- |
| Chain | 4 | 4 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Fork/join | 4 | 4 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Chain | 4 | 4 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 4 | 4 | Null | 1.04 [0.00, 3.12] | 1/0/95 |
| Chain | 4 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 4 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 4 | 8 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Fork/join | 4 | 8 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Chain | 4 | 8 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 4 | 8 | Null | 13.54 [7.29, 20.83] | 13/0/83 |
| Chain | 4 | 8 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 4 | 8 | False leaf | 10.42 [4.17, 16.67] | 10/0/86 |
| Chain | 4 | 12 | Intact | 96.88 [93.75, 100.00] | 93/0/3 |
| Fork/join | 4 | 12 | Intact | 96.88 [93.75, 100.00] | 93/0/3 |
| Chain | 4 | 12 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 4 | 12 | Null | 18.75 [11.46, 27.08] | 18/0/78 |
| Chain | 4 | 12 | False leaf | -1.04 [-3.12, 0.00] | 0/1/95 |
| Fork/join | 4 | 12 | False leaf | 17.71 [10.42, 25.00] | 17/0/79 |
| Chain | 8 | 4 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 4 | Intact | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 8 | 4 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 4 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 8 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 4 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 8 | 8 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Fork/join | 8 | 8 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Chain | 8 | 8 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 8 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 8 | 8 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 8 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Chain | 8 | 12 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Fork/join | 8 | 12 | Intact | 100.00 [100.00, 100.00] | 96/0/0 |
| Chain | 8 | 12 | Null | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 12 | Null | 2.08 [0.00, 5.21] | 2/0/94 |
| Chain | 8 | 12 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |
| Fork/join | 8 | 12 | False leaf | 0.00 [0.00, 0.00] | 0/0/96 |

## Analytic probabilities versus measured completion

The following36 cells were computed before research generation and are not discoveries. Blind probability is C(B−1,k−1)/C(31,k−1). For fully reachable-frontier traversal, let q be reachable true records, d the false leaf (0 or1), F=B−q−d, and missing=k−q. When B≥k, frontier completion probability is C(F,missing)/C(32−q−d,missing), using zero for an impossible choice. B<k is zero. The background-root approval does not affect selection. Finite-sample deviations from these expectations are not audit failures. Deterministic zeros (including blind topology contrasts) differ from empirical zero-event cells. A percentile interval [0,0] when all 96 observed family differences are zero does not establish a zero population effect; some such cells have nonzero frozen analytic recovery probabilities. No additional uncertainty analysis or samples were added.

| Topology | k | B | Condition | Frontier theory % | Frontier /96 | Blind theory % | Blind /96 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chain | 4 | 4 | Intact | 100.000000 | 96 | 0.022247 | 0 |
| Chain | 4 | 4 | Null | 0.022247 | 0 | 0.022247 | 0 |
| Chain | 4 | 4 | False leaf | 0.000000 | 0 | 0.022247 | 0 |
| Chain | 4 | 8 | Intact | 100.000000 | 96 | 0.778643 | 0 |
| Chain | 4 | 8 | Null | 0.778643 | 0 | 0.778643 | 0 |
| Chain | 4 | 8 | False leaf | 0.492611 | 0 | 0.778643 | 0 |
| Chain | 4 | 12 | Intact | 100.000000 | 96 | 3.670745 | 3 |
| Chain | 4 | 12 | Null | 3.670745 | 3 | 3.670745 | 3 |
| Chain | 4 | 12 | False leaf | 2.955665 | 2 | 3.670745 | 3 |
| Chain | 8 | 4 | Intact | 0.000000 | 0 | 0.000000 | 0 |
| Chain | 8 | 4 | Null | 0.000000 | 0 | 0.000000 | 0 |
| Chain | 8 | 4 | False leaf | 0.000000 | 0 | 0.000000 | 0 |
| Chain | 8 | 8 | Intact | 100.000000 | 96 | 0.000038 | 0 |
| Chain | 8 | 8 | Null | 0.000038 | 0 | 0.000038 | 0 |
| Chain | 8 | 8 | False leaf | 0.000000 | 0 | 0.000038 | 0 |
| Chain | 8 | 12 | Intact | 100.000000 | 96 | 0.012550 | 0 |
| Chain | 8 | 12 | Null | 0.012550 | 0 | 0.012550 | 0 |
| Chain | 8 | 12 | False leaf | 0.005894 | 0 | 0.012550 | 0 |
| Fork/join | 4 | 4 | Intact | 100.000000 | 96 | 0.022247 | 0 |
| Fork/join | 4 | 4 | Null | 3.448276 | 1 | 0.022247 | 0 |
| Fork/join | 4 | 4 | False leaf | 0.000000 | 0 | 0.022247 | 0 |
| Fork/join | 4 | 8 | Intact | 100.000000 | 96 | 0.778643 | 0 |
| Fork/join | 4 | 8 | Null | 17.241379 | 13 | 0.778643 | 0 |
| Fork/join | 4 | 8 | False leaf | 14.285714 | 10 | 0.778643 | 0 |
| Fork/join | 4 | 12 | Intact | 100.000000 | 96 | 3.670745 | 3 |
| Fork/join | 4 | 12 | Null | 31.034483 | 21 | 3.670745 | 3 |
| Fork/join | 4 | 12 | False leaf | 28.571429 | 20 | 3.670745 | 3 |
| Fork/join | 8 | 4 | Intact | 0.000000 | 0 | 0.000000 | 0 |
| Fork/join | 8 | 4 | Null | 0.000000 | 0 | 0.000000 | 0 |
| Fork/join | 8 | 4 | False leaf | 0.000000 | 0 | 0.000000 | 0 |
| Fork/join | 8 | 8 | Intact | 100.000000 | 96 | 0.000038 | 0 |
| Fork/join | 8 | 8 | Null | 0.034188 | 0 | 0.000038 | 0 |
| Fork/join | 8 | 8 | False leaf | 0.000000 | 0 | 0.000038 | 0 |
| Fork/join | 8 | 12 | Intact | 100.000000 | 96 | 0.012550 | 0 |
| Fork/join | 8 | 12 | Null | 1.196581 | 2 | 0.012550 | 0 |
| Fork/join | 8 | 12 | False leaf | 0.769231 | 0 | 0.012550 | 0 |

## Label-conditioned checker diagnostics for all 240 groups

Each row has96 families. Complete refers to the private required set; resolved follows asserted observed references. Agree is agreement with private AND truth. FN is asserted_normal on a true violation, FV asserted_violation on a true normal, and unknown is abstention. Equal/defined compares resolved observed-set membership with private truth only when resolved; an undefined rate is not zero. All actual verdict counts, recall/precision, edge coverage, distractor reads and denominators remain in the full machine-readable summary. Full catalog uses32 reads once per view, not a budget-matched competitor.

| Topology | k | B | Condition | Method | Truth | Complete | Resolved | Agree | FN | FV | Unknown | Equal/defined |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fork/join | 4 | 12 | Intact | Blind | normal | 3 | 3 | 3 | 0 | 0 | 93 | 3/3 |
| Fork/join | 4 | 12 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 12 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 12 | Intact | Blind | violation | 3 | 3 | 3 | 0 | 0 | 93 | 3/3 |
| Fork/join | 4 | 12 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 12 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 12 | False leaf | Blind | normal | 3 | 7 | 4 | 0 | 3 | 89 | 0/7 |
| Fork/join | 4 | 12 | False leaf | Frontier | normal | 20 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 4 | 12 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | False leaf | Blind | violation | 3 | 7 | 7 | 0 | 0 | 89 | 0/7 |
| Fork/join | 4 | 12 | False leaf | Frontier | violation | 20 | 96 | 78 | 18 | 0 | 0 | 0/96 |
| Fork/join | 4 | 12 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Blind | normal | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Frontier | normal | 21 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Blind | violation | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Frontier | violation | 21 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 12 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 4 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 4 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 4 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 4 | False leaf | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 4 | 4 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | False leaf | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | False leaf | Frontier | violation | 0 | 96 | 78 | 18 | 0 | 0 | 0/96 |
| Fork/join | 4 | 4 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Frontier | normal | 1 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Frontier | violation | 1 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 4 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 8 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 8 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 8 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 8 | False leaf | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | False leaf | Frontier | normal | 10 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 4 | 8 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | False leaf | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | False leaf | Frontier | violation | 10 | 96 | 78 | 18 | 0 | 0 | 0/96 |
| Fork/join | 4 | 8 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Frontier | normal | 13 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Frontier | violation | 13 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 8 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 32* | Intact | Full catalog | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 32* | Intact | Full catalog | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 4 | 32* | False leaf | Full catalog | normal | 96 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 4 | 32* | False leaf | Full catalog | violation | 96 | 96 | 78 | 18 | 0 | 0 | 0/96 |
| Fork/join | 4 | 32* | Null | Full catalog | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 4 | 32* | Null | Full catalog | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 12 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 12 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 12 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 12 | False leaf | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 8 | 12 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | False leaf | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | False leaf | Frontier | violation | 0 | 96 | 77 | 19 | 0 | 0 | 0/96 |
| Fork/join | 8 | 12 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Frontier | normal | 2 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Frontier | violation | 2 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 12 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Intact | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | False leaf | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 4 | Null | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 8 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 8 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 8 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 8 | False leaf | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 8 | 8 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | False leaf | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | False leaf | Frontier | violation | 0 | 96 | 77 | 19 | 0 | 0 | 0/96 |
| Fork/join | 8 | 8 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 8 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 32* | Intact | Full catalog | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 32* | Intact | Full catalog | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Fork/join | 8 | 32* | False leaf | Full catalog | normal | 96 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Fork/join | 8 | 32* | False leaf | Full catalog | violation | 96 | 96 | 77 | 19 | 0 | 0 | 0/96 |
| Fork/join | 8 | 32* | Null | Full catalog | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Fork/join | 8 | 32* | Null | Full catalog | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Intact | Blind | normal | 3 | 3 | 3 | 0 | 0 | 93 | 3/3 |
| Chain | 4 | 12 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 12 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 12 | Intact | Blind | violation | 3 | 3 | 3 | 0 | 0 | 93 | 3/3 |
| Chain | 4 | 12 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 12 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 12 | False leaf | Blind | normal | 3 | 38 | 15 | 0 | 23 | 58 | 0/38 |
| Chain | 4 | 12 | False leaf | Frontier | normal | 2 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 4 | 12 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | False leaf | Blind | violation | 3 | 38 | 23 | 15 | 0 | 58 | 0/38 |
| Chain | 4 | 12 | False leaf | Frontier | violation | 2 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 4 | 12 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Blind | normal | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Frontier | normal | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Blind | violation | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Frontier | violation | 3 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 12 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 4 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 4 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 4 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 4 | False leaf | Blind | normal | 0 | 11 | 4 | 0 | 7 | 85 | 0/11 |
| Chain | 4 | 4 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 4 | 4 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | False leaf | Blind | violation | 0 | 11 | 7 | 4 | 0 | 85 | 0/11 |
| Chain | 4 | 4 | False leaf | Frontier | violation | 0 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 4 | 4 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 4 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 8 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 8 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 8 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 8 | False leaf | Blind | normal | 0 | 21 | 7 | 0 | 14 | 75 | 0/21 |
| Chain | 4 | 8 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 4 | 8 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | False leaf | Blind | violation | 0 | 21 | 14 | 7 | 0 | 75 | 0/21 |
| Chain | 4 | 8 | False leaf | Frontier | violation | 0 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 4 | 8 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 8 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 32* | Intact | Full catalog | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 32* | Intact | Full catalog | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 4 | 32* | False leaf | Full catalog | normal | 96 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 4 | 32* | False leaf | Full catalog | violation | 96 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 4 | 32* | Null | Full catalog | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 4 | 32* | Null | Full catalog | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 12 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 12 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 12 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 12 | False leaf | Blind | normal | 0 | 44 | 19 | 0 | 25 | 52 | 0/44 |
| Chain | 8 | 12 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 8 | 12 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | False leaf | Blind | violation | 0 | 44 | 25 | 19 | 0 | 52 | 0/44 |
| Chain | 8 | 12 | False leaf | Frontier | violation | 0 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 8 | 12 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 12 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Intact | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | False leaf | Blind | normal | 0 | 9 | 3 | 0 | 6 | 87 | 0/9 |
| Chain | 8 | 4 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 8 | 4 | False leaf | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | False leaf | Blind | violation | 0 | 9 | 6 | 3 | 0 | 87 | 0/9 |
| Chain | 8 | 4 | False leaf | Frontier | violation | 0 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 8 | 4 | False leaf | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Oracle | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 4 | Null | Oracle | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Intact | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Intact | Frontier | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 8 | Intact | Oracle | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 8 | Intact | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Intact | Frontier | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 8 | Intact | Oracle | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 8 | False leaf | Blind | normal | 0 | 26 | 11 | 0 | 15 | 70 | 0/26 |
| Chain | 8 | 8 | False leaf | Frontier | normal | 0 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 8 | 8 | False leaf | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | False leaf | Blind | violation | 0 | 26 | 15 | 11 | 0 | 70 | 0/26 |
| Chain | 8 | 8 | False leaf | Frontier | violation | 0 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 8 | 8 | False leaf | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Blind | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Frontier | normal | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Oracle | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Blind | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Frontier | violation | 0 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 8 | Null | Oracle | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 32* | Intact | Full catalog | normal | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 32* | Intact | Full catalog | violation | 96 | 96 | 96 | 0 | 0 | 0 | 96/96 |
| Chain | 8 | 32* | False leaf | Full catalog | normal | 96 | 96 | 46 | 0 | 50 | 0 | 0/96 |
| Chain | 8 | 32* | False leaf | Full catalog | violation | 96 | 96 | 50 | 46 | 0 | 0 | 0/96 |
| Chain | 8 | 32* | Null | Full catalog | normal | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |
| Chain | 8 | 32* | Null | Full catalog | violation | 96 | 0 | 0 | 0 | 0 | 96 | 0/0 |

## Costs and latency

Every feasible view transmits4096 catalog bytes,128 query bytes, and512B payload bytes:6272/8320/10368 bytes at B4/8/12. Blind uses1 payload batch. Frontier rounds depend on reachable depth and include one unexpanded fallback batch when needed. Full catalog uses20608 input bytes and32 reads. Oracle uses min(B,k) reads and additionally receives a canonical private truth-ID list, charged in bytes and work; it is not feasible. Backend N=32 index entries and16384 prepared payload bytes are separately charged for every invocation, excluded from transmitted input traffic and selector timing. Generation/observation preprocessing and scoring costs are separate. Authentication cost is0 because no authentication is present.

The table gives normal-view selection costs (paired violation selection costs are identical). All 240 groups, all work counters, checker costs and truth-scoring work are retained in JSON. Reads, batches, metadata/index/scan/sort work, payload parsing, reference/catalog checks, discovery/dedup/frontier work and reader request validation are not interchangeable cost units. Reported local selector microseconds include reads, not generation/backend preparation/checker/scoring. Modeled total waits at RTT r equal (1+payload_rounds)r; at0ms they are0, at1/10ms the last two columns apply. These are latency models, not measurements of a service.

| Topology | k | B | Condition | Method | Reads | Input bytes | Rounds | Catalog scans | Sort items | Pointer lookups | Local µs | 1ms RTT wait | 10ms RTT wait |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fork/join | 4 | 12 | Intact | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 55.96 | 2.00 | 20.00 |
| Fork/join | 4 | 12 | Intact | Frontier | 12 | 10368 | 4.00 | 32.00 | 35.00 | 4.00 | 81.52 | 5.00 | 50.00 |
| Fork/join | 4 | 12 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.16 | 2.00 | 20.00 |
| Fork/join | 4 | 12 | False leaf | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.21 | 2.00 | 20.00 |
| Fork/join | 4 | 12 | False leaf | Frontier | 12 | 10368 | 4.00 | 32.00 | 35.00 | 3.00 | 82.14 | 5.00 | 50.00 |
| Fork/join | 4 | 12 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.35 | 2.00 | 20.00 |
| Fork/join | 4 | 12 | Null | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 55.74 | 2.00 | 20.00 |
| Fork/join | 4 | 12 | Null | Frontier | 12 | 10368 | 4.00 | 32.00 | 34.00 | 2.00 | 72.98 | 5.00 | 50.00 |
| Fork/join | 4 | 12 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.45 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | Intact | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 55.91 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | Intact | Frontier | 4 | 6272 | 3.00 | 0.00 | 7.00 | 4.00 | 69.67 | 4.00 | 40.00 |
| Fork/join | 4 | 4 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.14 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | False leaf | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 56.79 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | False leaf | Frontier | 4 | 6272 | 3.00 | 0.00 | 7.00 | 3.00 | 69.53 | 4.00 | 40.00 |
| Fork/join | 4 | 4 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.03 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | Null | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 55.30 | 2.00 | 20.00 |
| Fork/join | 4 | 4 | Null | Frontier | 4 | 6272 | 4.00 | 32.00 | 34.00 | 2.00 | 71.30 | 5.00 | 50.00 |
| Fork/join | 4 | 4 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.83 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | Intact | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 54.92 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | Intact | Frontier | 8 | 8320 | 4.00 | 32.00 | 35.00 | 4.00 | 74.08 | 5.00 | 50.00 |
| Fork/join | 4 | 8 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.72 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | False leaf | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 56.32 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | False leaf | Frontier | 8 | 8320 | 4.00 | 32.00 | 35.00 | 3.00 | 81.25 | 5.00 | 50.00 |
| Fork/join | 4 | 8 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.77 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | Null | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 55.97 | 2.00 | 20.00 |
| Fork/join | 4 | 8 | Null | Frontier | 8 | 8320 | 4.00 | 32.00 | 34.00 | 2.00 | 72.47 | 5.00 | 50.00 |
| Fork/join | 4 | 8 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.86 | 2.00 | 20.00 |
| Fork/join | 4 | 32* | Intact | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 59.24 | 2.00 | 20.00 |
| Fork/join | 4 | 32* | False leaf | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 58.61 | 2.00 | 20.00 |
| Fork/join | 4 | 32* | Null | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 58.07 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | Intact | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.44 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | Intact | Frontier | 12 | 10368 | 6.00 | 32.00 | 39.00 | 8.00 | 94.97 | 7.00 | 70.00 |
| Fork/join | 8 | 12 | Intact | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 58.04 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | False leaf | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 57.53 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | False leaf | Frontier | 12 | 10368 | 6.00 | 32.00 | 37.00 | 5.00 | 84.19 | 7.00 | 70.00 |
| Fork/join | 8 | 12 | False leaf | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 56.85 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | Null | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.07 | 2.00 | 20.00 |
| Fork/join | 8 | 12 | Null | Frontier | 12 | 10368 | 6.00 | 32.00 | 36.00 | 4.00 | 82.33 | 7.00 | 70.00 |
| Fork/join | 8 | 12 | Null | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 58.04 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | Intact | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 56.07 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | Intact | Frontier | 4 | 6272 | 3.00 | 0.00 | 10.00 | 5.00 | 72.07 | 4.00 | 40.00 |
| Fork/join | 8 | 4 | Intact | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 56.01 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | False leaf | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 55.00 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | False leaf | Frontier | 4 | 6272 | 3.00 | 0.00 | 8.00 | 4.00 | 71.03 | 4.00 | 40.00 |
| Fork/join | 8 | 4 | False leaf | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 55.81 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | Null | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 57.72 | 2.00 | 20.00 |
| Fork/join | 8 | 4 | Null | Frontier | 4 | 6272 | 4.00 | 0.00 | 8.00 | 4.00 | 72.96 | 5.00 | 50.00 |
| Fork/join | 8 | 4 | Null | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 56.11 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | Intact | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 55.54 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | Intact | Frontier | 8 | 8320 | 5.00 | 0.00 | 15.00 | 8.00 | 87.31 | 6.00 | 60.00 |
| Fork/join | 8 | 8 | Intact | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 57.14 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | False leaf | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 56.34 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | False leaf | Frontier | 8 | 8320 | 6.00 | 32.00 | 37.00 | 5.00 | 89.42 | 7.00 | 70.00 |
| Fork/join | 8 | 8 | False leaf | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 56.70 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | Null | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 54.80 | 2.00 | 20.00 |
| Fork/join | 8 | 8 | Null | Frontier | 8 | 8320 | 6.00 | 32.00 | 36.00 | 4.00 | 88.06 | 7.00 | 70.00 |
| Fork/join | 8 | 8 | Null | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 57.78 | 2.00 | 20.00 |
| Fork/join | 8 | 32* | Intact | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 59.07 | 2.00 | 20.00 |
| Fork/join | 8 | 32* | False leaf | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 58.71 | 2.00 | 20.00 |
| Fork/join | 8 | 32* | Null | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 60.73 | 2.00 | 20.00 |
| Chain | 4 | 12 | Intact | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 57.53 | 2.00 | 20.00 |
| Chain | 4 | 12 | Intact | Frontier | 12 | 10368 | 5.00 | 32.00 | 35.00 | 3.00 | 78.05 | 6.00 | 60.00 |
| Chain | 4 | 12 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.25 | 2.00 | 20.00 |
| Chain | 4 | 12 | False leaf | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.85 | 2.00 | 20.00 |
| Chain | 4 | 12 | False leaf | Frontier | 12 | 10368 | 3.00 | 32.00 | 33.00 | 1.00 | 66.90 | 4.00 | 40.00 |
| Chain | 4 | 12 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.50 | 2.00 | 20.00 |
| Chain | 4 | 12 | Null | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.48 | 2.00 | 20.00 |
| Chain | 4 | 12 | Null | Frontier | 12 | 10368 | 2.00 | 32.00 | 32.00 | 0.00 | 61.42 | 3.00 | 30.00 |
| Chain | 4 | 12 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.14 | 2.00 | 20.00 |
| Chain | 4 | 4 | Intact | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 59.55 | 2.00 | 20.00 |
| Chain | 4 | 4 | Intact | Frontier | 4 | 6272 | 4.00 | 0.00 | 7.00 | 3.00 | 72.00 | 5.00 | 50.00 |
| Chain | 4 | 4 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 56.71 | 2.00 | 20.00 |
| Chain | 4 | 4 | False leaf | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 54.53 | 2.00 | 20.00 |
| Chain | 4 | 4 | False leaf | Frontier | 4 | 6272 | 3.00 | 32.00 | 33.00 | 1.00 | 65.46 | 4.00 | 40.00 |
| Chain | 4 | 4 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.83 | 2.00 | 20.00 |
| Chain | 4 | 4 | Null | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 56.68 | 2.00 | 20.00 |
| Chain | 4 | 4 | Null | Frontier | 4 | 6272 | 2.00 | 32.00 | 32.00 | 0.00 | 60.36 | 3.00 | 30.00 |
| Chain | 4 | 4 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.10 | 2.00 | 20.00 |
| Chain | 4 | 8 | Intact | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 62.69 | 2.00 | 20.00 |
| Chain | 4 | 8 | Intact | Frontier | 8 | 8320 | 5.00 | 32.00 | 35.00 | 3.00 | 75.53 | 6.00 | 60.00 |
| Chain | 4 | 8 | Intact | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 55.21 | 2.00 | 20.00 |
| Chain | 4 | 8 | False leaf | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 61.23 | 2.00 | 20.00 |
| Chain | 4 | 8 | False leaf | Frontier | 8 | 8320 | 3.00 | 32.00 | 33.00 | 1.00 | 67.32 | 4.00 | 40.00 |
| Chain | 4 | 8 | False leaf | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.95 | 2.00 | 20.00 |
| Chain | 4 | 8 | Null | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 56.33 | 2.00 | 20.00 |
| Chain | 4 | 8 | Null | Frontier | 8 | 8320 | 2.00 | 32.00 | 32.00 | 0.00 | 63.19 | 3.00 | 30.00 |
| Chain | 4 | 8 | Null | Oracle | 4 | 6413 | 1.00 | 0.00 | 4.00 | 0.00 | 54.46 | 2.00 | 20.00 |
| Chain | 4 | 32* | Intact | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 60.29 | 2.00 | 20.00 |
| Chain | 4 | 32* | False leaf | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 59.34 | 2.00 | 20.00 |
| Chain | 4 | 32* | Null | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 57.82 | 2.00 | 20.00 |
| Chain | 8 | 12 | Intact | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 57.09 | 2.00 | 20.00 |
| Chain | 8 | 12 | Intact | Frontier | 12 | 10368 | 9.00 | 32.00 | 39.00 | 7.00 | 97.83 | 10.00 | 100.00 |
| Chain | 8 | 12 | Intact | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 57.40 | 2.00 | 20.00 |
| Chain | 8 | 12 | False leaf | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 56.11 | 2.00 | 20.00 |
| Chain | 8 | 12 | False leaf | Frontier | 12 | 10368 | 3.00 | 32.00 | 33.00 | 1.00 | 68.48 | 4.00 | 40.00 |
| Chain | 8 | 12 | False leaf | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 71.41 | 2.00 | 20.00 |
| Chain | 8 | 12 | Null | Blind | 12 | 10368 | 1.00 | 32.00 | 31.00 | 0.00 | 55.66 | 2.00 | 20.00 |
| Chain | 8 | 12 | Null | Frontier | 12 | 10368 | 2.00 | 32.00 | 32.00 | 0.00 | 61.90 | 3.00 | 30.00 |
| Chain | 8 | 12 | Null | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 56.89 | 2.00 | 20.00 |
| Chain | 8 | 4 | Intact | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 59.61 | 2.00 | 20.00 |
| Chain | 8 | 4 | Intact | Frontier | 4 | 6272 | 4.00 | 0.00 | 8.00 | 4.00 | 73.69 | 5.00 | 50.00 |
| Chain | 8 | 4 | Intact | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 56.41 | 2.00 | 20.00 |
| Chain | 8 | 4 | False leaf | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 56.10 | 2.00 | 20.00 |
| Chain | 8 | 4 | False leaf | Frontier | 4 | 6272 | 3.00 | 32.00 | 33.00 | 1.00 | 67.31 | 4.00 | 40.00 |
| Chain | 8 | 4 | False leaf | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 55.93 | 2.00 | 20.00 |
| Chain | 8 | 4 | Null | Blind | 4 | 6272 | 1.00 | 32.00 | 31.00 | 0.00 | 55.54 | 2.00 | 20.00 |
| Chain | 8 | 4 | Null | Frontier | 4 | 6272 | 2.00 | 32.00 | 32.00 | 0.00 | 60.57 | 3.00 | 30.00 |
| Chain | 8 | 4 | Null | Oracle | 4 | 6553 | 1.00 | 0.00 | 8.00 | 0.00 | 55.39 | 2.00 | 20.00 |
| Chain | 8 | 8 | Intact | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 56.12 | 2.00 | 20.00 |
| Chain | 8 | 8 | Intact | Frontier | 8 | 8320 | 8.00 | 0.00 | 15.00 | 7.00 | 98.33 | 9.00 | 90.00 |
| Chain | 8 | 8 | Intact | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 57.87 | 2.00 | 20.00 |
| Chain | 8 | 8 | False leaf | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 55.14 | 2.00 | 20.00 |
| Chain | 8 | 8 | False leaf | Frontier | 8 | 8320 | 3.00 | 32.00 | 33.00 | 1.00 | 67.68 | 4.00 | 40.00 |
| Chain | 8 | 8 | False leaf | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 56.19 | 2.00 | 20.00 |
| Chain | 8 | 8 | Null | Blind | 8 | 8320 | 1.00 | 32.00 | 31.00 | 0.00 | 55.07 | 2.00 | 20.00 |
| Chain | 8 | 8 | Null | Frontier | 8 | 8320 | 2.00 | 32.00 | 32.00 | 0.00 | 72.63 | 3.00 | 30.00 |
| Chain | 8 | 8 | Null | Oracle | 8 | 8601 | 1.00 | 0.00 | 8.00 | 0.00 | 56.56 | 2.00 | 20.00 |
| Chain | 8 | 32* | Intact | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 59.96 | 2.00 | 20.00 |
| Chain | 8 | 32* | False leaf | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 58.56 | 2.00 | 20.00 |
| Chain | 8 | 32* | Null | Full catalog | 32 | 20608 | 1.00 | 32.00 | 32.00 | 0.00 | 58.78 | 2.00 | 20.00 |

## Interpretation and remaining limits

On false-leaf full-catalog views, all true records were read yet normal labels produced50/96 false violations at both k values and both topologies. Violation labels produced46/96 false normals for chains and18/96 or19/96 for fork/join at k4/8. Null faults yielded96/96 unknown per label/topology/k despite complete retrieval. Intact full catalog agreed96/96 in each cell. These diagnose the deliberately unauthenticated asserted-reference checker, not real-world identification errors. Extra selected records outside asserted closure are ignored by design.

Fork/join has more true edges and a smaller anchor-fault cut than the matched chain. There is no isolation of topology from that structural intervention, no arbitrary DAG coverage, no fault-position averaging, no adversarially optimized corruption and no realistic agent workload. Fake targets are existing background roots only. Declared arity and approval values are unmutated restrictions, not trusted/authenticated signals. Full32-record catalogs, tiny k/B and fixed512-byte wires bound generality. Random names prevent direct role fields, but topology and the hand-designed background remain observable once paid for.

No favorable condition was used to retune the methods. All18+18+36 contrasts, null outcomes and diagnostics are retained. The fixed-family bootstrap uses96 independent units and2,000 shared draws with endpoint indices49/1949; intervals are descriptive and unadjusted for multiplicity. Prior cohorts are separate. Source-lock consistency and same-agent independent code do not constitute external scientific validation.

