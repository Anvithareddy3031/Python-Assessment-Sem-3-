from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "unit_converter_secret_key"

def convert_value(value, conversion_type):
    conversions = {
        "km_to_miles": value * 0.621371,
        "miles_to_km": value / 0.621371,
        "kg_to_pounds": value * 2.20462,
        "pounds_to_kg": value / 2.20462
    }
    return round(conversions.get(conversion_type, 0), 4)

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    result = None

    if request.method == "POST":
        value = float(request.form["value"])
        conversion_type = request.form["conversion"]
        result = convert_value(value, conversion_type)

        record = {
            "value": value,
            "conversion": conversion_type.replace("_", " ").title(),
            "result": result
        }

        history = session["history"]
        history.insert(0, record)
        session["history"] = history[:5]  # keep last 5 entries

    return render_template("index.html", result=result, history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)
