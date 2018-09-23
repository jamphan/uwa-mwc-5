from datetime import datetime

import uwaPySense

def config(ctx):
    print("\nListening on {}".format(ctx.args.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.args.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.args.time_out))
    print("Press Ctrl+C to stop\n")
    
    @ctx.WorkRegister
    def _(m):
        now = datetime.now()
        print("[{}]:\t{}".format(now, m.as_string))

    ctx.counter = 0

@uwaPySense.listenerloop(rest_time=60, post_setup=config)
def main(ctx):

    ctx.counter += 1
    print("Time elapsed = {} mins".format(ctx.counter))

if __name__ == '__main__':
    main()