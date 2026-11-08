# SWARM-016 results and verification

**Public snapshot adaptation.** This describes the historical study; it is not a new preregistration or an execution instruction. Private Git ancestry, original locks and raw evidence are absent. Source commit/file hashes in [provenance](../provenance.json) identify the supplied bytes but do not independently establish when the design was fixed. See [evidence limits](evidence-availability.md). Operational coordination text is omitted; the original remains preserved privately.

## Stage 1 fresh-family repetition complete

Completed 2026-11-08T04:44:33+09:00. New N=192 families, 4,608 views, 46,080 rows. Primary finding: graph and equivalent join remain identical; graph-relative completion gains are adaptive +13.13 pp and mix +17.53 pp. The old and new holdouts are kept separate. These results are conditional on the same small synthetic generator.

| Method | Prior complete / 576 | New complete / 4608 | New correct | New unknown |
| --- | ---: | ---: | ---: | ---: |
| random | 60 | 72 | 66 | 4542 |
| recent | 120 | 696 | 532 | 4076 |
| object_id | 276 | 2592 | 1972 | 2636 |
| resource_time | 120 | 808 | 618 | 3990 |
| reference_join | 332 | 2543 | 1902 | 2706 |
| relation_graph | 371 | 2989 | 2217 | 2391 |
| relation_join | 371 | 2989 | 2217 | 2391 |
| adaptive_pointer | 452 | 3594 | 3490 | 1118 |
| object_relation_mix | 439 | 3797 | 2850 | 1758 |
| full_evidence | 576 | 4608 | 3490 | 1118 |

Primary differences below are baseline minus graph, the reverse of the saved summary sign. Intervals resample independent family means across the fixed 24-view grid; no pooling with prior evaluation.

| Contrast | Prior mean pp [95% interval] | New mean pp [95% interval] |
| --- | --- | --- |
| adaptive_pointer minus graph | 14.06 [8.16, 19.97] | 13.13 [11.26, 15.00] |
| object_relation_mix minus graph | 11.81 [5.90, 18.58] | 17.53 [15.41, 19.88] |
| relation_join minus graph | -0.00 [-0.00, -0.00] | -0.00 [-0.00, -0.00] |

Adaptive interval width shrank from 11.81 to 3.73 pp; mix from 12.67 to 4.47 pp. This is greater precision within this generator, not improved external validity. The mixture and adaptive descriptive order differs from the old 24-family sample; no universal method ordering is inferred.

Of 1,536 views assigned pointer faults, 1,118 true chains were damaged and 418 intact. The true-record diagnostic abstained on exactly the 1,118 damaged chains. Adaptive had 1,275 wins and 670 losses against graph; mixture had 808 wins and no losses under the original object-ID assumptions.

### Condition-level primary comparisons

Each row contains 192 paired families at one background/condition. Counts and descriptive paired 95% bootstrap intervals (pp) are shown; backgrounds are separately generated. All nine methods, diagnostic outcomes, operation/input costs, all paired method contrasts, and all 11 fault contrasts are in [the complete aggregate](../reports/swarm-016-repeat-summary.json).

Background 8 workflows:

| Condition | Graph | Adaptive | Mix | Adaptive minus graph pp [CI] | Mix minus graph pp [CI] |
| --- | ---: | ---: | ---: | --- | --- |
| explicit_clean | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| reference_drop | 131 | 192 | 164 | 31.77 [25.52, 38.02] | 17.19 [12.50, 22.92] |
| reference_false | 117 | 192 | 155 | 39.06 [32.29, 45.83] | 19.79 [14.58, 25.52] |
| resource_drop | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| resource_false | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| pointer_drop | 192 | 72 | 192 | -62.50 [-69.79, -55.73] | 0.00 [0.00, 0.00] |
| pointer_wrong | 192 | 85 | 192 | -55.73 [-63.02, -48.96] | 0.00 [0.00, 0.00] |
| implicit_clean | 110 | 192 | 153 | 42.71 [35.42, 49.48] | 22.40 [16.67, 28.65] |
| implicit_resource_drop | 64 | 192 | 131 | 66.67 [59.90, 72.92] | 34.90 [28.12, 42.19] |
| implicit_resource_false | 93 | 192 | 143 | 51.56 [44.27, 58.85] | 26.04 [19.79, 32.29] |
| implicit_pointer_drop | 110 | 72 | 153 | -19.79 [-27.08, -11.98] | 22.40 [16.67, 28.65] |
| implicit_pointer_wrong | 110 | 85 | 153 | -13.02 [-22.40, -3.12] | 22.40 [16.67, 28.65] |

