from flask import Flask, render_template, request
from analyzer import analyze_regex, test_regex

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    pattern = ""
    sample_text = ""
    matches = []

    if request.method == "POST":
        pattern = request.form["regex"]
        sample_text = request.form.get("text", "")
        result = analyze_regex(pattern)

        if sample_text and result.get("is_valid"):
            matches = test_regex(pattern, sample_text)

    return render_template(
        "index.html",
        result=result,
        pattern=pattern,
        sample_text=sample_text,
        matches=matches
    )

if __name__ == "__main__":
    app.run(debug=True)
