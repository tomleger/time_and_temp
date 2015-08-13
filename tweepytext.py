# coding: utf-8
import tweepy
import urllib2
import json
import time
import datetime
import random

consumer_key = 'jNSA6i7eIA564BRMRdMVCDrkF'
consumer_secret = 'L3908LNoYSh8bwIIhgtEJ6PuaFdXGBENaZdsVrG0iRJFMpWa4u'
access_token  = '3306456200-8Y9UUXPxM3t6B6KCL9eJxjC1lREmEtQ8zdkBR28'
access_token_secret = 'nd8L1PWQ4CxaBP07N1U548uWz1ei5Q7Bck65MhjsRsRIW'
wu_api_key = 'c925e374af6c3fc2'
wu_api_url = 'http://api.wunderground.com/api/'
wu_api_query = '/conditions/q/NY/Brooklyn.json'

#tweepy code to handle authorizing the API access
auth =  tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Get the weather information from Wunderground API in JSON format
def check_weather():
	f = urllib2.urlopen(wu_api_url + wu_api_key + wu_api_query)
	json_string = f.read()
	parsed_json = json.loads(json_string)
	#print json_string
	#print parsed_json
	current_temp = parsed_json['current_observation']['temp_f']
	current_icon = parsed_json['current_observation']['icon_url']
	observation_time  = parsed_json['current_observation']['local_epoch']
	observation_time = datetime.datetime.fromtimestamp(float(observation_time))
	fmt = '%-I:%M'  #format the time
	observation_time =  observation_time.strftime(fmt)
	current_time = datetime.datetime.now().time()
	tt_list = [current_temp, current_time, current_icon]
	return tt_list

#save the weather icon and upload it to the profile
def icon_update(current_icon):
	icon_file = urllib2.urlopen(current_icon)
	icon_file = icon_file.read()
	with open("icon.gif", "wb") as code:
		code.write(icon_file)
	api.update_profile_image('icon.gif')


def tweet_time_temp():
	secs = random.randint(2700,5400)  		#selects a random number of seconds between 45mins and 90mins
	tt_list = check_weather()			#gets all the new info from Wunderground
	current_temp = tt_list[0]
	current_time =  tt_list[1]
	time_fmt = '%-I:%M %p'
	current_time = current_time.strftime(time_fmt)
	current_status = "The time is %s and the temperature is %s°F." % (str(current_time), current_temp)
	current_icon = tt_list[2]
	print current_status
	print secs
	icon_update(current_icon)
	api.update_status(status=current_status) 	#updates the tweet feed via the API
	time.sleep(secs) 			#pauses for the random number of seconds
while True:
	tweet_time_temp()
