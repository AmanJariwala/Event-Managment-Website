import mysql.connector
import os
cnx = mysql.connector.connect(user="root", password="Hemali43",
                              host="35.239.148.20",
                              database="eventmanager")

cursor = cnx.cursor()

# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def signinn():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        emailid = request.form.get("fname")
        # getting input with name = lname in HTML form
        passwordd = request.form.get("lname")
        global userss
        try:
            cursor.execute("Select password from signup where email = '" + emailid + "' ;")
            userss = cursor.fetchone()
            if str(userss[0]) == passwordd:
                # cursor.execute("call RemoveCurrentEmail;")
                # cnx.commit()
                # cursor.execute("INSERT INTO CurrentEmail (user_email) values ('" + emailid + "');")
                # cnx.commit()
                print ("Done success sign in ")
                return render_template("Profile.html")
                # return "<a href = \"Profile.html\">Click here :)</a>"
            else:
                return render_template("alert.html")
        except:
            print("Error: Data is wrong;")
        return "You entered wrong data! Go back and try again!"
    return render_template("Log in.html")


@app.route('/signup', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        emailid = request.form.get("fname")
        # getting input with name = lname in HTML form
        passwordd = request.form.get("lname")
        first_name = request.form.get("fullname")
        locationid = request.form.get("locationname")
        try:
            cursor.execute(
                "INSERT INTO signup (email, name, password, location) values ('" + emailid + "', '" + first_name + "', '" + passwordd + "', '" + locationid + "');")
            cnx.commit()
            print ("Done success!")
        except:
            print("Error: Data not done;")
        global users
        try:
            cursor.callproc('GetUserEmails')
            # print results
            for result in cursor.stored_results():
                listusers = result.fetchall()
            print(listusers)
        except:
            print("Error: fetching not done;")
        return "Good you signed up! Now go here to sign-in:  " + "<a href = \"/\">Click here :)</a>"
    return render_template("Sign up.html")






# @app.route('/', methods=["GET", "POST"])
# def signinn():
#     if request.method == "POST":
#         # getting input with name = fname in HTML form
#         emailid = request.form.get("email address")
#         # getting input with name = lname in HTML form
#         passwordd = request.form.get("password")
#
#         locationn = request.form.get("location")
#
#         global userss
#         try:
#             cursor.execute("Select password from signup where email = '" + emailid + "' ;")
#             userss = cursor.fetchone()
#             if str(userss[0]) == passwordd:
#                 cursor.execute("call RemoveCurrentEmail;")
#                 cnx.commit()
#                 cursor.execute("INSERT INTO CurrentEmail (user_email) values (" + emailid + ");")
#                 cnx.commit()
#                 print ("Log In successful!")
#                 return "<a href = \"/Profile\">Click here:)</a>"
#             else:
#                 return render_template("Incorrect details.html")
#         except:
#             print("Error: Data is incorrect;")
#         return "You entered incorrect data! Go back and try again!"
#     return render_template("Log in.html")
#
# @app.route('/signup', methods=["GET", "POST"])
# def gfg():
#     if request.method == "POST":
#         emailid = request.form.get("email address")
#         passwordd = request.form.get("password")
#         first_name = request.form.get("fullname")
#         locationid = request.form.get("location")
#         try:
#             cursor.execute("INSERT INTO signup (name, email, password) values ('" + first_name + "', '" + emailid + "' '" + passwordd + "');")
#             cnx.commit()
#             print ("Done Successfully!")
#         except:
#             print ("Error!")
#         global users
#         try:
#             cursor.callproc('GetUserEmails')
#             # print results
#             for result in cursor.stored_results():
#                 listusers = result.fetchall()
#             print(listusers)
#         except:
#             print("Error: fetching not done;")
#         return "Good you signed up! Now go here to sign-in:  " + "<a href = \"/\">Click here :)</a>"
#     return render_template("Sign up.html")




app.run(debug=True)
print ("dd")
print ("ddddd")
cnx.commit()
cursor.close()
cnx.close()
