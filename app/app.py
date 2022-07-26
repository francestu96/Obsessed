from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from flask_mysqldb import MySQL
from datetime import datetime
import logging

app = Flask(__name__)

app.secret_key = '1n_0rd3r_t0_3ncrypt_535510n_c00ki3'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Yr%Pq79J6My7wb'
app.config['MYSQL_DB'] = 'leodb'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mysql = MySQL(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('login_attempts.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, admin FROM users WHERE username=%s AND password=%s", (username, password))
        account = cur.fetchone()

        if account:
            session['logged_in'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['admin'] = account[2]

            return redirect(url_for('login_attempts'))
        else:
            cur.execute("SELECT id, username FROM users WHERE username=%s", (username,))
            account_exists = cur.fetchone()
            if account_exists:

                if request.headers.getlist("X-Forwarded-For"):
                    ip = request.headers.getlist("X-Forwarded-For")[0]
                else:
                    ip = request.remote_addr

                time_connection = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                cur.execute("INSERT INTO login_attempts (user_id, ip, time) VALUES (%s, %s, %s)", (account_exists[0], ip, time_connection))
                mysql.connection.commit()

                msg = 'Incorrect password!'
                flash(msg)
                return render_template('login.html')
            else:
                msg = 'Incorrect username!'
                flash(msg)
                return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        account_exists = cur.execute("SELECT username FROM users WHERE username=%s", (username,))
        if account_exists:
            msg = 'Username taken'
            flash(msg)
            return render_template('register.html')

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        msg = 'You created your account. You can now log in'
        flash(msg)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')

@app.route("/login_attempts")
def login_attempts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, ip, time FROM login_attempts WHERE user_id=%s", (session['id'],))
    login_attempts = cur.fetchall()
    ids = [(i[0],) for i in login_attempts]
    cur = mysql.connection.cursor()
    cur.executemany("DELETE FROM login_attempts WHERE id=%s", ids)
    mysql.connection.commit()
    return render_template("login_attempts.html", attempts=login_attempts)

if __name__=="__main__":
    app.run(host='0.0.0.0', port='5000')
