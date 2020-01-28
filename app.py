from flask import Flask, render_template, request, Response
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

db_user = os.environ.get("MYSQL_USER")
db_pass = os.environ.get("MYSQL_PASS")
db_name = os.environ.get("MYSQL_DB")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

db_user='root'
db_pass='password348'
db_name='test'


app = Flask(__name__)

#connect = "mysql+pymysql://{}:{}@/{}?unix_socket=/cloudsql/{}"""
#db = create_engine(connect.format(db_user,db_pass,db_name,cloud_sql_connection_name))

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        # query={'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)}
    ),
)

@app.route('/')
def hello_world():
    res = ["ERROR"]
    with db.connect() as conn:
        res = conn.execute(
            "Select * from MOVIE_USER;"
        ).fetchall()
    for row in res:
        return(row[0]+" "+str(row[1]))


@app.route('/abc/')
def hello():
    return 'Hello, abc!'
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
