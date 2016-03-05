from twython import TwythonStreamer
import twitter
import random
import constants

class TweetBotLocationAndCaller(TwythonStreamer):

    dictOfCallers = ['Anakin (Family)', 'Chewbacca (Friend)', 'Han (Friend)', 'Jango (Stranger)', 'JarJar (Friend)', 'Leia (Family)', 'Luke (Family)', 'Mace (Colleague)', 'ObiWan (Colleague)', 'Padme (Family)', 'Yoda (Colleague)']

    def on_success(self, data):
        if 'text' in data:
            response = data['text']
            #look for call tweets and give them a call
            if constants.unityId in response and "CALL" in response:
                caller = random.choice(self.dictOfCallers)
                urgency = 0
                if "Family" in caller or "Colleague" in caller:
                    urgency = 1
                else:
                    urgency = 0
                sender = data['user']['screen_name']
                callRequest = response.split(' ')
                hashP2 = callRequest[len(callRequest) - 1]
                unity = callRequest[len(callRequest) - 2]
                callTweet = "@" + sender +"\n" + "Call from: " + caller + "\n" + "URGENCY: " + str(urgency) + "\n" + unity + " " + hashP2
                print "Calling ----------> "
                print callTweet
                api.PostUpdate(callTweet)

            #look for my check ins and send the location noise level
            screen_name = constants.screenName
            if "I checked in at" in response:
                self.runLocationBot(screen_name, response) # returns the noise level. Response to check-in from place where you checked-in


    def runLocationBot(self, screen_name, tweet):
        s = tweet.split(' ')
        location = s[len(s)-3].lstrip('#')
        unityId = s[len(s)-2]

        noise = 2
        if "hunt" in location:
            noise = 1
        if "eb2" in location:
            noise = 3
        if "carmichael" in location:
            noise = 4
        if "oval" in location:
            noise = 4
        if "party" in location:
            noise = 5

        x = "@" + screen_name + "\n" + "LOCATION: " + location + "\n" + "NOISE: " + str(noise) + "\n" + unityId + " #P2CSC555F15"
        status = api.PostUpdate(status = x)



    def on_error(self, status_code, data):
        print status_code



api = twitter.Api(consumer_key=constants.consumer_key,
			      consumer_secret=constants.consumer_secret,
			      access_token_key=constants.access_token_key,
			      access_token_secret=constants.access_token_secret)
api.VerifyCredentials()


streamer = TweetBotLocationAndCaller(constants.consumer_key, constants.consumer_secret,
                         constants.access_token_key, constants.access_token_secret)

print "Location and call handler bot starting...."
streamer.statuses.filter(track = '#P2CSC555F15')

