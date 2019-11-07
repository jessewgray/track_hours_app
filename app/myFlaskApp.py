from flask import (
    Flask,
    render_template,
    jsonify,
    request
)
import mysql.connector

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


#this route can display data from the api in html
@app.route('/getdata')
def getData():
   
    return render_template('getData.html')



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
        "rate": request.form['rate']

    }

    thePersonId = request.form['personId']
    theLastName = str(request.form['lastName'])
    theFirstName = str(request.form['firstName'])
    theAddress = str(request.form['address'])
    theCity =   str(request.form['city'])
    theRate = str(request.form['rate'])

    cnx = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="flaskapp")
    
    mycursor = cnx.cursor()

    insertStatement = ('INSERT INTO flaskapp.Users (PersonId, LastName, FirstName, Address, City, Rate) VALUES (%s, %s, %s, %s, %s, %s)')
    insertData = (thePersonId, theLastName, theFirstName, theAddress, theCity, theRate)

    mycursor.execute(insertStatement, insertData)
    cnx.commit()

    jsonParams = jsonify(params)

    #print(thePersonId)



    return jsonParams;


#this route pulls data from the db and shows as json
@app.route('/userlist', methods=['GET'])
def getUserList():

	cnx = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="flaskapp")
	
	mycursor = cnx.cursor()
	mycursor.execute("SELECT * From flaskapp.Users")
	myresult = mycursor.fetchall()

	userList = []
	content = {}

	for x in myresult:
		print(x)
		content = {'PersonId': x[0], 'LastName': x[1], 'FirstName': x[2], 'Address': x[3], 'City': x[4], 'Rate': x[5]}
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

    cnx = mysql.connector.connect(user="root", password="root", host="127.0.0.1", database="flaskapp")
    
    selectStatement = ("SELECT * FROM flaskapp.Users WHERE FirstName = %(value)s")
    selectParam = {'value': newUsername}


    mycursor = cnx.cursor()
    mycursor.execute(selectStatement, selectParam)
    myresult = mycursor.fetchall()

    userList = []
    content = {}

    for x in myresult:
        print(x)
        content = {'PersonId': x[0], 'LastName': x[1], 'FirstName': x[2], 'Address': x[3], 'City': x[4], 'Rate': x[5]}
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



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)