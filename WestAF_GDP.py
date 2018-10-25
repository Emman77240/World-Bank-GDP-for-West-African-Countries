#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Emman
#
# Created:     01/10/2018
# Copyright:   (c) Emman 2018
# Licence:     <your licence>
#------------------------------------------------------------------------------
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, session, redirect, url_for, flash, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'godman'
app.config['MYSQL_DB'] = 'westaf_gdp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

bootstrap = Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/invalid')
def invalid():
    return render_template('404.html')

# Register form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Country info class
class CountryYearForm(Form):
    year = StringField('Year', [validators.Length(4)])

# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create Cursor
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #Commit to DataBase
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get started hash
            data = cur.fetchone()
            password = data['password']

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
               # Passed
               session['logged_in'] = True
               session['username'] = username

               flash('You are now logged in', 'success')
               return redirect(url_for('dashboard'))
            else:
                error = 'Invaid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

# Form input for Nigeria
@app.route('/nigeria_year', methods=['GET','POST'])
@is_logged_in
def nigeria_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM NGA WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('nigeria_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('nigeria_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('nigeria_year.html', form=form)

# Nigeria data display
@app.route('/nigeria_data/<string:year>')
def nigeria_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM NGA WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('nigeria_data.html', data=data)

    # Close connection
    cur.close()

# Form input for Senegal
@app.route('/senegal_year', methods=['GET','POST'])
@is_logged_in
def senegal_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM SEN WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('senegal_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('senegal_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('senegal_year.html', form=form)

# Senegal data display
@app.route('/senegal_data/<string:year>')
def senegal_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM SEN WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('senegal_data.html', data=data)

    # Close connection
    cur.close()

# Form input for Ghana
@app.route('/ghana_year', methods=['GET','POST'])
@is_logged_in
def ghana_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM GHA WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('ghana_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('ghana_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('ghana_year.html', form=form)

# Ghana data display
@app.route('/ghana_data/<string:year>')
def ghana_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM GHA WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('ghana_data.html', data=data)

    # Close connection
    cur.close()

# Form input for Cote d'Ivoire
@app.route('/civ_year', methods=['GET','POST'])
@is_logged_in
def civ_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM CIV WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('civ_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('civ_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('civ_year.html', form=form)

# Cote D'Ivoire data display
@app.route('/civ_data/<string:year>')
def civ_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM CIV WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('civ_data.html', data=data)

    # Close connection
    cur.close()

# Form input for Burkina Faso
@app.route('/bfa_year', methods=['GET','POST'])
@is_logged_in
def bfa_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM BFA WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('bfa_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('bfa_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('bfa_year.html', form=form)

# Burkina Faso data display
@app.route('/bfa_data/<string:year>')
def bfa_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM BFA WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('bfa_data.html', data=data)

    # Close connection
    cur.close()

# Form input for Benin Republic
@app.route('/ben_year', methods=['GET','POST'])
@is_logged_in
def ben_year():
    form = CountryYearForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields
        year = request.form['year']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get GDP by year
        result = cur.execute("SELECT * FROM BEN WHERE year = %s", [year])

        data = cur.fetchone()

        if result > 0:
            flash('Your information request came through !!', 'success')
            return render_template('ben_data.html', data=data)

        else:
            flash('Invalid Year Input', 'danger')
            return render_template('ben_year.html', form=form)

        # Close connection
        cur.close()

    else:
        return render_template('ben_year.html', form=form)

# Benin Republic data display
@app.route('/ben_data/<string:year>')
def ben_data(year):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM BEN WHERE year = %s", [year])

    data = cur.fetchone()

    return render_template('ben_data.html', data=data)

    # Close connection
    cur.close()


if __name__ == '__main__':
    app.secret_key='hardtotellsecret5891'
    app.run(debug=True)



