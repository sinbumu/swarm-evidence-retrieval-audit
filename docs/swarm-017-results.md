# SWARM-017 fixed reservation results

**Public snapshot adaptation.** This describes the historical study; it is not a new preregistration or an execution instruction. Private Git ancestry, original locks and raw evidence are absent. Source commit/file hashes in [provenance](../provenance.json) identify the supplied bytes but do not independently establish when the design was fixed. See [evidence limits](evidence-availability.md). Operational coordination text is omitted; the original remains preserved privately.

**The fixed two-slot relation reservation did not improve overall completion.** On 96 fresh families / 2,304 paired views it completed **1,535**, versus **1,626** for the original object-first mixture and **1,632** for graph/join. Versus mixture it won 29 and lost 120 views: **−3.95 percentage points [−5.16, −2.82]**. Partial collision produced some gains, but implicit references with unique retained IDs caused substantial regression. Explicit full collision remained unimproved. No selector, condition, N or seed was changed after observing these results; no further experiment was started.

This is a separate fixed cohort (seeds 5001–5096, development 501–506), never pooled with SWARM-016. Counts below are paired views, not independent samples. [Adapted historical protocol](swarm-017-protocol.md), [full summary](../reports/swarm-017-summary.json), [timing summary](../reports/swarm-017-timing-summary.json) retain all methods/conditions/backgrounds and exact intervals. The private verification receipt is excluded; personal review does not establish independent scientific validation.

## Overall primary comparisons

| Reserved minus comparator | Wins | Losses | Ties | Difference pp [95% interval] |
| --- | ---: | ---: | ---: | --- |
| object_relation_mix | 29 | 120 | 2155 | -3.95 [-5.16, -2.82] |
| relation_graph | 70 | 167 | 2067 | -4.21 [-5.73, -2.52] |
| relation_join | 70 | 167 | 2067 | -4.21 [-5.82, -2.47] |

The 2,000 bootstrap resamples operate on 96 family means, each averaging 24 views. Per-condition means average the two backgrounds within a family. Per-background/condition comparisons also resample families. Intervals are descriptive and conditional on this generator/grid, without multiplicity correction. Graph and join return identical selections: their separate label-keyed bootstrap streams can give slightly different Monte Carlo percentile endpoints, not different observed performance or independent evidence.

## All 12 condition results

| Condition | Graph/join | Original mix | Reserved mix | Reserved−mix pp [95% interval] | Wins/losses vs mix | Reserved−graph pp [95% interval] |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| explicit_unique_r100 | 192 | 192 | 192 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |
| explicit_unique_r050 | 192 | 192 | 192 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |
| explicit_unique_r000 | 192 | 192 | 192 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |
| explicit_collision_r100 | 192 | 113 | 113 | +0.00 [0.00, 0.00] | 0/0 | -41.15 [-47.40, -35.42] |
| explicit_collision_r050 | 192 | 120 | 137 | +8.85 [5.21, 12.50] | 17/0 | -28.65 [-34.90, -22.40] |
| explicit_collision_r000 | 192 | 192 | 192 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |
| implicit_unique_r100 | 80 | 192 | 109 | -43.23 [-50.00, -36.98] | 0/83 | +15.10 [9.90, 20.83] |
| implicit_unique_r050 | 80 | 99 | 94 | -2.60 [-5.21, -0.52] | 0/5 | +7.29 [3.65, 11.46] |
| implicit_unique_r000 | 80 | 80 | 80 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |
| implicit_collision_r100 | 80 | 113 | 83 | -15.62 [-21.35, -10.42] | 0/30 | +1.56 [-4.17, 7.29] |
| implicit_collision_r050 | 80 | 61 | 71 | +5.21 [2.08, 8.85] | 12/2 | -4.69 [-10.42, 1.04] |
| implicit_collision_r000 | 80 | 80 | 80 | +0.00 [0.00, 0.00] | 0/0 | +0.00 [0.00, 0.00] |

Each row has 192 views from 96 families. Adaptive pointer and the true-record diagnostic both complete 192/192 in every row; all pointers are exact. Correct verdict counts equal complete counts throughout this cohort; all remaining verdicts are unknown, with no wrong normal/violation verdicts. These are synthetic-contract outcomes, not evidence of deployment safety.

