# 作業ルールとPR運用方針

作成日: 2026-05-14  
位置づけ: 研究プロジェクト運用ルール / PRレビュー方針  
Status: accepted  
Phase: P0  
Step: PR-A  
Covers: governance for C01, C03, C16, C18, C20  
Coverage note: governance rules introduced; substantive design specs are not yet accepted  
Supersedes: none  
Related ADR: none  
対象研究: LLMエージェントによる人間社会カオス・シミュレーション  
前提草案: 以下はリポジトリ外で作成済みの検討メモであり、後続PRで順次取り込む。
- `research_history_and_rationale.md`
- `research_framework_design.md`
- `technical_selection_for_social_simulation.md`
- `phase_step_checkpoint_coverage_plan.md`

---

## 0. 本文書の目的

この文書は、今後の研究作業をPR単位で進めるための運用ルールを定める。

本研究は、LLMエージェントを人間の完全な代理人として扱うものではない。LLMエージェントを、曖昧さ、圧力、利害、慣習、情報非対称、責任分散、制度疲労といった社会的摩擦を発生させる人工的参加者として使い、小さな人工組織における制度破綻の発生条件を探索する研究である。

そのため、通常のソフトウェア開発とは異なり、研究方針・シナリオ・評価指標・技術構成は検証過程で変わる可能性がある。一方で、変更が自由すぎると、何を検証したのか、どの前提が変わったのか、どの成果がどの設計要素をカバーしたのかが分からなくなる。

この文書では、以下を定める。

1. フォルダ構成ルール
2. ファイル命名・文書メタデータルール
3. PRの単位と禁止される混在
4. PR本文テンプレート
5. PRレビュー観点
6. checkpointと設計カバレッジ管理
7. 研究方針が変わる場合の変更管理

---

## 1. 基本原則

### 1.1 研究は変わってよいが、変更理由は残す

本研究では、初期仮説、scenario、event taxonomy、metrics、技術選定が後から変わることを前提にする。

ただし、変更は暗黙に行わない。変更する場合は、次のいずれかに記録する。

- PR本文
- `docs/adr/` の意思決定記録
- `docs/coverage_ledger.md` のギャップ・状態更新
- 該当するspec文書のrevision note

### 1.2 PRは「作業量」ではなく「意思決定単位」で切る

1つのPRは、1つの明確な問いまたは意思決定に対応させる。

悪い例:

> ODD-Socialを直し、scenarioを追加し、event taxonomyを変更し、runnerも少し直す。

良い例:

> P1-S02として、支払・購買ドメイン用のODD-Social v0.1を追加する。

### 1.3 研究主張と実装変更を混ぜない

研究上の主張、scenario設計、評価指標、実装コード、実験結果は、できるだけ別PRにする。

特に、以下は同じPRに混ぜない。

- 新しい研究主張 + 実装変更
- scenario追加 + event taxonomy大幅変更
- 実験結果 + 評価基準の後出し変更
- 技術選定変更 + 既存結果の解釈変更

### 1.4 地図画像ではなくカバレッジ台帳で管理する

以前の「世界地図のように色塗りする」可視化は採用しない。

代わりに、`docs/coverage_ledger.md` を用いて、研究全体設計の各構成要素がどのPR・どのcheckpointでどの状態になったかを表形式で管理する。

### 1.5 LLMログは証拠だが、人間社会の直接証明ではない

LLMエージェントの挙動は、社会的摩擦や制度破綻の仮説を生成するための証拠である。

ただし、LLMがそう振る舞ったことをもって、「人間も必ずそう振る舞う」とは主張しない。

---

## 2. 推奨フォルダ構成

初期段階では、コード実装よりも研究設計・scenario・評価プロトコルを優先する。フォルダ構成は以下を基準にする。

