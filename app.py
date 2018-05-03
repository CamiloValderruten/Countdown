from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect

from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash

from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId

import os

host = "mongo" if os.environ.get('SERVICE_ENVIRONMENT') == "PRODUCTION" else "0.0.0.0"
db = MongoClient(host=host)['countdown']
app = Flask(__name__)
app.config['SECRET_KEY'] = 'BNJqqX8cuQe^$U68DrxMb8aGSk8LaD0CKO$78WKB!ySM'
socket = SocketIO(app, async=None)


@socket.on('timer')
def timer(data):
    socket.emit('timer', dumps(data), broadcast=True)


@socket.on('order_changed')
def order_changed(timers_ids):
    category = db.categories.find_one({"timers._id": ObjectId(timers_ids[0])})
    for timer in category.get('timers', []):
        timer['order'] = timers_ids.index(str(timer.get('_id')))
    db.categories.save(category)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    email = request.form.get('email').lower()
    password = request.form.get('password')
    user = db.users.find_one({"email": email})
    if user and check_password_hash(user['password'], password):
        session['logged_in'] = True
    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    del(session['logged_in'])
    return redirect('login')


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if db.users.count() == 0:
        if request.method == "GET":
            return render_template('setup.html')

        email = request.form.get('email').lower()
        password = request.form.get('password')
        db.users.save({"email": email, "password": generate_password_hash(password)})
        session['logged_in'] = True
    return redirect('/')


@app.route('/')
def home():
    if db.users.count() == 0:
        return redirect('setup')

    if session.get('logged_in') is None:
        return redirect('login')

    return render_template('home.html', categories=list(db.categories.find()))


@app.route('/clock')
def clock():
    return render_template('clock.html')


@app.route('/categories/<category_id>/timers', methods=['POST'])
def timers(category_id):
    hours = int(request.form['hours']) if len(request.form['hours']) > 0 else 0
    minutes = int(request.form['minutes']) if len(request.form['minutes']) > 0 else 0
    seconds = int(request.form['seconds']) if len(request.form['seconds']) > 0 else 0
    seconds = seconds + (minutes * 60) + (hours * 60 * 60)
    next_ = True if request.form.get('next', 'off') == "on" else False
    timer = dict(name=request.form['name'], next=next_, seconds=seconds, _id=ObjectId(), order=0)
    db.categories.update({'_id': ObjectId(category_id)}, {'$push': {'timers': timer}})
    return redirect('/')


@app.route('/categories/<category_id>/timers/<timer_id>/delete')
def delete_timer(category_id, timer_id):
    db.categories.update({"_id": ObjectId(category_id)},  {"$pull": {"timers": {"_id": ObjectId(timer_id)}}})
    return redirect('/')


@app.route('/categories', methods=['POST', 'GET'])
def categories():
    if request.method == "GET":
        return dumps(db.categories.find())
    data = dict(name=request.form['name'], description=request.form['description'])
    db.categories.save(data)
    return redirect('/')


@app.route('/categories/<_id>/delete')
def delete_category(_id):
    db.categories.delete_one({"_id": ObjectId(_id)})
    return redirect('/')
