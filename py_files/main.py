from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from game import Game
from comment import Comment
from gamecategory import Category
from user import User

app = Flask(__name__)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def hello_world():
    return redirect("/categories")


@app.route('/games')
def list_posts():
    return render_template('all_games.html', games=Game.all())


@app.route('/games/<int:id>')
def show_game(id):
    game = Game.find(id)

    return render_template('game.html', game=game)


@app.route('/games/<int:id>/edit', methods=['GET', 'POST'])
def edit_game(id):
    game = Game.find(id)
    if request.method == 'GET':
        return render_template(
            'edit_game.html',
            game=game,
            categories=Category.all()
        )
    elif request.method == 'POST':
        game.name = request.form['name']
        game.author = request.form['developers']
        game.content = request.form['content']
        game.category = Category.find(request.form['category_id'])
        game.save()
        return redirect(url_for('show_game', id=game.id))


@app.route('/games/new', methods=['GET', 'POST'])
@require_login
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', categories=Category.all())
    elif request.method == 'POST':
        categ = Category.find(request.form['category_id'])
        values = (
            None,
            request.form['name'],
            request.form['developers'],
            request.form['content'],
            categ
        )
        Game(*values).create()

        return redirect('/')


@app.route('/games/<int:id>/delete', methods=['POST'])
def delete_post(id):
    game = Game.find(id)
    game.delete()

    return redirect('/')


@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        game = Game.find(request.form['game_id'])
        values = (None, game, request.form['message'])
        Comment(*values).create()

        return redirect(url_for('show_game', id=game.id))


@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=Category.all())


@app.route('/categories/new', methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return render_template("new_category.html")
    elif request.method == "POST":
        category = Category(None, request.form["name"])
        category.create()
        return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
    return render_template("category.html", category=Category.find(id))


@app.route('/categories/<int:id>/delete')
def delete_category(id):
    Category.find(id).delete()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        User(*values).create()

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run()
