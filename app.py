from flask import Flask, render_template, request, jsonify
import sys
import statistics
import json
app = Flask(__name__)

@app.route("/")
def index():
    with open("db.json") as db:
        stats = json.load(db)
    return render_template("index.html",stats=stats)

@app.route("/enroll",methods=["POST"])
def enroll():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        pressions = json.loads(request.form.getlist("pressions")[0])
        save_file(pressions,user,password)
        return render_template("verify.html")


@app.route("/verify",methods=["POST","GET"])
def verify():
    if request.method =="POST":
        user = request.form["user"]
        pressions = json.loads(request.form.getlist("pressions")[0])
        with open("db.json") as db:
            stats = json.load(db)

        user_stats = stats[user]
        results = get_formula_result(user_stats,pressions)

        return render_template("verify.html",results=results)
    else:
        return render_template("verify.html")

def get_formula_result(user_stats,pressions):
    #formula
    counter = 0
    results=[]
    triples = user_stats["triples"]
    password = user_stats["password"]
    for i,triple in enumerate(triples):
        average = triple[0]
        median = triple[1]
        sdev = triple[2]

        char_pression = pressions[i]

        if min(average,median)*(0.95- sdev/average) <= char_pression and \
        char_pression <= max(average,median)*(1.05 + sdev/average):
            results.append({password[i]:True})
            counter +=1
        else:
            results.append({password[i]:False})

    percentage = (counter/len(results))*100
    return {"stats":results,"percentage":percentage}


def save_file(pressions,user,password):
    calculated_triples = []

    with open("db.json") as db:
        stats = json.load(db)
    print(type(pressions),file=sys.stderr)
    for char_pressions in pressions: #pression is an array of arrays of pressions for each char
        print(char_pressions,file=sys.stderr)
        average = statistics.mean(list(map(int, char_pressions)))
        median = statistics.median(list(map(int, char_pressions)))
        sdeviation = statistics.stdev(list(map(int, char_pressions)))
        calculated_triples.append((average,median,sdeviation))

    stats[user]={"password":password,"triples":calculated_triples}
    with open("db.json","w") as db:
        json.dump(stats, db)
