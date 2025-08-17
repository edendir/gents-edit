import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import BlogPost
from app.extensions import mail
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route("/")
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template("blog.html", posts=posts)

@main.route("/article/<int:post_id>")
def article_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("article.html", post=post)

@main.route("/services")
def services():
    return render_template("services.html")

@main.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get('q', '').strip()

    if not query:
        return render_template('search.html', posts=[], query=query)

    posts = BlogPost.query\
        .join(Author)\
        .filter(
            or_(
                BlogPost.title.ilike(f'%{query}%'),
                BlogPost.content.ilike(f'%{query}%'),
                BlogPost.tags.ilike(f'%{query}%'),
                func.lower(Author.name).ilike(f'%{query.lower()}%')
            )
        )\
        .order_by(BlogPost.created_at.desc())\
        .all()

    return render_template('search.html', posts=posts, query=query)


@main.route("/contact", methods=["GET", "POST"])
def contact():
    site_key = "6LdX6p4rAAAAANeRqbAZ4su0RTagxhp_JGH2ruNj"
    if request.method == "POST":
        recaptcha_response = request.form.get("g-recaptcha-response")
        print(recaptcha_response)
        if not recaptcha_response:
            flash("reCAPTCHA response is missing. Please try again.", "danger")
            return redirect(url_for("main.contact"))

        secret_key = "6LdX6p4rAAAAAJPWt8CL0IHjSOCT7qZ0GPQKBAdq"
        import requests
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": recaptcha_response},
        )
        result = r.json()
        print(result)
        if result.get("success") != True or result.get("score", 0) < 0.5:
            flash("Invalid reCAPTCHA. Please try again.", "danger")
            return redirect(url_for("main.contact"))

        name = request.form["name"]
        email = request.form["email"]
        service = request.form["service"]
        message = request.form["message"]

        msg = Message(
            subject=f"Contact Form Submission from {name} regarding {service}",
            sender=email,
            recipients=["info@the-gents-edit.com"],
            body=f"Name: {name}\nEmail: {email}\nService: {service}\nMessage: {message}",
        )
        mail.send(msg)
        return render_template("success.html", success=True)
    return render_template("contact.html", site_key=site_key)
