from app import server
from flask import render_template
from app import flaskApp

@flaskApp.route('/')
@flaskApp.route('/index')
def index():
    jsonData = server.getJSON()
    return render_template('home.html', data=jsonData)