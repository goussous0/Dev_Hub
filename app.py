from flask import Flask ,render_template,request ,url_for ,redirect ,send_from_directory
from webui import webui
from UI import UI
from flask_script import Manager
from flask_admin import Admin 
from flask_security import current_user
from werkzeug.security import generate_password_hash



import os 

from models import db 
from models import User
from models import Admin
from config import config







app = Flask(__name__)
app.config.from_object(config['dev'])
app.register_blueprint(webui)
app.register_blueprint(UI)
db.init_app(app)
manager = Manager(app)




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'webui/static'),
                          'logo.ico',mimetype='image/vnd.microsoft.icon')



## a simple header with app name 
@app.after_request
def headers(response):
    response.headers["Server"] = "Devhub"
    return response





@manager.command
def initdb():
    db.drop_all()
    db.create_all()
    admins = db.session.query(Admin).count()
    # remove or edit this section to change admin creds 
    if not admins:
        admin = Admin()
        admin.username = 'admin'
        admin.password = generate_password_hash('123', method='sha256')
        db.session.add(admin)

    
    db.session.commit()

    
if __name__ == '__main__':
    manager.run()
