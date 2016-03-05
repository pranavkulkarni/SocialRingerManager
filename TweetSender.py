import twitter
import time
import constants


api = twitter.Api(consumer_key=constants.consumer_key,
			      consumer_secret=constants.consumer_secret,
			      access_token_key=constants.access_token_key,
			      access_token_secret=constants.access_token_secret)
api.VerifyCredentials()

tweetBotAddress = constants.tweetBotAddress
unityId = constants.unityId
checkInNum = 50
callNum = 9
location = constants.location

#first clear your timeline
statuses = api.GetUserTimeline(screen_name="", count = 2000)
for status in statuses:
	api.DestroyStatus(status.id)


#Check in multiple times in the same location to make utility function adapt.


#Now you are ready to check in
x = "I checked in at" + location + unityId + str(checkInNum) + tweetBotAddress
status = api.PostUpdate(x)
print x

time.sleep(30)

y = "CALL" + unityId + str(checkInNum) + "_" + str(callNum) + tweetBotAddress
print y
call = api.PostUpdate(y)
checkInNum = checkInNum + 1
callNum = callNum + 1

time.sleep(30)

#Now you are ready to check in
x = "I checked in at" + location + unityId + str(checkInNum) + tweetBotAddress
status = api.PostUpdate(x)
print x

time.sleep(30)

y = "CALL" + unityId + str(checkInNum) + "_" + str(callNum) + tweetBotAddress
print y
call = api.PostUpdate(y)
checkInNum = checkInNum + 1
callNum = callNum + 1


#Now you are ready to check in
x = "I checked in at" + location + unityId + str(checkInNum) + tweetBotAddress
status = api.PostUpdate(x)
print x

time.sleep(30)

y = "CALL" + unityId + str(checkInNum) + "_" + str(callNum) + tweetBotAddress
print y
call = api.PostUpdate(y)
checkInNum = checkInNum + 1
callNum = callNum + 1