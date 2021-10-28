from flask import Flask, render_template, abort, jsonify, request, url_for
#from content_management import Content
from model import db, save_db

#TOPIC_DICT = Content()

app = Flask(__name__)

@app.route('/')
def homepage():
    cards=db
    return render_template("intro.html")


@app.route('/main', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Form has been submitted, process data
        CA = {"IP": request.form["IP"], "VLAN": request.form["VLAN"],"MAC": request.form["MAC"],"KC": request.form["KC"],"CA": request.form["CA"], "IP": request.form["IP"],}
        db.append(CA)
        save_db()
        return render_template("result.html")
#        return redirect(url_for("provisioning", CA))
    else:
        CA = {"IP": request.form["IP"], "VLAN": request.form["VLAN"],"MAC": request.form["MAC"],"KC": request.form["KC"],"CA": request.form["CA"], "IP": request.form["IP"],}
        return render_template("result.html")

#@app.route('/addKC/')
#def provisioning(CA):
     # Connect to device
#    return render_template("main.html")

if __name__ == "__main__":
    app.run()