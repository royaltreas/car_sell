from flask import Flask, render_template, redirect, url_for,request,session
from flask_mysqldb import MySQL
import MySQLdb
app = Flask(__name__)
app.secret_key = "12456789"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)
@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        if 'username' in request.form and 'password' in request.form:
            username = request.form["username"]
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE Email=%s AND Password = %s",(username,password))
            info = cursor.fetchone()
            if info is not None:
                if info["Email"] == username and info['Password'] == password:
                    session['loginsuccess']=True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/new',methods=['GET','POST'])
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            username = request.form['one']
            email = request.form['two']
            password = request.form['three']
            id = (request.form['four'])
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO logininfo(id,Name,Email,Password) VALUES (%s,%s,%s,%s)",(id,username,email,password))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/act',methods=['GET','POST'])
def contact_college():
    if request.method == "POST":
        if "username" in request.form and "subject" in request.form and "message" in request.form:
            username = request.form['username']
            subject = request.form['subject']
            message = request.form['message']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO Queries(username,subject,message) VALUES (%s,%s,%s)",(username,subject,message))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template('contact.html')

@app.route('/new/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template("profile.html")

@app.route('/new/logout')
def logout():
    session.pop('loginsuccess',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
