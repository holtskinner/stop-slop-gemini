#!/usr/bin/env python3
"""Deterministic prose and deliverable linter for the stop-slop skill.

Scans markdown or plain-text drafts across essay, exec, tech, comms, and slides
registers for predictable LLM and Gemini writing patterns while protecting
fenced code blocks, inline code, attributed quotes, URLs, and grounding
citations, and inspecting prose inside Markdown table data cells.
"""

import argparse
import json
import re
import sys
from typing import Any

ASSISTANT_WRAPPERS = [
    r"^\s*(?:great|excellent|fantastic|good)\s+question[!.,]",
    r"^\s*(?:certainly|absolutely|of course|sure thing)[!.,]\s+(?:here|let['’]?s|i\b)",
    r"^\s*here\s+is\s+a\s+(?:comprehensive\s+|detailed\s+|quick\s+|concise\s+)?(?:breakdown|overview|summary|look)\s+of\b",
    r"\bhope\s+this\s+helps[!.]?",
    r"\blet\s+me\s+know\s+if\s+you['’]?d\s+like\s+(?:me\s+to\s+|any\s+|more\s+)",
    r"\bfeel\s+free\s+to\s+(?:reach\s+out|ask)\s+if\b",
]

RETRIEVAL_NARRATION = [
    r"\b(?:based\s+on|after\s+reviewing|having\s+reviewed|from\s+my\s+review\s+of)\s+(?:the\s+provided\s+|your\s+recent\s+|the\s+attached\s+|your\s+)?(?:emails?|gmail\s+threads?|threads?|documents?|docs?|files?|context|workspace|messages?|chats?)\b",
    r"\bupon\s+reviewing\s+(?:your|the)\b",
]

COMMS_CLICHES = [
    r"\bi\s+hope\s+this\s+(?:email|message|note)\s+finds\s+you\s+well\b",
    r"\bplease\s+do\s+not\s+hesitate\s+to\b",
    r"\bjust\s+(?:wanted\s+to\s+)?(?:circling|circle)\s+back\b",
    r"\bper\s+my\s+last\s+(?:email|message)\b",
]

THROAT_CLEARING = [
    r"\bhere['’]?s the thing\b",
    r"\bhere['’]?s (?:what|this|that|why)\b",
    r"\bthe uncomfortable truth is\b",
    r"\bit turns out\b",
    r"\blet me be clear\b",
    r"\bthe truth is\b",
    r"\bi['’]?ll say it again\b",
    r"\bi['’]?m going to be honest\b",
    r"\bcan we talk about\b",
    r"\bin today['’]?s [a-z -]+(?:world|landscape|era|environment|age)\b",
    r"\bin a world where\b",
    r"\bit['’]?s worth noting\b",
    r"\bwhen it comes to\b",
    r"\bat its core\b",
    r"\bat the end of the day\b",
]

EMPHASIS_AND_META = [
    r"\bfull stop\.",
    r"\blet that sink in\b",
    r"\bmake no mistake\b",
    r"\bthis matters because\b",
    r"\bhere['’]?s why that matters\b",
    r"\band that['’]?s okay\b",
    r"\bplot twist:",
    r"\bspoiler:",
    r"\bis a feature, not a bug\b",
    r"\blet me walk you through\b",
    r"\bin this (?:section|essay|article|post), we['’]?ll\b",
]

RECAP_CLOSERS = [
    r"^\s*(?:in conclusion|ultimately|to summarize|in summary|all in all|to wrap up)\b",
]

LLM_AND_GEMINI_VOCAB = [
    "delve",
    "delves",
    "delving",
    "tapestry",
    "testament",
    "underscore",
    "underscores",
    "underscoring",
    "pivotal",
    "seamless",
    "seamlessly",
    "foster",
    "fosters",
    "fostering",
    "realm",
    "multifaceted",
    "interplay",
    "overarching",
    "bolster",
    "garner",
    "beacon",
    "robust",
    "streamline",
    "streamlines",
    "streamlining",
    "empower",
    "empowers",
    "empowering",
    "holistic",
    "actionable",
    "frictionless",
    "elevate",
    "elevates",
    "elevating",
    "spearhead",
    "spearheading",
    "supercharge",
    "supercharging",
]

