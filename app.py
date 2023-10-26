from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

app = Flask(__name__)

# Konfigurasi basis data
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "flaskmysql",
}

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
    cursor.execute("SELECT * FROM mahasiswa")
    records = cursor.fetchall()
    return render_template('mahasiswa.html', data=records)

# membuat route untuk insert data dan update data
@app.route("/mahasiswa", methods=['GET', 'POST'])
@app.route("/update_mahasiswa/<int:id>", methods=['GET', 'POST'])
def insert_or_update_mahasiswa(id=None):
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

@app.route("/delete_mahasiswa/<int:id>")
def delete_mahasiswa(id):
    cursor.execute("DELETE FROM mahasiswa WHERE id = %s", (id,))
    connection.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
