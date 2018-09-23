from datetime import datetime
import uwaPySense

app = uwaPySense.App()

@app.addwork
def _(m):
    print("[{}]:\t{}".format(datetime.now(), m.as_string))

@app.setup
def config(ctx):
    print("\nListening on {}".format(ctx.args.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.args.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.args.time_out))
    print("Press Ctrl+C to stop\n")

@app.loop(rest_time=60)
def main(ctx):

    ctx.counter += 1
    print("Time elapsed = {} mins".format(ctx.counter))

if __name__ == '__main__':
    main()