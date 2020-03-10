from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
#from flask_session import Session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import sqlalchemy
import os
import pymysql
import uuid
from datetime import datetime

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
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
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
        uid = str(uuid.uuid4())
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
                "INSERT INTO users(uid, user_name, password) VALUES(%s, %s, %s)",(uid, username, password)
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
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['uid'] = result[0][0]
                session.permanent = True
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Password'
                return render_template('login.html', error=error)
            # Close Connection
        else:
            error = 'Username is not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

# @app.route('/home')
# @is_user_logged_in
# def home():
#     data = []
#     with db.connect() as conn:
#         data = conn.execute(
#             "Select movie_title, country, imdb_score, genres,title_year, language from MOVIE_USER;"
#         ).fetchall()
#     return render_template('home.html', outdata=data)

@app.route('/dashboard',  methods=['GET', 'POST'])
@is_user_logged_in
def dashboard():
    if request.method == 'POST':
        select = request.form.get('genre')
        country = request.form.get('country')
        score = request.form.get('score')
        year = request.form.get('year')
        if year == "year":
            year = "title_year"
        if select == "All":
            select = "%"
        if score == None:
            score = 0
        with db.connect() as conn:
            if country == "country":
                data = conn.execute(
                    """Select distinct movie_title, country, imdb_score, genres,title_year, language, mid from movies where
                    genres like %s and imdb_score >= %s and title_year =""" + year +";", [select+"%",score]
                ).fetchall()
            else:
                data = conn.execute(
                    """Select distinct movie_title, country, imdb_score, genres,title_year, language, mid from movies where
                    genres like %s and country = %s and imdb_score >= %s and title_year =""" + year+";", [select+"%", country, score]
                ).fetchall()

        return(render_template('home.html', outdata=data))
    data = []
    with db.connect() as conn:
        data = conn.execute(
            "Select distinct movie_title, country, imdb_score, genres,title_year, language, mid from movies;"
        ).fetchall()
    return render_template('home.html', outdata=data)


@app.route('/wishlist',  methods =['GET', 'POST'])
@is_user_logged_in
def wishlist():
    if request.method == 'POST':
        select = request.form.get('genre')
        country = request.form.get('country')
        score = request.form.get('score')
        year = request.form.get('year')
        if year == "year":
            year = "title_year"
        if select == "All":
            select = "%"
        if score == None:
            score = 0
        with db.connect() as conn:
            if country == "country":
                data = conn.execute(
                    """Select distinct movie_title, country, imdb_score, genres,title_year, language, movies.mid from movies, wishlist where
                    movies.mid = wishlist.mid and wishlist.uid = %s and
                    genres like %s and imdb_score >= %s and title_year =""" + year +";", [session['uid'],select+"%",score]
                ).fetchall()
            else:
                data = conn.execute(
                    """Select distinct movie_title, country, imdb_score, genres,title_year, language, movies.mid from movies, wishlist where
                    movies.mid = wishlist.mid and wishlist.uid = %s and
                    genres like %s and country = %s and imdb_score >= %s and title_year =""" + year+";", [session['uid'], select+"%", country, score]
                ).fetchall()

        return(render_template('wishlist.html', outdata=data))
    data = []
    with db.connect() as conn:
        data = conn.execute(
            """Select distinct movie_title, country, imdb_score, genres,title_year, language, movies.mid from movies, wishlist where
            movies.mid = wishlist.mid and wishlist.uid = %s;""", [session['uid']]
        ).fetchall()
    return render_template('wishlist.html', outdata=data)


@app.route('/recommendation',  methods=['GET'])
@is_user_logged_in
def recommendation():
    data = []
    header = ["Title", "imdb_score", "genres","year", "mid"]
    with db.connect() as conn:
        data = conn.execute(
            "Select distinct movie_title, imdb_score, genres,title_year, mid from movies;"
        ).fetchall()
    type = request.args.get('type')
    if type == 'genrePopular':
        header = ["Title", "Genres", "Mid"]
        with db.connect() as conn:
            data = conn.execute(
                """select movie_title, movies.genres, movies.mid
                	from test.movies as movies,
                	(select genres, max(num_voted_users) as num_voted_users
                	from test.movies
                	group by genres) a
                where movies.genres = a.genres
                and movies.num_voted_users = a.num_voted_users
                ;"""
            ).fetchall()
    elif type == 'ratingYear':
        header = ["Title", "Year", "Score", "Mid"]
        with db.connect() as conn:
            data = conn.execute(
                """select movie_title, movies.title_year, movies.imdb_score, movies.mid
                        from test.movies as movies,
                        (select title_year, max(imdb_score) as imdb_score
                        from test.movies
                        group by title_year) a
                where movies.title_year = a.title_year
                and movies.imdb_score = a.imdb_score
                order by a.title_year
                ;"""
            ).fetchall()
    elif type == 'directorPopular':
        header = ["Title", "Director", "Mid"]
        with db.connect() as conn:
            data = conn.execute(
                """select movie_title, a.director_name, mid
                        from test.movies,
                	(select d.did, d.director_name, max(b.num_voted_users) as  num_voted_users
                        from test.movies b, test.movie2director as c, test.directors as d where
                	b.mid = c.mid and
                	c.did = d.did
                        group by d.did, d.director_name) as a
                where movies.director_name = a.director_name
                and movies.num_voted_users = a.num_voted_users
                ;"""
            ).fetchall()

    return render_template('recommendation.html', outdata=data, header = header)





@app.route('/process_wishlist',methods=['POST'])
def process_wishlist():
    content=request.get_json(force=True)
    uid = session['uid']
    mid = content[6]
    date = datetime.today().strftime('%Y-%m-%d')
    with db.connect() as conn:
        firstStep = conn.execute(
            "Select * from wishlist where uid = %s and mid = %s;",(uid, mid)
        ).fetchall()
        if len(firstStep) < 1:
            data = conn.execute(
                "INSERT INTO wishlist(uid, mid, date_created) VALUES(%s, %s, %s)",(uid, mid, date)
            )
    return redirect(url_for('dashboard'))

@app.route('/logout')
# @is_user_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
