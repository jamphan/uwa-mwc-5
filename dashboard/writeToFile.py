from datetime import datetime
import uwaPySense

app = uwaPySense.App()

# Shared file with Flask App
target_file = 'test.csv'

@uwaPySense.messages.is_valid
def is_valid(m):
    
    if len(m.as_string) > 0 and m.as_string.startswith("test:"):
        return True
    else:
        return False

# Write to the shared file
@app.addwork
def _(m):
    with open(target_file , 'a') as fd:
        fd.write("{},{}".format(datetime.now(), m.as_string[:-1]))
        
@app.addwork
def _(m):
    print('test!')
    
@app.addwork
def ItDoesntMatterWhatICallThis(m):
    print('test2:' + m.as_string)

@app.setup
def config(ctx):
    print("\nListening on {}".format(ctx.args.serial_port))
    print("\tBaud rate = {:.0f}".format(ctx.args.baud_rate))
    print("\tTime out = {:.2f}".format(ctx.args.time_out))
    print("Press Ctrl+C to stop\n")

    ctx.counter = 0

@app.loop(rest_time=60)
def main(ctx):

    ctx.counter += 1
    print("Time elapsed = {} mins".format(ctx.counter))

if __name__ == '__main__':
    main()
    
    
# #### C Code for your arduino


# int timer_s = 0;

# void setup() {
#   // put your setup code here, to run once:
#   Serial.begin(9600);
# }

# void loop() {
#   // put your main code here, to run repeatedly:
#   Serial.print("test: " + timer_s);
#   delay(1000);
#   timer_s = timer_s + 1;
# }