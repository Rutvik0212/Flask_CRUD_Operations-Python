from flask import *

import pymysql
import re


# connect to database
db = pymysql.connect(host="localhost",
                     user="root",
                     password="",
                     database="S_manager")

cursor = db.cursor()

app = Flask(__name__)


# login page
@app.route('/')
def login():
    return render_template('login.html')


# login check
@app.route("/sign_in", methods=["POST"])
def sign_in():

    global uname
    # receiving data from html
    uname = request.form.get("Username")
    pwd = request.form.get("pwd")

    que = "select username, password from login_details where username = '{}'".format(
        uname)

    cursor.execute(que)
    data = cursor.fetchall()

    if len(data) > 0:
        if data[0][1] == pwd:
            return redirect(url_for("home"), )
        else:
            return render_template("login.html", info='Invalid Username or Password')
    else:
        return render_template("login.html", info='Invalid Username or Password')


# create account page
@app.route('/craccount')
def craccount():
    return render_template('signup.html')


# create new account
@app.route("/sign_up", methods=["POST"])
def sign_up():

    uname = request.form.get("Username")
    pwd = request.form.get("pwd")

    # to check username is already present or not
    checkq = "select * from login_details where username = '{}'".format(uname)
    cursor.execute(checkq)
    data = cursor.fetchall()
    # print(data)

    if len(data) > 0:
        return render_template("login.html", info="Username already exist")
    else:
        inq = "insert into login_details (username, password) values ('{}', '{}')".format(
            uname, pwd)
        try:
            cursor.execute(inq)
            db.commit()
            return render_template("login.html", info="Account created succesfully..")
        except:
            db.rollback()
            return "Error in Query.."


# HOME PAGE
@app.route("/home")
def home():
    global uname
    return render_template('home.html')


# Adding NEW details
@app.route("/create", methods=['POST'])
def create():

    # strip for removing both sides white spaces (otherwise raisaing error in re)
    sname = (request.form.get("sname")).title().strip()
    div = (request.form.get("div")).title().strip()
    cls = str(request.form.get("cls")).strip()
    contact = request.form.get("contact")

    # calling function and store value in out
    out = validating_details(div, cls, contact)

    if out[0]:                    # validating division
        if out[1]:                # validating standard i.e. cls
            if out[2]:            # validating contact number

                # QUERY FOR INSERT DATA
                insq = "insert into student_details(name,division,standard,phone) values('{}','{}','{}','{}')".format(
                    sname, div, cls, contact)

                try:
                    cursor.execute(insq)
                    db.commit()
                    return render_template('home.html', info="Details added")
                except:
                    db.rollback()
                    return "Error in Query"

            else:
                return render_template('home.html', info="Invalid Phone Number")
        else:
            return render_template('home.html', info="School is upto 9th std.")
    else:
        return render_template('home.html', info="Class have only 4 div A,B,C,D")



# checking entered details using regular expression
def validating_details(div, cls, contact):

    # validate div , standard , phone number
    division = re.fullmatch(r'[A-D]', div)       # contain only four div
    clas = re.fullmatch(r'\d', cls)              # School is upto 9th standard
    con = re.fullmatch(r'[6-9]\d{9}', contact)   # validating number

    out = [division, clas, con]
    return out


# show datails
# table name - student_details
@app.route("/manage")
def manage():
    cursor.execute("select * from student_details")
    data = cursor.fetchall()
    length = len(data)
    return render_template("manage.html", userdata=data, length=length)


# Deleting details
@app.route('/delete')
def delete():
    id = request.args.get("id")

    delq = "delete from student_details where id={}".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for("manage"))

    except:
        db.rollback()
        return "Error in Query.."


# edit details
@app.route('/edit')
def edit():
    global data1
    id = request.args.get('id')
    # return "id is",id

    selq = "select * from student_details where id = '{}'".format(id)
    try:
        cursor.execute(selq)
        data1 = cursor.fetchone()
        return render_template('edit.html', row=data1)
    except:
        db.rollback()
        return "Error in Query.."


# update edited details
@app.route('/update', methods=['POST'])
def update():
    # using value of edit page
    global data1

    sname = (request.form.get("sname")).title().strip()
    div = (request.form.get("div")).title().strip()
    cls = str(request.form.get("cls")).strip()
    contact = request.form.get("contact")    
    uid = request.form.get("uid")
    
    out = validating_details(div, cls, contact)

    5
    if out[0]:                    # validating division
        if out[1]:                # validating standard i.e. cls
            if out[2]: 

                updq = "update student_details set name = '{}', division = '{}', standard = '{}', phone = '{}' where id = '{}'".format(
                    sname, div, cls, contact, uid)
                try:
        
                    cursor.execute(updq)
                    db.commit()
                    return redirect(url_for('manage'))

                except:
                    db.rollback()
                    return "Error in Query.."
            else:
                return render_template('edit.html', info="Invalid Phone Number",row = data1)
        else:
            return render_template('edit.html', info="School is upto 9th std.",row = data1)
    else:
        return render_template('edit.html', info="Class have only 4 div A,B,C,D",row = data1)


# method for render search page
@app.route('/search')
def search():
    return render_template('search.html')


# search details method
@app.route('/search_details', methods=['POST'])
def search_details():
    search_data = request.form.get('details')
    searchq = "select * from student_details where name = '{a}' or division = '{a}' or standard = '{a}' or phone = '{a}' or name like '%{a}' or name like '{a}%' ".format(
        a=search_data)

    try:
        cursor.execute(searchq)
        data = cursor.fetchall()
        if len(data) > 0:
            return render_template('search.html', userdata=data)
        else:
            return render_template('search.html', info="Details not Found")
    except:
        db.rollback()
        return "Error in Query.."


@app.route('/about')
def about():
    return render_template("about.html")


# feedback entry method
@app.route('/feedback', methods=['POST'])
def feedback():
    firstname = (request.form.get("firstname")).title()
    lastname = (request.form.get("lastname")).title()
    subject = (request.form.get('subject')).capitalize()

    # print("name",firstname)
    # return ("firstname = " ,firstname)
    with open('feedback.txt', 'a+') as file:
        try:
            file.seek(0)
            file.write("Name :")
            file.write(firstname)
            file.write(' ')
            file.write(lastname)
            file.write('\n')
            file.write('Feedback :')
            file.write(subject)
            file.write('\n')
            file.close()
        finally:
            return render_template('about.html', msg="Thank You For Your Feedback...")


if __name__ == "__main__":
    app.run(debug=True)
