from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def test():
    return jsonify({"message": "endpoint working"})

if __name__ == "__main__":
    app.run(debug=True)