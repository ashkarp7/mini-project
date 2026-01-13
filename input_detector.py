import re

def detect_input_type(text):
    url_pattern = re.compile(
        r'^(http://|https://|www\.)'
    )

    if url_pattern.match(text.lower()):
        return "URL"
    else:
        return "MESSAGE"
