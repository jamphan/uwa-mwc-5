from uwaPySense import listenerloop

def post_setup(ctx):
    print("\nListening on {}".format(ctx.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.time_out))
    print("\tMessage type = {}".format(ctx.message_type.__name__))
    print("Press Ctrl+C to stop\n")

    ctx.counter = 0

@listenerloop(rest_time=60, post_setup=post_setup)
def main(ctx):
    """ Program main loop"""

    ctx.counter += 1
    print("Time elapsed = {} mins".format(ctx.counter))

if __name__ == '__main__':
    main()