```text
repo-root/
  README.md
  CONTRIBUTING.md

  docs/
    research/
      00_history_and_rationale.md
      01_framework_design.md
      02_phase_step_checkpoint_plan.md
      03_working_rules_and_pr_policy.md
      04_technical_selection.md

    adr/
      ADR-0001-research-positioning.md
      ADR-0002-technical-architecture.md

    coverage_ledger.md
    glossary.md

  protocols/
    odd-social/
      odd-social-v0.1.md
      odd-social-template.md

    evaluation/
      event-taxonomy-v0.1.md
      metrics-v0.1.md
      evidence-pack-v0.1.md
      human-review-protocol-v0.1.md

  scenarios/
    org-payment/
      README.md
      scenario-matrix.md
      s01-clear-policy-low-pressure.yaml
      s02-ambiguous-policy-low-pressure.yaml
      s03-ambiguous-policy-high-pressure.yaml
      s04-role-overlap-high-pressure.yaml
      s05-audit-intervention.yaml
      s06-hard-control.yaml

  society/
    org-payment/
      organization.yaml
      roles.yaml
      norms.yaml
      incentives.yaml
      communication_channels.yaml
      trust_network.yaml

  institutions/
    org-payment/
      policies/
      controls/
      sanctions/
      audit_rules/

  schemas/
    scenario.schema.json
    agent.schema.json
    event.schema.json
    evidence-pack.schema.json

  experiments/
    planned/
      exp-0001-baseline-payment.md
    completed/
      exp-0001-summary.md

  runs/
    .gitkeep

  results/
    org-payment/
      exp-0001/
        README.md
        aggregate_metrics.csv
        event_summary.md
        evidence_samples/

  reviews/
    pr-0002.md
    pr-0003.md

  src/
    social_sim/
      .gitkeep

  tests/
    .gitkeep

  legacy/
    README.md
```

---

## 3. フォルダごとのルール

### 3.1 `docs/research/`

研究の経緯、全体設計、ロードマップ、作業ルール、技術選定を置く。

ルール:

- 研究の根幹に関わる文書だけを置く。
- 古い文書を黙って削除しない。
- 大きく方針が変わった文書には、冒頭に `Status: superseded` または `Status: revised` を書く。
- 最新の中心文書はREADMEからリンクする。

### 3.2 `docs/adr/`

研究上・技術上の重要な意思決定を記録する。

ADRが必要な例:

- 研究対象をAIエージェント評価から人間社会カオス疑似再現へ変更する。
- LangChain DeepAgentsを中核にしない。
- Game Master / Arbiter型を採用する。
- 初期ドメインを支払・購買に限定する。
- event taxonomyを大幅に変更する。

ADRファイル名:

```text
ADR-0001-research-positioning.md
ADR-0002-game-master-architecture.md
ADR-0003-initial-domain-org-payment.md
```

ADRの基本構成:

```markdown
# ADR-000X: Title

Date:
Status: proposed | accepted | superseded

## Context
## Decision
## Alternatives considered
## Consequences
## Follow-up
```

### 3.3 `docs/coverage_ledger.md`

設計カバレッジを管理する台帳。

地図画像ではなく、この台帳を正とする。

各PRで、カバー対象が変わる場合は更新する。

推奨フォーマット:

```markdown
| ID | Design area | Status | First covered by | Latest PR | Evidence | Remaining gaps | Next step |
|---|---|---|---|---|---|---|---|
| C01 | Research Concept | Accepted | P0-S01 | PR #x | research_history... | none | revisit after P7 |
| C04 | ODD-Social | Draft | P1-S01 | PR #y | odd-social-v0.1 | not dry-run tested | P5-S01 |
```

Statusは以下を使う。

| Status | 意味 |
|---|---|
| Not started | 未着手 |
| Draft | 文書案がある |
| Specified | 仕様として一旦定義済み |
| Tried | dry run / pilotで試した |
| Revised | 検証により修正済み |
| Validated | checkpointを通過した |
| Extended | 別ドメイン・別条件に拡張済み |
| Superseded | より新しい設計に置き換え済み |

