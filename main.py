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
        global cemail
        global cname
        global cpassword
        global clocation
        try:
            cursor.execute("Select password from signup where email = '" + emailid + "' ;")
            userss = cursor.fetchone()
            if str(userss[0]) == passwordd:
                cursor.execute("DELETE FROM currentemail;")
                cnx.commit()
                cursor.execute("Select email from signup where email = '" + emailid + "' ;")
                cemail = cursor.fetchone()
                cursor.execute("Select name from signup where email = '" + emailid + "' ;")
                cname = cursor.fetchone()
                cursor.execute("Select password from signup where email = '" + emailid + "' ;")
                cpassword = cursor.fetchone()
                cursor.execute("Select location from signup where email = '" + emailid + "' ;")
                clocation = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO currentemail (email, name, password, location) values ('" + cemail[0] + "', '" + cname[
                        0] + "', '" + cpassword[0] + "', '" + clocation[0] + "');")
                cnx.commit()

                print ("Done success sign in ")
                return profilee()

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
  <p style="font-size: 20px; text-align: right; padding-right: 40px; background-color: white;"><a href="">.</a></p>
</head>
<body>
<div>
  <div style="width: 100%">
    <img src="/static/PP3.jpeg" style="float:right;" width="750" height="650">
  </div>
  <div >
    <form action="/">
    <h2 >PROFILE</h2>

        """
        returnval += "<fieldset> <legend></legend>"
        returnval += " <label for=\"firstname\">Email:</label></br> <input name=\"firstname\" type=\"text\" value=\"" + ctemail + "\"readonly> </br>"
        returnval += " <label for=\"fullname\">Name:</label></br> <input type=\"text\" id=\"fullname\" name=\"fullname\" value=\"" + ctname + "\"readonly></br>"
        returnval += " <label for=\"location\">City/Location:</label></br> <input type=\"text\" id=\"location\" name=\"locationname\" value=\"" + ctlocation + "\"readonly></br>"
        returnval += "<a href = \"/Log in.html\"><button type=\"submit\"> Sign Out </button></a></br>"

        returnval += "<a href = \"/feed\">Go to feed</a></br>"

        returnval += "<a href = \"/recinvite\">Click here to view Invitations</a>"
        return returnval
        print ("Done sucess profile")
    except:
        print("Error: Data not done;")
        return "Good you signed up! Now go here back for sign-in:  " + "<a href = \"/\">Click here :)</a>"


@app.route('/invites', methods=["GET", "POST"])
def invites():
    if request.method == "POST":
        ev_name = request.args.get('ev_name', None)
        print(ev_name)
        x = request.form.getlist("hi")
        # store data in table
        for k in x:
            cursor.execute("INSERT INTO invitation (event_name, email) values ('" + ev_name + "', '" + k + "');")
            cnx.commit()
        return feed()

    people = "select * from signup"
    cursor.execute(people)

    p_id = []
    p_names = []
    p_email = []
    p_password = []
    p_location = []
    for (pep_id, pep_names, pep_email, pep_password, pep_location) in cursor:
        p_id.append(pep_id)
        p_names.append(pep_names)
        p_email.append(pep_email)
        p_password.append(pep_password)
        p_location.append(pep_location)

    jariwala = """
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
textarea {
  padding-left: 100px;
  font-size: large;
}
body {
  background-color: #ff9999
}
input[type=submit] {
  width: 20%;
  background-color: #000000;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
textarea{
  width: 30%;
  /*padding: 14px 20px;*/
  margin: 15px 0;
  border: none;
  border-radius: 4px;
}

input[type=submit]:hover {
  background-color: #000000;
}

input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 35%;
  background-color: #000000;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #000000;
}

.container {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 22px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
  background-color: #ccc;
}