With explicit references, the full-collision result is unchanged at 113/192: the final object slot can still admit a distractor. Partial collision improves from 120 to 137, because relation reservation can recover missing true matches while allowing one useful object match. This does not recover graph/join's 192 completions. With implicit references and unique full linkage, reservation can commit two slots to wrong relation-ranked records even though object-first retrieval is complete: 109 versus 192. Under implicit partial collision, gains and losses coexist (12 wins, 2 losses versus mix); the contrast against graph includes zero. The no-linkage p=0 controls reproduce join exactly.

## All methods and full accounting

| Method | Complete / 2304 | Correct | Unknown |
| --- | ---: | ---: | ---: |
| random | 96 | 96 | 2208 |
| recent | 312 | 312 | 1992 |
| object_id | 840 | 840 | 1464 |
| resource_time | 396 | 396 | 1908 |
| reference_join | 1308 | 1308 | 996 |
| relation_graph | 1632 | 1632 | 672 |
| relation_join | 1632 | 1632 | 672 |
| adaptive_pointer | 2304 | 2304 | 0 |
| object_relation_mix | 1626 | 1626 | 678 |
| relation_reserved_mix | 1535 | 1535 | 769 |
| full_evidence | 2304 | 2304 | 0 |

## Primary comparator costs

| Method | Index insertions | Build checks | Query checks | Edge visits | Sorted items | Local time µs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| relation_reserved_mix | 81.438 | 0.000 | 161.875 | 6.964 | 2.408 | 174.24 |
| object_relation_mix | 64.214 | 0.000 | 110.203 | 4.136 | 3.170 | 248.88 |
| relation_graph | 40.719 | 2546.281 | 0.000 | 6.964 | 0.000 | 369.16 |
| relation_join | 40.719 | 0.000 | 122.156 | 6.964 | 0.000 | 169.21 |

All four comparators read four distinct 512-byte payloads in one batch, plus a 512-byte anchor query and the full catalog: mean 40.71875 records / 20,848 metadata bytes, total 23,408 input bytes. Backend initialization adds 40.71875 index insertions on average and four payload lookups per view. Modeled waits are 0/1/10 ms at 0/1/10 ms per round; these are not observed network latency.

Reservation always computes the full four-record join rank, creates its own N-record metadata index, scans all N−1 nonanchor records, and sorts all eligible unreserved object candidates. Its mean query checks and indexing exceed both mixture and join even when it falls back. Catalog transmission is charged once; repeated serialization/work stays in local time. Graph materialization's build checks are a distinct cost category. The displayed selector-plus-read time is one local Python measurement, not a causal speed comparison or service-performance claim. Projection generation and backend initialization are outside that timing boundary. All condition-level costs/timing remain in the saved artifacts.

## Saved failure and improvement examples

The examples are the earliest seed/background within each listed outcome category below, selected from saved evaluation files after auditing. They are illustrations, not additional observations or representative sampling. Underlying IDs and traces are excluded from this snapshot; these illustrations cannot be independently reconstructed from the aggregates alone.

| Condition | Comparator | Seed / background | Outcome | True records in two reserved slots | Final slot true |
| --- | --- | --- | --- | ---: | --- |
| explicit_collision_r050 | object_relation_mix | 5009 / 24 | win | 2 | True |
| implicit_unique_r100 | object_relation_mix | 5001 / 8 | loss | 1 | True |
| explicit_collision_r100 | relation_graph | 5001 / 8 | loss | 2 | False |
| implicit_collision_r050 | object_relation_mix | 5009 / 24 | win | 2 | True |
| implicit_collision_r050 | object_relation_mix | 5017 / 24 | loss | 1 | True |

## Every prespecified primary contrast

The following retains all 111 overall, condition-pooled and background-specific contrasts, including both graph and join. No favorable subset is substituted for the full grid.

