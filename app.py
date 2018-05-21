#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, g, session, url_for, redirect, flash
import mysql.connector
import hashlib
import requests
import schedule
import time
import datetime
import serrure

#Construct app
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('secret_config')


#Database functions
def connect_db () :
    g.mysql_connection = mysql.connector.connect(
        host = app.config['DATABASE_HOST'],
        user = app.config['DATABASE_USER'],
        password = app.config['DATABASE_PASSWORD'],
        database = app.config['DATABASE_NAME']
    )

    g.mysql_cursor = g.mysql_connection.cursor()
    return g.mysql_cursor

def get_db () :
    if not hasattr(g, 'db') :
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db (error) :
    if hasattr(g, 'db') :
        g.db.close()

#Pages
@app.route('/')
def index () :
    if not session.get('user') :
        return redirect(url_for('login'))

    return render_template('index.html', user = session['user'])

@app.route('/login/', methods = ['GET', 'POST'])
def login () :
    email = str(request.form.get('email'))
    password = hashlib.sha512(str(request.form.get('password')).encode('utf-8')).hexdigest()

    valid_user = False

    db = get_db()
    db.execute('SELECT * FROM user WHERE email= %s AND password= %s', (email, password))
    found = db.fetchone()
    if found:
        valid_user = True
    else:
        flash('Nop !')

    if valid_user :
        session['user'] = True
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout/')
def logout():
    session['user'] = False
    return redirect(url_for('login'))

@app.route('/logs/')
def showLogs():
    if not session.get('user') :
        return redirect(url_for('login'))

    with open('/home/pi/log.txt') as event_log:
        event_lines = event_log.readlines()

        door_history = []
        events = len(event_lines)

        for x in range(events):
            door_history.append(event_lines[x].split(" "))        

    return render_template('door-logs.html', events=events, door_history=door_history, user = session['user'])        

@app.route('/open-door/')
def openDoor():
    if not session.get('user') :
        return redirect(url_for('login'))

    serrure.turn_hight(LED_GREEN)
    flash('The door is opened !')
    serrure.open_door()
    serrure.turn_low(LED_GREEN)
    flash('The door is closed ...!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

