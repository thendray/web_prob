from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug import security


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Time_to_fly@localhost/web_prob"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "asdfgrtyeofdhggkjdjfh09586"
db = SQLAlchemy(app)

current_user = None


class User(db.Model):
    #__tablename__ = "Users"

    def __init__(self, name: str, login: str, password: str = ""):

        self.name = name
        self.login = login
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String(50), nullable=False)
    login = db.Column("login", db.String(50), nullable=True)
    password = db.Column("password", db.String(500))

    def __repr__(self):
        return f"<Information> {self.id}"


class TextFile(db.Model):

    def __init__(self, file_name: str = None, text: str = None):

        self.text = text
        self.file_name = file_name
        self.create_datetime = datetime.now()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    file_name = db.Column("file_name", db.String(100), nullable=False)
    text = db.Column("text", db.String(500), nullable=True)
    create_datetime = db.Column("create_datetime", db.DateTime, nullable=False)

    def __repr__(self):
        return f"<TextFiles> {self.id}"


@app.route("/")
def home():
    return render_template("home.html", current_user=current_user)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    global current_user
    if request.method == "POST":
        name = request.form["name"]
        login = request.form["login"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password']

        if confirm_password != password:
            # Вернуть ту же страничку с ошибкой не правильного пароля
            flash("Пароли не совпадают!", 'error')
            return redirect("/registration")

        elif User.query.filter(User.login == login).count() > 0:
            # Вернуть ту же страничку с ошибкой не уникального login
            flash("Такой логин уже существует!", 'error')
            return redirect("/registration")

        password = security.generate_password_hash(password)
        user = User(name, login, password)

        try:
            db.session.add(user)
            db.session.commit()
            # Вернуть домашнюю страничку авторизованного пользователя
            current_user = user
            return redirect("/")
        except Exception as error:
            return str(error)

    return render_template("registration_form.html")


@app.route("/enter", methods=["GET", "POST"])
def enter():
    global current_user
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        check = User.query.filter(User.login == login)
        if check.count() > 0 and security.check_password_hash(User.query.first().password, password):
            current_user = check.first()
            # Вернуть домашнюю страницу авторизованного пользователя
            return redirect("/")
        else:
            # Вернуть ту же страницу с сообщением
            flash("Пользователь не найден!", "error")
            return redirect("/enter")

    return render_template("enter_form.html")


@app.route("/exit")
def sign_out():
    global current_user
    current_user = None
    return redirect('/')


@app.route("/account")
def account():
    user_texts = TextFile.query.filter(
        TextFile.user_id == current_user.id).\
        order_by(TextFile.create_datetime.desc()).\
        limit(3).all()
    return render_template("account.html", current_user=current_user, user_texts=user_texts)


@app.route("/account/<int:id>")
def text_detail(id: int):
    text = TextFile.query.get(id)
    return render_template("text_detail.html", text=text)


@app.route("/result")
def result():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)