| Scope | Background | Condition | Comparator | Wins | Losses | Ties | Difference pp [95% interval] |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| overall | both | all | object_relation_mix | 29 | 120 | 2155 | -3.95 [-5.16, -2.82] |
| overall | both | all | relation_graph | 70 | 167 | 2067 | -4.21 [-5.73, -2.52] |
| overall | both | all | relation_join | 70 | 167 | 2067 | -4.21 [-5.82, -2.47] |
| condition | both | explicit_unique_r100 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r100 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r100 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r050 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r050 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r050 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r000 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r000 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_unique_r000 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_collision_r100 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_collision_r100 | relation_graph | 0 | 79 | 113 | -41.15 [-47.40, -35.42] |
| condition | both | explicit_collision_r100 | relation_join | 0 | 79 | 113 | -41.15 [-46.88, -35.42] |
| condition | both | explicit_collision_r050 | object_relation_mix | 17 | 0 | 175 | +8.85 [5.21, 12.50] |
| condition | both | explicit_collision_r050 | relation_graph | 0 | 55 | 137 | -28.65 [-34.90, -22.40] |
| condition | both | explicit_collision_r050 | relation_join | 0 | 55 | 137 | -28.65 [-34.90, -22.92] |
| condition | both | explicit_collision_r000 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_collision_r000 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | explicit_collision_r000 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_unique_r100 | object_relation_mix | 0 | 83 | 109 | -43.23 [-50.00, -36.98] |
| condition | both | implicit_unique_r100 | relation_graph | 29 | 0 | 163 | +15.10 [9.90, 20.83] |
| condition | both | implicit_unique_r100 | relation_join | 29 | 0 | 163 | +15.10 [9.90, 20.31] |
| condition | both | implicit_unique_r050 | object_relation_mix | 0 | 5 | 187 | -2.60 [-5.21, -0.52] |
| condition | both | implicit_unique_r050 | relation_graph | 14 | 0 | 178 | +7.29 [3.65, 11.46] |
| condition | both | implicit_unique_r050 | relation_join | 14 | 0 | 178 | +7.29 [3.65, 11.46] |
| condition | both | implicit_unique_r000 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_unique_r000 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_unique_r000 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_collision_r100 | object_relation_mix | 0 | 30 | 162 | -15.62 [-21.35, -10.42] |
| condition | both | implicit_collision_r100 | relation_graph | 17 | 14 | 161 | +1.56 [-4.17, 7.29] |
| condition | both | implicit_collision_r100 | relation_join | 17 | 14 | 161 | +1.56 [-3.65, 6.77] |
| condition | both | implicit_collision_r050 | object_relation_mix | 12 | 2 | 178 | +5.21 [2.08, 8.85] |
| condition | both | implicit_collision_r050 | relation_graph | 10 | 19 | 163 | -4.69 [-10.42, 1.04] |
| condition | both | implicit_collision_r050 | relation_join | 10 | 19 | 163 | -4.69 [-10.42, 1.04] |
| condition | both | implicit_collision_r000 | object_relation_mix | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_collision_r000 | relation_graph | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| condition | both | implicit_collision_r000 | relation_join | 0 | 0 | 192 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r100 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r100 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r100 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r050 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r050 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r050 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_unique_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_collision_r100 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_collision_r100 | relation_graph | 0 | 16 | 80 | -16.67 [-25.00, -9.38] |
| background_condition | 8 | explicit_collision_r100 | relation_join | 0 | 16 | 80 | -16.67 [-23.96, -9.38] |
| background_condition | 8 | explicit_collision_r050 | object_relation_mix | 7 | 0 | 89 | +7.29 [3.12, 12.50] |
| background_condition | 8 | explicit_collision_r050 | relation_graph | 0 | 16 | 80 | -16.67 [-23.96, -10.42] |
| background_condition | 8 | explicit_collision_r050 | relation_join | 0 | 16 | 80 | -16.67 [-23.96, -9.38] |
| background_condition | 8 | explicit_collision_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_collision_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | explicit_collision_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_unique_r100 | object_relation_mix | 0 | 21 | 75 | -21.88 [-30.21, -13.54] |
| background_condition | 8 | implicit_unique_r100 | relation_graph | 16 | 0 | 80 | +16.67 [9.38, 23.96] |
| background_condition | 8 | implicit_unique_r100 | relation_join | 16 | 0 | 80 | +16.67 [9.38, 23.96] |
| background_condition | 8 | implicit_unique_r050 | object_relation_mix | 0 | 2 | 94 | -2.08 [-5.21, 0.00] |
| background_condition | 8 | implicit_unique_r050 | relation_graph | 7 | 0 | 89 | +7.29 [2.08, 12.50] |
| background_condition | 8 | implicit_unique_r050 | relation_join | 7 | 0 | 89 | +7.29 [3.12, 13.54] |
| background_condition | 8 | implicit_unique_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_unique_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_unique_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_collision_r100 | object_relation_mix | 0 | 14 | 82 | -14.58 [-21.88, -8.33] |
| background_condition | 8 | implicit_collision_r100 | relation_graph | 12 | 5 | 79 | +7.29 [-1.04, 15.62] |
| background_condition | 8 | implicit_collision_r100 | relation_join | 12 | 5 | 79 | +7.29 [-1.04, 15.62] |
| background_condition | 8 | implicit_collision_r050 | object_relation_mix | 7 | 1 | 88 | +6.25 [1.04, 12.50] |
| background_condition | 8 | implicit_collision_r050 | relation_graph | 7 | 12 | 77 | -5.21 [-14.58, 3.12] |
| background_condition | 8 | implicit_collision_r050 | relation_join | 7 | 12 | 77 | -5.21 [-13.54, 3.12] |
| background_condition | 8 | implicit_collision_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_collision_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 8 | implicit_collision_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r100 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r100 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r100 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r050 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r050 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r050 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_unique_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_collision_r100 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_collision_r100 | relation_graph | 0 | 63 | 33 | -65.62 [-75.00, -56.25] |
| background_condition | 24 | explicit_collision_r100 | relation_join | 0 | 63 | 33 | -65.62 [-75.00, -56.25] |
| background_condition | 24 | explicit_collision_r050 | object_relation_mix | 10 | 0 | 86 | +10.42 [5.21, 16.67] |
| background_condition | 24 | explicit_collision_r050 | relation_graph | 0 | 39 | 57 | -40.62 [-51.04, -31.25] |
| background_condition | 24 | explicit_collision_r050 | relation_join | 0 | 39 | 57 | -40.62 [-50.00, -31.25] |
| background_condition | 24 | explicit_collision_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_collision_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | explicit_collision_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_unique_r100 | object_relation_mix | 0 | 62 | 34 | -64.58 [-73.96, -55.21] |
| background_condition | 24 | implicit_unique_r100 | relation_graph | 13 | 0 | 83 | +13.54 [7.29, 20.83] |
| background_condition | 24 | implicit_unique_r100 | relation_join | 13 | 0 | 83 | +13.54 [7.29, 20.83] |
| background_condition | 24 | implicit_unique_r050 | object_relation_mix | 0 | 3 | 93 | -3.12 [-7.29, 0.00] |
| background_condition | 24 | implicit_unique_r050 | relation_graph | 7 | 0 | 89 | +7.29 [2.08, 12.50] |
| background_condition | 24 | implicit_unique_r050 | relation_join | 7 | 0 | 89 | +7.29 [3.12, 13.54] |
| background_condition | 24 | implicit_unique_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_unique_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_unique_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_collision_r100 | object_relation_mix | 0 | 16 | 80 | -16.67 [-23.96, -9.38] |
| background_condition | 24 | implicit_collision_r100 | relation_graph | 5 | 9 | 82 | -4.17 [-11.46, 3.12] |
| background_condition | 24 | implicit_collision_r100 | relation_join | 5 | 9 | 82 | -4.17 [-11.46, 3.12] |
| background_condition | 24 | implicit_collision_r050 | object_relation_mix | 5 | 1 | 90 | +4.17 [0.00, 9.38] |
| background_condition | 24 | implicit_collision_r050 | relation_graph | 3 | 7 | 86 | -4.17 [-10.42, 2.08] |
| background_condition | 24 | implicit_collision_r050 | relation_join | 3 | 7 | 86 | -4.17 [-11.46, 2.08] |
| background_condition | 24 | implicit_collision_r000 | object_relation_mix | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_collision_r000 | relation_graph | 0 | 0 | 96 | +0.00 [0.00, 0.00] |
| background_condition | 24 | implicit_collision_r000 | relation_join | 0 | 0 | 96 | +0.00 [0.00, 0.00] |


Historical test failure, correction, execution and validation claims are preserved in [research history](research-history.md); the original evidence is not distributed.