### 3.4 `protocols/`

研究プロトコルを置く。コードではなく、実験・評価・記録方法の仕様を管理する。

例:

- ODD-Social記述プロトコル
- event taxonomy
- metrics定義
- evidence pack仕様
- human review protocol
- LLM judge利用ルール

ルール:

- `v0.1`, `v0.2` のようにバージョンを明記する。
- 仕様が変わった場合、古い版を削除せず、必要なら `superseded` とする。
- 実験結果PRで評価基準を後出し変更しない。

### 3.5 `scenarios/`

検証scenarioを置く。

ルール:

- ドメインごとにサブフォルダを切る。
- 初期ドメインは `org-payment/` とする。
- 1つのscenarioファイルは1つの比較条件を表す。
- scenario matrixは `scenario-matrix.md` にまとめる。
- scenarioごとに、操作変数と非操作変数を明記する。

scenarioファイル名例:

```text
s01-clear-policy-low-pressure.yaml
s02-ambiguous-policy-low-pressure.yaml
s03-ambiguous-policy-high-pressure.yaml
s04-role-overlap-high-pressure.yaml
s05-audit-intervention.yaml
s06-hard-control.yaml
```

### 3.6 `society/`

人工社会の人口・役割・関係・慣習・利害を置く。

ここには、LLMプロンプトそのものではなく、社会モデル上の定義を置く。

例:

- 組織構造
- 役割
- 上下関係
- 信頼関係
- 非公式慣習
- incentive
- 情報共有構造
- communication channel

### 3.7 `institutions/`

制度、規程、権限、監査、制裁、hard controlを置く。

ルール:

- agent prompt内に制度を閉じ込めない。
- Institution Layerとして、環境側の制約を明示する。
- soft / monitored / hard controlの違いをファイル上で識別できるようにする。

### 3.8 `schemas/`

YAML / JSON / JSONLの構造検証用schemaを置く。

初期は未完成でよいが、P3以降のPRではschema整備を進める。

対象:

- scenario
- agent / role
- action
- event
- metrics
- evidence pack

### 3.9 `experiments/`

実験計画と実験要約を置く。

ルール:

- `planned/` には実行前の実験計画を置く。
- `completed/` には実験後の要約だけを置く。
- raw run dataは `runs/` または外部保存先に置き、必要なサンプルのみ `results/` に整理する。

### 3.10 `runs/`

実行生成物の置き場。

ルール:

- 原則としてGit管理しない。
- `.gitignore` で除外する。
- 各runは `run_id` ごとに完全分離する。
- 後から検証する場合は、必要なものだけ `results/` にcurated evidenceとして移す。

### 3.11 `results/`

公開・レビュー用に整理した実験結果を置く。

ルール:

- raw log置き場ではない。
- 集計結果、代表的evidence、結果解釈、限界を置く。
- 結果PRでは、評価基準がどのprotocol versionに基づくかを明記する。

### 3.12 `reviews/`

PRレビューの記録を置く。

PR単位でAIレビューを行うため、必要に応じてレビュー結果を保存する。

例:

```text
reviews/pr-0002.md
reviews/pr-0003.md
```

レビュー記録には、以下を含める。

- PR番号
- 対象phase / step
- 対象設計要素
- Must fix
- Should fix
- Consider
- Merge readiness
- checkpoint判断

### 3.13 `legacy/`

既存PoCコードや旧設計を保存する。

ルール:

- 既存コードはすぐに削除しない。
- 新研究基盤への移行時に、比較対象・履歴として残す。
- legacy内のコードを研究基盤の正としない。

---

## 4. ファイル命名ルール

### 4.1 基本

- Markdown: lowercase kebab-case
- YAML: lowercase kebab-case
- JSON schema: lowercase kebab-case + `.schema.json`
- Event type: snake_case
- PR branch: type/phase-step-short-title

例:

