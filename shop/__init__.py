import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SUBJECT_PREFIX'] = '[Happy Shopping] '
app.config['MAIL_SENDER'] = 'Admin <nikitadasmsd@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')

mail=Mail(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
moment = Moment(app)

login_manager = LoginManager(app)
login_manager.login_view = 'customer_login'
login_manager.login_message_category =  'danger'



from shop.admin import routes
from shop.products import routes

from shop.customers import routes
from shop.main import routes