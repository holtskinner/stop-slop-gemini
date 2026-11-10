# Evaluation Suite: `stop-slop`

## Test Case 1: Opinion Essay Paragraph Rewrite (`essay` register, Edit Mode)
- **Prompt**: "Rewrite this paragraph to sound human and cut AI slop: 'Here's the thing: building products is genuinely hard. Not because the technology is complex, but because people are complex—highlighting why alignment is pivotal in today's fast-paced landscape. Let that sink in.'"
- **Expected Output**: Connected, concrete prose with varied sentence lengths, active human subjects, zero em dashes, zero banned phrases, and no printed rubric score.
- **Verification**: Run `python3 scripts/lint_slop.py <output_file> --register essay` and confirm `PASS (essay register): 0 slop patterns flagged`, plus verify sentence lengths are not 3 consecutive <=5-word fragments.

## Test Case 2: Factual Quantifier & Inline Verbatim Quote Preservation (Edit Mode)
- **Prompt**: "Tighten this section without changing any data or quotes: 'It turns out that roughly 64% of enterprise migrations overrun their initial timeline, underscoring a multifaceted challenge. As CTO Maya Lin wrote, \"Here's the thing: we underestimated legacy data cleanup by six months.\" Ultimately, teams must lean into early discovery.'"
- **Expected Output**: Keeps `roughly 64%` and preserves Maya Lin's inline verbatim quote (including `"Here's the thing:"` inside quotes) word-for-word, while cutting `"It turns out"`, `"underscoring"`, `"multifaceted"`, `"Ultimately"`, and `"lean into"` from the surrounding prose.
- **Verification**: Confirm `64%` and the exact quoted string appear unchanged, and `python3 scripts/lint_slop.py <output_file> --register essay` passes with 0 issues even with the inline quote present.

## Test Case 3: Technical Documentation (`tech` register, Edit Mode)
- **Prompt**: "Clean up the AI slop in this developer guide section while keeping technical accuracy: 'Whether you're new or experienced, event ingestion is pivotal. When it comes to payloads, the gateway leverages schemas seamlessly. When a client omits the `Idempotency-Key` header, the service rejects the request immediately and logs the error locally, ensuring robust safety. In conclusion, always pass a key.'"
- **Expected Output**: Preserves the conditional `When a client omits...` clause, inline code `` `Idempotency-Key` ``, system subjects (`the gateway`, `the service`), and functional adverbs (`immediately`, `locally`), while removing `"Whether you're..."`, `"When it comes to"`, `"leverages"`, `"seamlessly"`, `", ensuring robust safety"`, and `"In conclusion"`.
- **Verification**: Run `python3 scripts/lint_slop.py <output_file> --register tech` and verify 0 issues flagged and all technical terms/conditions preserved.

## Test Case 4: Executive Rollup With Table, Citations & Links (`exec` register)
- **Prompt**: "Clean up this status rollup without losing links or citations: 'Great question! After reviewing your recent Gmail threads and Drive docs, here is a comprehensive breakdown:\n\n| Stream | Status | Notes |\n| --- | --- | --- |\n| Auth | Amber | Leveraging holistic caching, ensuring seamless SSO [call_88.1]. |\n| Docs | Green | Streamlining guides in [Runbook](https://docs.google.com/document/d/123) [call_89.2]. |\n\nHope this helps! Let me know if you'd like me to refine anything!'"
- **Expected Output**: Drops the concierge bookends and retrieval narration, rewrites the slop inside the Markdown table cells into concrete status notes, and keeps `[call_88.1]`, `[call_89.2]`, and `[Runbook](https://docs.google.com/document/d/123)` intact.
- **Verification**: Confirm `scripts/lint_slop.py` flags `assistant-wrapper`, `retrieval-narration`, `gemini-phrase`, `llm-vocabulary`, and `participial-tail` on the input, and `PASS (exec register): 0 slop patterns flagged` on the rewritten output with all citations/links preserved.

## Test Case 5: Audit Mode (Review Without Rewriting)
- **Prompt**: "Audit this draft for AI writing patterns and score it—do not rewrite it yet: 'While cloud costs vary, teams must delve into usage metrics. Not because finance demands it, but because efficiency fosters innovation. Let that sink in.'"
- **Expected Output**: Lists specific line-level findings (`delve`, binary contrast `Not because... but because`, `fosters`, `Let that sink in.`), provides the 5-dimension anchored rubric score (< 38/50), and does **not** replace the user's draft with a full rewrite.
- **Verification**: Confirm all four slop patterns are cited and the 5-dimension rubric breakdown is included.

## Test Case 6: Explicit Style-Guide or Memory Override (`--allow-em-dash`)
- **Prompt**: "Edit this paragraph to remove AI buzzwords, keeping our publication's house style of using em dashes for parenthetical asides: 'In today's landscape, our compiler—written in Rust by three engineers—seamlessly fosters faster builds, underscoring a pivotal win.'"
- **Expected Output**: Preserves the parenthetical em-dash aside (`—written in Rust by three engineers—`) per house style while cutting `"In today's landscape"`, `"seamlessly"`, `"fosters"`, `"underscoring"`, and `"pivotal"`.
- **Verification**: Run `python3 scripts/lint_slop.py <output_file> --register essay --allow-em-dash` and confirm 0 issues flagged and em dashes remain intact.

## Test Case 7: Fast-Path Stakeholder Email (`comms` register)
- **Prompt**: "Draft a quick email to @dana asking her to confirm sandbox quota for Friday's Austin workshop by Wednesday 3pm CT."
- **Expected Output**: Executes on the Fast Path (single pass, no unnecessary reference/linter round trips), keeps a natural greeting/sign-off, omits `"I hope this email finds you well"`, `"Please do not hesitate"`, and subheadings, and states the quota ask and Wednesday 3:00 PM CT deadline in sentence one.
- **Verification**: Confirm output is under 120 words, has 0 subheadings, and passes `python3 scripts/lint_slop.py <output_file> --register comms` with 0 issues.

## Test Case 8: Slide Deck Rewrite (`slides` register)
- **Prompt**: "Tighten this slide so it doesn't read like AI marketing fluff: '## Unlocking Next-Gen Pipeline Velocity\n- Empowering data teams with holistic lineage, highlighting seamless governance\n- Leveraging automated checks to streamline schema changes'"
- **Expected Output**: Replaces the gerund slogan title with a concrete metric or outcome title and uses concise parallel verb phrases (even <=5 words) without triggering staccato-fragment warnings.
- **Verification**: Confirm `scripts/lint_slop.py --register slides` flags `slide-slogan-title` on the input and returns `PASS (slides register): 0 slop patterns flagged` on the output.

## Test Case 9: Google Docs Surgical Edit & Memory Product Casing (Edit Mode)
- **Prompt**: "Edit paragraph 2 of our shared Google Doc to cut AI buzzwords without disturbing colleague comments on paragraphs 1 and 3, keeping Personalized Memory casing for 'Gemini agent'."
- **Expected Output**: Applies a targeted replacement only to paragraph 2 rather than overwriting the full document, and preserves exact `"Gemini agent"` lowercase-*agent* casing.
- **Verification**: Confirm only the targeted range is modified and `"Gemini agent"` casing is preserved.
