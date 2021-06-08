
from flask import session , render_template
from flask import jsonify ,url_for,Blueprint,abort, flash, redirect , send_file ,request


## importing classes from models file
from models import db
from models import User 
from models import Admin



from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from datetime import datetime , timedelta
import os 



from functools import wraps 



	
def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
    	
    	admin = Admin.query.filter_by(username='admin').first()


    	try:

    		if session['usr'] == 'admin':
    			return func(*args, **kwargs)
    		else:
    			return redirect(url_for('UI.panel'))
    	
    	except KeyError as ke:
    		return redirect(url_for('UI.panel'))


    return wrapper





UI = Blueprint('UI', __name__ )



### login page for admin 

@UI.route('/admin' , methods=['GET','POST'])
def panel():
	''' check for admin  '''


	admin_usr = Admin.query.filter_by(username='admin').first()
	if request.method == "POST":

		

		password = request.form.get('password')
		check_password_hash(admin_usr.password , password )
		if not check_password_hash(admin_usr.password , password ) :

			flash("Wrong user name ")
			return render_template ('admin_login.html')

		else:
			session['usr'] = 'admin'
			return redirect(url_for('webui.home'))

	else:
		return render_template('admin_login.html')







### login in as admin to be able to change any user username , text , email , status 
@UI.route('/admin_edit/<id>', methods=['GET','POST'] )
@require_admin
def edit(id):
	''' edit user info '''

	usr = User.query.get(id)

	if request.method == 'POST':
		if request.form['username']:
			usr.username = request.form['username']
			

			 
		if request.form['email']:
			usr.email =  request.form['email']
			
		if request.form['text']:
			usr.text = request.form['text']

		if request.form['status']:
			usr.status = request.form['status']
			
		db.session.commit()
		
		return redirect(url_for('webui.home'))

	else:

		return render_template('edit.html')