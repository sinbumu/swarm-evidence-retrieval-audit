# Historical design counterexamples

**Public snapshot adaptation.** This describes the historical study; it is not a new preregistration or an execution instruction. Private Git ancestry, original locks and raw evidence are absent. Source commit/file hashes in [provenance](../provenance.json) identify the supplied bytes but do not independently establish when the design was fixed. See [evidence limits](evidence-availability.md). Operational coordination text is omitted; the original remains preserved privately.

## Counterexamples to conflating observation and truth

Aliases in this table are hand-checkable fixture names, never production record identifiers. R is the root, J the known anchor; the four-node private fork has J→{A,B}, A→R, B→R. S lists paid distinct records in a hypothetical checker input, not an asserted output of an unimplemented selector. All unspecified approvals are true.

| Case | Private truth and observed change | Read set S | True recovery | Expected observed diagnostic | Consequence |
| --- | --- | --- | --- | --- | --- |
| Zero evidence | Intact chain | ∅ | 0/4; incomplete | Unknown | No query answer without anchor evidence. |
| One branch missing | Intact fork | J,A,R | 3/4; incomplete | Unknown | Resolving one branch does not satisfy AND. |
| False value visible but other branch missing | Intact fork; A=false | J,A,R | 3/4; incomplete | Unknown | Resolve all asserted dependencies before a definitive assertion. |
| Shared root | Intact fork; R=false | J,A,B,R | 4/4; complete | Asserted violation | R is one record/read despite two incoming paths. |
| Null branch with full true set | Fork J→{A,null}; arity remains2 | J,A,B,R | 4/4; complete | Unknown | Complete retrieval does not repair a missing assertion. |
| False pointer takes a shortcut | Private chain J→B→A→R; B=false; observed J→D00, D00 is a true distractor leaf | J,D00 | 1/4; incomplete | Asserted normal, wrong against private label | A resolved asserted closure is not the private required set. |
| Oracle supplies R but misses the false target | Same false-pointer chain | J,B,A,R | 4/4; complete | Unknown | An oracle retrieval diagnostic does not make the checker trustworthy. |
| Full R plus false target | Same false-pointer chain | J,B,A,R,D00 | 4/4; complete | Asserted normal, wrong | Even all true evidence can be ignored by the redirected observed closure. |
| False branch omits a negative | Private fork; B=false; observed J→{A,D00} | J,A,R,D00 | 3/4; incomplete | Asserted normal, wrong | Extra asserted terminal roots are accepted by the general checker; no hidden trusted root-count rule. |
| Agreement with incomplete/wrong evidence | Private fork; A=false; observed J→{A,D00} | J,A,R,D00 | 3/4; incomplete | Asserted violation, agrees | Agreement must not be called genuine identification. |
| Eight-node budget shortage | Intact chain k8, B4 | J,B3,B2,B1 | 4/8; incomplete | Unknown | No method can recover eight distinct records with four reads. |
| Duplicate versus shared dependency | Observed J→{A,A} versus valid A→R and B→R | J,A,B,R | Complete in both | Duplicate-in-one-node unknown; shared-root case valid | Set deduplication must not silently repair malformed AND slots. |
| Coherently rewritten arity, outside evaluation | Private fork; B=false; asserted J has arity1 and parent A | J,A,B,R | 4/4; complete | Asserted normal, wrong | The evaluation forbids arity edits; their absence is a model restriction, not authentication. This is a trust counterexample only. |
| Negative irrelevant leaf | Private fork normal; observed J→{A,D00}; D00=false | J,A,R,D00 | 3/4; incomplete | Asserted violation, wrong | A negative approval in a distractor is not a true target violation. |

The JSON fixture file specifies all24 cases, including k8 fork closure, cycles and nonpublic targets. Cases marked out-of-model/negative tests never become extra evaluation conditions. The alias-to-test-ID mapping fixes lexical tie-breaks for12 intact frontier traces. Development must also cover the full72 topology/k/budget/label/condition combinations. A handwritten trace expectation is not a measured run.

## Hidden-assumption challenge

| Challenge | Resolution fixed before implementation | Remaining limit / rejection criterion |
| --- | --- | --- |
| Does fork/join silently require an extra join/root record? | k includes every unique root/interior/anchor; 4 and8 records in both structures; common R, N=32, k-independent candidate size | Any extra proof/manifest/branch record outside k or unequal pools is no-go. |
| Does matching nodes also match edges and damage severity? | No: chain has k−1 edges, fork/join k. Exactly one anchor assertion changes, not an edge-wise drop probability. Explicitly report q/m cut consequences and analytic expectations | This is one anchor-fault structural intervention, not arbitrary-fault robustness or an isolated branching-factor effect. |
| Can IDs, ordering or metadata reveal generator roles? | Opaque uniformly randomized IDs under a private frozen key; identical format, constant catalog/query sizes, only ID/size in metadata; seeds/slots/k/topology/keys never cross method boundary; canonical ordering and permutation tests; background diamonds have arities0/1/2 and independent approval bits | Logical Python API boundary, not a security sandbox. Payload arity learned after a paid read is legitimate observed structure. Any private field or unsalted positional encoding in actual input blocks acceptance. |
| Is global graph access uncharged? | No metadata edges at all. Only full ID catalog is supplied and charged; parent assertions are inside paid payloads. Every frontier reference resolution, scan, index and sort is counted | Full catalog itself is a strong access assumption. No free backend payload inspection or precomputed reachable set. |
| Does the traversal use a topology-specific oracle? | Same level-synchronous BFS, ID tie-break, dedup and one final blind fallback, with no k/topology/label argument | Batching exploits observed branching; it does not discover whether assertions are true. False edges are followed. |
| Does a union of two branches get charged as one read? | Every new ID in every batch costs one512-byte read; a shared ID is read once, with every reference inspection/lookup still counted | Failed/repeated requests are logged, rejected atomically, and never used for free probing. |
| Can null or false references redefine private truth? | R and label derive from private DAG/approval before observation mutation; preserve them across conditions | Arity/approval immutability is a restricted fault model, not authenticated truth. False-reference membership is determined only by offline scoring. |
| Is normal/violation ambiguous under AND? | Private AND over all distinct R nodes; one uniformly chosen required nonanchor false in violation view; checker separately ANDs only a fully resolved asserted closure | Unknown precedes false-value shortcut. Normal and violation views are correlated paired views, not new families. |
| Is checker correctness tautological or oracle-assisted? | Named asserted outputs, separate offline agreement/false-normal/unknown; examples of incomplete agreement and complete-retrieval wrong assertion; diagnostics excluded from method ranking | No genuine identification metric. A negative distractor can cause false violation. Intact sufficient-budget success is a model consequence. |
| Will many views inflate uncertainty precision? |96 new families, each with72 correlated views. One shared2000×96 bootstrap matrix; average labels within family;72 predeclared contrast intervals | No row bootstrap, pooling older cohorts, post-hoc weighting, multiplicity claim or significance-driven selection. |
| Can favorable data rescue a failed contract? | Versioned protocol, before-evaluation freeze, unit/development corrections logged within fixed gate, at most2 dev attempts; final eval failure stops with raw evidence preserved | Scientific changes require a new version and coordination; any inspected eval cohort is spent for design correction. No weakened expected fixture or silently skipped family. |
| Is there enough time to finish the whole result responsibly? | Worst-case4–6h phase2 +90min evaluation/audit +3h report; acceptance by2026-11-08 10:29 KST reserves completion by20:59 KST | Estimates are unmeasured for this new implementation. Recheck measured dev time and remaining wall time; stop with the SWARM-017 report intact if gates cannot fit. |

