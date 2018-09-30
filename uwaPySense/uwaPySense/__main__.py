import paho.mqtt.publish
import uwaPySense
from datetime import datetime

app = uwaPySense.App()

MQTT_BROKER = "m2m.eclipse.org"
MQTT_TOPIC = "UWA/CITS/DATA"

@uwaPySense.messages.is_valid
def valid_messages(m):

    msg_header = 'F:'

    if len(m.as_string) > 0 and m.as_string.startswith(msg_header):

        # Remove the frame control
        m.as_string = m.as_string[len(msg_header):]
        m.as_string = m.as_string[:-1]

        return True
    else:
        return False

@app.addwork
def _(m):

    message_parts = m.as_string.split(',')
    sensor_id = message_parts[0]
    data = message_parts[1]
    rrsi = message_parts[2]
    print("Published data for sensor={}\tdata={}\tRRSI={}".format(sensor_id, data, rrsi))
    paho.mqtt.publish.single(MQTT_TOPIC, "{},{},{}".format(sensor_id, data, rrsi), hostname=MQTT_BROKER)

@app.setup
def config(ctx):
    print("\nListening on {}".format(ctx.args.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.args.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.args.time_out))
    print("Press Ctrl+C to stop\n")

@app.loop(rest_time=60)
def main(ctx):
    pass

if __name__ == '__main__':
    main()