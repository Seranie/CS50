from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    if not request.args.get("color"):
        return render_template("index.html")
    else:
        color = request.args.get("color")
        return render_template("color.html", color=color)