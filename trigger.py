class Trigger(object):
	def __init__(self):
		print "Trigger"

import nest
from nest import utils as nest_utils

class NestInfo(Trigger):
	def __init__(self, username, password, pincode):
		# Connect to the nest device
		# TODO - Should this be in __start__()?
		self.username = username
		self.password = password
		self.token = pincode
		self.napi = nest.Nest()
		self.poll_current_state()
		self.triggered = False

	def poll_current_state(self):
		nest_info_struct = self.napi.structures[0]
		self.away = nest_info_struct.away
		thermostat = nest_info_struct.devices[0]
		self.current_temperature = nest_utils.c_to_f(thermostat.temperature)
		self.fan = thermostat.fan
		self.humidity = thermostat.humidity
		self.mode = thermostat.mode
		self.target = thermostat.target
		self.current_weather = nest_info_struct.weather.current
		#time_str = structure.weather.current.datetime.strftime('%Y-%m-%d %H:%M:%S')

	def is_away(self, refresh_info = False):
		if refresh_info:
			self.poll_current_state()
		return self.away

	# Status can be "away" or "home"
	def set_away(self, status = "away"):
		self.napi.structures[0].away = status

	def get_temperature(self, refresh_info = False):
		if refresh_info:
			self.poll_current_state()
		return self.current_temperature

	def trigger(self):
		pass

	# Places the current weather into memory
	# Structure:
	#   condition
	# 	temperature
	# 	humidity
	# 	wind.direction
	# 	wind.azimuth
	# 	wind.kph
	def get_weather(self):
		return self.current_weather()
		


if __name__ == '__main__':
	import config
	from time import sleep
	n = NestInfo(config.USER, config.NEST_PASSWORD, config.NEST_PINCODE)
	print n.is_away()
	n.set_away(status = "home")
	for x in xrange(30):
		print n.get_temperature(refresh_info=True)
		sleep(10)