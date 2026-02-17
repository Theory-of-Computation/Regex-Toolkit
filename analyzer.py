import re

def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def detect_redos_patterns(pattern):
    warnings = []

    if "(a+)+" in pattern or "(.*)+" in pattern:
        warnings.append("Nested quantifiers → catastrophic backtracking")

    if ".*.*" in pattern:
        warnings.append("Multiple greedy wildcards")

    if "(.*)" in pattern and "|" in pattern:
        warnings.append("Wildcard inside alternation")

    return warnings

def analyze_regex(pattern: str):
    analysis = {}
    analysis["is_valid"] = is_valid_regex(pattern)

    if not analysis["is_valid"]:
        return analysis

    analysis["length"] = len(pattern)
    analysis["stars"] = pattern.count("*")
    analysis["pluses"] = pattern.count("+")
    analysis["questions"] = pattern.count("?")
    analysis["alternations"] = pattern.count("|")
    analysis["groups"] = pattern.count("(")

    analysis["has_repetition"] = any(x in pattern for x in ["*", "+"])
    analysis["has_alternation"] = "|" in pattern
    analysis["has_groups"] = "(" in pattern and ")" in pattern

    redos = detect_redos_patterns(pattern)
    analysis["redos_warnings"] = redos

    score = 0
    if analysis["stars"] > 2: score += 2
    if analysis["groups"] > 2: score += 2
    if analysis["alternations"] > 1: score += 2
    if ".*" in pattern: score += 3
    if redos: score += 3

    if score >= 7:
        analysis["complexity"] = "HIGH ⚠️ High Backtracking Risk"
    elif score >= 3:
        analysis["complexity"] = "MEDIUM ⚡ Moderate Complexity"
    else:
        analysis["complexity"] = "LOW ✅ Safe"

    return analysis

def test_regex(pattern, text):
    try:
        matches = re.findall(pattern, text)
        return matches[:10]
    except:
        return []
