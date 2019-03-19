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
        password = request.form["password"]
        pressions = json.loads(request.form.getlist("pressions")[0])

        with open("db.json") as db:
            stats = json.load(db)


        if  not user in stats or  stats[user]["password"] != password \
         or len(stats[user]["pressions"]) != len(pressions):
            error = "Wrong password, wrong typing or wrong username"
            return render_template("verify.html",error=error)

        results = get_formula_result(user,pressions)

        return render_template("verify.html",results=results)
    else:
        return render_template("verify.html")

def get_formula_result(user,pass_pressions):
    #formula
    counter = 0
    results=[]

    with open("db.json") as db:
        stats = json.load(db)

    stat_pressions = stats[user]["pressions"]
    password = stats[user]["password"]
    for i,char_pression in enumerate(stat_pressions):
        average = statistics.mean(list(map(int, char_pression)))
        median = statistics.median(list(map(int, char_pression)))
        sdev = statistics.stdev(list(map(int, char_pression)))

        pass_char_pression = pass_pressions[i]

        if min(average,median)*(0.95- sdev/average) <= pass_char_pression and \
        pass_char_pression <= max(average,median)*(1.05 + sdev/average):
            results.append({password[i]:True})
            counter +=1
        else:
            results.append({password[i]:False})

    percentage = (counter/len(results))*100

    if percentage >= 75:
        for i,stat in enumerate(stat_pressions):
            stat.append(pass_pressions[i])
            stat.pop(0)

        stats[user]["pressions"] = stat_pressions

        with open("db.json","w") as db:
            json.dump(stats, db)

    return {"stats":results,"percentage":percentage}


def save_file(pressions,user,password):

    with open("db.json") as db:
        stats = json.load(db)

    with open("db.json","w") as db:
        stats[user]={"password":password,"pressions":pressions}
        json.dump(stats, db)
    #for char_pressions in pressions: #pression is an array of arrays of pressions for each char

        #average = statistics.mean(list(map(int, char_pressions)))
        #median = statistics.median(list(map(int, char_pressions)))
        #sdeviation = statistics.stdev(list(map(int, char_pressions)))
        #calculated_triples.append((average,median,sdeviation))

    #stats[user]={"password":password,"triples":calculated_triples}
    #with open("db.json","w") as db:
        #json.dump(stats, db)
