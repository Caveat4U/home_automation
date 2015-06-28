import nest
from config import *

username = USER
password = NEST_PASSWORD

napi = nest.Nest(username, password)

for structure in napi.structures:
    print 'Structure %s' % structure.name
    print '    Away: %s' % structure.away
    print '    Devices:'

    for device in structure.devices:
        print '        Device: %s' % device.name
        print '            Temp: %0.1f' % device.temperature

# The Nest object can also be used as a context manager
with nest.Nest(username, password) as napi:
    for device in napi.devices:
        device.temp = 23

# Weather data is also availible under structure or device
# The api is the same from either

structure = napi.structures[0]
time_str = structure.weather.current.datetime.strftime('%Y-%m-%d %H:%M:%S')
print 'Current Weather at %s:' % time_str
print '    Condition: %s' % structure.weather.current.condition
print '    Temperature: %s' % structure.weather.current.temperature
print '    Humidity: %s' % structure.weather.current.humidity
print '    Wind Dir: %s' % structure.weather.current.wind.direction
print '    Wind Azimuth: %s' % structure.weather.current.wind.azimuth
print '    Wind Speed: %s' % structure.weather.current.wind.kph

# NOTE: Hourly forecasts do not contain a "contidion" its value is `None`
#       Wind Speed is likwise `None` as its generally not reported
print 'Hourly Forcast:'
for f in structure.weather.hourly:
    print '    %s:' % f.datetime.strftime('%Y-%m-%d %H:%M:%S')
    print '        Temperature: %s' % f.temperature
    print '        Humidity: %s' % f.humidity
    print '        Wind Dir: %s' % f.wind.direction
    print '        Wind Azimuth: %s' % f.wind.azimuth


# NOTE: Daily forecasts temperature is a tuple of (low, high)
print 'Daily Forcast:'
for f in structure.weather.daily:
    print '    %s:' % f.datetime.strftime('%Y-%m-%d %H:%M:%S')
    print '    Condition: %s' % structure.weather.current.condition
    print '        Low: %s' % f.temperature[0]
    print '        High: %s' % f.temperature[1]
    print '        Humidity: %s' % f.humidity
    print '        Wind Dir: %s' % f.wind.direction
    print '        Wind Azimuth: %s' % f.wind.azimuth
    print '        Wind Speed: %s' % structure.weather.current.wind.kph


# NOTE: By default all datetime objects are timezone unaware (UTC)
#       By passing `local_time=True` to the `Nest` object datetime objects
#       will be converted to the timezone reported by nest. If the `pytz`
#       module is installed those timezone objects are used, else one is
#       synthesized from the nest data
napi = nest.Nest(username, password, local_time=True)
print napi.structures[0].weather.current.datetime.tzinfo