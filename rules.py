def rule_based_check(text):
    score = 0
    keywords = ["verify", "urgent", "password", "login", "bank"]

    for word in keywords:
        if word in text.lower():
            score += 20

    if "http://" in text:
        score += 30

    return score
