class FeedbackObject():

    def __init__(self, location, silentCount, loudCount, positiveCount, negativeCount, neutralCount):
      self.location = location
      self.silentCount = silentCount
      self.loudCount = loudCount
      self.positiveCount = positiveCount
      self.negativeCount = negativeCount
      self.neutralCount = neutralCount

    def printFeedbackCounts(self):
      print "For feedback object = ", self.location, str(self.positiveCount), " ", str(self.negativeCount), " ", str(self.neutralCount)