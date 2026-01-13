def rule_based_check(text, input_type):
    score = 0
    reasons = []

    keywords = {
        "verify": 15,
        "urgent": 20,
        "password": 25,
        "login": 20,
        "bank": 20,
        "click": 10
    }

    for word, weight in keywords.items():
        if word in text.lower():
            score += weight
            reasons.append(f"Contains keyword: '{word}'")

    if input_type == "URL":
        if "http://" in text:
            score += 25
            reasons.append("Uses insecure HTTP URL")

        if "-" in text:
            score += 10
            reasons.append("Suspicious URL structure (hyphen detected)")

    if len(text) < 15:
        score += 10
        reasons.append("Very short suspicious content")

    return score, reasons
