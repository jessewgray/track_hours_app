from flask import (Flask, render_template, jsonify, request, flash, redirect, session, abort)
import mysql.connector
import os

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
    
#login route which sends you back to home when logged in
@app.route('/login', methods=['POST'])
def doAdminLogin():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else: 
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



#this route has a form to add user data
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    
    return render_template('addUser.html')



#this route posts the data from the form as json
@app.route('/postdata', methods=['GET', 'POST'])
def postData():
    
    params = {
        "personId": request.form['personId'],
        "lastName": request.form['lastName'],
        "firstName": request.form['firstName'],
        "address": request.form['address'],
        "city": request.form['city'],
        "rate": request.form['rate'],
        "regHours": request.form['regHours']
    }

    thePersonId = request.form['personId']
    theLastName = str(request.form['lastName'])
    theFirstName = str(request.form['firstName'])
    theAddress = str(request.form['address'])
    theCity =   str(request.form['city'])
    theRate = str(request.form['rate'])
    regHours = request.form['regHours']

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
    
    mycursor = cnx.cursor()

    insertStatement = ('INSERT INTO hours_flaskapp.users (PersonId, LastName, FirstName, Address, City, Rate, RegHours) VALUES (%s, %s, %s, %s, %s, %s, %s)')
    insertData = (thePersonId, theLastName, theFirstName, theAddress, theCity, theRate, regHours)

    mycursor.execute(insertStatement, insertData)
    cnx.commit()

    jsonParams = jsonify(params)

    #print(thePersonId)



    return jsonParams;


#this route pulls data from the db and shows as json
@app.route('/userlist', methods=['GET'])
def getUserList():

	cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
	
	mycursor = cnx.cursor()
	mycursor.execute("SELECT * From hours_flaskapp.users ORDER BY LastName")
	myresult = mycursor.fetchall()

	userList = []
	content = {}

	for x in myresult:
		print(x)
		content = {'PersonId': x[0], 'LastName': x[1], 'FirstName': x[2], 'Address': x[3], 'City': x[4], 'Rate': x[5], 'RegHours': x[6]}
		userList.append(content)
		content = {}
	
	cnx.close()

	return jsonify(userList)
	#return render_template('home.html')



#this route will accept userName and return data
@app.route('/userdata/<username>', methods=['GET'])
def getUserData(username):

    nUsername = username.capitalize()
    newUsername = str(nUsername.strip())
    print(newUsername)

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
    
    selectStatement = ("SELECT * FROM hours_flaskapp.Users WHERE FirstName = %(value)s")
    selectParam = {'value': newUsername}


    mycursor = cnx.cursor()
    mycursor.execute(selectStatement, selectParam)
    myresult = mycursor.fetchall()

    userList = []
    content = {}

    for x in myresult:
        print(x)
        content = {'PersonId': x[0], 'LastName': x[1], 'FirstName': x[2], 'Address': x[3], 'City': x[4], 'Rate': x[5], 'RegHours': x[6]}
        userList.append(content)
        content = {}
    
    cnx.close()

    return jsonify(userList)


#this route you can select user from dropdown and get user data return
@app.route('/selectuser', methods=['GET'])
def getSelectUserData():

    return render_template('selectUser.html')



#this route you will select user, add your hours and post
@app.route('/addweekhours', methods=['GET', 'POST'])
def addWeekHours():

    return render_template('addWeekHours.html')


