import os
from flask import Flask,render_template, request, redirect,flash, jsonify, url_for
import json
from flask_mail import Mail, Message
import pymysql



app = Flask(__name__)


connection = pymysql.connect(host='mydatabase.cccssd5sqciz.ca-central-1.rds.amazonaws.com',
                            user=os.environ.get('user'),
                            password=os.environ.get('pass'),
                            db='SALON',
                            )

app.secret_key = "its_secure"




@app.route('/', methods=["GET", "POST"])
def index():
    
     if request.method=="POST":
        
        username = request.form['username'] + " " + request.form['password']
        print(username)
        return redirect(url_for('bookings'))
     return render_template("index.html", title = "Index Page")



        
@app.route('/bookings')
def bookings():
    try:
     
     result=""
     with connection.cursor(pymysql.cursors.DictCursor) as cursor:
          sql = """ SELECT BOOKINGS.BOOKING_ID, SERVICES.SERVICE_NAME, CUSTOMERS.CUSTOMER_NAME, 
          CUSTOMERS.CUSTOMER_EMAIL, CUSTOMERS.CUSTOMER_TELEPHONE,BOOKINGS.DATE, BOOKINGS.TIME FROM BOOKINGS 
          INNER JOIN CUSTOMERS ON BOOKINGS.CUSTOMER_ID = CUSTOMERS.CUSTOMER_ID
          INNER JOIN SERVICES ON BOOKINGS.SERVICE_ID = SERVICES.SERVICE_ID; """
          cursor.execute(sql)
          result = cursor.fetchall()
          connection.commit()
     cursor.close()
     print(result)
    finally:
     return render_template("bookings.html", title = "Bookings", booking_data=result)  
       
       
       
       
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=False)
    