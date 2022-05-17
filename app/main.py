import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    job = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Volunteer {self.firstname}>'

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        job = request.form['job']
        volunteer = Volunteer(firstname=firstname,
                            lastname=lastname,
                          email=email,
                          job=job)
        db.session.add(volunteer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')  

@app.route('/')
def index():
    volunteers = Volunteer.query.all()
    return render_template('index.html', volunteers=volunteers)

@app.route('/<int:volunteer_id>/')
def volunteer(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    return render_template('volunteer.html', volunteer=volunteer)

@app.route('/<int:volunteer_id>/edit/', methods=('GET', 'POST'))
def edit(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        job = request.form['job']

        volunteer.firstname = firstname
        volunteer.lastname = lastname
        volunteer.email = email
        volunteer.bio = job

        db.session.add(volunteer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', volunteer=volunteer)

@app.post('/<int:volunteer_id>/delete/')
def delete(volunteer_id):
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    db.session.delete(volunteer)
    db.session.commit()
    return redirect(url_for('index'))    