Background 24 workflows:

| Condition | Graph | Adaptive | Mix | Adaptive minus graph pp [CI] | Mix minus graph pp [CI] |
| --- | ---: | ---: | ---: | --- | --- |
| explicit_clean | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| reference_drop | 69 | 192 | 134 | 64.06 [56.77, 70.83] | 33.85 [27.08, 40.62] |
| reference_false | 107 | 192 | 141 | 44.27 [36.98, 51.04] | 17.71 [12.50, 23.44] |
| resource_drop | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| resource_false | 192 | 192 | 192 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| pointer_drop | 192 | 23 | 192 | -88.02 [-92.19, -83.33] | 0.00 [0.00, 0.00] |
| pointer_wrong | 192 | 81 | 192 | -57.81 [-64.58, -50.52] | 0.00 [0.00, 0.00] |
| implicit_clean | 41 | 192 | 116 | 78.65 [72.40, 84.38] | 39.06 [32.29, 45.83] |
| implicit_resource_drop | 9 | 192 | 97 | 95.31 [92.19, 97.92] | 45.83 [38.54, 52.60] |
| implicit_resource_false | 26 | 192 | 105 | 86.46 [81.25, 91.15] | 41.15 [34.38, 47.92] |
| implicit_pointer_drop | 41 | 23 | 116 | -9.38 [-16.67, -2.60] | 39.06 [32.29, 46.35] |
| implicit_pointer_wrong | 41 | 81 | 116 | 20.83 [12.50, 29.69] | 39.06 [32.29, 45.83] |

### Historical validation

Historical execution and failure facts are summarized in [research history](research-history.md). Private original audit inputs are not distributed.

## Stage 2 object linkage stress complete

Completed 2026-11-08T04:54:32+09:00. New N=96 families, 2,304 views, 23,040 rows. **Object collisions invalidate the original mixture no-loss pattern.** With explicit true references and full retained colliding IDs, graph completes 192/192 while mixture completes 110/192: -42.71 pp [-48.96,-36.98]. In the same explicit regime, unique partially retained IDs still give mixture 192/192 because join fills the unused slots.

The p=0.5 collision point estimate in the explicit regime is 121/192, higher than the p=1 value of 110/192; partial retention need not be harmful. In the implicit regime, unique p=1 gives a large gain, while collision p=0.5 yields mix-minus-graph -5.21 pp [-11.46,0.52], an interval including zero. Do not describe that last condition as a clearly established deficit.

### All fixed conditions

Each row pools two backgrounds within each of 96 families (192 views). The difference interval resamples 96 paired family means, not 192 independent views. Pointer and true-record diagnostic are 192/192 in every row because all payload pointers remain exact. All count outcomes below also equal correct verdict counts; remaining cases are unknown, with zero wrong verdicts.