```text
odd-social-v0.1.md
event-taxonomy-v0.1.md
s03-ambiguous-policy-high-pressure.yaml
scenario.schema.json
approval_bypass
responsibility_diffusion
```

### 4.2 ID体系

| 種類 | 形式 | 例 |
|---|---|---|
| Phase | `P0`〜`P9` | `P3` |
| Step | `P3-S02` | `P3-S02` |
| Design component | `C01`〜`C20` | `C13` |
| Scenario | `S01`〜 | `S04` |
| Experiment | `EXP-0001` | `EXP-0001` |
| ADR | `ADR-0001` | `ADR-0002` |
| Event type | snake_case | `responsibility_diffusion` |

### 4.3 Markdown冒頭メタデータ

主要Markdownには冒頭に以下を書く。

```markdown
# Title

Date: 2026-05-14
Status: draft | proposed | accepted | revised | superseded
Phase: P1
Step: P1-S02
Covers: C04, C05, C06
Supersedes: none
Related ADR: ADR-0001
```

---

## 5. PR単位のルール

### 5.1 1 PR = 1 checkpointに近づける

PRは、原則として1つのphase / step / checkpointに対応させる。

例:

| PR種別 | 良いPR単位 |
|---|---|
| research docs | 研究の位置づけを1文書に固定する |
| ADR | 1つの設計判断を記録する |
| protocol | event taxonomy v0.1を追加する |
| scenario | S01〜S03の初期scenario matrixを追加する |
| evidence | evidence pack仕様v0.1を追加する |
| experiment plan | EXP-0001の実験計画を追加する |
| result | EXP-0001の結果要約を追加する |
| code | 1つのモジュール + 対応テストを追加する |

### 5.2 混ぜてはいけないPR

以下の混在は避ける。

| 混在 | 理由 |
|---|---|
| 研究方針変更 + 実装 | 何を検証したのか不明になる |
| event taxonomy変更 + 実験結果 | 評価基準の後出しに見える |
| scenario追加 + 技術選定変更 | 研究条件と実装条件が同時に動く |
| raw run追加 + 解釈文書追加 | 証拠と主張の境界が曖昧になる |
| refactor + behavior change | 差分レビューが困難になる |

### 5.3 PRサイズ目安

| 種別 | 目安 |
|---|---|
| docs / research | 1〜3ファイル、中心論点1つ |
| ADR | 1ファイル |
| protocol | 1仕様または密接に関係する2仕様まで |
| scenario | 1 scenario familyまたはscenario matrix v0.1 |
| code | 1責務のmodule + tests |
| results | 1 experiment単位 |

大きくなる場合は、PR本文で「なぜ分割しないのか」を説明する。

---

## 6. ブランチ・PRタイトル・ラベル

### 6.1 ブランチ名

```text
docs/p0-s01-research-positioning
adr/p0-s03-game-master-decision
protocol/p3-s01-event-taxonomy
scenario/p2-s01-org-payment-matrix
experiment/p7-s01-baseline-plan
results/p7-s03-baseline-summary
code/p4-s02-run-store
refactor/legacy-isolation
```

### 6.2 PRタイトル

```text
[P0-S01] Fix research positioning and scope
[P1-S02] Add ODD-Social v0.1 for org-payment domain
[P3-S01] Add event taxonomy v0.1
[P7-S01] Add baseline experiment plan EXP-0001
```

### 6.3 推奨ラベル

```text
phase/P0
phase/P1
phase/P2
phase/P3
phase/P4
phase/P5
phase/P6
phase/P7
phase/P8
phase/P9

type/docs
type/adr
type/protocol
type/scenario
type/architecture
type/experiment-plan
type/results
type/code
type/refactor

status/draft
status/needs-review
status/needs-revision
status/checkpoint
status/ready-to-merge
status/superseded

risk/research-scope
risk/evaluation
risk/validity
risk/reproducibility
risk/implementation
```

---

## 7. PR本文テンプレート

