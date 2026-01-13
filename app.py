from flask import Flask, render_template, request
from rules import rule_based_check
from score_engine import final_decision

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["input"]
        score = rule_based_check(user_input)
        result = final_decision(score)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