GEMINI_PHRASES = [
    r"\bbridge\s+the\s+gap\b",
    r"\bsingle\s+source\s+of\s+truth\b",
    r"\bleverage(?:s|d|ing)?\b",
    r"\bunlock(?:s|ed|ing)?\s+(?:new\s+|the\s+|full\s+|true\s+|next-gen\s+)?(?:potential|value|efficiency|insights?|capabilities|power|growth|synergies|scalability)\b",
]

FORMULAIC_RANGE_OPENERS = [
    r"^\s*Whether\s+you['’]?re\s+[^,\n]+?\s+or\s+[^,\n]+,",
    r"^\s*From\s+[a-z\s]+?\s+to\s+[a-z\s]+?,\s+(?:modern|today['’]?s|every|organizations|teams|businesses|developers)\b",
]

BUSINESS_JARGON = [
    r"\bnavigate (?:uncertainty|challenges|complexity|the landscape)\b",
    r"\blean into\b",
    r"\bgame-changer\b",
    r"\bdouble down\b",
    r"\bdeep dive\b",
    r"\bcircle back\b",
    r"\blow-hanging fruit\b",
    r"\bsynergy\b",
    r"\bmoving forward\b",
    r"\btake a step back\b",
]

EMPTY_INTENSIFIERS = [
    "really",
    "just",
    "literally",
    "genuinely",
    "honestly",
    "simply",
    "actually",
    "deeply",
    "truly",
    "fundamentally",
    "inherently",
    "inevitably",
    "crucially",
    "importantly",
    "interestingly",
    "remarkably",
    "undoubtedly",
]

BINARY_CONTRASTS = [
    r"\bnot because [^.!?\n]+[,.;:]\s*(?:but )?because\b",
    r"\b(?:isn['’]?t|is not) the problem[.,;:]\s*[^.!?\n]+\bis\b",
    r"\bthe (?:answer|question) (?:isn['’]?t|is not)\b",
    r"\bit['’]?s not (?:just |about )?[^.!?\n]+[,;.]\s*it['’]?s\b",
    r"\bstops being [^.!?\n]+ and starts being\b",
]

PARTICIPIAL_TAILS = [
    r",\s*(?:highlighting|underscoring|emphasizing|ensuring|fostering|showcasing|demonstrating|paving the way|solidifying)\b",
]

VAGUE_DECLARATIVES = [
    r"\bthe reasons are structural\b",
    r"\bthe implications are significant\b",
    r"\bthe stakes are high\b",
    r"\bthe consequences are real\b",
]

WH_CLEFT_OPENERS = [
    r"(?:^|(?<=[.!?]\s))(?:What|Why|How)\s+(?:makes|matters|is\s+interesting|most\s+people|nobody|we\s+need|this\s+means)\b",
]

SLIDE_SLOGAN_HEADING_RE = re.compile(
    r"^#{1,3}\s+(?:Unlocking|Empowering|Transforming|Revolutionizing|Supercharging|Driving|Elevating|Reimagining|Navigating)\b"
)
ADDITIVE_OPENER_RE = re.compile(
    r"^\s*(?:[-*+]|\d+\.)?\s*(?:Additionally|Furthermore|Moreover|Specifically|Consequently),",
    flags=re.IGNORECASE,
)
EG_PAREN_RE = re.compile(r"\(\s*e\.g\.,[^)]+\)", flags=re.IGNORECASE)

