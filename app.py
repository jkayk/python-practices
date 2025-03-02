from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") # when user goes to "/", run the home() function. make sure there's no line between @app and def
def home():
    return render_template("home.html", name="John")

@app.route("/search") 
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)