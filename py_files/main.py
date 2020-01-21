from functools import wraps
from flask import Flask, session
from flask import render_template, request, session, redirect, url_for
from logger import info_log, error_log
import json
from requirements import Requirements
from user import User
from owned import Owned
from datetime import timedelta
from rating import Rating
from game import Game
from comment import Comment
from game_categories import Category
app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
SECURITY_PASSWORD_SALT = '35586E9D-C04C-53FA-CFA9D3CFB9727A28'

@app.before_first_request
def function_to_run_only_once():
	session["USERNAME"] = None
	session["logged_in"] = None
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

def require_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not session['logged_in']:
			return redirect('/login')
		return func(*args, **kwargs)

	return wrapper


def require_admin(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		user = User.find_by_username(session["USERNAME"])
		if not user.admin:
			return redirect('/')
		return func(*args, **kwargs)

	return wrapper


@app.route('/')
def start():
	return redirect("/main")


@app.route("/login", methods=["GET", "POST"])
def sign_in():

	if request.method == "POST":
		error = ''
		req = request.form

		username = req.get("username")
		password = req.get("password")
		user = User.find_by_username(username)
		if not user or not user.verify_password(password):
			error_log.error("Login failed for %s!" % username)
			error = "Invalid username or password!"
			return render_template("login.html", error=error)

		else:
			session["logged_in"] = True
			session["USERNAME"] = username
			info_log.info("%s logged in successfully." % username)
			return redirect('/')
	error = ''
	return render_template("login.html", error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':
		user = User.find_by_username(request.form['username'])
		if user:
			username_error = "Username already in use!"
		else:
			username_error = ''
		if len(request.form["password"]) < 8:
			len_error = "Password must be at least 8 symbols"
			pass_len = 1
		else:
			len_error = ''
			pass_len = 0
		if request.form['password'] != request.form['confirm-password']:
			match_error = "Passwords must match!"
			match = 1
		else:
			match_error = ''
			match = 0
		if not user and not pass_len == 1 and not match == 1:
			values = (
				None,
				request.form['username'],
				User.hash_password(request.form['password']),
				0
			)
			User(*values).create()
			info_log.info(" User %s registred successfully." %
						  request.form['username'])

			return redirect('/')
		else:
			error_log.error("Registration failed!")
			return render_template('register.html', username_error=username_error, len_error=len_error, match_error=match_error, username=request.form['username'], password=request.form['password'])


@app.route('/games/sort_by_rating')
def sort_by_rating():
	return render_template("games.html", games=Game.sort_by_rating())


@app.route('/games/sort_by_alp')
def sort_by_alp():
	return render_template("games.html", games=Game.sort_by_alp())


@app.route('/games/newest')
def sort_by_newest():
	return render_template("games.html", games=Game.sort_by_newest())


@app.route('/main')
def main_page():
	if User.find_by_username(session["USERNAME"]):
		user = 1
	else:
		user = 0
	return render_template("main.html", user = user, username = session["USERNAME"])


@app.route('/profile')
@require_login
def view_profile():

	user = User.find_by_username(session["USERNAME"])

	return render_template("user_profile.html", user=user, games=Game.owned_by_user(user.id), username = session["USERNAME"])
	

@app.route('/logout')
def sign_out():

	session["USERNAME"] = None
	session["logged_in"] = False
	info_log.info("User logged_out")
	return redirect('/')


@app.route('/games/<int:id>/rate', methods=["POST"])
@require_login
def rate_game(id):
	p = request.form["rating"]

	game = Game.find(id)
	user = User.find_by_username(session["USERNAME"])
	values = (
		None,
		request.form["rating"],
		user,
		game
	)
	Rating(*values).create()
	info_log.info("User rated game %s" % game.name)
	return redirect('/games/%s' %game.id)

@app.route('/games/<int:id>/like', methods=["POST"])
@require_login
def like_game(id):
	game = Game.find(id)
	user = User.find_by_username(session["USERNAME"])
	values = (
		None,
		user,
		game
	)
	Owned(*values).create()
	info_log.info("User added %s to favorites" %game.name)
	return redirect('/games/%s' %game.id)

@app.route('/games/<int:id>/unlike', methods=["POST"])
@require_login
def unlike_game(id):
	game = Game.find(id)
	user = User.find_by_username(session["USERNAME"])
	Owned.find_by_game_and_user(game, user).delete()
	info_log.info("User added %s to favorites" %game.name)
	return redirect('/games/%s' %game.id)


@app.route('/games/<int:id>/add_comment', methods=["POST"])
@require_login
def add_comment(id):
	game = Game.find(id)
	user = User.find_by_username(session["USERNAME"])
	content = request.form["content"]
	values = (
		None,
		content,
		user,
		game
	)
	Comment(*values).create()
	info_log.info("User added a comment to %s" %game.name)
	return redirect('/games/%s' %game.id)
@app.route('/games/<int:id>/delete_comment/<int:cid>', methods=["POST"])
@require_login
def delete_comment(id,cid):
	game = Game.find(id)
	Comment.find_by_id(cid).delete()
	info_log.info("User deleted a comment on %s" %game.name)
	return redirect('/games/%s' %game.id)

@app.route('/categories/<int:id>/delete')
@require_admin
def delete_category(id):
	Category.find(id).delete()
	info_log.info("Category deleted")
	return redirect("/categories")


@app.route('/categories/new', methods=["GET", "POST"])
@require_admin
def new_category():
	if request.method == "GET":
		return render_template("new_category.html")
	elif request.method == "POST":
		category = Category(None, request.form["name"])
		category.create()
		info_log.info("Category %s added successfully" % category.name)
		return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
	user = User.find_by_username(session['USERNAME'])
	return render_template("category.html", user=user, category=Category.find(id), username = session["USERNAME"])


@app.route('/categories')
def get_categories():
	if User.find_by_username(session["USERNAME"]):
		user = 1
	else:
		user = 0
	return render_template("categories.html", categories=Category.all(), user=User.find_by_username(session['USERNAME']), username = session["USERNAME"])


@app.route('/games')
def list_games():
	if User.find_by_username(session["USERNAME"]):
		user = 1
	else:
		user = 0
	return render_template('games.html', games=Game.all(), user = user, username = session["USERNAME"])


@app.route('/games/<int:id>')
@require_login
def show_game(id):
	logged_in = session["logged_in"]
	game = Game.find(id)
	comments = Comment.find_by_game(game)
	requirements = Requirements.find_by_game(Game.find(id))
	rating = Game.calc_rating(id)
	owned = 1
	user = User.find_by_username(session['USERNAME'])
	if not Owned.find_by_game_and_user(game, user):
		owned = 0

	return render_template('game.html', game=game, rating=rating, logged_in = logged_in, requirements = requirements, owned = owned, comments = comments, user = user, username = session["USERNAME"])