/* When the checkbox is checked, add a blue background */
.container input:checked ~ .checkmark {
  background-color: #2196F3;
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
</style>
    <center><h1>EVENT MANAGER</h1></center>
  <p style="font-size: 20px; text-align: right; padding-right: 40px; background-color: white;"><a href="/feed">Feed</a></p>
</head>
<body>
<div>
  <div style="width: 100%">
    <img src="/static/PP3.jpeg" style="float:right;" width="750" height="650">
  </div>
  <div >
    <h2 style="font-family:noteworthy;">INVITE</h2>
    <form method="POST">
    """
    for i in range(len(p_email)):
        jariwala += "<label class='container'>" + p_email[i] + "<input type='checkbox' name='hi' value='" + p_email[
            i] + "'><span class='checkmark'></span></label>"

    jariwala += """
            <input type="submit" value="Invite">
    </form>
  </div>
</div>
</body>
</html>
    """
    return jariwala


@app.route('/recinvite')
def recinvite():
    cursor.execute("Select email from currentemail;")
    recemail = cursor.fetchone()
    recemail = str(recemail[0])

    cursor.execute("Select event_name from invitation where email = '" + recemail + "' ;")
    eventsss = cursor.fetchall()

    names = []
    types = []
    locations = []
    dates = []
    details = []
    orgzzz = []
    for event in eventsss:
        query = "select * from events where name='" + event[0] + "';"
        cursor.execute(query)

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
        aman += "<div class= 'lalala'>" + "Event_Name: " + names[i] + "</br>" + dates[i] + "</br>" + locations[i]
        aman += "</br>" + types[i] + "</br>" + details[i] + "</br>" + orgzzz[i] + "</br>"
        aman += "<a href='/accept?ev_name=" + names[i] + "'>Accept invitation</a></br>"
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


@app.route('/feed')
def feed():
    query = "select email from currentemail"
    cursor.execute(query)
    email = str(cursor.fetchone()[0])

    query = "select * from events where organizer='" + email + "';"
    cursor.execute(query)

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
    <p style="font-size: 20px; text-align: right; padding-right: 40px; background-color: white;"><a href="/createevent"> Create event </a></p>
</head>
<body>
<div>
  <div style="width: 100%">
    <img src="/static/PP3.jpeg" style="float:right;" width="750" height="650">
  </div>
  <div >
    <form action="/Profile">
    <h2>FEED</h2>  
    """
    for i in range(len(names)):
        aman += "<div class= 'lalala'>" + "Event_Name: " + names[i] + "</br>" + dates[i] + "</br>" + locations[i]
        aman += "</br>" + types[i] + "</br>" + details[i] + "</br>" + orgzzz[i] + "</br>"
        aman += "<a href='/invites?ev_name=" + names[i] + "'>Send Invitation</a>""</div>"
    aman += """
    <input type="submit" value="Go to Profile">
    </div>


  </form>
</div>
</body>
</html>
    """

    return aman


@app.route('/createevent', methods=["GET", "POST"])
def createevent():
    if request.method == "POST":
        event_name = request.form.get("eventname")
        event_date = request.form.get("date")
        event_location = request.form.get("location")
        event_type = request.form.get("type")
        event_details = request.form.get("details")
        event_organizer = request.form.get("organizer")
        print ("createevents")
        try:
            cursor.execute(
                "INSERT INTO events (name, date, location, type, details, organizer) values ('" + event_name + "', '" + event_date + "', '" + event_location + "', '" + event_type + "', '" + event_details + "', '" + event_organizer + "');")
            cnx.commit()
            print ("Done success!")
            return feed()
        except:
            print("Error: Data not done;")
    return render_template("Create event.html")


@app.route('/accept')
def accept_invite():
    cursor.execute("Select email from currentemail;")
    recemail = cursor.fetchone()
    recemail = str(recemail[0])

    ev = request.args.get('ev_name', None)
    print("accepted " + str(ev) + " invitation!!!")

    query = "select * from events where name='" + ev + "';"
    cursor.execute(query)

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

    cursor.execute(
        "INSERT INTO events (name, date, location, type, details, organizer) values ('" + names[0] + "', '" + dates[
            0] + "', '" + locations[0] + "', '" + types[0] + "', '" + details[0] + "', '" + recemail + "');")
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
    cursor.execute("Delete from invitation where event_name='" + ev + "' and email='" + recemail + "';")
    cnx.commit()
    return recinvite()




app.run(debug=True)
print ("dd")
print ("ddddd")
cnx.commit()
cursor.close()
cnx.close()
