# Study and result guide

The cohorts are distinct; their observations are not pooled. A family is the independent seed-level unit. Multiple conditions, backgrounds, methods and label views within a family are paired observations, not independent samples. Intervals are descriptive paired family-bootstrap intervals for the fixed simulator, not multiplicity-adjusted population or safety claims.

| Study | Evaluation families | Development / evaluation seeds | Main contract | Included result |
| --- | --- | --- | --- | --- |
| Original exploratory pilot SWARM-007 | 24 | 101–106 / 1001–1024 | Four-record workflows, metadata baselines, four reads | [summary](../reports/swarm-007-summary.json) |
| Original comparison SWARM-009 | 24 | 201–206 / 2001–2024 | Nine selectors plus true-record diagnostic;12 conditions ×2 backgrounds | [summary](../reports/swarm-009-summary.json) |
| Fresh repetition SWARM-016 | 192 | 301–306 / 3001–3192 | Same generator/grid;4,608 views | [summary](../reports/swarm-016-repeat-summary.json) |
| Object stress SWARM-016 | 96 | 401–406 / 4001–4096 | Explicit/implicit references ×unique/four-bucket IDs ×retention1/0.5/0 | [summary](../reports/swarm-016-object-summary.json) |
| Fixed reservation SWARM-017 | 96 | 501–506 / 5001–5096 | Reserve two relation-ranked nonanchor slots, one object/fallback slot | [summary](../reports/swarm-017-summary.json) |
| Matched topology SWARM-018 | 96 | 601–606 / 6001–6096 | Chain/fork,32 IDs,k4/8,B4/8/12,intact/null/false-leaf anchor assertion | [summary](../reports/swarm-018-summary.json) |

Original workflows contain produce, transform, authorize and commit records; three actor IDs are assigned A,B,C,B. Each workflow samples three entries without replacement from a12-ID pool. Separate draws from the same seeded generator set object reuse and approval with thresholds0.5; this does not guarantee exact sample balance or statistical independence. Private violation is false authorization. Background8/24 workflows are generated separately, not a causal load intervention.

The original fixed-stage checker follows payload pointers and validates IDs/stages/values/approval; malformed or incomplete chains yield unknown. Only a valid chain distinguishes Boolean approval false versus true. Metadata graph and equivalent join use the same information; adaptive reads discover pointers sequentially. A complete true set can still yield unknown if asserted payload pointers are damaged.

The topology checker instead resolves the asserted prerequisite closure and ANDs observed approvals. References point dependent→prerequisite. A false-leaf target is a background root with no own prerequisites, but other background records may reference it. Observed closure can differ from private required membership. Full-catalog access can therefore produce false verdicts despite complete retrieval; the true-set oracle abstains under damaged references in this frozen model. These are different checker contracts.

## Results and bounded interpretation

The repetition completes2,989/4,608 views with graph/join,3,594 with adaptive and3,797 with the object-relation mixture. In object stress, explicit/full collision reduces mix to110/192 versus graph192/192. Fixed reservation gains under explicit partial collisions (137 versus120/192) but regresses overall (1,535 versus1,626/2,304); implicit unique/full retention falls109 versus192/192. All gains and losses remain in the complete summaries and [repeat/object results](swarm-016-results.md), [reservation results](swarm-017-results.md).

For topology k4/B12, fork-minus-chain completion is +18.75 percentage points [11.46,27.08] under either null or false-leaf faults. Gains are limited for k8. All18 blind fork-minus-chain differences are zero; blind completion counts are not all zero. The [topology results](swarm-018-results.md) retain all18 primary,18 control and36 method contrasts, all240 conditional groups and costs. Zero-event empirical intervals do not establish population zero. Topology/edge counts and fault cut severity are not isolated from one another.

## Protocol descriptions

- [Original four-record model](swarm-007-pilot.md)
- [Fresh repetition](swarm-016-repeat-protocol.md)
- [Object linkage/collisions](swarm-016-object-protocol.md)
- [Fixed relation reservation](swarm-017-protocol.md)
- [Matched topology](swarm-018-topology-protocol-v1.md) and [hand counterexamples](swarm-018-acceptance-v1.md)

These are adapted scientific descriptions of historical designs. Original private chronology/freeze claims cannot be independently established from this snapshot. No new experiment or authorization to run one is implied. Read [evidence limits](evidence-availability.md) and [research history](research-history.md).
