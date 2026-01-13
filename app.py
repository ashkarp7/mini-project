from flask import Flask, render_template, request
from rules import rule_based_check
from score_engine import final_decision
from advisor import advisory_message

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
    advice = None
    reasons = []
    user_input = None

    if request.method == "POST":
        user_input = request.form["input"]

        score, reasons = rule_based_check(user_input)
        result = final_decision(score)
        advice = advisory_message(result)

    return render_template(
        "index.html",
        user_input=user_input,
        result=result,
        score=score,
        advice=advice,
        reasons=reasons
    )

if __name__ == "__main__":
    app.run(debug=True)
