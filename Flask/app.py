from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"]) 
def predict():
    location = request.form.get("location", "")

    result = {
        "location": location,
        "score": 82,
        "state": "High potential",
    }
    return result


if __name__ == "__main__":
    app.run(debug=True)
