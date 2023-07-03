from flask import Flask, flash, url_for
from flask import render_template, request
import sqlite3 as sql
import os 
from werkzeug.exceptions import abort


app = Flask(__name__)

def get_db_connection():
    conn = sql.connect('filmflix.db')
    conn.row_factory = sql.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template(
        'index.html', posts = posts
    )

@app.route("/display")
def display():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template(
        'display.html', posts = posts
    )
 
@app.route('/insertRecord')
def insertRecord():
   return render_template('insertRecord.html')

@app.route('/getId')
def getId():
   return render_template('getId.html')

@app.route('/updateRecord', methods = ['GET','POST'])
def updateRecord():
   conn = get_db_connection()
   if request.method == 'POST':
      try:
         filmID1 = request.form['filmID']
         print(filmID1)
         posts = conn.execute(f'SELECT * FROM tblFilms WHERE filmID = {filmID1}').fetchall()
         conn.close()
      except:
         msg = "error in update operation"
      finally:
         if(posts):
            return render_template(
               'updateRecord.html', posts = posts
            )
         else:
            msg="ID is not found, please try again"
            return render_template("result.html",msg = msg)

@app.route('/deleteRecord')
def deleteRecord():
   return render_template('deleteRecord.html')

@app.route('/reportBy')
def reportBy():
   return render_template('reportBy.html')

@app.route('/reportRecord', methods = ['GET','POST'])
def reportRecord():
   conn = get_db_connection()
   if request.method == 'POST':
      try:
         field = request.form['reportBy']
         print(field)
         fieldValue = request.form['filterValue']
         fieldValue = '"%'+fieldValue+'%"'
         print(fieldValue)
         posts = conn.execute(f'SELECT * FROM tblFilms WHERE {field} LIKE {fieldValue}').fetchall()
         conn.close()
      except:
         msg = "error in record operation"
      finally:
         return render_template(
            'display.html', posts = posts
         )



#create Exit Function
@app.route('/welcome')
def welcome():
   return render_template("welcome.html")


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         title = request.form['title']
         yearRld = request.form['yearRld']
         rating = request.form['rating']
         duration = request.form['duration']
         genre = request.form['genre']
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            if(title=='' or yearRld=='' or rating =='' or duration =='' or genre==''):
               msg = "Some of the fields are empty"
            else:
               cur.execute(f"INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?,?,?,?,?)", (title, yearRld, rating, duration, genre))
            
               con.commit()
               msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/updaterec',methods = ['POST', 'GET'])
def updaterec():
   if request.method == 'POST':
      try:
         filmID = request.form['filmID']
         filmID = int(filmID)
         title = request.form['title']
         yearRld = request.form['yearRld']
         yearRld = int(yearRld)
         rating = request.form['rating']
         duration = request.form['duration']
         duration = int(duration)
         genre = request.form['genre']
         
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            print(cur)
            cur.execute(f"UPDATE tblFilms SET title=?, yearReleased=?, rating=?, duration=?, genre=? WHERE filmID = ?", (title, yearRld, rating, duration, genre, filmID))
            print("execute")
            con.commit()
            msg = "Record successfully updated"
      except:
         con.rollback()
         msg = "error in update operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/deleterec',methods = ['POST', 'GET'])
def deleterec():
   if request.method == 'POST':
      try:
         filmID = request.form['filmID']
         filmID = int(filmID)
         
         with sql.connect("filmflix.db") as con:
            cur = con.cursor()
            posts = cur.execute(f'SELECT * FROM tblFilms WHERE filmID = {filmID}').fetchall()
            print(posts)
            if(posts):
               cur.execute(f"DELETE FROM tblFilms WHERE filmID = {filmID}")
               con.commit()
               msg = "Record successfully deleted"
            else:
               msg = "ID does not exist, please try again later!"
               
      except:
         con.rollback()
         msg = "error in delete operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)