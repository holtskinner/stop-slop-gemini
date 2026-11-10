# Phrases to Cut or Replace

## 1. Eager Assistant Wrappers & Retrieval Narration (Gemini & Agent Tells)

Gemini's most recognizable habit in agentic workflows is wrapping deliverables in polite concierge chatter and narrating its own Workspace search steps. Cut both unless the user asked a casual conversational question.

### Cut: Concierge Openers & Closers
- "Great question!" / "Excellent question!"
- "Certainly! Here is a comprehensive breakdown of..."
- "Here is an overview / summary / look at..."
- "Hope this helps!"
- "Let me know if you'd like me to refine / adjust / dive deeper into any section!"
- "Feel free to reach out / ask if you need anything else."

### Cut: Retrieval & Synthesis Narration
State the grounded fact, owner, and citation directly instead of describing how you found it:
- "Based on the provided documents / context..." -> State the finding and cite the source.
- "After reviewing your recent Gmail threads and Drive documents, I found..." -> Lead with the current status or blocker.
- "Upon reviewing the tracker..." -> Name the metric or row state directly.

## 2. Throat-Clearing Openers & Outreach Clichés

Delete announcement phrases that delay the claim.

### General Prose Openers
- "Here's the thing:"
- "Here's what / why / how [X]"
- "The uncomfortable truth is"
- "It turns out (that)"
- "The real [X] is"
- "Let me be clear"
- "The truth / reality is,"
- "I'll say it again:"
- "I'm going to be honest"
- "Can we talk about"
- "In today's fast-paced [world / landscape / era]"
- "In a world where"
- "It's worth noting (that)"
- "When it comes to"
- "At its core"
- "At the end of the day"

### Email & Chat Clichés (`comms` & `exec`)
Keep brief human warmth (*"Hi Maya,"*, *"Thanks, Alex"*), but cut stiff template filler:
- "I hope this email / message finds you well."
- "Please do not hesitate to reach out."
- "Just circling back / touching base on..."
- "Per my last email..."

## 3. Emphasis Crutches & Permission Endings

These manufacture gravitas or false intimacy without adding evidence. Delete them.

- "Full stop." / "Period."
- "Let that sink in."
- "Make no mistake"
- "This matters because" / "Here's why that matters"
- "And that's okay."
- "I promise." / "They exist, I promise."

## 4. High-Frequency LLM & Gemini Vocabulary

Beyond older GPT-4 tells (*delve, tapestry*), Gemini leans heavily on abstract enterprise verbs and polish adjectives (*robust, streamline, holistic, actionable, leverage*). Swap them for concrete mechanisms.

| Avoid | Plain Replacement |
| :--- | :--- |
| Robust | Fault-tolerant, redundant, tested under 10k RPS (state what makes it strong) |
| Streamline | Cut two approval steps, automate, shorten from 5 days to 1 |
| Leverage (as a verb for *use*) | Use, call, query, reuse (keep *leverage* only for financial debt or physics) |
| Holistic / end-to-end (as filler) | Full-stack, cross-team, covering X, Y, and Z |
| Actionable | Specific, assigned to an owner, ready to run |
| Empower / supercharge / elevate | Let, enable, allow, speed up |
| Frictionless / seamless / seamlessly | Zero-config, single-click, automatic, direct |
| Unlock [potential / value / insights] | Expose, cut latency, surface, allow |
| Bridge the gap (between X and Y) | Connect X to Y, sync X with Y |
| Single source of truth (used vaguely) | Canonical tracker, primary table, authoritative repo |
| Delve (into) | Examine, inspect, test, read |
| Tapestry / symphony / kaleidoscope | Mix, set, system, collection |
| Underscore / highlight / showcase | Show, prove, expose |
| Testament (to) | Proof (of), result (of) |
| Pivotal / paramount / crucial | Key, decisive, required, blocking |
| Foster / cultivate / spearhead | Build, train, lead, fund |
| Realm / landscape / ecosystem (vague) | Field, market, stack, toolset |
| Multifaceted / nuanced (as filler) | Complex (name the specific parts) |
| Interplay | Interaction, tradeoff, feedback loop |
| Overarching | Main, shared, top-level |
| Bolster / garner | Strengthen, earn, win |

## 5. Corporate & Business Jargon

| Avoid | Plain Replacement |
| :--- | :--- |
| Navigate uncertainty / challenges | Handle, resolve, cut risk |
| Unpack | Explain, break down |
| Lean into | Commit to, accept, test |
| Game-changer | Major shift (state the measurable impact) |
| Double down | Increase budget/focus, commit |
| Deep dive | Audit, investigation, breakdown |
| Take a step back | Reassess, check assumptions |
| Moving forward | Next, starting Monday, in Q4 |
| Circle back | Follow up, revisit on [date] |
| Low-hanging fruit | Quick fixes, first targets |
| Synergy | Shared savings, combined throughput |

## 6. Empty Intensifiers vs. Functional Adverbs

Do **not** blindly delete every word ending in `-ly`. Separate empty intensifiers from load-bearing modifiers:

### Cut: Empty Intensifiers & Performative Hedges
- `really`, `just`, `literally`, `genuinely`, `honestly`, `simply`, `actually`
- `deeply`, `truly`, `fundamentally`, `inherently`, `inevitably`
- `crucially`, `importantly`, `interestingly`, `remarkably`, `undoubtedly`

### Keep: Functional Adverbs & Non-Adverb `-ly` Words
- **Technical execution & manner:** `asynchronously`, `concurrently`, `sequentially`, `locally`, `remotely`, `deterministically`, `automatically`, `manually`, `strictly`, `explicitly`
- **Cadence & time:** `daily`, `weekly`, `quarterly`, `annually`, `immediately`, `previously`
- **Epistemic precision (when backed by uncertainty or data):** `approximately`, `roughly`, `statistically`, `conditionally`
- **Nouns/adjectives ending in `-ly`:** `family`, `early`, `only`, `likely`, `supply`, `reply`, `assembly`, `anomaly`, `costly`, `timely`

## 7. Meta-Commentary & Unprompted Recap Closers

Do not narrate the document's structure or summarize a short note at the bottom.

- "Hint:" / "Plot twist:" / "Spoiler:"
- "You already know this, but"
- "But that's another post"
- "X is a feature, not a bug"
- "Let me walk you through..."
- "In this section, we'll explore..."
- "In conclusion," / "Ultimately," / "To summarize," / "All in all,"

## 8. Vague Declaratives

Never announce that something is important, structural, or high-stakes without naming the concrete mechanism or cost.

- "The reasons are structural" -> Name the incentive, org boundary, or quota rule.
- "The implications are significant" -> State what breaks, speeds up, or changes cost.
- "The stakes are high" -> Name the deadline, revenue exposure, or outage risk.