PR本文は以下のテンプレートを使う。

```markdown
## Summary

このPRで何を追加・変更するか。

## Phase / Step

- Phase:
- Step:
- Checkpoint:

## Covered design components

- Cxx:
- Cxx:

## Motivation

なぜこの変更が必要か。
研究上の問い、前提、既存文書との関係を書く。

## Changes

- 変更1
- 変更2
- 変更3

## Non-goals

このPRでは扱わないこと。

## Validation performed

- [ ] markdown check
- [ ] link check
- [ ] terminology consistency check
- [ ] schema validation
- [ ] dry run
- [ ] human review
- [ ] not applicable

## Impact on coverage ledger

- [ ] `docs/coverage_ledger.md` を更新した
- [ ] カバレッジに影響しない

## Risks / uncertainties

- 未確定の論点
- 後続PRで検証すべきこと

## Reviewer focus

レビューで特に見てほしい点。

## Checkpoint decision proposed

- [ ] Advance
- [ ] Revise
- [ ] Branch
- [ ] Reduce
- [ ] Retire
- [ ] Escalate
```

---

## 8. PRレビュー方針

ユーザーはPR単位でAIレビューを依頼する。レビューでは、単なるコードレビューではなく、研究方針との整合性を確認する。

### 8.1 レビュー時に見る観点

| 観点 | 確認内容 |
|---|---|
| Scope | 1 PR = 1意思決定になっているか |
| Phase alignment | 対象phase / stepに合っているか |
| Design coverage | どのC要素をカバーするか明確か |
| Research consistency | 研究目的がAI評価に戻っていないか |
| Claim control | 主張が証拠より強すぎないか |
| Change management | 既存方針変更がADR/coverageに残っているか |
| Evaluation readiness | event / metric / evidenceとの関係が明確か |
| Reproducibility | 後から同じ条件を追えるか |
| Reviewability | 差分が小さく、レビュー可能か |
| Non-goals | 扱わないことが明記されているか |

### 8.2 レビュー結果の分類

レビュー結果は、以下の分類で返す。

```markdown
## Review summary

## Merge readiness
- Ready
- Ready with minor fixes
- Not ready
- Needs redesign

## Must fix
マージ前に直すべき点。

## Should fix
強く推奨するが、後続PRでもよい点。

## Consider
検討事項。

## Coverage impact
どの設計要素が進み、どこが未カバーか。

## Checkpoint recommendation
Advance / Revise / Branch / Reduce / Retire / Escalate
```

### 8.3 Merge readinessの基準

| 判定 | 意味 |
|---|---|
| Ready | そのままマージ可能 |
| Ready with minor fixes | 軽微な文言・形式修正後にマージ可能 |
| Not ready | PRの範囲・証拠・整合性に問題がある |
| Needs redesign | 前提や設計判断を見直すべき |

---

## 9. Checkpoint運用

各PRは、単に「マージする/しない」ではなく、checkpointとして次の判断を行う。

| 判断 | 意味 | 例 |
|---|---|---|
| Advance | 次のstepへ進む | ODD-Social v0.1が十分明確 |
| Revise | 同じstep内で修正 | event定義が曖昧 |
| Branch | 複数案を残す | 2種類のscenario設計を比較したい |
| Reduce | 複雑性を減らす | agent数や変数が多すぎる |
| Retire | 仮説・event・scenarioを外す | 観察不能または低価値 |
| Escalate | 外部確認が必要 | 監査実務・法務・倫理判断が必要 |

Checkpoint判断はPR本文またはレビュー記録に残す。

---

## 10. 設計カバレッジ管理

### 10.1 カバー対象の設計要素

全体設計は以下の20要素で管理する。

