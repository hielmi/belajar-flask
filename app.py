from flask import Flask, render_template, request
from flask_mysqldb import MySQL

#init main app
app = Flask(__name__)

#database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

#init mysql
mysql = MySQL(app)

#set route
@app.route("/")
def index():

    # cursor koneksi mysql
    cursor = mysql.connection.cursor()

    # eksekusi queri
    cursor.execute("SELECT * FROM users")

    #get data
    data = cursor.fetchall()

    #tutup kursor
    cursor.close()

    return render_template('data.html', users=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
    
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)