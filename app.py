from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import sqlite3
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

DATABASE = "reviews.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    create_table()


@app.route("/")
def home():
    conn = get_db()
    reviews = conn.execute("""
        SELECT * FROM reviews
        WHERE approved = 1
        ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    return render_template("Home.html", reviews=reviews)


@app.route("/add-review", methods=["POST"])
def add_review():
    name = request.form["review_name"]
    rating = request.form["review_rating"]
    review_text = request.form["review_text"]

    conn = get_db()
    conn.execute("""
        INSERT INTO reviews (name, rating, review_text)
        VALUES (?, ?, ?)
    """, (name, rating, review_text))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]

        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_reviews"))

        return render_template("admin_login.html", error="Incorrect password")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))


@app.route("/admin/reviews")
def admin_reviews():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    reviews = conn.execute("""
        SELECT * FROM reviews
        ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    return render_template("admin_reviews.html", reviews=reviews)


@app.route("/approve-review/<int:id>", methods=["POST"])
def approve_review(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    conn.execute("UPDATE reviews SET approved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_reviews"))


@app.route("/delete-review/<int:id>", methods=["POST"])
def delete_review(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_reviews"))
@app.route("/testimonials")
def testimonials():
    conn = get_db()
    reviews = conn.execute("""
        SELECT * FROM reviews
        WHERE approved = 1
        ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    return render_template("Testimonials.html", reviews=reviews)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)