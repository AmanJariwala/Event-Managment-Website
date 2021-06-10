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

  @app.route('/Profile')
def profilee():
    try:
        global ctemail
        global ctname
        global ctlocation

        cursor.execute("Select email from currentemail;")
        ctemail = cursor.fetchone()
        ctemail = str(ctemail[0])
        print ("I was here")
        print (ctemail)
        cursor.execute("Select name from currentemail;")
        ctname = cursor.fetchone()
        ctname = str(ctname[0])
        print (ctname)
        cursor.execute("Select location from currentemail;")
        ctlocation = cursor.fetchone()
        ctlocation = str(ctlocation[0])
        print (ctlocation)
        returnval = """
                    <!DOCTYPE html>
<html lang="en">
<head>
<style>
h1{
  font-family:noteworthy;
}
h2 {
  padding-top: 60px;
  padding-left: 200px;
  font-family:noteworthy;
  text-decoration: underline;
}

h3{
  text-decoration: underline;
}
textarea {
  padding-left: 100px;
  font-size: large;
}
body {
  background-color: #ff9999
}

form {
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0, 0.4); /* Black w/opacity/see-through */
  color: white;
  font-weight: bold;
  border: 3px solid #f1f1f1;
  z-index: 2;
  width: 40%;
  padding: 40px;
  float: left;
}

button[type=submit] {
  width: 50%;
  background-color: #000000;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-family:gillsans;
  font-size: large;
}

textarea{
  width: 20%;
  /*padding: 14px 20px;*/
  margin: 15px 0;
  border: none;
  border-radius: 4px;
}

button[type=submit]:hover {
  background-color: #000000;
}
</style>
    <center><h1>EVENT MANAGER</h1></center>
  <p style="font-size: 20px; text-align: right; padding-right: 40px; background-color: white;"><a href="">Feed</a></p>
</head>
<body>
<div>
  <div style="width: 100%">
    <img src="/static/PP3.jpeg" style="float:right;" width="750" height="650">
  </div>
  <div >
    <form action="{{ url_for("profilee")}}" method="post">
    <h2 >PROFILE</h2>
    
        """
        returnval += "<fieldset> <legend></legend>"
        returnval += " <label for=\"firstname\">Email:</label></br> <input name=\"firstname\" type=\"text\" value=\"" + ctemail + "\"readonly> </br>"
        returnval += " <label for=\"fullname\">Name:</label></br> <input type=\"text\" id=\"fullname\" name=\"fullname\" value=\"" + ctname + "\"readonly></br>"
        returnval += " <label for=\"location\">City/Location:</label></br> <input type=\"text\" id=\"location\" name=\"locationname\" value=\"" + ctlocation + "\"readonly></br>"
        returnval += "<a href = \"/Log in.html\"><button type=\"submit\"> Sign Out </button></a></br>"

        returnval += "<a href = \"/feed\">Go to feed</a></br>"

        # returnval += "<a href = \"/feed\"><button type=\"submit\"> Go to Feed </button></a></br>"
        # returnval += "<a href = \"/chooseevent\">Click here to send Invitations</a></br>"
        returnval += "<a href = \"/invitesrec\">Click here to view Invitations</a>"
        return returnval
        print ("Done sucess profile")
    except:
        print("Error: Data not done;")
        return "Good you signed up! Now go here back for sign-in:  " + "<a href = \"/\">Click here :)</a>"

