from flask import Flask, session, render_template, request
from flask_session import Session
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure secret key for session management
app.secret_key = 'your_secret_key_here'

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    #posts = BlogPost.query.all()
    return render_template('blog.html')

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
        service = request.form['service']
        message = request.form['message']
        
        msg = Message(
            subject=f'Contact Form Submission from {name} regarding {service}',
            sender = email,
            recipients=['info@the-gents-edit.com'],
            body=f'Name: {name}\nEmail: {email}\nService: {service}\nMessage: {message}'
        )
        mail.send(msg)
        return render_template('success.html', success=True)
    return render_template('contact.html')