| ID | Design area |
|---|---|
| C01 | Research Concept |
| C02 | Research Questions |
| C03 | Scope / Domain |
| C04 | ODD-Social |
| C05 | World / Environment |
| C06 | Institution Layer |
| C07 | Population Layer |
| C08 | Interaction Layer |
| C09 | Game Master / Arbiter |
| C10 | LLM Actor Layer |
| C11 | Scenario Matrix |
| C12 | Experiment Harness |
| C13 | Event Taxonomy |
| C14 | Metrics |
| C15 | Evidence Pack |
| C16 | Validity Protocol |
| C17 | Human / LLM Review |
| C18 | Reporting / Claims |
| C19 | Domain Expansion |
| C20 | Ethics / Misuse Boundaries |

### 10.2 カバレッジ更新ルール

PRが以下のいずれかに該当する場合、`docs/coverage_ledger.md` を更新する。

- 新しいC要素を初めて定義する
- C要素のstatusを進める
- C要素をsupersedeする
- C要素に未解決gapを追加する
- C要素の次stepを変更する

### 10.3 カバレッジ台帳の例

```markdown
| ID | Design area | Status | First covered by | Latest PR | Evidence | Remaining gaps | Next step |
|---|---|---|---|---|---|---|---|
| C01 | Research Concept | Accepted | P0-S01 | PR #2 | docs/research/00_history... | Scope drift risk | Revisit after P7 |
| C04 | ODD-Social | Draft | P1-S01 | PR #5 | protocols/odd-social/odd-social-v0.1.md | Not dry-run tested | P5-S01 |
| C13 | Event Taxonomy | Draft | P3-S01 | PR #7 | protocols/evaluation/event-taxonomy-v0.1.md | Inter-rater reliability unknown | P5-S02 |
```

---

## 11. 文書更新ルール

### 11.1 historical docsを消さない

研究経緯を追えるようにするため、重要文書は削除ではなく `superseded` として残す。

### 11.2 最新文書をREADMEで明示する

READMEには、最新の中心文書を列挙する。

例:

```markdown
## Current canonical documents

- Research history: docs/research/00_history_and_rationale.md
- Framework design: docs/research/01_framework_design.md
- Phase plan: docs/research/02_phase_step_checkpoint_plan.md
- Working rules: docs/research/03_working_rules_and_pr_policy.md
- Technical selection: docs/research/04_technical_selection.md
- Coverage ledger: docs/coverage_ledger.md
```

### 11.3 用語変更はglossaryに反映する

以下のような用語は `docs/glossary.md` で統一する。

- social chaos
- institutional failure
- social friction
- Game Master / Arbiter
- Institution Layer
- evidence pack
- event taxonomy
- ODD-Social
- soft / monitored / hard control

---

## 12. 実験結果PRのルール

実験結果PRでは、結果そのものよりも、再検証可能性を重視する。

### 12.1 必須情報

- experiment id
- scenario id
- protocol version
- model / provider / parameters
- seed or randomization policy
- number of runs
- exclusion rule
- evidence pack location
- event taxonomy version
- metrics version
- known failure / uncertainty

### 12.2 禁止事項

- 評価基準を結果に合わせて後から変更する
- 代表例だけで一般化する
- LLMログだけを根拠に人間社会の結論を出す
- raw logを大量に追加して、レビュー不能にする

### 12.3 結果解釈の分類

結果は以下のように分類する。

| 分類 | 意味 |
|---|---|
| Observation | run内で観察された事実 |
| Pattern | 複数runで繰り返された傾向 |
| Hypothesis | 現実社会にもあり得ると考える仮説 |
| Claim | evidenceと妥当性確認により主張可能な結論 |
| Limitation | 主張できないこと |

---

## 13. コードPRのルール

コードレベルの検討は今後行うが、運用ルールとして先に最低限を定める。

### 13.1 研究仕様なしにコードを書かない

実装PRは、対応するspec / protocol / ADRを参照する。

例:

- Game Master実装 → ADR-0002 + protocol仕様
- event detector実装 → event-taxonomy-v0.1
- scenario loader実装 → scenario.schema.json

