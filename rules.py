import re

# Try to import ML predictor (gracefully handle if models not trained yet)
try:
    from ml_predictor import ml_predictor
    ML_AVAILABLE = True
except Exception as e:
    ML_AVAILABLE = False
    print(f"⚠ ML models not available: {e}")

def rule_based_check(text, input_type, detection_data=None):
    """
    Enhanced rule-based checking system that integrates with input_detector analysis
    and ML predictions.
    
    Args:
        text: The input text (URL or message)
        input_type: 'URL' or 'MESSAGE'
        detection_data: Analysis data from input_detector (optional)
    
    Returns:
        tuple: (score, reasons) - risk score and list of detection reasons
    """
    score = 0
    reasons = []
    
    # ============ ML PREDICTIONS (if available) ============
    if ML_AVAILABLE:
        try:
            if input_type == "URL":
                ml_result = ml_predictor.predict_url(text)
                if ml_result:
                    ml_score = ml_result['ml_score']
                    score += ml_score
                    reasons.append(
                        f"ML Model: {ml_result['prediction'].upper()} "
                        f"(confidence: {ml_result['confidence']:.1%}, score: +{ml_score})"
                    )
            else:  # MESSAGE
                ml_result = ml_predictor.predict_message(text)
                if ml_result:
                    ml_score = ml_result['ml_score']
                    score += ml_score
                    reasons.append(
                        f"ML Model: {ml_result['prediction'].upper()} "
                        f"(confidence: {ml_result['confidence']:.1%}, score: +{ml_score})"
                    )
        except Exception as e:
            print(f"ML prediction error: {e}")
    

    
    # If we have detection data from input_detector, use it
    if detection_data and 'risks' in detection_data:
        # Add all risks from input_detector
        for risk in detection_data['risks']:
            score += risk['score']
            reasons.append(risk['message'])
    
    # Additional keyword-based checks
    # Expanded keyword database with categories
    high_risk_keywords = {
        # Urgency and pressure
        'urgent': 20,
        'immediately': 20,
        'expires': 18,
        'limited time': 18,
        'act now': 18,
        'hurry': 15,
        
        # Credential requests
        'password': 25,
        'username': 20,
        'login': 20,
        'signin': 20,
        'credentials': 25,
        
        # Financial
        'bank': 20,
        'credit card': 25,
        'account number': 25,
        'ssn': 30,
        'social security': 30,
        'wire transfer': 25,
        'bitcoin': 20,
        'cryptocurrency': 20,
        
        # Threats
        'suspended': 25,
        'locked': 22,
        'blocked': 22,
        'terminated': 25,
        'unauthorized': 20,
        'security alert': 20,
        
        # Rewards/Scams
        'winner': 25,
        'prize': 25,
        'won': 22,
        'free money': 30,
        'lottery': 28,
        'inheritance': 30,
        
        # Verification
        'verify': 15,
        'confirm': 15,
        'update': 12,
        'validate': 15,
        'reactivate': 18,
        
        # Action requests
        'click here': 15,
        'click': 10,
        'download': 18,
        'install': 18,
        'open attachment': 20,
        
        # Generic suspicious
        'congratulations': 20,
        'claim': 18,
        'refund': 18,
        'tax return': 20,
        'irs': 22,
        'government': 15,
    }
    
    text_lower = text.lower()
    
    # Check for keywords (avoid double-counting with input_detector)
    # Only add if not already detected by input_detector
    existing_categories = set()
    if detection_data and 'risks' in detection_data:
        existing_categories = {risk['category'] for risk in detection_data['risks']}
    
    for keyword, weight in high_risk_keywords.items():
        if keyword in text_lower:
            # Only add if similar category not already detected
            category_map = {
                'urgency': ['urgent', 'immediately', 'expires', 'limited time', 'act now', 'hurry'],
                'credential_request': ['password', 'username', 'login', 'signin', 'credentials'],
                'financial': ['bank', 'credit card', 'account number', 'ssn', 'social security', 'wire transfer', 'bitcoin', 'cryptocurrency'],
                'threat': ['suspended', 'locked', 'blocked', 'terminated', 'unauthorized', 'security alert'],
                'reward_scam': ['winner', 'prize', 'won', 'free money', 'lottery', 'inheritance'],
                'verification_request': ['verify', 'confirm', 'update', 'validate', 'reactivate'],
                'action_request': ['click here', 'click', 'download', 'install', 'open attachment'],
            }
            
            # Find category for this keyword
            keyword_category = None
            for cat, keywords in category_map.items():
                if keyword in keywords:
                    keyword_category = cat
                    break
            
            # Only add if category not already in existing detections
            if not keyword_category or keyword_category not in existing_categories:
                score += weight
                reasons.append(f"Contains high-risk keyword: '{keyword}'")
                # Mark category as used
                if keyword_category:
                    existing_categories.add(keyword_category)
    
    # URL-specific additional checks
    if input_type == "URL":
        # Check for suspicious file extensions in URL
        suspicious_extensions = ['.exe', '.zip', '.rar', '.bat', '.cmd', '.scr', '.js', '.vbs']
        for ext in suspicious_extensions:
            if ext in text_lower:
                score += 25
                reasons.append(f"URL contains suspicious file extension: {ext}")
                break
        
        # Check for obfuscation techniques
        if '%' in text and text.count('%') > 3:
            score += 15
            reasons.append("URL contains excessive encoding (potential obfuscation)")
        
        # Check for data URI (can hide malicious content)
        if text_lower.startswith('data:'):
            score += 30
            reasons.append("Uses data URI scheme (potential code injection)")
    
    # Message-specific additional checks
    else:
        # Check for multiple URLs in message (spam indicator)
        url_count = text_lower.count('http://') + text_lower.count('https://') + text_lower.count('www.')
        if url_count > 1:
            score += 20
            reasons.append(f"Message contains multiple URLs ({url_count} URLs)")
        
        # Check for poor grammar indicators (common in scams)
        # Simple check: excessive spaces, unusual punctuation
        if '  ' in text:  # Double spaces
            score += 5
            reasons.append("Formatting issues detected (double spaces)")
        
        # Check for mixed language scripts (potential phishing)
        has_latin = bool(re.search(r'[a-zA-Z]', text))
        has_cyrillic = bool(re.search(r'[а-яА-Я]', text))
        has_greek = bool(re.search(r'[α-ωΑ-Ω]', text))
        
        script_count = sum([has_latin, has_cyrillic, has_greek])
        if script_count > 1:
            score += 25
            reasons.append("Mixed character scripts detected (potential spoofing)")
    
    # Length-based checks
    if len(text) < 10:
        score += 10
        reasons.append("Very short content (suspicious)")
    elif len(text) > 500:
        score += 5
        reasons.append("Unusually long content")
    
    # Check for personal information requests
    pii_patterns = [
        r'\bssn\b',
        r'\bsocial security\b',
        r'\bdate of birth\b',
        r'\bdob\b',
        r'\bmother.?s maiden name\b',
        r'\bdriving license\b',
        r'\bpassport\b',
    ]
    
    for pattern in pii_patterns:
        if re.search(pattern, text_lower):
            score += 25
            reasons.append("Requests personally identifiable information (PII)")
            break
    
    return score, reasons


import re
