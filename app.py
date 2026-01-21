from flask import Flask, render_template, request
from rules import rule_based_check
from score_engine import final_decision
from advisor import advisory_message
from input_detector import detect_input_type

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
    advice = None
    reasons = []
    user_input = None
    input_type = None

    if request.method == "POST":
        user_input = request.form["input"]
        
        # Get enhanced detection with detailed analysis
        detection_result = detect_input_type(user_input)
        input_type = detection_result['type']
        
        # Pass detection data to rule_based_check for comprehensive analysis
        score, reasons = rule_based_check(user_input, input_type, detection_result)
        
        result = final_decision(score)
        advice = advisory_message(result)


    return render_template(
        "index.html",
        user_input=user_input,
        input_type=input_type,
        result=result,
        score=score,
        advice=advice,
        reasons=reasons
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
