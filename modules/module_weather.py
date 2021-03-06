# -*- coding: utf-8 -*-


has_pywapi = False
try:
    import pywapi
    has_pywapi = True
except:
    print('Error loading library pywapi. Probably you havent installed it yet.')

def feels_like(temperature, air_speed):
    """tempeture as °C, air_speed as kmph. The formula from http://www.bbc.co.uk/weather/features/understanding/feelslike.shtml"""
    air_speed = air_speed ** 0.16
    return (13.12 + 0.6215 * temperature - 11.37 * air_speed + 0.3965 * temperature * air_speed)

def parse_google_wind_condition(wind_condition):
    """ Parses the data from string """
    wind_condition = wind_condition.split(' ')
    kmph = int(wind_condition[3])*1.609344
    mps = kmph / 3.6
    return wind_condition[1], kmph, mps

def command_weather(bot, user, channel, args):
    """ This module tells a weather for location."""
    if not has_pywapi: return

    result_dict = pywapi.get_weather_from_google(args)
    if not all(result_dict.values()):
        bot.say(channel, 'unknown location')
        return

    compass_point, kmph, mps = parse_google_wind_condition(result_dict['current_conditions']['wind_condition'])
	
    compass_points = {'N': 'north', 'S': 'south', 'W': 'west', 'E': 'east', 'NW': 'northwest', 'NE': 'northeast', 'SW': 'southwest', 'SE': 'southeast'}
    compass_point = compass_points[compass_point]

    city = result_dict['forecast_information']['city']
    humidity = result_dict['current_conditions']['humidity']
    condition = result_dict['current_conditions']['condition']
    temperature = int(result_dict['current_conditions']['temp_c'])
    
    answer = u'%s: %s, %d °C feels like %d °C, Wind: %.1f m/s from %s, %s' % \
	     (city, condition, temperature, feels_like(temperature, kmph), mps, compass_point, humidity)
    answer = answer.encode("utf-8")
    return bot.say(channel, answer)

