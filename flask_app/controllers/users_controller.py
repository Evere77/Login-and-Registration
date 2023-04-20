from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



# ============= LOGIN / REG PAGE - VIEW =============
@app.route('/')
def index():
    return render_template('index.html')


# ============= REGISTER - METHOD - ACTION =============
@app.route('/users/register', methods=['POST'])
def user_reg():
    if not User.validate(request.form):
        return redirect('/')

    # 1 hash the plain text password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # 2 get the data dict ready with the new hashed pw to create a User
    user_data = {
        **request.form,
        'password' : pw_hash
    }
    # 3 pass it to the User model
    user_id = User.create(user_data)
    session['user_id'] = user_id

    return redirect('/dashboard')


# ============= LOGIN ACTION / POST=============
@app.route('/users/login', methods=['POST'])
def user_login():
    user_in_db = User.get_by_email(request.form['email'])
    if not user_in_db:
        flash('Invalid Credentials', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ('Invalid Credentials', 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')


# ============= DASHBOARD PAGE -- RENDER / VIEW =============
@app.route('/dashboard')
def dash():
    # route guard
    if 'user_id' not in session:
        return redirect('/')
    
    logged_user = User.get_by_id(session['user_id'])

    return render_template('welcome.html', logged_user=logged_user)


# ============= LOGOUT =============
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')