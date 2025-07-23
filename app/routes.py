from flask import Blueprint, render_template, request
from app.models import BlogPost
from app.extensions import mail

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/blog")
def blog():
    posts = BlogPost.query.all()
    return render_template("blog.html", posts=posts)

@main.route("/services")
def services():
    return render_template("services.html")

@main.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        results = BlogPost.query.filter(BlogPost.content.contains(query)).all()
        return render_template("search.html", results=results, query=query)
    else:
        return render_template("search.html")


@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        service = request.form["service"]
        message = request.form["message"]

        msg = Message(
            subject=f"Contact Form Submission from {name} regarding {service}",
            sender=email,
            recipients=["lannonhomenetworks@gmail.com"],
            body=f"Name: {name}\nEmail: {email}\nService: {service}\nMessage: {message}",
        )
        mail.send(msg)
        return render_template("success.html", success=True)
    return render_template("contact.html")
