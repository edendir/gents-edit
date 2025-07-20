from flask import Flask, session, render_template, request
from models import db, BlogPost, Author
from config import Config
from admin import admin
from extensions import mail, session_manager

# Initialize and configure app
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    session_manager.init_app(app)
    admin.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/about")
    def about():
        return render_template("about.html")


    @app.route("/blog")
    def blog():
        posts = BlogPost.query.all()
        return render_template("blog.html", posts=posts)


    @app.route("/search", methods=["GET", "POST"])
    def search():
        if request.method == "POST":
            query = request.form["query"]
            results = BlogPost.query.filter(BlogPost.content.contains(query)).all()
            return render_template("search.html", results=results, query=query)
        else:
            return render_template("search.html")


    @app.route("/contact", methods=["GET", "POST"])
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

    return app


# Create tables if running this file directly
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
