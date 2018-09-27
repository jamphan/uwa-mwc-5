from app import server
from flask import render_template
from app import flaskApp
from app.database.jsonDb import jsonDb


@flaskApp.route('/')
@flaskApp.route('/index')
def index():

    db = jsonDb('app/data.json')
    bin_ids = db.get_all_bins()
    print(bin_ids)
    data = db.data

    return render_template('home.html', data=data, bin_ids = bin_ids)