| Reference | Namespace | Retention p | Object ID | Graph = join | Mix | Mix minus graph pp [95% CI] |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Explicit | Unique | 1 | 192 | 192 | 192 | 0.00 [0.00, 0.00] |
| Explicit | Unique | 0.5 | 44 | 192 | 192 | 0.00 [0.00, 0.00] |
| Explicit | Unique | 0 | 25 | 192 | 192 | 0.00 [0.00, 0.00] |
| Explicit | Collision K=4 | 1 | 108 | 192 | 110 | -42.71 [-48.96, -36.98] |
| Explicit | Collision K=4 | 0.5 | 31 | 192 | 121 | -36.98 [-44.27, -30.21] |
| Explicit | Collision K=4 | 0 | 25 | 192 | 192 | 0.00 [0.00, 0.00] |
| Implicit | Unique | 1 | 192 | 60 | 192 | 68.75 [62.50, 75.00] |
| Implicit | Unique | 0.5 | 44 | 60 | 84 | 12.50 [8.33, 17.19] |
| Implicit | Unique | 0 | 25 | 60 | 60 | 0.00 [0.00, 0.00] |
| Implicit | Collision K=4 | 1 | 108 | 60 | 110 | 26.04 [18.23, 33.85] |
| Implicit | Collision K=4 | 0.5 | 31 | 60 | 50 | -5.21 [-11.46, 0.52] |
| Implicit | Collision K=4 | 0 | 25 | 60 | 60 | 0.00 [0.00, 0.00] |

Partial retention applies independently to every record, including the query anchor. An unretained ID is replaced by an opaque per-event token: it removes shared linkage, not the record or payload. Collisions are generated by fixed random workflow-to-bucket assignment, independent of the target and outcome; true parent chains remain unambiguous. Unique p=1 deliberately gives all workflows stable object links, unlike the original binary-stability grid. These are different regimes, not pooled evidence.

| Method | Complete / 2304 | Correct | Unknown |
| --- | ---: | ---: | ---: |
| random | 108 | 108 | 2196 |
| recent | 300 | 300 | 2004 |
| object_id | 850 | 850 | 1454 |
| resource_time | 372 | 372 | 1932 |
| reference_join | 1302 | 1302 | 1002 |
| relation_graph | 1512 | 1512 | 792 |
| relation_join | 1512 | 1512 | 792 |
| adaptive_pointer | 2304 | 2304 | 0 |
| object_relation_mix | 1555 | 1555 | 749 |
| full_evidence | 2304 | 2304 | 0 |

Overall grid-weighted mixture 1,555 versus graph 1,512 hides large condition changes: 227 paired wins and 184 losses. No overall ranking is promoted as universal. The full [aggregate](../reports/swarm-016-object-summary.json) includes every background/condition/method count/cost, 192 per-background method contrasts, 400 prespecified sensitivity contrasts (two metrics), eight overall contrasts, and 96 pooled-condition method contrasts.

### Realized ambiguity and mechanism

| Condition | Views | With earlier object distractors | Candidate distractors | Mix-selected distractor records | Mix fallback views |
| --- | ---: | ---: | ---: | ---: | ---: |
| explicit_collision_r100 | 192 | 155 | 1613 | 134 | 0 |
| explicit_collision_r050 | 192 | 79 | 376 | 126 | 119 |
| implicit_collision_r100 | 192 | 155 | 1613 | 134 | 0 |
| implicit_collision_r050 | 192 | 79 | 376 | 126 | 119 |

Bucket collisions do not automatically imply a selected distractor: visibility and recency matter. At explicit/full collision, 155/192 views have earlier same-ID distractors, and 134 distractor records are selected across the views. The mixture fills all three non-anchor slots from object matches, so join fallback never runs. With partial collision it runs in 119/192 views, but already selected distractors still consume budget. In unique conditions all object matches are true predecessors; p=0 produces exact mixture/join selection equality.

### Historical validation

See [research history](research-history.md) for the reported development, evaluation and reproduction chronology. This snapshot performs no new research run.

### Remaining structural assumptions

All metadata is available up to the query cutoff; each target is a known four-record chain and every true record is visible. Object corruption changes a synthetic observation signal, not real storage objects or log-authentication guarantees. All pointer payloads are exact in this stress grid. Four buckets, independent per-record masks, one query per ledger, and fixed recency priority cover a limited mechanism; they do not model semantic object ownership, coordinated attackers, real agents, or a calibrated distribution of missingness. The exact-pointer result is expected from its information contract.

