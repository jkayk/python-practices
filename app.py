from flask import Flask, render_template, request
from extractors.berlinstartupjobs import extract_berlinstartupjobs
from extractors.web3 import extract_web3
from extractors.weworkremotely import extract_weworkremotely

app = Flask(__name__)

@app.route("/") # when user goes to "/", run the home() function. make sure there's no line between @app and def
def home():
    return render_template("home.html", name="John")

@app.route("/search") 
def search():
    keyword = request.args.get("keyword")
    berlinstartupjobs = extract_berlinstartupjobs(keyword)
    web3 = extract_web3(keyword)
    weworkremotely = extract_weworkremotely(keyword)
    jobs = berlinstartupjobs + web3 + weworkremotely
    return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)