from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/test"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('index.html')

@app.route('/tambah_data')
def tambah_data():
    db.create_all()

    new_user = User(username='test user')
    db.session.add(new_user)
    db.session.commit()

    # Retrieve users from the database
    users = User.query.all()
    
    user_list = [user.username for user in users]
    
    return 'Users: {}'.format(', '.join(user_list))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        return f"<h1> Hai, {email}!"
    
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)