from flask import Flask, render_template, request
# from markupsafe import escape

#main app 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/salad")
# def salad():
#     return render_template('saladIn.html')

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         return f"<h1> Hai, {email}!"
    
#     return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)