INLINE_CODE_RE = re.compile(r"`[^`]+`")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((?:https?://|mailto:)[^)]+\)")
BARE_URL_RE = re.compile(r"https?://\S+")
CITATION_RE = re.compile(
    r"\[(?:source:\s*)?(?:call_[A-Za-z0-9_.,\s-]+|\d+(?:\s*,\s*\d+)*)\]"
)
MENTION_RE = re.compile(r"@[A-Za-z0-9_.-]+(?:@[A-Za-z0-9_.-]+)?")
INLINE_QUOTE_RE = re.compile(r'(?:"[^"\n]{8,}"|“[^”\n]{8,}”)')
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
BOLD_COLON_BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\*\*[^*]{2,60}:\*\*")
WHILE_OPENER_RE = re.compile(r"^\s*While\s+[^,\n]+,")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|=-]+\|\s*$")


def clean_protected_tokens(line: str) -> str:
  """Mask code, attributed quotes, URLs, citations, and @-mentions."""
  out = INLINE_CODE_RE.sub("code_token", line)
  stripped = out.strip()
  # Mask inline attributed quotations unless the entire line is wrapped in quotes.
  if not (
      (stripped.startswith('"') and stripped.endswith('"') and stripped.count('"') == 2)
      or (stripped.startswith("“") and stripped.endswith("”"))
  ):
    out = INLINE_QUOTE_RE.sub("quoted_span", out)
  out = MD_LINK_RE.sub(r"\1", out)
  out = BARE_URL_RE.sub("link_ref", out)
  out = CITATION_RE.sub("", out)
  out = MENTION_RE.sub("person_ref", out)
  return out


def check_segment_patterns(
    segment: str, idx: int, register: str, allow_em_dash: bool
) -> list[dict[str, Any]]:
  """Run lexical and structural regex checks against a single cleaned line or cell."""
  seg_findings: list[dict[str, Any]] = []

  if not allow_em_dash and ("—" in segment or " -- " in segment):
    seg_findings.append({
        "line": idx,
        "rule": "em-dash",
        "severity": "info" if register in ("tech", "slides") else "warn",
        "message": (
            "Em dash detected; replace with period, comma, or colon unless house"
            " style or Personalized Memory permits it."
        ),
    })

  pattern_groups = [
      (
          "assistant-wrapper",
          ASSISTANT_WRAPPERS,
          "warn",
          "Strip eager concierge wrapper; start and end with the deliverable itself.",
      ),
      (
          "retrieval-narration",
          RETRIEVAL_NARRATION,
          "warn",
          "Cut search/retrieval narration; state the grounded status and cite directly.",
      ),
      (
          "comms-cliche",
          COMMS_CLICHES,
          "warn",
          "Cut stiff email/Chat cliché; state the ask or context directly.",
      ),
      (
          "throat-clearing",
          THROAT_CLEARING,
          "warn",
          "Cut throat-clearing opener; state the claim directly.",
      ),
      (
          "emphasis-or-meta",
          EMPHASIS_AND_META,
          "warn",
          "Remove performative emphasis or meta-commentary.",
      ),
      (
          "recap-closer",
          RECAP_CLOSERS,
          "warn",
          "Delete unprompted summary opener; end once the point is made.",
      ),
      (
          "formulaic-range-opener",
          FORMULAIC_RANGE_OPENERS,
          "warn",
          "Cut formulaic 'Whether you're A or B / From X to Y' opener; name the concrete target.",
      ),
      (
          "business-jargon",
          BUSINESS_JARGON,
          "warn",
          "Replace corporate cliché with concrete action or noun.",
      ),
      (
          "binary-contrast",
          BINARY_CONTRASTS,
          "warn",
          "Rewrite telegraphed 'not X, but Y' contrast as a direct statement.",
      ),
      (
          "participial-tail",
          PARTICIPIAL_TAILS,
          "warn",
          "Cut or promote trailing participial clause ('..., highlighting/ensuring...').",
      ),
      (
          "vague-declarative",
          VAGUE_DECLARATIVES,
          "warn",
          "Replace vague importance claim with the specific consequence or metric.",
      ),
  ]
  for rule_id, patterns, severity, msg in pattern_groups:
    for pat in patterns:
      m = re.search(pat, segment, flags=re.IGNORECASE)
      if m:
        seg_findings.append({
            "line": idx,
            "rule": rule_id,
            "severity": severity,
            "match": m.group(0),
            "message": msg,
        })

  for pat in GEMINI_PHRASES:
    for m in re.finditer(pat, segment, flags=re.IGNORECASE):
      matched = m.group(0)
      low = matched.lower()
      if low.startswith("leverage"):
        msg = "Replace 'leverage' with 'use/call/query' unless referring to financial or mechanical leverage."
        sev = "warn"
      elif "single source of truth" in low:
        msg = "Replace 'single source of truth' with the specific tracker, table, or repo name."
        sev = "info" if register in ("exec", "tech") else "warn"
      else:
        msg = f"Replace Gemini cliché '{matched}' with the concrete mechanism or metric."
        sev = "warn"
      seg_findings.append({
          "line": idx,
          "rule": "gemini-phrase",
          "severity": sev,
          "match": matched,
          "message": msg,
      })

  for pat in WH_CLEFT_OPENERS:
    m = re.search(pat, segment)
    if m:
      seg_findings.append({
          "line": idx,
          "rule": "wh-cleft-opener",
          "severity": "warn",
          "match": m.group(0),
          "message": "Restructure rhetorical Wh- cleft opener; lead with the actor or concrete subject.",
      })

  vocab_regex = r"\b(" + "|".join(LLM_AND_GEMINI_VOCAB) + r")\b"
  for m in re.finditer(vocab_regex, segment, flags=re.IGNORECASE):
    seg_findings.append({
        "line": idx,
        "rule": "llm-vocabulary",
        "severity": "warn",
        "match": m.group(0),
        "message": f"Replace signature AI word '{m.group(0)}' with plain, concrete language.",
    })

  adv_regex = r"\b(" + "|".join(EMPTY_INTENSIFIERS) + r")\b"
  for m in re.finditer(adv_regex, segment, flags=re.IGNORECASE):
    seg_findings.append({
        "line": idx,
        "rule": "empty-intensifier",
        "severity": "warn",
        "match": m.group(0),
        "message": f"Cut empty intensifier/hedge '{m.group(0)}'.",
    })

  return seg_findings


def lint_text(
    text: str, register: str = "essay", allow_em_dash: bool = False
) -> dict[str, Any]:
  findings: list[dict[str, Any]] = []
  in_fence = False
  fence_marker = ""
  bold_colon_streak = 0
  while_opener_lines: list[int] = []
  additive_streak = 0
  eg_paren_lines: list[int] = []
  subheading_lines: list[int] = []
  total_doc_words = 0
  prose_paragraphs: list[tuple[int, str]] = []
  current_para_lines: list[str] = []
  current_para_start = 1

  bold_colon_limit = {"essay": 3, "comms": 3, "exec": 6}.get(register, 0)

  lines = text.splitlines()
  # Identify table header rows (immediately preceding a table separator row) so column names are not flagged as prose.
  table_header_indices: set[int] = set()
  for i, raw in enumerate(lines):
    if TABLE_SEP_RE.match(raw.strip()) and i > 0 and lines[i - 1].strip().startswith("|"):
      table_header_indices.add(i)  # 1-indexed line number of the header row

  for idx, raw_line in enumerate(lines, start=1):
    stripped = raw_line.strip()

    # Track fenced code blocks.
    fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
    if fence_match:
      marker = fence_match.group(1)[0]
      if not in_fence:
        in_fence = True
        fence_marker = marker
      elif marker == fence_marker:
        in_fence = False
        fence_marker = ""
      continue

    if in_fence:
      continue

    # Ignore verbatim blockquotes.
    if stripped.startswith(">"):
      if current_para_lines:
        prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))
        current_para_lines = []
      bold_colon_streak = 0
      continue

    # Inspect Markdown table body cells (>= 4 words) instead of skipping tables blindly.
    if stripped.startswith("|"):
      if current_para_lines:
        prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))
        current_para_lines = []
      bold_colon_streak = 0
      if TABLE_SEP_RE.match(stripped) or idx in table_header_indices:
        continue
      raw_cells = [c.strip() for c in stripped.strip("|").split("|")]
      for cell in raw_cells:
        clean_cell = clean_protected_tokens(cell)
        cell_words = len(re.findall(r"\b\w+\b", clean_cell))
        total_doc_words += cell_words
        if cell_words >= 4:
          findings.extend(
              check_segment_patterns(clean_cell, idx, register, allow_em_dash)
          )
      continue

    clean_line = clean_protected_tokens(raw_line)

    # Track headings and check slide slogan titles.
    if stripped.startswith("#"):
      if current_para_lines:
        prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))
        current_para_lines = []
      if re.match(r"^#{2,6}\s+", stripped):
        subheading_lines.append(idx)
      if register == "slides" and SLIDE_SLOGAN_HEADING_RE.match(stripped):
        findings.append({
            "line": idx,
            "rule": "slide-slogan-title",
            "severity": "warn",
            "match": stripped,
            "message": (
                "Slide title uses an abstract gerund slogan; lead with the"
                " concrete takeaway, metric, or decision."
            ),
        })
      continue

    if not stripped:
      if current_para_lines:
        prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))
        current_para_lines = []
      continue

    total_doc_words += len(re.findall(r"\b\w+\b", clean_line))

    # Track register-calibrated Bold-Colon bullet walls.
    if BOLD_COLON_BULLET_RE.match(raw_line):
      bold_colon_streak += 1
      if bold_colon_limit and bold_colon_streak == bold_colon_limit:
        findings.append({
            "line": idx,
            "rule": "bold-colon-wall",
            "severity": "warn",
            "message": (
                f"{bold_colon_limit}+ consecutive '**Bold:** explanation' bullets"
                f" in '{register}' register read as mechanical AI formatting;"
                " vary list style or use prose/tables."
            ),
        })
    else:
      bold_colon_streak = 0

    # Track paragraph prose for sentence-rhythm checks.
    is_list_item = bool(re.match(r"^(?:[-*+]|\d+\.)\s+", stripped))
    if not is_list_item:
      if not current_para_lines:
        current_para_start = idx
        # Check paragraph-initial additive transition chains.
        if ADDITIVE_OPENER_RE.match(clean_line):
          additive_streak += 1
          if additive_streak == 2:
            findings.append({
                "line": idx,
                "rule": "additive-transition-chain",
                "severity": "warn",
                "message": (
                    "Consecutive paragraphs open with mechanical additive"
                    " transitions (Additionally/Furthermore/Moreover/Specifically);"
                    " cut the connector or link via cause and effect."
                ),
            })
        else:
          additive_streak = 0
      current_para_lines.append(clean_line.strip())
    else:
      if current_para_lines:
        prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))
        current_para_lines = []
      if ADDITIVE_OPENER_RE.match(clean_line):
        additive_streak += 1
        if additive_streak == 2:
          findings.append({
              "line": idx,
              "rule": "additive-transition-chain",
              "severity": "warn",
              "message": (
                  "Consecutive bullets open with mechanical additive transitions"
                  " (Additionally/Furthermore/Moreover/Specifically); state items"
                  " directly."
              ),
          })
      else:
        additive_streak = 0

    # Track '(e.g., ...)' saturation.
    eg_matches = EG_PAREN_RE.findall(clean_line)
    for _ in eg_matches:
      eg_paren_lines.append(idx)

    # Symmetric 'While X, Y' openers.
    if WHILE_OPENER_RE.match(clean_line):
      while_opener_lines.append(idx)

    findings.extend(
        check_segment_patterns(clean_line, idx, register, allow_em_dash)
    )

  if current_para_lines:
    prose_paragraphs.append((current_para_start, " ".join(current_para_lines)))

  if len(while_opener_lines) >= 2:
    findings.append({
        "line": while_opener_lines[1],
        "rule": "repeated-while-opener",
        "severity": "warn",
        "message": (
            f"'While X, Y' opener repeated on lines {while_opener_lines}; vary"
            " sentence openings."
        ),
    })

  if len(eg_paren_lines) >= 3 or (
      len(eg_paren_lines) == 2 and eg_paren_lines[1] - eg_paren_lines[0] <= 6
  ):
    findings.append({
        "line": eg_paren_lines[1],
        "rule": "eg-parenthetical-stuffing",
        "severity": "info" if register == "tech" else "warn",
        "message": (
            f"Multiple '(e.g., ...)' parentheticals clustered on lines"
            f" {eg_paren_lines}; weave concrete examples directly into clauses."
        ),
    })

  # Proportional heading inflation check on short notes (excluding slides/tech).
  if register in ("essay", "exec", "comms") and 20 <= total_doc_words <= 220:
    if len(subheading_lines) >= 3 and (total_doc_words / len(subheading_lines)) < 55:
      findings.append({
          "line": subheading_lines[1],
          "rule": "heading-inflation",
          "severity": "warn" if register == "comms" else "info",
          "message": (
              f"{len(subheading_lines)} subheadings in a {total_doc_words}-word"
              " note create scannability theater; use clean paragraphs or one"
              " compact list."
          ),
      })

  # Sentence rhythm checks on prose paragraphs (essay, exec, comms only; slides and tech exempt).
  if register in ("essay", "exec", "comms"):
    for start_line, para in prose_paragraphs:
      sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(para) if s.strip()]
      word_counts = [len(re.findall(r"\b\w+\b", s)) for s in sentences]

      # Flag 3+ ultra-short staccato fragments in a row (<= 5 words each).
      for i in range(len(word_counts) - 2):
        window = word_counts[i : i + 3]
        if all(0 < w <= 5 for w in window):
          findings.append({
              "line": start_line,
              "rule": "staccato-fragmentation",
              "severity": "warn",
              "message": (
                  f"3 consecutive ultra-short sentences ({window} words) create"
                  " staccato 'broetry'; combine or vary length."
              ),
          })
          break

      # Flag 4+ consecutive medium/long sentences within a narrow +-2 word band.
      for i in range(len(word_counts) - 3):
        window = word_counts[i : i + 4]
        if min(window) >= 8 and (max(window) - min(window) <= 2):
          findings.append({
              "line": start_line,
              "rule": "monotone-sentence-length",
              "severity": "info",
              "message": (
                  f"4 consecutive sentences have nearly identical lengths ({window}"
                  " words); vary cadence."
              ),
          })
          break

  findings.sort(key=lambda item: item["line"])
  return {
      "register": register,
      "issue_count": len(findings),
      "passed": len(findings) == 0,
      "findings": findings,
  }


