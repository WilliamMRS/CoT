# Imports
from flask import Flask, url_for, request, render_template
from markupsafe import escape
# Private modules
import cot

app = Flask(__name__)

token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcyIn0.y6Ud_mLvXvJeSAsdikQXq5AsIXUBBp0E9UBP0_UNw2Q"

cot_api = cot.cot_api(token) # grab the api and pass it the token value

print(cot_api.get_data("1429"))

# load static files
#url_for('static', filename='style.css')
#with app.test_request_context():
#    print(url_for('index'))
#    print(url_for('login'))
#    print(url_for('login', next='/'))
#    print(url_for('profile', username='John Doe'))

# Routing - Visible public sites
@app.route('/')
def index():
    return 'index'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# Routing - Secured API
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()