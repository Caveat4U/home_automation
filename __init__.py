from iclickerpoll import *
import signal, argparse

parser = argparse.ArgumentParser(description='Start an iClicker poll')
parser.add_argument('--debug', action='store_true', default=False,
                    help='Display debug information about the USB transactions')
parser.add_argument('--type', type=str, default='alpha',
                    help='Sets the poll type to alpha, numeric, or alphanumeric')
parser.add_argument('--duration', type=str, default='0m0s',
                    help='Sets the duration of the poll in minutes and seconds. 0m0s is unlimited.')
parser.add_argument('--dest', type=str, default='',
                    help='Sets the file to save polling data to.')
parser.add_argument('--frequency', type=str, default='aa',
                    help='Sets the two base-station frequency codes. Should be formatted as two letters (e.g., \'aa\' or \'ab\')')

args = parser.parse_args()

#
# Process all the arguments
#

if args.debug:
    log.setLevel(0)
if args.type in ['alpha', 'numeric', 'alphanumeric']:
    poll_type = args.type
else:
    raise ValueError("Poll type must be 'alpha', 'numeric', or 'alphanumeric', not '{0}'".format(args.type))
if args.duration:
    poll_duration = 1000
if args.frequency:
    freq1 = args.frequency[0].lower()
    freq2 = args.frequency[1].lower()
    if freq1 not in ('a', 'b', 'c', 'd') or freq2 not in ('a', 'b', 'c', 'd'):
        raise ValueError("Frequency combintation '{0}{1}' is not valid".format(freq1, freq2))


#
# Initiate the polling
#
print('Finding iClicker Base')
base = IClickerBase()
base.get_base()
print('Initializing iClicker Base')
base.initialize(freq1, freq2)

poll = IClickerPoll(base)
signal.signal(signal.SIGINT, lambda *x: close_pole(poll))
# Set a callback to stop the poll after the desired amount of time
if poll_duration:
    stop_timer = threading.Timer(poll_duration, lambda *x: close_pole(poll))
    stop_timer.start()
print('Poll Started')
poll.start_poll(poll_type)

# If we made it this far and stop_timer wasn't triggered, we were asked to stop another
# way, so we should stop the stop_timer
stop_timer.cancel()