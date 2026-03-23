from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

# ================= DATABASE MODEL =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))

# Create DB
with app.app_context():
    db.create_all()

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username

            # simple admin check
            if username == "admin":
                return redirect("/admin")
            else:
                return redirect("/dashboard")

        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")

# -------- USER DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome {session['user']} 🎉"
    return redirect("/login")

# -------- ADMIN --------
@app.route("/admin")
def admin():
    if "user" in session and session["user"] == "admin":
        return render_template("admin.html")
    return redirect("/login")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)