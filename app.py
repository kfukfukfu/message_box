from flask import Flask, flash, redirect, render_template, request
from werkzeug.security import generate_password_hash
from config import User

app = Flask(__name__)
app.secret_key = "secret"  # 秘密鍵


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # データの検証
        if not name or not password or not email:
            flash("未入力の項目があります。")
            return render_template("register.html", name=name, email=email)
        if User.select().where(User.name == name):
            flash("その名前はすでに使われています。")
            return render_template("register.html", name=name, email=email)
        if User.select().where(User.email == email):
            flash("そのメールアドレスはすでに使われています。")
            return render_template("register.html", name=name, email=email)

        # ユーザー登録
        User.create(
            name=name,
            email=email,
            password=generate_password_hash(password),
        )
        return redirect("/")

    return render_template("register.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
