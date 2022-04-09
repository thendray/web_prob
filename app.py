from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Time_to_fly@localhost/web_prob"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Information(db.Model):
    __tablename__ = "web_prob"

    def __init__(self, name: str, telephone: str, address: str = ""):

        self.name = name
        self.telephone = telephone
        self.address = address

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), nullable=False)
    telephone = db.Column("telephone", db.String(20), nullable=True)
    address = db.Column("address", db.String(200))

    def __repr__(self):
        return f"<Information> {self.id}"


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        telephone = request.form["telephone"]
        address = request.form["address"]

        info = Information(name, telephone, address)

        try:
            db.session.add(info)
            db.session.commit()
            return redirect("/")
        except:
            return "SOS"
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)



