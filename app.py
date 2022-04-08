from flask import Flask

app = Flask(__name__)


@app.route("/Hello")
def hello():
    return "Начинаем работать!"


if __name__ == "__main__":
    app.run(debug=True)



