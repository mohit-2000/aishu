from flask import Flask, request, render_template, session
from hashlib import sha1
import sqlite3 as sql

from werkzeug.utils import redirect
import filter
import os
import re

# Dev config
dev = True
prod_port = 80

# Directories config
static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
template_dir = os.path.join(static_dir, 'templates')
image_dir = os.path.join(static_dir, 'images')

app = Flask(__name__, template_folder = template_dir)
app.secret_key = os.urandom(10)

# Database functions

def verify(name, email, password, confirmation):
    print (name, email, password, confirmation)
    if not name:
        return False, 'Username cannot be empty'
    if not email:
        return False, 'Email cannot be empty'
    email_pattern = re.compile(r'\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?')
    if not re.match(email_pattern, email):
        return False, 'Invalid Email'
    if not password:
        return False, 'Password cannot be empty'
    if password != confirmation:
        return False, 'The reentered password does not match with the original one'
    
    return True, None

def insert_user(name, email, password, confirmation):
    con = sql.connect('data/database.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (name, email, sha1(password.encode()).hexdigest()))
    con.commit()
    con.close()

def get_user(name, password):
    con = sql.connect('data/database.db')
    cur = con.cursor()
    cur.execute("SELECT username FROM users WHERE username=? and password=?", (name, sha1(password.encode()).hexdigest()))
    u = cur.fetchone()
    con.close()
    if u:
        u = u[0]
    return u

# Routes
@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', logged_in=('logged_in' in session))

@app.route('/page/<page>', methods=['GET'])
def return_static_page(page):
    if page not in os.listdir('static/templates'):
        return 'Requested resource not found on the server', 404
    return render_template(page, logged_in=('logged_in' in session))

@app.route('/api/login', methods=['POST'])
def login():
    try:
        u = get_user(request.form['Name'], request.form['Password'])
        print (request.form['Name'], request.form['Password'])
        print (u)
        if not u:
            return {'error': 'Invalid username or password'}, 400
        session['username'] = request.form['Name']
        session['logged_in'] = True
        return redirect('/')
    except Exception as e:
        session.clear()
        return {'success': False, 'error': str(e)}

@app.route('/api/register', methods=['POST'])
def register():
    ver, err = verify(**request.form)
    if not ver:
        return {'success': False, 'error': err}, 400
    insert_user(**request.form)
    return redirect('/')

@app.route('/api/data', methods=['GET', 'POST'])
def display_data():
    income = request.form.get('income', 'any')
    prof = request.form.get('profession', 'any')
    church = request.form.get('church', 'Total_churches')
    safety = request.form.get('safety', 'any')
    data = filter.filter(income, prof, church, safety)
    return render_template('table.html', data=data, logged_in=('logged_in' in session))

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

app.run('localhost', port = (8081 if dev else prod_port))
