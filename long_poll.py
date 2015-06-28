import eventsource
from config import *
url = "https://developer-api.nest.com/devices.json?auth=c.mQU1xt9tNRnVZwLRQDAtxGYocFdtJkm39We58OFJN1bn2dQbYnceFpJSLCDAQU3gL3re8YOwflrIc8IMcjxkCQOIgiW2Yd1BsA7rHbAmyhqsQe8mjMGUhxCjbkYFPT8lhKsUrhTXsEgIZb6C"
action = "LISTEN"
target = ""
client = eventsource.listener.Event(url, action, target, callback=None, retry=0)
client.poll()