def rule_based_check(text):
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
            reasons.append(f"Contains keyword: {word}")

    if "http://" in text:
        score += 25
        reasons.append("Uses insecure HTTP link")

    if len(text) < 15:
        score += 10
        reasons.append("Very short suspicious message")

    return score, reasons
