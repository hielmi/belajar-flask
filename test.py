from flask import Flask,render_template
import mysql.connector

app = Flask(__name__)

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flaskmysql',
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT * FROM users"
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('user_data.html', data=data)

    return result
    # user_list = [result.username for user in result]
    
    # return 'Users: {}'.format(', '.join(user_list))

if __name__ == '__main__':
    app.run(debug=True)
