from flask import Flask, render_template

#init main app
app = Flask(__name__)

#set route
@app.route("/")
def index():
    return render_template('index.html', )

if __name__ == "__main__":
    app.run(debug=True)