# Synthetic evidence retrieval audit

This is the **public snapshot** of a small synthetic evidence-retrieval study at [sinbumu/swarm-evidence-retrieval-audit](https://github.com/sinbumu/swarm-evidence-retrieval-audit). The owner approved the selected 80-file snapshot plus a code-only MIT LICENSE and minimal publication guidance updates. The repository starts with a new initial commit; no private Git history is imported.

The study separates complete evidence retrieval from correct checking under different information-access assumptions. It compares metadata selection, sequential payload pointers, object linkage/collisions, a fixed reservation rule, and matched chains versus forks. It uses synthetic records and deterministic checkers, with no strategic agents, experimental model calls, real conversations or operational safety validation.

Start with the [latest manuscript adapted for this snapshot](report/swarm-report-draft.md), [study guide](docs/study-guide.md), and [evidence and reproduction limits](docs/evidence-availability.md). The manuscript derives from private-origin document commit `03914899e361944c4a687070f483f663f1dd40b3`. Its scientific main text, 183-word abstract and eight numerical tables are preserved; author identity and a private Discord quotation/reference are omitted. The private source PDF had eight main pages, one reference page and nine appendix pages. This Markdown derivative has no independently verified PDF pagination, and no public PDF/DOCX is included.

## Included material

- `src/`: 39 unchanged research source files.
- `configs/`: seven unchanged configurations, including the fixed numeric bootstrap index matrix.
- `tests/`: six unchanged research test files defining45 test methods by static inspection; none was run for this preparation. The historical60-test total also included15 service-integration tests excluded here.
- `fixtures/`: one hand-written synthetic topology fixture file, not a research sample.
- `reports/`: eight unchanged synthetic aggregate/timing JSON files, including unfavorable and zero/null results.
- `docs/`: adapted protocol/result descriptions, historical failure disclosure, evidence limits and rights/publication review.
- `report/`: the adapted Markdown manuscript, its guide, and one authored synthetic figure PNG.
- [provenance.json](provenance.json): exact payload allowlist, output hashes, private-origin commit/file hashes, transformations and exclusions.

No original Git history is imported. The separate origin repository is private and is not an accessible evidence source for a public reader. The snapshot records source commits, but does not make them reachable or prove their creation time. In particular, mentioning `bad9cfb`, `c24ca65` or a hash does **not** independently verify prospective freezing or preregistration. Adapted protocols are not byte-identical to the historical frozen protocol files.

## What can be checked

Readers can inspect source/configuration/fixtures, read all included aggregate cells and reported contrasts, compare the manuscript's tables, and check copied-file hashes. This does not reproduce the underlying observations or verify every aggregate from original raw rows. The [study guide](docs/study-guide.md) maps the separate cohorts and definitions.

This is **not a clone-only reproduction package**. Original raw observations, private keys, execution locks, audit inputs, the original instruction document, the template and original Git ancestry are excluded. Unchanged freeze routines reference some excluded inputs; the topology runner additionally checks private design commit `bad9cfb`, an elapsed evaluation-freeze date and a one-evaluation/one-reproduction limit used in the origin workspace. No state/key/attempt was reset or recreated, and no guard was relaxed. The matrix alone is insufficient. No research, tests or bootstrap ran during snapshot preparation; no executable quick-start is offered.

## Contributions and limits

The author chose the topic/scope, authorized the pilots/follow-ups and personally reviewed the research content and contribution description. Codex performed literature review, protocol/code development, historical tests/experiments, analysis and drafting. The author did not personally rerun the code or exhaustively reverify all numbers and cited originals. No LLM served as an experimental agent or judge. These facts do not establish independent scientific validation or final manuscript/submission approval. Personal author identification remains withheld in this public derivative.

The original research includes an import failure and later test-harness defects before evaluation. Their reported chronology is retained in [research history](docs/research-history.md); the original logs and archives are not included or claimed publicly verifiable. Synthetic assumptions, adverse results, conditional effects, abstentions, checker errors and uncertainty limitations remain explicit.

The [MIT LICENSE](LICENSE) applies only to `src/**/*.py` and `tests/test_record_*.py`. No license grant is made for the manuscript, other documentation, configurations, fixtures, aggregate data, figures or provenance index. See [rights and publication scope](docs/rights-and-publication.md). The original formatted PDF/DOCX, template, embedded fonts, third-party articles, recordings/transcripts and private coordination material are excluded.
