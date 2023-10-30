from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL

#init main app
app = Flask(__name__)

#database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

#init mysql
mysql = MySQL(app)

# Set the secret key
app.secret_key = 'aplikasipertamaflask'

#set route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        if email == '' or password == '':
            return redirect(url_for('login.html'))

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (email, password))

        result = cursor.fetchone()

        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]

            print('password benar')
            return redirect(url_for('home'))
        else:
            print('password salah')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route("/home")
def home():
    if 'is_logged_in' in session:

        # cursor koneksi mysql
        cursor = mysql.connection.cursor()

        # eksekusi queri
        cursor.execute("SELECT * FROM users")

        #get data
        data = cursor.fetchall()

        #tutup kursor
        cursor.close()

        return render_template('home.html', users=data)
    
    else: 
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)