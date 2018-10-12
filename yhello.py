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
from flask_script import Manager
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('Please input year', validators=[Required()])
    submit = SubmitField('Submit')
# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

manager = Manager(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like the requested data is unavailable!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/invalid')
def invalid():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)

manager = Manager(app)

# ...

if __name__ == '__main__':
    manager.run()
# ...

