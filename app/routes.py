import os
from flask import Blueprint, render_template, request
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
    if request.method == "POST":
        recaptcha_response = request.form["g-recaptcha-response"]
        secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
        r = request.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": recaptcha_response},
        )
        result = r.json()
        if not result.get("success"):
            return render_template("contact.html", error="Invalid reCAPTCHA. Please try again.")
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
    return render_template("contact.html", secret_key=os.getenv("RECAPTCHA_SECRET_KEY"))
