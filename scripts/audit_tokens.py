#!/usr/bin/env python3
"""
scripts/audit_tokens.py
Zero-dependency token budget and schema compliance auditor for Dion agent skills.
Validates 3-Stage LLM Token Optimization:
  Stage 1: Cold-Start Router Diet (YAML Frontmatter 15-24 words, strict formula)
  Stage 2: Context Injection Diet (Markdown body < 120 tokens, ~30 lines, 3 sections)
  Stage 3: Output Token Clamp (Explicit negative constraints against verbosity)
"""

import os
import sys
import re
from pathlib import Path

# Action verbs commonly starting valid descriptions
ACTION_VERB_REGEX = r"^[A-Z][a-z]+(?:s|es)\b"

def estimate_tokens(text: str) -> int:
    """
    Standard zero-dependency LLM token estimator.
    Blends subword BPE heuristic with standard 1.25x word ratio.
    """
    words = text.split()
    if not words:
        return 0
    # Average across char/4 heuristic and word*1.25 heuristic
    char_est = len(text) / 4.0
    word_est = len(words) * 1.25
    return int(round((char_est + word_est) / 2.0))

def parse_skill(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    warnings = []

    # Check YAML delimiters
    if not content.startswith("---\n"):
        return None, ["Missing opening YAML delimiter (---)"]

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return None, ["Malformed YAML frontmatter or missing closing delimiter"]

    fm_raw = parts[1]
    body_raw = parts[2]

    # Parse YAML fields strictly
    fm_lines = [line.strip() for line in fm_raw.splitlines() if line.strip()]
    fields = {}
    for line in fm_lines:
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"').strip("'")
        else:
            errors.append(f"Invalid YAML line: {line}")

    # Rule: Never add extra YAML fields beyond name and description
    allowed_keys = {"name", "description"}
    extra_keys = set(fields.keys()) - allowed_keys
    if extra_keys:
        errors.append(f"Extraneous YAML fields: {', '.join(extra_keys)}")

    skill_name = fields.get("name", "")
    expected_name = file_path.parent.name
    if skill_name != expected_name:
        errors.append(f"Skill name '{skill_name}' does not match folder '{expected_name}'")

    desc = fields.get("description", "")
    desc_words = desc.split()
    desc_word_count = len(desc_words)

    # Rule: strictly between 15 and 24 words (~20-26 tokens)
    if not (15 <= desc_word_count <= 24):
        errors.append(f"Description length ({desc_word_count} words) outside 15-24 words range")

    # Rule: Formula: [Action Verb] + [Deliverable] + ". Use when " + [Exact Trigger].
    if not re.match(ACTION_VERB_REGEX, desc):
        warnings.append("Description should start with a 3rd-person singular action verb (e.g., Generates, Formats, Synthesizes)")
    
    if ". Use when " not in desc:
        errors.append("Description missing required trigger anchor '. Use when '")

    if not desc.endswith("."):
        errors.append("Description must end with a period")

    # Body validation
    body = body_raw.strip()
    body_lines = len(body.splitlines())
    body_tokens = estimate_tokens(body)
    router_tokens = estimate_tokens(f"name: {skill_name}\ndescription: {desc}")

    # Rule: Under 120 tokens (~30 lines)
    if body_tokens > 120:
        errors.append(f"Body tokens ({body_tokens}) exceed 120 token ceiling")
    if body_lines > 30:
        errors.append(f"Body lines ({body_lines}) exceed 30 line limit")

    # Rule: 3 exact sections
    has_protocol = bool(re.search(r"^## Protocol\b", body, re.M))
    has_guardrails = bool(re.search(r"^## Guardrails\b", body, re.M))
    has_schema = bool(re.search(r"^## Output Schema\b", body, re.M))

    if not has_protocol:
        errors.append("Missing '## Protocol' section")
    if not has_guardrails:
        errors.append("Missing '## Guardrails' section")
    if not has_schema:
        errors.append("Missing '## Output Schema' section")

    # Rule: Telegraphic arrows '->' in protocol
    if has_protocol and "->" not in body:
        warnings.append("Protocol should use telegraphic arrows ('->') for deterministic step transitions")

    # Rule: Output clamp guardrails
    if has_guardrails:
        guard_text = body.split("## Guardrails")[1].split("## Output Schema")[0] if "## Output Schema" in body else body.split("## Guardrails")[1]
        if not re.search(r"\b(never|zero|no|strictly|forbid)\b", guard_text, re.I):
            warnings.append("Guardrails should contain strict negative constraints (Never, Zero, etc.)")

    metadata = {
        "file": str(file_path),
        "name": skill_name,
        "domain": file_path.parent.parent.name,
        "desc_words": desc_word_count,
        "router_tokens": router_tokens,
        "body_lines": body_lines,
        "body_tokens": body_tokens,
        "errors": errors,
        "warnings": warnings,
    }
    return metadata, errors

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    if not skills_dir.exists():
        print(f"Error: {skills_dir} not found.")
        sys.exit(1)

    skill_files = sorted(skills_dir.glob("**/SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found.")
        sys.exit(1)

    total = len(skill_files)
    passed = 0
    failed = 0
    total_router_tokens = 0
    total_body_tokens = 0

    print("=" * 96)
    print("DION AGENT SKILLS: 3-STAGE LLM TOKEN OPTIMIZATION AUDIT")
    print("Spec: agentskills.io progressive disclosure | Target: Body < 120 toks, Desc 15-24 words")
    print("=" * 96)
    print(f"{'DOMAIN':<14} {'SKILL NAME':<30} {'DESC W':<7} {'R-TOK':<7} {'LINES':<6} {'B-TOK':<7} {'STATUS'}")
    print("-" * 96)

    failures = []

    for sf in skill_files:
        meta, errs = parse_skill(sf)
        if meta is None or errs:
            failed += 1
            domain = sf.parent.parent.name
            name = sf.parent.name
            desc_w = meta["desc_words"] if meta else 0
            r_tok = meta["router_tokens"] if meta else 0
            b_lines = meta["body_lines"] if meta else 0
            b_tok = meta["body_tokens"] if meta else 0
            status = "FAIL"
            failures.append((sf, errs if meta else ["Could not parse file"]))
        else:
            passed += 1
            domain = meta["domain"]
            name = meta["name"]
            desc_w = meta["desc_words"]
            r_tok = meta["router_tokens"]
            b_lines = meta["body_lines"]
            b_tok = meta["body_tokens"]
            total_router_tokens += r_tok
            total_body_tokens += b_tok
            status = "PASS"

        print(f"{domain:<14} {name:<30} {desc_w:<7} {r_tok:<7} {b_lines:<6} {b_tok:<7} {status}")

    print("=" * 96)
    avg_router = (total_router_tokens / passed) if passed else 0
    avg_body = (total_body_tokens / passed) if passed else 0
    print(f"Audit Summary: {total} total skills | {passed} PASSED | {failed} FAILED")
    print(f"Aggregate Token Footprint (Passing): Router={total_router_tokens} toks (avg {avg_router:.1f}) | Body={total_body_tokens} toks (avg {avg_body:.1f})")
    
    if failures:
        print("\n" + "!" * 40 + " FAILURES DETECTED " + "!" * 40)
        for sf, errs in failures:
            rel = sf.relative_to(root)
            print(f"\n[X] {rel}:")
            for e in errs:
                print(f"    - {e}")
        print("!" * 96)
        sys.exit(1)
    else:
        print("\nAll skills 100% compliant with 3-Stage Token Optimization architecture!")
        sys.exit(0)

if __name__ == "__main__":
    main()