#this route you will post user hours
@app.route('/postweekhours', methods=['POST'])
def postHours():

    name = str(request.form['name'])
    lName = str(request.form['lName'])
    fName = str(request.form['fName'])
    rate = float(request.form['rate'])
    otRate = float((rate / 2) + rate)
    regHours = float(request.form['regHours'])
    fromDate = str(request.form['fromDate'])
    toDate = str(request.form['toDate'])
    personId = str(request.form['personId'])
    mondayInHour = float(request.form['mondayInHour'])
    mondayInMin = float(request.form['mondayInMin'])
    mondayInAmPm = str(request.form['mondayInAmPm'])
    mondayOutHour = float(request.form['mondayOutHour'])
    mondayOutMin = float(request.form['mondayOutMin'])
    mondayOutAmPm = str(request.form['mondayOutAmPm'])
    if mondayInAmPm == 'off' or mondayOutAmPm == 'off':
        monday = 0
    else:
        if mondayInAmPm == 'pm':
            mondayIn = mondayInHour + 12 + mondayInMin
        else:
            mondayIn = mondayInHour + mondayInMin
        if mondayOutAmPm == 'pm':
            mondayOut = mondayOutHour + 12 + mondayOutMin
        else:
            mondayOut = mondayOutHour + mondayOutMin
        monday = mondayOut - mondayIn
    tuesdayInHour = float(request.form['tuesdayInHour'])
    tuesdayInMin = float(request.form['tuesdayInMin'])
    tuesdayInAmPm = str(request.form['tuesdayInAmPm'])
    tuesdayOutHour = float(request.form['tuesdayOutHour'])
    tuesdayOutMin = float(request.form['tuesdayOutMin'])
    tuesdayOutAmPm = str(request.form['tuesdayOutAmPm'])
    if tuesdayInAmPm == 'off' or tuesdayOutAmPm == 'off':
        tuesday = 0
    else:
        if tuesdayInAmPm == 'pm':
            tuesdayIn = tuesdayInHour + 12 + tuesdayInMin
        else:
            tuesdayIn = tuesdayInHour + tuesdayInMin
        if tuesdayOutAmPm == 'pm':
            tuesdayOut = tuesdayOutHour + 12 + tuesdayOutMin
        else:
            tuesdayOut = tuesdayOutHour + tuesdayOutMin
        tuesday = tuesdayOut - tuesdayIn
    wednesdayInHour = float(request.form['wednesdayInHour'])
    wednesdayInMin = float(request.form['wednesdayInMin'])
    wednesdayInAmPm = str(request.form['wednesdayInAmPm'])
    wednesdayOutHour = float(request.form['wednesdayOutHour'])
    wednesdayOutMin = float(request.form['wednesdayOutMin'])
    wednesdayOutAmPm = str(request.form['wednesdayOutAmPm'])
    if wednesdayInAmPm == 'off' or wednesdayOutAmPm == 'off':
        wednesday = 0
    else:
        if wednesdayInAmPm == 'pm':
            wednesdayIn = wednesdayInHour + 12 + wednesdayInMin
        else:
            wednesdayIn = wednesdayInHour + wednesdayInMin
        if wednesdayOutAmPm == 'pm':
            wednesdayOut = wednesdayOutHour + 12 + wednesdayOutMin
        else:
            wednesdayOut = wednesdayOutHour + wednesdayOutMin
        wednesday = wednesdayOut - wednesdayIn
    thursdayInHour = float(request.form['thursdayInHour'])
    thursdayInMin = float(request.form['thursdayInMin'])
    thursdayInAmPm = str(request.form['thursdayInAmPm'])
    thursdayOutHour = float(request.form['thursdayOutHour'])
    thursdayOutMin = float(request.form['thursdayOutMin'])
    thursdayOutAmPm = str(request.form['thursdayOutAmPm'])
    if thursdayInAmPm == 'off' or thursdayOutAmPm == 'off':
        thursday = 0
    else:
        if thursdayInAmPm == 'pm':
            thursdayIn = thursdayInHour + 12 + thursdayInMin
        else:
            thursdayIn = thursdayInHour + thursdayInMin
        if thursdayOutAmPm == 'pm':
            thursdayOut = thursdayOutHour + 12 + thursdayOutMin
        else:
            thursdayOut = thursdayOutHour + thursdayOutMin
        thursday = thursdayOut - thursdayIn
    fridayInHour = float(request.form['fridayInHour'])
    fridayInMin = float(request.form['fridayInMin'])
    fridayInAmPm = str(request.form['fridayInAmPm'])
    fridayOutHour = float(request.form['fridayOutHour'])
    fridayOutMin = float(request.form['fridayOutMin'])
    fridayOutAmPm = str(request.form['fridayOutAmPm'])
    if fridayInAmPm == 'off' or fridayOutAmPm == 'off':
        friday = 0
    else:
        if fridayInAmPm == 'pm':
            fridayIn = fridayInHour + 12 + fridayInMin
        else:
            fridayIn = fridayInHour + fridayInMin
        if fridayOutAmPm == 'pm':
            fridayOut = fridayOutHour + 12 + fridayOutMin
        else:
            fridayOut = fridayOutHour + fridayOutMin
        friday = fridayOut - fridayIn
    saturdayInHour = float(request.form['saturdayInHour'])
    saturdayInMin = float(request.form['saturdayInMin'])
    saturdayInAmPm = str(request.form['saturdayInAmPm'])
    saturdayOutHour = float(request.form['saturdayOutHour'])
    saturdayOutMin = float(request.form['saturdayOutMin'])
    saturdayOutAmPm = str(request.form['saturdayOutAmPm'])
    if saturdayInAmPm == 'off' or saturdayOutAmPm == 'off':
        saturday = 0
    else:
        if saturdayInAmPm == 'pm':
            saturdayIn = saturdayInHour + 12 + saturdayInMin
        else:
            saturdayIn = saturdayInHour + saturdayInMin
        if saturdayOutAmPm == 'pm':
            saturdayOut = saturdayOutHour + 12 + saturdayOutMin
        else:
            saturdayOut = saturdayOutHour + saturdayOutMin
        saturday = saturdayOut - saturdayIn
    sundayInHour = float(request.form['sundayInHour'])
    sundayInMin = float(request.form['sundayInMin'])
    sundayInAmPm = str(request.form['sundayInAmPm'])
    sundayOutHour = float(request.form['sundayOutHour'])
    sundayOutMin = float(request.form['sundayOutMin'])
    sundayOutAmPm = str(request.form['sundayOutAmPm'])
    if sundayInAmPm == 'off' or sundayOutAmPm == 'off':
        sunday = 0
    else:
        if sundayInAmPm == 'pm':
            sundayIn = sundayInHour + 12 + sundayInMin
        else:
            sundayIn = sundayInHour + sundayInMin
        if sundayOutAmPm == 'pm':
            sundayOut = sundayOutHour + 12 + sundayOutMin
        else:
            sundayOut = sundayOutHour + sundayOutMin
        sunday = sundayOut - sundayIn
    totHours = float(monday + tuesday + wednesday + thursday + friday + saturday + sunday)
    

    if totHours > regHours:
        
        otHours = totHours - regHours
    else:
        regHours = totHours
        otHours = 0   
    
    regPay = regHours * rate 
    otPay =  otHours * otRate
    totPay = regPay + otPay


    params = {
        'lName': lName,
        "fName": fName,
        "rate": rate,
        "otRate": otRate,
        "regHours": regHours,
        "fromDate": fromDate,
        "toDate": toDate,
        "personId": personId,
        "monday": monday,
        "tuesday": tuesday,
        "wednesday": wednesday,
        "thursday": thursday,
        "friday": friday,
        "saturday": saturday,
        "sunday": sunday,
        "totHours": totHours,
        "regHours": regHours,
        "otHours": otHours,
        "regPay": regPay,
        "otPay": otPay,
        "totPay": totPay 
    }

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
    
    mycursor = cnx.cursor()

    insertStatement = ('INSERT INTO hours_flaskapp.hours (FromDate, ToDate, PersonId, LastName, FirstName, Mon, Tue, Wed, Thu, Fri, Sat, Sun, TotHours, RegHours, OtHours, RegPay, OtPay, TotPay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    insertData = (fromDate, toDate, personId, lName, fName, monday, tuesday, wednesday, thursday, friday, saturday, sunday, totHours, regHours, otHours, regPay, otPay, totPay)

    mycursor.execute(insertStatement, insertData)
    cnx.commit()



    print(params)

    return jsonify(params)



#this route will show json of joined tables for user hours
@app.route('/showuserhours/<username>', methods=['GET'])
def showUserHours(username):

    nUsername = username.capitalize()
    newUsername = str(nUsername.strip())
    print(newUsername)


    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
    
    selectStatement = ("SELECT hours_flaskapp.hours.FromDate, hours_flaskapp.hours.ToDate, hours_flaskapp.users.PersonID, hours_flaskapp.users.LastName, hours_flaskapp.users.FirstName, hours_flaskapp.users.Rate, hours_flaskapp.hours.TotHours, hours_flaskapp.hours.RegHours, hours_flaskapp.hours.OtHours, hours_flaskapp.hours.RegPay, hours_flaskapp.hours.OtPay, hours_flaskapp.hours.TotPay FROM hours_flaskapp.users RIGHT JOIN hours_flaskapp.hours ON hours_flaskapp.hours.PersonId = hours_flaskapp.users.PersonID WHERE hours_flaskapp.users.FirstName = %(value)s")
    selectParam = {'value': newUsername}


    mycursor = cnx.cursor()
    mycursor.execute(selectStatement, selectParam)
    myresult = mycursor.fetchall()

    userHours = []
    content = {}

    for x in myresult:
        print(x)
        content = {'FromDate': x[0], 'ToDate': x[1], 'PersonID': x[2], 'LastName': x[3], 'FirstName': x[4], 'Rate': x[5], 'TotHours': x[6], 'RegHours': x[7], 'OtHours': x[8], 'RegPay': x[9], 'OtPay': x[10], 'TotPay': x[11]}
        userHours.append(content)
        content = {}
    
    cnx.close()

    return jsonify(userHours)



#this route will allow you to select user to drop
@app.route('/dropuser', methods=['GET'])
def dropUser():

    return render_template('dropUser.html')


#this route will post dropped user and user hours
@app.route('/dropuserbyid', methods=['GET', 'POST'])
def showDropUser():

    userId = str(request.form['userId'])
    fName = str(request.form['fName'])
    lName = str(request.form['lName'])

    params = {
        'User ID': userId,
        'First Name': fName,
        'Last Name': lName
    }

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="hours_flaskapp")
    
    mycursor = cnx.cursor()

    dropUserStatement = ('DELETE FROM hours_flaskapp.users WHERE PersonID = "%s";' % userId)
    dropUserHoursStatement = ('DELETE FROM hours_flaskapp.hours WHERE PersonID = "%s";' % userId)

    mycursor.execute(dropUserStatement)
    mycursor.execute(dropUserHoursStatement)
    cnx.commit()

    
    return jsonify(params)
    #return render_template('dropUser.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, ssl_context='adhoc')