### 13.2 agentに世界状態を直接変更させない

本研究の中心思想として、LLM agentの自然言語行為と、環境上の状態遷移を分離する。

そのため、コードPRでは以下を守る。

- LLM actorは「意図」または「提案行為」を出す。
- Game Master / Arbiterが制度・権限・環境に基づいて裁定する。
- 世界状態の変更はGM/Arbiter側で記録される。

### 13.3 実装PRではテストまたは検証方法を書く

コードPRには、少なくとも以下を含める。

- unit test
- fixture test
- dry run
- schema validation
- あるいは、なぜ現時点で不要かの説明

---

## 14. AIレビュー依頼時の運用

ユーザーがPRレビューを依頼する場合、基本的にはPR URLだけでよい。

ただし、レビュー精度を上げるため、可能であれば次を添える。

```text
対象PR:
想定Phase / Step:
特に見てほしい点:
このPRでAdvanceしたいcheckpoint:
```

AIレビューでは、以下を行う。

1. PR本文を確認する。
2. diffを確認する。
3. 変更ファイルの位置づけを確認する。
4. 対象phase / step / C要素との対応を見る。
5. scope creepや混在を確認する。
6. 研究主張が強すぎないか確認する。
7. coverage ledger更新の必要性を見る。
8. Merge readinessとcheckpoint recommendationを返す。

---

## 15. 初期PR計画

今後の最初のPRは、以下の順序が望ましい。

### PR-A: 作業ルール導入

目的:

- 本文書をリポジトリに追加する。
- READMEまたはCONTRIBUTINGから参照する。

対象:

- `docs/research/03_working_rules_and_pr_policy.md`
- `CONTRIBUTING.md` または READMEの最小更新

checkpoint:

- 今後のPRレビュー単位が明確になる。

### PR-B: カバレッジ台帳導入

目的:

- 地図画像ではなく、表形式のcoverage ledgerを導入する。

対象:

- `docs/coverage_ledger.md`

checkpoint:

- C01〜C20の状態がPR単位で追跡できる。

### PR-C: ADR導入

目的:

- 研究方針転換と技術方針の重要判断をADRとして固定する。

対象:

- `docs/adr/ADR-0001-research-positioning.md`
- `docs/adr/ADR-0002-game-master-architecture.md`
- `docs/adr/ADR-0003-initial-domain-org-payment.md`

checkpoint:

- 研究の前提を後から追跡できる。

### PR-D: ODD-Social v0.1

目的:

- 人工組織を記述するための最初のプロトコルを定義する。

対象:

- `protocols/odd-social/odd-social-v0.1.md`
- `protocols/odd-social/odd-social-template.md`

checkpoint:

- コードを書かずに、初期ドメインの社会モデルを説明できる。

### PR-E: org-payment scenario matrix v0.1

目的:

- 初期支払・購買ドメインの比較scenarioを定義する。

対象:

- `scenarios/org-payment/scenario-matrix.md`
- `scenarios/org-payment/s01-...yaml` など

checkpoint:

- どの条件差を検証するかが明確になる。

---

## 16. この文書自体の更新ルール

この文書は固定ではない。

ただし、変更する場合は以下を守る。

- PRで変更する。
- 変更理由をPR本文に書く。
- PR単位、folder rule、review ruleを変える場合はADR化を検討する。
- 既存PRレビューの前提が変わる場合は、影響を明記する。

---

## 17. 最終方針

この研究では、作業を速く進めることよりも、後から研究経緯・判断・証拠・限界を追えることを優先する。

そのため、今後の運用方針は以下とする。

> 研究設計は検証によって変わってよい。  
> ただし、変更はPR単位で行い、どのphase / step / design componentに影響したかを記録する。  
> PRレビューでは、コード品質だけでなく、研究方針、証拠性、再現性、主張可能範囲を確認する。  
> 地図画像ではなく、coverage ledgerによって設計カバレッジを管理する。
