from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from flask_session import Session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import sqlalchemy
import os
import pymysql


# from dotenv import load_dotenv
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
#
# db_user = os.getenv("MYSQL_USER")
# db_pass = os.getenv("MYSQL_PASS")
# db_name = os.getenv("MYSQL_DB")
# cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")


cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")



prod = False


app = Flask(__name__)
app.secret_key = os.urandom(24)

# app.config.update(
#     #Set the secret key to a sufficiently random value
#     SECRET_KEY=os.urandom(24),
#
#     #Set the session cookie to be secure
#     SESSION_COOKIE_SECURE=True,
#     SESSION_TYPE = 'filesystem'
# )
# Session(app)

#connect = "mysql+pymysql://{}:{}@/{}?unix_socket=/cloudsql/{}"""
#db = create_engine(connect.format(db_user,db_pass,db_name,cloud_sql_connection_name))


if prod:
    db_user = os.environ.get("MYSQL_USER")
    db_pass = os.environ.get("MYSQL_PASSWORD")
    db_name = os.environ.get("MYSQL_DB")
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            username=db_user,
            password=db_pass,
            database=db_name,
            query={'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)}
        ),
    )
else:
    db_user='root'
    db_pass='password348'
    db_name='test'
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            username=db_user,
            password=db_pass,
            database=db_name,
            # query={'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)}
        ),
    )


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4,max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password!')

def is_user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('logged_in' in session)
        if 'logged_in' in session:
            print("here")
            return f(*args, **kwargs)
        else:
            print("here2")
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('land.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        with db.connect() as conn:
            result = conn.execute(
                """Select * from users where user_name = %s limit 1""",(username)
            ).fetchall()
            if len(result) > 0:
                flash('User name already exists')
                return render_template('register.html', form=form)
            data = conn.execute(
                "INSERT INTO users(uid, user_name, password) VALUES(%s, %s, %s)",(username, username, password)
            )
        flash('You are registered and can log in', 'Success!')
        return redirect(url_for('index'))
        #return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        with db.connect() as conn:
            result = conn.execute(
                """Select * from users where user_name = %s limit 1""",[username]
            ).fetchall()
        # Get user by username
        if len(result) > 0:
            # Get stored hash
            password = result[0][2]
            print(password)
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                print('logged_in' in session)
                flash('You are now logged in','success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid Password'
                return render_template('login.html', error=error)
            # Close Connection
        else:
            error = 'Username is not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/home')
@is_user_logged_in
def home():
    data = []
    with db.connect() as conn:
        data = conn.execute(
            "Select movie_title, imdb_score, genres from MOVIE_USER;"
        ).fetchall()
    return render_template('home.html', outdata=data)

@app.route('/dashboard',  methods=['GET', 'POST'])
@is_user_logged_in
def dashboard():
    if request.method == 'POST':
        select = request.form.get('genre')
        if select == "All":
            return redirect(url_for('home'))
        with db.connect() as conn:
            data = conn.execute(
                """Select movie_title, imdb_score, genres from MOVIE_USER where
                genres like %s limit 10;""", [select+"%"]
            ).fetchall()
        return(render_template('home.html', outdata=data))




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
