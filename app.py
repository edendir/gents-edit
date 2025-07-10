from flask import Flask, session, render_template, request

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    posts = BlogPost.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = BlogPost.query.filter(BlogPost.content.contains(query)).all()
        return render_template('search.html', results=results, query=query)
    else:
        return render_template('search.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # TODO: save the message to a database or send an email
        return render_template('contact.html', success=True)
    return render_template('contact.html')