@app.route('/recinvite')
def recinvite():
    cursor.execute("Select email from currentemail;")
    recemail = cursor.fetchone()
    recemail = str(recemail[0])

    cursor.execute("Select event_name from invitation where email = '" + recemail + "' ;")
    eventsss = cursor.fetchall()    # check from invitation table if email matches the login email then print the event details and and give accept and decline option

    names = []
    types = []
    locations = []
    dates = []
    details = []
    orgzzz = []
    for event in eventsss:
        query = "select * from events where name='" + event[0] + "';"
        # query = "select ev.event_id, ev.event_name, ev.event_type, ev.location, ev.date_time from Event ev join Feed fd on ev.event_id = fd.event_id where fd.user_email = %s;"
        cursor.execute(query)
        # ev_data = str(cursor.fetchall())

        (event_name, event_date, location, event_type, detail, organizer) = cursor.fetchall()[0]
        names.append(event_name)
        types.append(event_type)
        locations.append(location)
        dates.append(event_date)
        details.append(detail)
        orgzzz.append(organizer)

    aman = """
        <!DOCTYPE html>
    <html lang="en">
    <head>
    <style>
    h1{
      font-family:noteworthy;
    }
    h2 {

      padding-left: 200px;
      font-family:noteworthy;
      text-decoration: underline;
    }

    h3{
      text-decoration: underline;
    }
    textarea {
      padding-left: 100px;
      font-size: large;
    }
    body {
      background-color: #ff9999
    }
    input[type=submit] {
      width: 50%;
      background-color: #000000;
      color: white;
      padding: 14px 20px;
      margin: 8px 0;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    textarea{
      width: 20%;
      /*padding: 14px 20px;*/
      margin: 15px 0;
      border: none;
      border-radius: 4px;
    }

    input[type=submit]:hover {
      background-color: #000000;
    }
    div.lalala {
      background-color: rgb(0,0,0); /* Fallback color */
      background-color: rgba(0,0,0, 0.4); /* Black w/opacity/see-through */
      color: white;
      font-weight: bold;
      border: 3px solid #f1f1f1;
      z-index: 2;
      width: 70%;
      padding: 40px;
      float: left;
    }

    form {
      background-color: rgb(0,0,0); /* Fallback color */
      background-color: rgba(0,0,0, 0.4); /* Black w/opacity/see-through */
      color: white;
      font-weight: bold;
      border: 3px solid #f1f1f1;
      z-index: 2;
      width: 40%;
      padding: 40px;
      float: left;
    }
    </style>
        <center><h1>EVENT MANAGER</h1></center>
    </head>
    <body>
    <div>
      <div style="width: 100%">
        <img src="/static/PP3.jpeg" style="float:right;" width="750" height="650">
      </div>
      <div >
        <form>
        <h2>Invitations Received</h2>  
        """
    for i in range(len(names)):
            # aman += "<div class= 'lalala'>" + "Event_Name: " + names[i] + "</br>" + dates[i] + "</br>" + locations[i] + "</br>" + types[i] + "</br>" + details[i] + "</br>" + orgzzz[i] + "</br>" + "<a href='/invites'>Send Invitation</a>""</div>"
            aman += "<div class= 'lalala'>" + "Event_Name: " + names[i] + "</br>" + dates[i] + "</br>" + locations[i]
            aman += "</br>" + types[i] + "</br>" + details[i] + "</br>" + orgzzz[i] + "</br>"
            aman += "<a href='/accept?ev_name="+ names[i] +"'>Accept invitation</a></br>"
            aman += "<a href='/decline?ev_name=" + names[i] + "'>Decline invitation</a></div>"
    aman += """
        <input type="submit" value="Go to Profile" formaction = "/Profile">
        </div>


      </form>
    </div>
    </body>
    </html>
        """
    return aman

@app.route('/accept')
def accept_invite():
    cursor.execute("Select email from currentemail;")
    recemail = cursor.fetchone()
    recemail = str(recemail[0])

    ev = request.args.get('ev_name', None)
    print("accepted " + str(ev) + " invitation!!!")

    query = "select * from events where name='" + ev + "';"
    # query = "select ev.event_id, ev.event_name, ev.event_type, ev.location, ev.date_time from Event ev join Feed fd on ev.event_id = fd.event_id where fd.user_email = %s;"
    cursor.execute(query)
    # ev_data = str(cursor.fetchall())

    names = []
    types = []
    locations = []
    dates = []
    details = []
    orgzzz = []
    for (event_name, event_date, location, event_type, detail, organizer) in cursor:
        names.append(event_name)
        types.append(event_type)
        locations.append(location)
        dates.append(event_date)
        details.append(detail)
        orgzzz.append(organizer)

    cursor.execute("INSERT INTO events (name, date, location, type, details, organizer) values ('" + names[0] + "', '" + dates[0] + "', '" + locations[0] + "', '" + types[0] + "', '" + details[0] + "', '" + recemail + "');")
    cnx.commit()

    cursor.execute("Delete from invitation where event_name='" + ev + "' and email='" + recemail + "';")
    cnx.commit()

    return recinvite()

@app.route('/decline')
def decline_invite():
    cursor.execute("Select email from currentemail;")
    recemail = cursor.fetchone()
    recemail = str(recemail[0])

    ev = request.args.get('ev_name', None)
    print("declined " + str(ev) + " invitation!!!")
    cursor.execute("Delete from invitation where event_name='" + ev + "' and email='"+ recemail +"';")
    cnx.commit()
    return recinvite()



  
  
  
  
  
  
  
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
