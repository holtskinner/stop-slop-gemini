# Verified Before/After Examples Across Registers

Every **After** example below passes `scripts/lint_slop.py` under its target `--register` with zero warnings while preserving factual qualifiers, links, and citations.

## Example 1: Opinion Essay (`essay` register)

**Before:**
> Here's the thing: building products is genuinely hard. Not because the technology is complex, but because people are complex. In today's fast-paced landscape, teams need to lean into discomfort and navigate uncertainty—highlighting why alignment actually matters. Let that sink in.

**After:**
> Shipping software gets hard once three teams share one roadmap. You can debug a flaky database query in an afternoon, while two directors can argue for a month over who owns checkout latency. Clear ownership unblocks engineers faster than another planning offsite.

**Why it works:** Cuts throat-clearing, empty intensifiers, binary contrast, corporate jargon, em dash, participial tail, and emphasis crutch. Replaces abstractions with a concrete engineering scene and varied sentence lengths (9, 22, and 11 words).

---

## Example 2: Preserving Quantifiers & Data (`essay` / `exec` registers)

**Before:**
> It turns out that most enterprise pilots stall before production. The uncomfortable truth is that roughly 68% of teams lack production evaluation datasets, underscoring a pivotal gap in governance. And that's okay—everyone is still learning.

**After:**
> Most enterprise AI pilots stall before reaching production. In last quarter's survey, roughly 68% of platform teams had no production evaluation dataset to catch regressions before launch. Building a 100-row golden test set fixes that blind spot in a week.

**Why it works:** Preserves truthful quantifiers (*"Most"*, *"roughly 68%"*) instead of exaggerating into *"Every pilot stalls"*, while deleting throat-clearing openers, LLM vocabulary (*underscoring, pivotal*), the em dash, and the patronizing *"And that's okay"* closer.

---

## Example 3: Paragraph Rewrite Without Unprompted Summary (`essay` register)

**Before:**
> While code review tools have evolved, teams still delve into nitpicks over formatting. What makes this frustrating is that deep architectural flaws slip through the cracks, fostering technical debt. Ultimately, engineering leaders must cultivate a culture of high-signal feedback.

**After:**
> Reviewers still burn twenty minutes debating variable names on a pull request while missing an unindexed join that will lock the orders table at peak traffic. Run a formatter in CI so humans spend review time on data models, failure modes, and rollback plans.

**Why it works:** Removes the *"While X, Y"* opener, `Wh-` cleft (*"What makes this..."*), LLM buzzwords (*delve, fostering, cultivate*), and the unprompted *"Ultimately..."* moralizing closer.

---

## Example 4: Multi-Source Rollup With Table & Citations (`exec` register)

**Before:**
> Great question! After reviewing your recent Gmail threads and Drive documents, here is a comprehensive breakdown of the Q4 Billing Migration:
>
> | Workstream | Status | Update |
> | :--- | :--- | :--- |
> | Ledger Cutover | Amber | Leveraging holistic caching, ensuring seamless throughput [call_401.2]. |
> | EU Compliance | Green | Streamlining audit logs to bridge the gap with legal [Tracker](https://docs.google.com/spreadsheets/d/abc). |
>
> Hope this helps! Let me know if you'd like me to dive deeper into any section!

**After:**
> **Q4 Billing Migration Rollup (Nov 10): Amber**
> Cutover holds for Nov 24 across 85% of accounts, gated on p99 invoice-write latency (420 ms vs. 200 ms SLO) [call_401.2].
>
> | Workstream | Status | Next Milestone & Owner |
> | :--- | :--- | :--- |
> | Ledger Cutover | Amber | Priya benchmarking connection pooling by Nov 12 before sharding decision [call_401.2]. |
> | EU Compliance | Green | Legal signed off on retention schema; audit export ships Nov 14 in [Migration Tracker](https://docs.google.com/spreadsheets/d/abc). |

**Why it works:** Strips the concierge bookends and retrieval narration (*"After reviewing your recent Gmail threads..."*), cleans Gemini buzzwords (*leveraging, holistic, ensuring seamless, streamlining, bridge the gap*) inside Markdown table cells, and preserves `[call_401.2]` grounding citations and the Sheets link intact.

---

## Example 5: Technical Documentation (`tech` register)

**Before:**
> Whether you're a new contributor or a seasoned SRE, background jobs are pivotal. When it comes to queues, workers leverage Redis seamlessly. Additionally, tasks run asynchronously, ensuring robust reliability. Furthermore, retries happen automatically.

**After:**
> Workers poll the `jobs` queue in Redis every 500 ms and execute handlers asynchronously in isolated subprocesses. When a handler exits with a non-zero status or exceeds its 30-second timeout, the scheduler requeues the payload with exponential backoff up to five attempts.

**Why it works:** Cuts the formulaic *"Whether you're A or B"* opener, Gemini buzzwords (*leverage, seamlessly, ensuring, robust*), and chained *Additionally / Furthermore* transitions, while keeping functional adverbs (*asynchronously*, *automatically* if needed), a conditional *When* clause, and system subjects.

---

## Example 6: Stakeholder Email or Chat (`comms` register — Fast Path)

**Before:**
> Subject: Quick Sync
>
> Hi Dana,
>
> I hope this email finds you well! Just circling back on the London workshop lab guide.
>
> ### 1. Current Overview
> Based on the attached doc, we are empowering proctors with a robust new setup flow.
>
> ### 2. Actionable Next Steps
> Please do not hesitate to reach out if you have feedback before Thursday!

**After:**
> Subject: Sign-Off Needed by Thu 2 PM PT: London Workshop Lab Guide
>
> Hi Dana,
>
> Can you confirm whether the 40 sandbox accounts for Tuesday's London workshop are provisioned in `argon-prod` by Thursday at 2:00 PM PT? Once confirmed, I will lock the participant lab guide and send the proctor runbook.
>
> Thanks,
> Holt

**Why it works:** Keeps natural human warmth (*"Hi Dana," / "Thanks, Holt"*), deletes stiff outreach clichés (*"finds you well"*, *"circling back"*, *"do not hesitate"*), removes multi-heading inflation on a 50-word note, and puts the exact ask and deadline in sentence one.

---

## Example 7: Presentation Slide (`slides` register)

**Before:**
> ## Unlocking Next-Gen Developer Onboarding
> - Empowering engineers with holistic sandbox environments, ensuring frictionless setup
> - Leveraging automated scripts to streamline regional workshop prep

**After:**
> ## Pre-Warmed Sandboxes Cut Workshop Setup From 25 Minutes to 90 Seconds
> - Provision 150 isolated cloud projects per event via Terraform
> - Pre-load sample datasets and API credentials before doors open
> - Eliminate local laptop dependency failures across 12 tour cities

**Why it works:** Replaces an abstract gerund slogan title (*"Unlocking Next-Gen..."*) with a concrete metric takeaway, removes Gemini filler (*empowering, holistic, ensuring frictionless, leveraging, streamline*), and uses crisp parallel verb phrases suited to slides.
