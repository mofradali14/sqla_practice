"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def users_list():
    """ Displays list of users"""
    users = User.query.all()
    return render_template('user_listing.html', users=users)


@app.route('/', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash(f"Added User: {new_user.first_name} {new_user.last_name}")

    return redirect(f'{new_user.id}')



@app.route('/create_user')
def new_user_form():
    return render_template('create_user.html')


@app.route('/<int:user_id>')
def display_user(user_id):
    """ Show users details"""
    user = User.query.get_or_404(user_id)
    # users = User.query.all()
    return render_template('user_details.html', user=user)


@app.route('/user_edit/<int:user_id>')
def edit_user_form(user_id):
    """ Edit user information """
    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)


@app.route('/user_edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"Edited User: {user.first_name} {user.last_name}")
    return redirect('/')





@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash(f"Deleted User: {user.first_name} {user.last_name}")
    return redirect('/')

@app.route('/users/<int:user_id>/post/new')
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)
    
@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Added Post: {new_post.title}")
    return redirect(f'/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Deleted Post: {post.title}")
    return redirect(f'/{post.user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Edited Post: {post.title}")
    return redirect('/')

# @app.route('/<int:user_id>/delete', methods=['POST'])
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)

#     db.session.delete(user)
#     db.session.commit()

#     return redirect('/')