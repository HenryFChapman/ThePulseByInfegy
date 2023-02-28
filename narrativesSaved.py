def parseNarratives(data, source):

	timeframeDict = {}

	keysList = list(data.keys())

	universeSum = sum(data['totals']['universe'])

	keysList.remove("dates")
	keysList.remove("totals")

	keys = []
	universes = []
	convoPercent = []

	count = 0
	for key in keysList[0:6]:

		tempSum = 0
		for dataPoint in data[key]['universe']:
			tempSum = tempSum + dataPoint

		keys.append(key)
		universes.append(data[key]['universe'])
		convoPercent.append(str(round((tempSum/universeSum)*100, 2)) + "%")

	timeframeDict.update({'keys':keys})
	timeframeDict.update({'data':universes})	
	timeframeDict.update({'percentage':convoPercent})

	return timeframeDict