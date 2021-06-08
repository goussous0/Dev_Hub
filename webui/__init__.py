from flask import Blueprint ,render_template, request, url_for ,abort, flash, redirect , send_file ,make_response
from flask import session
from flask import jsonify 



from models import db
from models import User 


from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from flask import current_app

from werkzeug.security import generate_password_hash, check_password_hash

from config import config


from functools import wraps

import jwt
import re 
import random 
import string 
from datetime import datetime , timedelta
import os 




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({"status": "error","message": {"token": "Токен истёк"}}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({"status": "error","message": {"token": "Токен истёк"}}), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated








webui = Blueprint('webui', __name__, static_folder='static', static_url_path='/static/webui', template_folder='templates')



@webui.route('/home' , methods=['GET'])
def home():


    all_users = User.query.all()

    return render_template('Home.html', all_users=all_users )


    





@webui.route('/signup', methods=['POST', 'GET'])
def signup():


    if request.method == 'POST':


        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            return render_template('login.html')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, username=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for('webui.login'))
    else:
        return render_template('signup.html')

    






@webui.route('/login', methods=['GET' , 'POST'])
def login():



    if request.method == "POST":


        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        password = request.form.get('password')


        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')

            return render_template('login.html') 
        else:


            session['username'] = user.username
 

            token = jwt.encode({'username': user.username , 'exp' : datetime.utcnow() + timedelta(minutes=1440)}, current_app.config['SECRET_KEY'])  



            return make_response(jsonify({'token' : token}), 201)



        return render_template('login.html')


    else:
        return render_template('login.html')












@webui.route('/create', methods=['POST'])
def create( ):
    ## task a user name , email , text 


    mail_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

    error_data  = {
        "status": "error",
        "message": {
            "username": "Поле является обязательным для заполнения",
            "email": "Неверный email",
            "text": "Поле является обязательным для заполнения"
        }
    }


    get_error = {
        "status": "error",
        "message": "Не передано имя разработчика"
    }


    if request.method == 'POST':
        ## continue
        usrname = request.args.get('username')
        email = request.args.get('email')
        text = request.args.get('text')

        usr = User.query.filter_by(email=email).first()

        if usr:

            usr.text = text 
            db.session.commit()
            data = {
            "status": "ok",
            "message": {
                "id": f"{usr.id}",
                "username": f"{usr.username}",
                "email": f"{usr.email}",
                "text": f"{usr.text}",
                "status": 0
                }
            }

            return jsonify(data)

       


        if bool(re.match(mail_regex , email )) == True and usrname != "" and text != "" :
            n3w = User() 
            n3w.name = usrname
            n3w.email = email
            n3w.text  = text 

            db.session.add(n3w)
            db.session.commit()

            data = {
            "status": "ok",
            "message": {
                "id": f"{n3w.id}",
                "username": f"{n3w.username}",
                "email": f"{n3w.email}",
                "text": f"{n3w.text}",
                "status": 0
                }
            }

            return jsonify(data)

        elif bool(re.match(mail_regex , email )) == False or request.args.get('username') is None  or request.args.get('text') is None : 
            return jsonify(error_data)

        else:   

            return jsonify(error_data)

    else:

        return jsonify(get_data)





## this is used for editing the task 

@webui.route('/update/<id>', methods=['POST'])
@token_required
def update(id):
    user = User.query.get(id)
 

    
    text = request.args.get('text')
    status = request.args.get('status')


    ## if user is in the database and the token is valid then edit the text and the status 
    if user:

        

        user.text = request.args['text']
        user.status = request.args['status']
        
        db.session.commit()

        success = {
            "status" : "ok"
        }
        return jsonify(success)

    
    
    















@webui.route('/text', methods=['GET','POST'])
def text():


    
    
    if session:
        usrname = session['username']
        usr = User.query.filter_by(username=usrname).first()

        if request.method == "POST":
		  ## GET THE TEXT FROM THE USER
            TEXT =request.form.get('text')
            usr.text = TEXT
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for('webui.home'))
        else:
            render_template('add_text.html')

    else:
        render_template('add_text.html')

    return render_template('add_text.html')




    







