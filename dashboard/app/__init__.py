from flask import Flask
flaskApp = Flask(__name__)
from app import routes
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__, server=flaskApp)

app.layout = html.Div(children=[
    html.H1(children='UWA Bin Level Sensor Network'),

    html.Div(children='''
        A network t.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
	# app.run_server(debug=True, port=8050, host='127.0.0.1')
	app.run_server(debug=True)