"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql123@host:80/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "$blZacNat123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
# debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def users_list():
    return redirect('/users')
    

@app.route('/users')
def users_and_form_link():
    """ shows users and a link for the form"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users-and-form-link.html', users=users)

@app.route('/users/new')
def new_user_form():
    """form to create a new user"""
    return render_template('new-user-form.html')

@app.route('/users/new', methods = ["POST"])
def add_new_user():
    """processes new user form then goes back to users"""
    #ADD new user to python
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    #add new user to sql alchemy
    db.session.add(new_user)
    db.session.commit()
    #flash NEW USER ADDED and redirect back
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail_page(user_id):
    user=User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    ''' show editing form'''
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit_form(user_id):
    ''' process editing form and update the db'''
    #get form data and update record in db
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
    
    # db.session.add(user) #don't need for an update
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """delete specified user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/dice')
def dice_page():
    return render_template("dice.html")

@app.route('/campaigns')
def campaigns_page():
    return render_template("campaigns.html")

@app.route('/characters')
def characters_page():
    return render_template("characters.html")

@app.route('/inventory')
def inventory_page():
    return render_template("inventory.html")

@app.route('/treasure')
def treasure_page():
    return render_template("treasure.html")

@app.route('/about')
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run()