def main() -> int:
  parser = argparse.ArgumentParser(
      description="Lint prose and Workspace deliverables for AI writing patterns."
  )
  parser.add_argument("path", help="File path to lint, or '-' for stdin.")
  parser.add_argument(
      "--register",
      choices=["essay", "exec", "tech", "comms", "slides"],
      default="essay",
      help="Target writing register or surface (default: essay).",
  )
  parser.add_argument(
      "--allow-em-dash",
      action="store_true",
      help="Do not flag em dashes when permitted by user/brand style or Memory.",
  )
  parser.add_argument(
      "--json",
      action="store_true",
      help="Emit machine-readable JSON output.",
  )
  args = parser.parse_args()

  if args.path == "-":
    content = sys.stdin.read()
  else:
    with open(args.path, "r", encoding="utf-8") as f:
      content = f.read()

  report = lint_text(
      content, register=args.register, allow_em_dash=args.allow_em_dash
  )

  if args.json:
    print(json.dumps(report, indent=2))
  else:
    if report["passed"]:
      print(f"PASS ({args.register} register): 0 slop patterns flagged.")
    else:
      print(
          f"FLAGGED ({args.register} register): {report['issue_count']} issue(s)"
          " found:"
      )
      for item in report["findings"]:
        match_str = f" [{item['match']}]" if "match" in item else ""
        print(
            f"  Line {item['line']} ({item['severity']}/{item['rule']}){match_str}:"
            f" {item['message']}"
        )

  return 0


if __name__ == "__main__":
  sys.exit(main())
