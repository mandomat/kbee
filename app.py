from flask import Flask, render_template, request, jsonify
import sys
import statistics
import json
import base64
import hashlib
import os
from pymongo import MongoClient
import face_recognition
import numpy as np

app = Flask(__name__)

client = MongoClient(
    #os.environ['DB_PORT_27017_TCP_ADDR'],
    #27017
    )
db = client.kbee
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        image = request.form["image"]
        pressions = json.loads(request.form.getlist("pressions")[0])
        res = save_user_stats(pressions,user,password)
        if res:
            convert_and_save_image(image,user+".jpg")
            known_image = face_recognition.load_image_file(user+".jpg")
            biden_encoding = face_recognition.face_encodings(known_image)[0]

            db.users_collection.update_one({"_id":user},{'$set':{"img_encoding":biden_encoding.tolist()}})
            return render_template("exams.html",user=user)
        else:
             return render_template("index.html",error="Existing user")

@app.route("/testenroll",methods=["POST","GET"])
def testenroll():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        pressions = json.loads(request.form.getlist("pressions")[0])
        save_file(pressions,user,password)
        with open("db.json") as db:
            stats = json.load(db)
        users=list(stats.keys())
        return render_template("testverify.html",users=users)
    else:
        with open("db.json") as db:
            stats = json.load(db)
        return render_template("testenroll.html",stats=stats)


@app.route("/verify",methods=["POST","GET"])
def verify():
    if request.method =="POST":
        user = request.form["user"]
        password = request.form["password"]
        pressions = json.loads(request.form.getlist("pressions")[0])
        #with open("db.json") as f:
        #    stats = json.load(f)
        db_user = db.users_collection.find_one({"_id":user})
        if  not db_user or  db_user["password"] != hashlib.sha256(password.encode('UTF-8')).hexdigest() \
         or len(db_user["pressions"]) != len(pressions):
            error = "Wrong password, wrong typing or wrong username"
            return render_template("exams.html",error=error)

        results = get_formula_result(user,pressions)
        if results["percentage"] >= 75:
            return render_template("exam.html",results=results,user=user)
        else:
            error = "Seems like you're not who you say you are... ("+str(results["percentage"])+"%) match"
            return render_template("exams.html",error=error)
    else:
        return render_template("exams.html")

@app.route("/testverify",methods=["POST","GET"])
def testverify():
    with open("db.json") as db:
        stats = json.load(db)
    users=list(stats.keys())
    if request.method =="POST":
        tester = request.form["tester"]
        user = request.form["user"]
        password = request.form["password"]
        pressions = json.loads(request.form.getlist("pressions")[0])

        if  not user in stats or  stats[user]["password"] != password \
         or len(stats[user]["pressions"]) != len(pressions):
            error = "Wrong password, wrong typing or wrong username"
            return render_template("testverify.html",error=error,selected=user,tester=tester,users=users)

        results = get_formula_result_test(user,pressions)

        with open("stats.txt") as f:
            stats = f.readlines()

        stats.append(tester+"\t"+user+"\t"+str(results["percentage"])+"\n")

        with open("stats.txt","w") as f:
            f.writelines(stats)

        return render_template("testverify.html",results=results,selected=user,tester=tester,users=users)
    else:
        return render_template("testverify.html",users=users)

@app.route("/verify_image",methods=["POST"])
def verify_image():
    image = request.form["image"]
    user = request.form["user"]
    convert_and_save_image(image,user+".jpg")

    unknown_image = face_recognition.load_image_file(user+".jpg")

    biden_encoding = db.users_collection.find_one({"_id":user})["img_encoding"]
    biden_encoding = np.array(biden_encoding)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

    print(results, file = sys.stderr)

    return str(results)

@app.route("/stats")
def stats():
    with open("stats.txt") as f:
        stats = f.read()
    return render_template("stats.html",stats=stats)

def convert_and_save_image(imgstring,imagename):
    imgstring = imgstring.split(',')[1]
    imgdata = base64.b64decode(imgstring)
    with open(imagename, 'wb') as f:
        f.write(imgdata)

def get_formula_result(user,pass_pressions):
    #formula
    counter = 0
    results=[]
    db_user = db.users_collection.find_one({"_id":user})

    stat_pressions = db_user["pressions"]
    password = db_user["password"]
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

        db.users_collection.update({"_id": user}, {"$set": {"pressions": stat_pressions}})

    return {"stats":results,"percentage":percentage}

def get_formula_result_test(user,pass_pressions):
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

def save_user_stats(pressions,user,password):
    db_user = db.users_collection.find_one({"_id":user})
    if not db_user:
        hashed_pw = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        db.users_collection.insert_one({"_id":user,"password":hashed_pw,"pressions":pressions})
        return True
    else:
         return False
