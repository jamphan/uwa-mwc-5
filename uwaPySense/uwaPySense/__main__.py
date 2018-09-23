import uwaPySense

@uwaPySense.messages.end_flag
def flag(m):

    return 'END'

@uwaPySense.messages.is_valid
def valid(m):

    if len(m.as_string) > 0 and m.as_string[0].isdigit():
        return True
    else:
        return False

def post_setup(ctx):
    print("\nListening on {}".format(ctx.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.time_out))
    print("Press Ctrl+C to stop\n")

    ctx.counter = 0

@uwaPySense.listenerloop(rest_time=60, post_setup=post_setup)
def main(ctx):
    """ Program main loop"""

    ctx.counter += 1
    print("Time elapsed = {} mins".format(ctx.counter))

if __name__ == '__main__':
    main()