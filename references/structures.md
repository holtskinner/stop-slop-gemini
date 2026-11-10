# Structural Patterns to Avoid

## 1. Binary Contrasts & Negative Listings

AI leans on negation-then-reveal templates to manufacture drama. State the affirmative claim directly unless contrasting two real, concrete options.

| Formulaic Pattern | Direct Fix |
| :--- | :--- |
| "Not because X, but because Y." | "Because Y." / State how X and Y differ concretely. |
| "[X] isn't the problem. [Y] is." | "[Y] causes the bottleneck." |
| "The answer/question isn't X. It's Y." | "Ask Y instead." / State Y directly. |
| "It's not just X; it's Y." | Name both concrete effects without theatrical buildup. |
| "Not an X. Not a Y. A Z." | "Build a Z." |
| "stops being X and starts being Y" | Describe what changed in behavior or design. |

## 2. Participial Tail Clauses

Appending `, highlighting...`, `, underscoring...`, or `, ensuring...` to explain why the main clause matters is a textbook LLM tell across prose, slide bullets, and status table cells.

| Slop Pattern | Fix |
| :--- | :--- |
| "The team cut build times by 40%, highlighting the value of caching." | "Caching cut the team's build times by 40%." |
| "We added schema checks, ensuring seamless downstream ingestion." | "Schema checks block malformed rows before ingestion." |
| "Attendance doubled in Q3, underscoring strong developer demand." | "Attendance doubled in Q3 from 420 to 850 developers." |

## 3. Gemini Openers, Additive Transition Chains & `(e.g., ...)` Stuffing

Gemini exhibits three distinct sentence- and paragraph-level habits:

1. **Formulaic Range Openers:** Opening sections with `"Whether you're a startup founder or an enterprise architect, ..."` or `"From small scripts to global deployments, modern teams..."` adds zero information. Start with the specific audience or problem.
2. **Symmetric `"While X, Y"` & Chained Additive Transitions:** Starting consecutive paragraphs or bullets with `"Additionally,"`, `"Furthermore,"`, `"Moreover,"`, or `"Specifically,"`—or repeating `"While [concession], [claim]"`—creates a mechanical checklist cadence. Cut the connector or link clauses through concrete cause and effect.
3. **Parenthetical `(e.g., X, Y, and Z)` Saturation:** Packing two or three `(e.g., ...)` parentheticals into one paragraph breaks reading flow. Weave one sharp example directly into the sentence instead.

## 4. Heading Inflation & Scannability Theater

Left unchecked, Gemini splits a 150-word email or status note into four `###` headings, numbered sub-lists, and bolded phrases in every sentence.

- **Proportional structure:** Under ~250 words (especially in `comms` and short `exec` updates), default to clean paragraphs or a single compact table/list without multi-level subheadings unless the user requested a template.
- **Register-calibrated Bold-Colon lists:**
  - In `essay` and `comms`: Avoid `- **Abstract Label:** explanation` bullet walls (3+ in a row reads like an LLM).
  - In `exec`: Up to 4–5 bolded owner/workstream bullets or a Markdown table work well when labels are real nouns (`**Auth Cutover (Priya):**`), not abstract buzzwords (`**Strategic Synergy:**`).
  - In `tech` and `slides`: Bolded flag/parameter lists (`**--timeout:**`) and concise parallel slide items are idiomatic—keep them, and keep their prose free of buzzwords.

## 5. Workspace Surface Adaptations (`slides`, `comms`, and Google Docs)

- **Google Slides (`slides`):**
  - *Titles:* Ban abstract gerund slogans (`"Unlocking Next-Gen Velocity"`, `"Empowering Seamless Collaboration"`). Write takeaway titles with a verb or metric (`"Pre-Warming Containers Cuts Lab Startup to 90 Seconds"`).
  - *Body bullets:* Short, parallel fragments (3–6 words) belong on slides and are exempt from prose staccato-fragmentation rules.
- **Gmail, Chat & Slack (`comms`):**
  - Keep natural 1-line human openings (`"Hi Sam,"`) and sign-offs, lead with the ask or answer in sentence one, and put deadlines/owners in plain text rather than over-formatted headers.
- **Google Docs In-Place Edits (Edit Mode):**
  - Prefer targeted paragraph/sentence replacements over rewriting an entire document from top to bottom so existing comment threads, suggested edits, and heading styles survive.

## 6. Dramatic Fragmentation ("Broetry") in Prose

In `essay`, `exec`, and `comms` prose, stacking ultra-short fragments reads like engagement bait.

- **Avoid:** `"Speed. Quality. Cost. Pick two. That's it. That's the job."` (6 fragments in 11 words)
- **Better:** `"Every release trades off speed, quality, and budget; pick which two govern this sprint."`

## 7. Rhetorical Setups & `Wh-` Cleft Openers

- **Cut rhetorical clefts:** `"What makes distributed caching hard is invalidation."` -> `"Cache invalidation causes most distributed state bugs."`
- **Cut condescending prompts:** `"What if I told you..."`, `"Think about it:"`, `"Here's what I mean:"`.
- **Keep legitimate `When` clauses & real questions:** Conditional clauses in `tech` and `exec` writing (*"When a worker exceeds its memory limit, the supervisor restarts the task"*) and genuine open questions are clean prose—keep them.

## 8. False Agency & Register-Aware Subjects

Abstract nouns cannot think, decide, or steer. Match subject rules to the active register:

- **In `essay`, `exec`, and `comms` registers:** Name the human, team, or organization.
  - Avoid: `"The alignment emerged during planning"` -> Fix: `"Product and Eng agreed on Q4 scope on Tuesday."`
- **In `tech` register:** Concrete software/hardware components *can* perform technical verbs (*"The load balancer drains open connections"*, *"The query scans two partitions"*), while vague abstractions still cannot (*"The architecture embraces simplicity"* -> *"Services query Postgres directly without a message broker"*).

## 9. Passive Voice & Legitimate Exceptions

Prefer active voice (`Actor -> Verb -> Object`) so accountability is clear:
- Avoid: `"A decision was reached to sunset v1."` -> Fix: `"Platform leadership decided to sunset v1 on May 1."`
- **Legitimate exceptions:** Keep passive voice when the actor is unknown, irrelevant to procedural focus (*"Tokens are hashed with SHA-256 before storage"*), or mandated by scientific/legal conventions.

## 10. Rhythm, Lists, Punctuation & Epistemic Precision

- **Sentence length variation:** In prose registers (`essay`, `exec`, `comms`), break runs of four equal-length (~14-word) sentences in a row.
- **Break reflexive triads:** AI defaults to groups of three (*"fast, scalable, and secure"*). Use the exact number of items that carry distinct meaning.
- **Em-dash discipline:** Default to periods, commas, colons, or parentheses unless the user's style guide or Personalized Memory explicitly permits em dashes.
- **Epistemic precision:** Cut unbacked lazy universals (`always`, `never`, `everyone`, `nobody`), and preserve real quantifiers (`most`, `often`, `rarely`, percentages) and inline grounding citations (`[call_...]`).
