from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Api, reqparse
from flask_jwt import JWT
from flask_mail import Mail
from flask_mail import Message
import flask_login

from security import authenticate, identity

from models.user import UserModel
from resources.media import Media, MediaList
import web_scraper
import time

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'vikrumn.flaskapp@gmail.com',
    MAIL_PASSWORD = 'flaskapppass',
    DEFAULT_MAIL_SENDER = 'vikrumn.flaskapp@gmail.com'
))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost:5432/postgres' # can be mysql, postgresql, others
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
app.secret_key = 'vik'
api = Api(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.before_first_request
def create_tables():
	db.create_all()

@login_manager.user_loader
def load_user(user_id):
	user = UserModel.find_by_id(user_id)
	if user:
		return user
	return None
	
jwt = JWT(app, authenticate, identity) #creates new endpoint, /auth
#api.add_resource(UserRegister, '/register')
#api.add_resource(User, '/users/<string:username>')
api.add_resource(Media, '/media/<string:title>')
api.add_resource(MediaList, '/title_list')

@app.route('/', methods = ["GET", "POST"])
def home():
	return render_template('index.html')

@app.route('/register', methods = ["POST"])
def register_new_user():
	parser = reqparse.RequestParser()
	parser.add_argument('username', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('password', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	data = parser.parse_args()

	if UserModel.find_by_username(data['username']):
		return jsonify({"message" : "A user with that username already exists"}, 400)

	user = UserModel(**data)
	user.save_to_db()
	return jsonify({"message" : "User created successfully."}), 201

@app.route('/register', methods = ["GET"])
def register():
	return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    username = request.form['username']
    password = request.form['password']
    user = UserModel.find_by_username(username)

    if user.password == password:
        flask_login.login_user(user)
        return redirect(url_for('add_media'))
    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + str(flask_login.current_user.id)

@app.route('/add_media')
@flask_login.login_required
def add_media():
    return render_template('add_media.html', username = flask_login.current_user.username, password = flask_login.current_user.password)

@app.route("/imdb_search", methods = ['POST'])
@flask_login.login_required
def search_title():
	parser = reqparse.RequestParser()
	parser.add_argument('title', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	data = parser.parse_args()
	results_list = web_scraper.search_imdb(data['title'])
	presented_list = results_list[:]
	for i in range(len(results_list)):
		presented_list[i] = results_list[i].split(" aka ")[0]
		results_list[i] = results_list[i].replace("\"", '`')
	
	return jsonify({"results_list" : results_list, "presented_list" : presented_list}), 200

@app.route("/scrape_services", methods = ['POST'])
@flask_login.login_required
def scrape_services():
	parser = reqparse.RequestParser()
	parser.add_argument('media_title', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	data = parser.parse_args()
	title = data['media_title']
	scrape_list = [title]
	words = title.split(" ")
	if 'aka' in words:
		parsed_title = ' '.join(words[:words.index('aka')])
		scrape_list.append(parsed_title)
		parsed_title = ' '.join(words[words.index('aka') + 1:])
		scrape_list.append(parsed_title[1:-2])
	if '(' in title:
		scrape_list.append(title[:title.index('(')])
	found = False
	on_netflix = False
	print(scrape_list)
	for elem in scrape_list:
		#print(elem == "Rogue One: A Star Wars story")
		#print(scrape_netflix(elem))
		found = found or web_scraper.scrape_netflix(elem)
		if found:
			on_netflix = True
			break
		print("iterating")
		time.sleep(10)
	return jsonify({"on_netflix": on_netflix, "media_title" : title})

@app.route('/email', methods = ['POST'])
@flask_login.login_required
def send_mail():
	parser = reqparse.RequestParser()
	parser.add_argument('media_title', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('email', 
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	data = parser.parse_args()
	title = data['media_title'].replace('`', '\"')
	msg = Message(title + ' is on netflix', sender = "vikrumn.flaskapp@gmail.com", recipients=[data['email']])
	mail.send(msg)

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug = True)
