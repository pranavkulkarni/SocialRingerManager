from twython import TwythonStreamer
import twitter
import constants


from FeedbackObject import FeedbackObject


class ResponseListener(TwythonStreamer):

    mode = "Silent"
    listOfNeighbors = []
    feedbackStore = {}

    def initilize(self):
        #initilize the objects with past feedback counts
        with open(constants.fileName, 'r') as feedFile:
            for line in feedFile:
                splitLine = line.split(',')
                obj = FeedbackObject(splitLine[0], int(splitLine[1]), int(splitLine[2]), int(splitLine[3]), int(splitLine[4]), int(splitLine[5]))
                #print obj.printFeedbackCounts()
                self.feedbackStore[splitLine[0]] = obj
        feedFile.close()

    def on_success(self, data):
        if 'text' in data:
            response = data['text']
            location = ""
            noise = ""
            name = ""

            #this is a response from location bot
            if "@" + constants.screenName in response and constants.unityId in response and "NOISE" in response:
                splitLines = response.split('\n')
                location = splitLines[1].split(" ")[1] # pick the last word from location
                noise = splitLines[2].split(" ")[1] # pick the last word from Noise

            #this is a response from other users to my check in, so capture these users/neighbors in my list of neighbors
            if "@" + constants.screenName in response and "MY_MODE" in response:
                print "Response from other user --> "
                print response
                self.listOfNeighbors.append(response)
                print "List of neighbors = ", self.listOfNeighbors
                linesplit = response.split('\n')
                myMode = "Silent" # some default value because many neighbours have not followed the naming convention
                expectedMode = "Silent"
                for line in linesplit:
                    if "MY_MODE" in line:
                        t = line.split(' ')
                        myMode = t[len(t)-1]
                    if "EXPECTED_MODE" in line:
                        t = line.split(' ')
                        expectedMode = t[len(t)-1]
                    if "Name" in line:
                        t = line.split(' ')
                        name = t[len(t)-1]
                locationFeedBackObj = self.feedbackStore[constants.location.strip(' ').strip('#')]
                if "Silent" in myMode:
                    locationFeedBackObj.silentCount = locationFeedBackObj.silentCount + 1
                else:
                    locationFeedBackObj.loudCount = locationFeedBackObj.loudCount + 1


            #respond to other people's check ins who are in my location
            if constants.unityId not in response and "I checked in at" in response and constants.location in response:
                whoSentIt = data['user']['screen_name'] # contains the twitter handle of the sender
                #read last two words to capture their unity id and #P2...
                checkIn = response.split(' ')
                hashtagP2 = checkIn[len(checkIn) - 1]
                unityId = checkIn[len(checkIn) - 2]
                #set the expected mode for the other person based on where he/she checked in
                expectedMode = "Loud" # some default value
                if "#hunt" or "#eb2" in response:
                    expectedMode = "Silent"
                s = "@" + whoSentIt + "\n" + "Name: Pranav Kulkarni\n" + "MY_MODE: " + self.mode + "\n" + "EXPECTED_MODE: " + expectedMode + "\n" + unityId + " " + hashtagP2
                print "responding to other's check in as follows -- "
                print s
                api.PostUpdate(s)


            #Now give feedback to neighbors who answer/reject a call
            if "ACTION" in response and constants.unityId not in response:
                rSplit = response.split(' ')
                # rSplit[2] - this is the third word which contains unity id of the neighbor who answered/rejected the call
                neighborUnityId = rSplit[2].split('_')[0] + '_' + rSplit[2].split('_')[1]
                #check if this person is actually my neighbor because some people are responding even if they are
                # not in my location
                allNeighborsCombined = '\t'.join(self.listOfNeighbors)
                if neighborUnityId in allNeighborsCombined:
                    #now give feedback to that person based on the location we both are in
                    feed = "Positive"
                    if "hunt" in constants.location and "Yes" in response:
                        feed = "Negative"

                    replyTo = data['user']['screen_name'] # contains the twitter handle of the sender
                    f = "@" + replyTo + "\n" + "Name: Pranav Kulkarni\n" + "Response: " + feed + "\n" + rSplit[2] + " " + rSplit[3]
                    print "Giving following feedback to a neighbor...."
                    print f
                    api.PostUpdate(f)


            #Now read the call from the bot
            if "Call from" in response:
                senderOfTheCall = data['user']['screen_name'] # contains the twitter handle of the sender. Here it is my bot
                if constants.screenName in senderOfTheCall:
                    #read who is calling and send it to the utility func
                    callerSplit = response.split('\n')
                    caller = ""
                    urgency = ""
                    for line in callerSplit:
                        if "Call from" in line:
                            t = line.split(' ')
                            caller = t[len(t)-1]
                        if "URGENCY" in line:
                            t = line.split(' ')
                            urgency = t[len(t)-1]
                        if "#P2CSC555F15" in line:
                            unityIdWithHash = line

                    #call utility function to decide whether to answer the call
                    action = self.utilityFunc(location, caller, urgency, noise)
                    callAns = "ACTION: " + action + " " + unityIdWithHash
                    if "Yes" in action:
                        self.mode = "Loud"
                    api.PostUpdate(callAns)
                    print "My action to answer call : ", callAns


            #Now read feedback from neighbors
            if constants.screenName in response and "RESPONSE" in response:
                rSplit = response.split('\n')
                nameLine = rSplit[1]
                personGivingThisFeedback = nameLine[nameLine.index(" ") + 1:len(nameLine)]
                #check if this person who gave feedback is actually my neighbor because some people are responding even if they are
                # not in my location
                allNeighborsCombined = '\t'.join(self.listOfNeighbors)
                #if personGivingThisFeedback in allNeighborsCombined:
                if True:
                    feedback = rSplit[2]
                    print "Feedback from neighbor -- "
                    print feedback
                    print "------------------------"
                    self.captureFeedback(feedback)


    def captureFeedback(self, response):
        if "hunt" in constants.location:
            huntObj = self.feedbackStore["hunt"]
            if "Positive" or "positive" in response:
                huntObj.positiveCount = huntObj.positiveCount + 1
            if "Negative" or "negative" in response:
                huntObj.negativeCount = huntObj.negativeCount + 1
            if "Neutral" or "neutral" in response:
                huntObj.neutralCount = huntObj.neutralCount + 1

        if "eb2" in constants.location:
            eb2Obj = self.feedbackStore["eb2"]
            if "Positive" or "positive" in response:
                eb2Obj.positiveCount = eb2Obj.positiveCount + 1
            if "Negative" or "negative" in response:
                eb2Obj.negativeCount = eb2Obj.negativeCount + 1
            if "Neutral" or "neutral" in response:
                eb2Obj.neutralCount = eb2Obj.neutralCount + 1

        if "carmichael" in constants.location:
            carmichaelObj = self.feedbackStore["carmichael"]
            if "Positive" or "positive" in response:
                carmichaelObj.positiveCount = carmichaelObj.positiveCount + 1
            if "Negative" or "negative" in response:
                carmichaelObj.negativeCount = carmichaelObj.negativeCount + 1
            if "Neutral" or "neutral" in response:
                carmichaelObj.neutralCount = carmichaelObj.neutralCount + 1

        if "oval" in constants.location:
            ovalObj = self.feedbackStore["oval"]
            if "Positive" or "positive" in response:
                ovalObj.positiveCount = ovalObj.positiveCount + 1
            if "Negative" or "negative" in response:
                ovalObj.negativeCount = ovalObj.negativeCount + 1
            if "Neutral" or "neutral" in response:
                ovalObj.neutralCount = ovalObj.neutralCount + 1

        if "party" in constants.location:
            partyObj = self.feedbackStore["party"]
            if "Positive" or "positive" in response:
                partyObj.positiveCount = partyObj.positiveCount + 1
            if "Negative" or "negative" in response:
                partyObj.negativeCount = partyObj.negativeCount + 1
            if "Neutral" or "neutral" in response:
                partyObj.neutralCount = partyObj.neutralCount + 1

        self.backupFeedbackJob()


    def utilityFunc(self, location, caller, urgency, noise):
        print "In utility function...."
        action = "Yes" # bydefault initializing
        #now get the statistics from the location object to see what my previous feedback have been
        locFeedObj = self.feedbackStore[constants.location.strip(' ').strip('#')]
        print "loc Feed obj counts = ", locFeedObj.positiveCount, " ", locFeedObj.neutralCount, " ", locFeedObj.negativeCount
        if locFeedObj.positiveCount + locFeedObj.neutralCount < locFeedObj.negativeCount:
            #above condition indicates that majority of the past feedback have been negative. So I will not answer call unless there is urgency
            action = "No"
            if int(urgency) == 1 and locFeedObj.loudCount > locFeedObj.silentCount: #indicates that people here OK to some noise
                action = "Yes"
        return action


    def backupFeedbackJob(self):
        #capture the feedback in a file. Just Writing the values to a file every time I receive a feedback.
        print "In backupFeedJob..."
        result0 = open(constants.fileName, 'w')
        for key in self.feedbackStore.keys():
            ob = self.feedbackStore[key]
            line = str(ob.location) + "," + str(ob.silentCount) + "," + str(ob.loudCount) + "," + str(ob.positiveCount) + "," + str(ob.negativeCount) + "," + str(ob.neutralCount) + "\n"
            result0.write(line)
        result0.close()


    def on_error(self, status_code, data):
        print status_code


api = twitter.Api(consumer_key=constants.consumer_key,
			      consumer_secret=constants.consumer_secret,
			      access_token_key=constants.access_token_key,
			      access_token_secret=constants.access_token_secret)
api.VerifyCredentials()


streamer = ResponseListener(constants.consumer_key, constants.consumer_secret,
                         constants.access_token_key, constants.access_token_secret)

streamer.initilize()
print "Response Listener starting..."

streamer.statuses.filter(track = '#P2CSC555F15')

