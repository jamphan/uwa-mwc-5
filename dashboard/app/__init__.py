from flask import Flask
from flask_mqtt import Mqtt
flaskApp = Flask(__name__)

from app import routes
from app import server
<<<<<<< HEAD
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
=======
>>>>>>> 9fc516a002632479b57e2edacef66e5c0e787d9b

flaskApp.config['MQTT_BROKER_URL'] = 'm2m.eclipse.org'

mqtt = Mqtt(flaskApp)
mqtt.subscribe('UWA/CITS/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    server.addToJSON(data);
if __name__ == '__main__':
	# app.run_server(debug=True, port=8050, host='127.0.0.1')
	flaskApp.run_server(debug=True)
