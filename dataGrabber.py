#We need these imports for the script to work.
import requests
import json
import sys
import urllib

commonEntitiesToFilter = ['TikTok', 'F.Y.P', 'Instagram', 'Twitter', "Happy Birthday!", "Jesus Is King", "YouTube", "Spotify", "Netflix", "Livemusic", "Orgy (band)", "Etsy", "Amazon (company)", "Happy Sunday", "Love Yourself", "Tegna Inc."]
commonEntitiesToFilter = [elem.lower() for elem in commonEntitiesToFilter]

def calculateGrowth(tempList):

	midpoint = len(tempList) // 2
	first_half = tempList[:midpoint]
	second_half = tempList[midpoint:]

	first_half_sum = sum(first_half)
	second_half_sum = sum(second_half)

	growth_percentage = (second_half_sum / first_half_sum-1)

	return growth_percentage

def parseEntities(data, source):

	timeframeDict = {}

	names = []
	growth = []
	timelines = []

	for entity in data:

		if entity['name'].lower() in commonEntitiesToFilter:
			continue

		timelines.append(entity['timeline'])

		try: 
			tempGrowth = round(calculateGrowth(entity['timeline']) * 100, 2)
		except ZeroDivisionError:
			tempGrowth = 1000

		if tempGrowth > 1000:
			tempGrowth = 1000

		names.append(str(entity['name']))
		growth.append(float(tempGrowth))

	timeframeDict.update({'entities':names[0:6]})
	timeframeDict.update({'growth':growth[0:6]})
	timeframeDict.update({'timelines':timelines[0:6]})	

	return timeframeDict

def parseVolume(data, source):

	timeframeDict = {}

	dates = []
	postVolume = []

	for date in data:
		dates.append(date['group_name'])
		postVolume.append(date['posts_universe'])

	for i in range(len(postVolume)-1, -1, -1):
		if postVolume[i] == 0:
			postVolume.pop()
			dates.pop()
		else:
			break

	timeframeDict.update({'dates':dates})
	timeframeDict.update({'data':postVolume})	

	return timeframeDict

def parseSentiment(data, source):

	timeframeDict = {}

	dates = []
	postVolume = []

	for date in data:

		dates.append(date['group_name'])
		postVolume.append(date['net_sentiment'])

	for i in range(len(postVolume)-1, -1, -1):
		if postVolume[i] == 0:
			dates.pop()
			postVolume.pop()
		else:
			break

	timeframeDict.update({'dates':dates})
	timeframeDict.update({'data':postVolume})	

	return timeframeDict

#Calling Function that Identifies a query + target endpoint and returns a json
#Parameters:
#			query: A properly url encoded string in a format that Infegy Atlas understands. 
#			endpoint: The Infegy Atlas endpoint that you're looking for (eg. Ages, Volume, Entities, etc.)
#			limit: Number of results that you want in a query request. 
def getData(query, endpoint, limit):
	
	#This converts our query into a url_encoded string.
	query = urllib.parse.quote(str(json.dumps(query, indent = 4)))

	#This opens and loads the api.txt file that we created with your API key. 
    #We do this so you don't store your API key in the script.
	text_file = open("api.txt", "r")
	key = text_file.read()
	text_file.close()

	#Base URL. This allows us to pass in a different endpoint (e.g. volume, ages, entities, etc.) To look at all the entities, please reference our API documentation. 
	url = "https://atlas-staging.infegy.com/api/v3/" + endpoint + "?api_key=" + key +  "&limit=" + str(limit) + "&q="+ query

	#The meat of the script. This line of code sends a request to Infegy with all  those parameters and gets the data back in a formatted json.
	data = requests.get(url).json()

	return data['output']

#This function properly formats a query for Infegy Atlas.
#Parameters:
#			queryText: A properly formatted boolean string. For example, if you want to query all posts that mention "Tesla", the query would be "tesla".
#			dateRange: A string saying from when you want data from. For example, if you want data from three months ago to the present, this value would be "3 months ago"
def createQuery(channel, timeframe, groupBy):

	query = {
  "query_fields": ["body","title"],
  "analyze_fields": ["body","title"],
  "filter": [{
    "id": "published",
    "min": timeframe,
    "max": "now",
   },{
    "id": "channels",
    "value": channel
   },{
    "id": "source_age",
    "min": 13,
    "max": 122
   }],
  "group_by": groupBy,
  "group_on": "published"
 }

	return query

def main():

	siteData = {}

	channels = ["twitter", "instagram", "tiktok"]
	timeframes = [("1 day ago", "hour"), ("1 week ago", "hour"), ("1 month ago", "day")]

	for channel in channels:

		dataTypeDictionary = {}

		volumeDict = {}
		sentimentDict = {}
		narrativesDict = {}
		entitiesDict = {}

		for timeframe in timeframes:

			query = createQuery(channel, timeframe[0], timeframe[1])
			volumeQuery = getData(query, "volume", 50)
			tempVolume = parseVolume(volumeQuery, channel)
			volumeDict.update({timeframe[0]:tempVolume})

			sentimentQuery = getData(query, "sentiment", 50)
			tempSentiment = parseSentiment(sentimentQuery, channel)
			sentimentDict.update({timeframe[0]:tempSentiment})

			narrativesQuery = getData(query, "narratives", 50)
			tempNarratives = parseNarratives(narrativesQuery, channel)
			narrativesDict.update({timeframe[0]:tempNarratives})

			entityQuery = getData(query, "entities", 50)
			tempEntities = parseEntities(entityQuery, channel)
			entitiesDict.update({timeframe[0]:tempEntities})

		dataTypeDictionary.update({"volume": volumeDict})
		dataTypeDictionary.update({"sentiment": sentimentDict})
		dataTypeDictionary.update({"narratives": narrativesDict})
		dataTypeDictionary.update({"entities": entitiesDict})

		siteData.update({channel:dataTypeDictionary})

	with open('siteData.json', 'w') as fp:
		json.dump(siteData, fp)

main()


