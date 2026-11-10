---
name: stop-slop
description: >-
  Eliminate predictable AI and Gemini writing patterns ("AI slop") from prose
  and Workspace deliverables while preserving factual accuracy, grounding
  citations, and domain register. Use when drafting, editing, humanizing,
  tightening, or auditing essays, blog posts, executive briefs, scheduled
  routine rollups, Google Docs, Slides, Gmail or Chat messages, or technical
  documentation to cut LLM buzzwords, eager assistant wrappers, retrieval
  narration, throat-clearing openers, formulaic contrasts, participial tails,
  and heading bloat, or when asked to make writing sound natural. Don't use for
  code-only generation, raw data dumps, legal contracts, or altering verbatim
  quotes and source citations.
metadata:
  trigger: Drafting, editing, humanizing, or auditing prose and Workspace deliverables for AI writing patterns
  author: Hardik Pandya (https://hvpandya.com)
---

# Stop Slop

Eliminate predictable AI and Gemini writing patterns from prose and Workspace deliverables without sacrificing factual precision, source grounding, or domain-appropriate voice.

## Precedence, Memory & Grounding Guardrails

1. **User, Brand & Personalized Memory Precedence:** Explicit user instructions, house style guides, or standing preferences already loaded from Personalized Memory (for example, bottom-line-up-front tables, em-dash permissions, or exact product casing such as *"Gemini agent"*) override any default rule below.
2. **Epistemic & Factual Preservation:** Never strip truthful quantifiers (*most, ~70%, often, in benchmarks*), scope conditions, dates, metrics, or caveats just to sound punchier. Turning an accurate bounded claim into a false universal ("most teams struggle" -> "all teams fail") is an accuracy bug.
3. **Protected Blocks & Grounding Fidelity:** Leave fenced code blocks, inline code identifiers, verbatim quotes, grounding citations (such as `[call_...]` or numeric `[1]` markers), Workspace resource URLs/links, issue IDs, and `@`-mentions untouched. Never drop or paraphrase away source attribution to shorten a sentence.

## Step 1: Select Mode, Register & Execution Tier

Choose an **Operating Mode**, a **Register / Surface Profile**, and the matching **Execution Tier** before writing or editing:

### Operating Modes
- **Draft Mode** (writing new content): Apply rules silently. Output the deliverable or answer directly; never print rubric scores, concierge preambles, or self-referential notes about avoiding slop.
- **Edit Mode** (rewriting existing content): Preserve core claims, grounding citations, and author voice while cutting AI patterns. When editing shared Google Docs, apply targeted paragraph-level replacements rather than regenerating whole sections so colleague comment threads, suggestions, and heading styles remain intact.
- **Audit Mode** (reviewing without rewriting): Run `scripts/lint_slop.py`, score the draft with the anchored rubric below, and report line-specific findings and concrete fix suggestions without replacing the document.

### Register & Surface Profiles

| Register | Typical Formats & Surfaces | Subject & Voice Rules | Structure & Linter Calibration |
| :--- | :--- | :--- | :--- |
| `essay` | Essays, blog posts, op-eds, talks, newsletters | Prefer human actors or direct *you*; put the reader in concrete scenes. | Strict rhythm checks; avoid em dashes by default; flag **Bold-Colon** walls at 3+ bullets. |
| `exec` | Executive briefs, memos, status rollups, Scheduled Routine digests | Lead with the bottom line; name owners, metrics, and dates; report current state, not search history. | Concise bullets and Markdown tables encouraged (table cells are linted for slop; **Bold-Colon** flagged at 6+). |
| `tech` | Developer docs, lab guides, RFCs, architecture notes | Concrete system subjects (*the scheduler, the API, the query*) may perform technical actions. | Functional adverbs (*asynchronously, locally*) and *When/If* clauses allowed; CLI/API parameter lists exempt. |
| `comms` | Gmail threads, Google Chat, Slack, stakeholder DMs | Keep brief, natural human greetings/sign-offs when appropriate; write like a direct colleague. | Ban stiff outreach clichés (*"finds you well"*) and multi-heading scaffolding in short messages. |
| `slides` | Google Slides decks, speaker bullets, executive one-pagers | Lead slide titles with the takeaway, metric, or decision; keep bullets parallel and concrete. | Concise <=5-word fragments allowed (exempt from staccato warnings); ban abstract gerund title slogans. |

### Tiered Execution Budget (Turn & Latency Discipline)
Every extra file read or shell command in Gemini agent costs a model turn while the user waits. Match tool usage to task size:
- **Fast Path (under ~150 words, `comms` replies, quick inline rewrites):** Apply the rules in this `SKILL.md` directly in a single pass. Do **not** read `references/` files or run `scripts/lint_slop.py` unless the user explicitly asks for an audit.
- **Full Path (150+ word drafts, Google Docs/Slides deliverables, Scheduled Routine digests, local files, or Audit Mode):** Read only the needed reference file (`references/phrases.md`, `references/structures.md`, or `references/examples.md`) in parallel with your initial context reads, and run `scripts/lint_slop.py` once before final delivery.

## Step 2: Core Editorial Rules

1. **Strip eager assistant wrappers and retrieval narration.** Never bookend deliverables with concierge chatter (*"Great question!"*, *"Here is a comprehensive breakdown..."*, *"Hope this helps!"*, *"Let me know if you'd like me to refine..."*). When synthesizing Gmail, Chat, Drive, or web sources, report the grounded state directly instead of narrating your lookup (*"After reviewing your recent emails and Docs, it appears..."* -> state the decision, owner, and date). Read `references/phrases.md`.
2. **Cut throat-clearing, emphasis crutches, and stiff outreach clichés.** Delete announcement openers (*"Here's the thing:"*, *"It turns out"*, *"In today's fast-paced..."*), performative closers (*"Let that sink in"*, *"And that's okay"*), and stiff `comms` filler (*"I hope this email finds you well"*, *"Please do not hesitate to reach out"*). Read `references/phrases.md`.
3. **Ban signature LLM, Gemini, and corporate buzzwords.** Replace classic LLM tells (*delve, tapestry, underscore, pivotal, seamless, foster, realm, multifaceted*), high-frequency Gemini filler (*robust, streamline, empower, holistic, actionable, frictionless, elevate, bridge the gap, single source of truth*, *unlock potential*, and *leverage* as a verb for *use*), and business clichés (*navigate uncertainty, lean into, game-changer, circle back*) with plain verbs and nouns. Read `references/phrases.md`.
4. **Separate empty intensifiers from functional adverbs.** Cut empty intensifiers and hedges (*really, genuinely, literally, fundamentally, inherently, crucially, simply, actually*). Keep load-bearing adverbs of manner, cadence, or technical execution (*asynchronously, sequentially, locally, weekly, strictly*) when removing them changes meaning.
5. **Break formulaic contrasts, Gemini transition chains, and participial tails.** Cut telegraphed reversals (*"Not because X, but because Y"*), symmetric *"While X, Y"* or *"Whether you're A or B"* openers, consecutive paragraph-initial additive transitions (*Additionally, Furthermore, Moreover, Specifically*), repetitive *(e.g., X, Y, and Z)* parenthetical stuffing, and tacked-on participial clauses (*"...highlighting/ensuring..."*). Read `references/structures.md`.
6. **Prefer concrete actors and active verbs.** Name who decides, ships, or blocks work. In `essay`, `exec`, and `comms`, do not give human verbs to abstractions (*"alignment emerged"*). Use passive voice only when the actor is unknown, irrelevant, or standard in `tech` procedures.
7. **Scale headings, lists, and rhythm to length and surface.** Avoid "scannability theater": do not split notes under ~250 words into four subheadings, numbered sub-lists, and bolded phrases in every sentence. Mix sentence lengths in prose; avoid reflexive three-item triads, rhetorical `Wh-` clefts, compulsive **Bold-Colon** walls, default em dashes, gerund slide slogans, and unprompted *"In conclusion / Ultimately"* recaps. Read `references/structures.md`.
8. **Trust the reader.** Delete meta-navigation (*"In this section, we will explore..."*), hand-holding transitions, and duplicate points repeated across prose and table cells. Read `references/examples.md`.

## Step 3: Deterministic Lint & Anchored Scoring

On the **Full Path** or in **Audit Mode**, run `scripts/lint_slop.py` from the directory you read this `SKILL.md` from:

```bash
python3 scripts/lint_slop.py path/to/draft.md --register exec
```

Pass `--register` (`essay`, `exec`, `tech`, `comms`, or `slides`), `-` to lint standard input, `--allow-em-dash` when house style or Memory permits em dashes, and `--json` for structured output. The linter automatically strips inline code, attributed quotes, URLs, and citation tokens before checking prose and Markdown table cells. Fix flagged lines unless an explicit style or accuracy rule justifies keeping them.

### Anchored Rubric (Internal Check Unless Auditing)

Score each dimension from 1 to 10. Revise if the total is **below 38/50** or **any single dimension is below 6**:

| Dimension | 1–3 (Slop) | 4–6 (Mechanical) | 8–10 (Human & Sharp) |
| :--- | :--- | :--- | :--- |
| **Directness** | Concierge bookends, retrieval narration, throat-clearing, or recap bloat. | Mostly direct, but leans on *"While X, Y"* setups or chained *Additionally/Moreover* transitions. | Starts with substance; reports state directly; every sentence advances the point. |
| **Precision** | Vague declaratives, Gemini filler (*robust, holistic, leverage*), or stripped caveats. | Specific in spots, with occasional buzzwords inside prose or table cells. | Concrete nouns/verbs, preserved metrics, citations, and quantifiers; zero filler adverbs. |
| **Rhythm & Scale** | Monotone ~15-word sentences, heading inflation on short notes, or **Bold-Colon** walls. | Some variation, but predictable triads, *(e.g., ...)* stuffing, or repetitive openers. | Cadence and heading density match length and surface (`essay`, `exec`, `tech`, `comms`, `slides`). |
| **Agency** | Passive fog and abstract nouns performing human actions. | Actors named in main clauses, but trailing *"highlighting/ensuring"* tails remain. | Named human, team, or concrete system actors driving active, specific verbs. |
| **Trust** | Lectures the reader, explains obvious takeaways, adds *"Hope this helps!"* or *"Let that sink in."* | Minimal hand-holding, but repeats table facts in prose or summarizes a short note. | States grounded evidence cleanly and stops once the job is done. |

## Bundled Resources

- `references/phrases.md` — Concierge wrappers, retrieval narration, throat-clearing, LLM and Gemini vocabulary, `comms` clichés, and adverb rules.
- `references/structures.md` — Contrasts, participial tails, transition chains, proportional scaffolding, surface rules (`slides`/`comms`/Docs), and agency.
- `references/examples.md` — Verified before/after rewrites across `essay`, `exec`, `tech`, `comms`, and `slides` registers.
- `scripts/lint_slop.py` — Deterministic CLI linter supporting all five registers, Markdown table-cell scanning, and citation/URL protection.
- `LICENSE` — MIT license.
