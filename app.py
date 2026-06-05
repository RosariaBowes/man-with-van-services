from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extras

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=psycopg2.extras.RealDictCursor
    )


def create_table():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


create_table()


@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM reviews
        WHERE approved = TRUE
        ORDER BY created_at DESC
    """)
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("Home.html", reviews=reviews)


@app.route("/add-review", methods=["POST"])
def add_review():
    name = request.form["review_name"]
    rating = request.form["review_rating"]
    review_text = request.form["review_text"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reviews (name, rating, review_text)
        VALUES (%s, %s, %s)
    """, (name, rating, review_text))
    conn.commit()
    cur.close()
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
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM reviews
        ORDER BY created_at DESC
    """)
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("admin_reviews.html", reviews=reviews)


@app.route("/approve-review/<int:id>", methods=["POST"])
def approve_review(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE reviews SET approved = TRUE WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("admin_reviews"))


@app.route("/delete-review/<int:id>", methods=["POST"])
def delete_review(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM reviews WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("admin_reviews"))


@app.route("/testimonials")
def testimonials():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM reviews
        WHERE approved = TRUE
        ORDER BY created_at DESC
    """)
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("Testimonials.html", reviews=reviews)


@app.route("/google9710b3f238d55b7a.html")
def google_verification():
    return app.send_static_file("google9710b3f238d55b7a.html")


@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")


@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")


if __name__ == "__main__":
    app.run(debug=True)