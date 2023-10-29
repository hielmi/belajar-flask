from flask import Flask, render_template, redirect, request, url_for, session
import mysql.connector

app = Flask(__name__)

# Konfigurasi basis data
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "flaskmysql",
}

# secret key untuk session
app.secret_key = 'mysecretkey'
# Inisialisasi koneksi dan kursor
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Daftar pilihan untuk elemen <select>
option_select = [
    "Sistem Informasi",
    "Ilmu Komunikasi",
    "Teknik Komputer",
    "Teknik Elektro",
    "Informatika"
]

@app.route("/")
def index():
    if 'is_logged_in' in session:
        cursor.execute("SELECT * FROM mahasiswa")
        records = cursor.fetchall()
        return render_template('mahasiswa.html', data=records)
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                            (username, password))
        
        result = cursor.fetchone()
        print((username,password))
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]

            return redirect(url_for('index'))
        
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)

    return redirect(url_for('login'))

# membuat route untuk insert data dan update data
@app.route("/insert_mahasiswa", methods=['GET', 'POST'])
@app.route("/update_mahasiswa/<int:id>", methods=['GET', 'POST'])
def insert_or_update_mahasiswa(id=None):
    if 'is_logged_in' in session:
        if request.method == 'POST':
            nama = request.form['nama']
            npm = request.form['npm']
            jenis_kelamin = request.form['jenis_kelamin']
            prodi = request.form['prodi']
            alamat = request.form['alamat']

            if id is None:
                # Insert new data
                cursor.execute("INSERT INTO mahasiswa (nama, npm, jenis_kelamin, prodi, alamat) VALUES (%s, %s, %s, %s, %s)",
                            (nama, npm, jenis_kelamin, prodi, alamat))
            else:
                # Update existing data
                cursor.execute("UPDATE mahasiswa SET nama = %s, npm = %s, jenis_kelamin = %s, prodi = %s, alamat = %s WHERE id = %s",
                                (nama, npm, jenis_kelamin, prodi, alamat, id))

            connection.commit()
            return redirect(url_for('index'))

        if id is not None:
            cursor.execute("SELECT * FROM mahasiswa WHERE id = %s", (id,))
            data = cursor.fetchone()
            return render_template('form.html', option=option_select, default_value=data[4], data=data, url=url_for('insert_or_update_mahasiswa', id=id))

        return render_template('form.html', option=option_select, data=None)

    else:
        return redirect(url_for('login'))
    
@app.route("/delete_mahasiswa/<int:id>")
def delete_mahasiswa(id):
    if 'is_logged_in' in session:
        cursor.execute("DELETE FROM mahasiswa WHERE id = %s", (id,))
        connection.commit()
        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
