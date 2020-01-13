from functools import wraps
from flask import Flask, session
from flask import render_template, request, session, redirect, url_for
import json
username = 'none'
from user import User
app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
    
def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session["USERNAME"] is None:
        	redirect('/login')
        return func(*args, **kwargs)
        	
    return wrapper

@app.route('/')
def hello_world():
    return redirect("/main")

@app.route("/login", methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")
        user = User.find_by_username(username)

        if not user or not user.verify_password(password):
            print("Wrong username or password")
            return redirect(request.url)

        else:
            session["USERNAME"] = username
            print("session username set")
            return redirect('/')

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            0
        )
        User(*values).create()

        return redirect('/')

@app.route('/main')
def main_page():
    return render_template("main.html")

@app.route('/profile')
@require_login
def view_profile():
	
	user = User.find_by_username(session['USERNAME'])
	if User.check_if_admin(user):
		return redirect('/admin_profile')
	else:
		return redirect('/user_profile')

@app.route('/user_profile')
@require_login
def user_profile():
	return render_template("user_profile.html")

@app.route('/admin_profile')
@require_login
def admin_profile():
	return render_template("user_profile_admin.html")

if __name__ == "__main__":
    app.run(debug = True)