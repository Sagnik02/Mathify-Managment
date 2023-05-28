from flask import Flask,request, render_template,redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html',name="Sagnik")

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   #CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
   CONNECTION_STRING ="localhost" # this is the ip address
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING,27017)   #27017 is the port number

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['Mathify']


@app.route('/users')
def user_page():
    db_name=get_database()
    user_collection = db_name['user']
    user_details = user_collection.find()
    users = []
    for user in user_details:
        user_dict = {
            '_id':user['_id'],
            'name': user['name'],
            'roll_no': user['roll_no'],
            'email_id':user['email_id'],
            'phone_number': user['phone_number'],
            'attendance_cnt': user['attendance_cnt']
        }
        
        users.append(user_dict)
    return render_template('users.html', users=users)

@app.route('/notice')
def notice_page():
    db_name=get_database()
    notice_collection = db_name['notice']
    notice_details = notice_collection.find()
    notices = []
    for notice in notice_details:
        notice_dict = {
            'notice_name': notice['notice_name'],
            'notice_date': notice['notice_date'],
            'notice_body': notice['notice_body']
          
        }
        notices.append(notice_dict)
    return render_template('notice.html',notices=notices)

@app.route('/increase_attendance', methods=['POST'])
def increase_attendance():
    db_name = get_database()
    user_collection = db_name['user']
    user_id = request.form['user_id']
    user = user_collection .find_one({'_id':ObjectId(user_id)})
    if user:
        attendance_cnt = user.get('attendance_cnt', 0)
        new_cnt = attendance_cnt + 1
        user_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'attendance_cnt': new_cnt}})
    
    return redirect(url_for('user_page'))

@app.route('/register') 
def register_page():
        return render_template('register.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    db_name=get_database()
    user_collection = db_name['user']
    name = request.form['name']
    roll_no = request.form['roll_no']
    email_id = request.form['email_id']
    phone_number = request.form['phone_number']
    user_id = {'name': name, 'roll_no': roll_no, 'email_id': email_id,'phone_number': phone_number,'attendance_cnt':0}
    user_collection .insert_one(user_id)
    return redirect(url_for('register_page'))

@app.route('/display')
def display_page():
    db_name=get_database()
    user_collection = db_name['user']
    user_details = user_collection.find()
    users = []
    for user in user_details:
        user_dict = {
            'name': user['name'],
            'roll_no': user['roll_no'],
            'email_id':user['email_id'],
            'phone_number': user['phone_number'],
            'attendance_cnt': user['attendance_cnt']
        }
        
        users.append(user_dict)
    return render_template('display.html', users=users)

@app.route('/classdisplay')
def class_page():
    db_name=get_database()
    class_collection = db_name['classtiming']
    class_details = class_collection.find()
    classes = []
    for class_det in class_details:
        class_dict={
            'class_topic':class_det['class_topic'],
            'class_date':class_det['class_date'],
            'class_duration':class_det['class_duration'],
            'prerequisite':class_det['prerequisite']
        }

        classes.append(class_dict)
       
    return render_template('classdisplay.html', classes =classes )

app.run(host='0.0.0.0', port=8080)

