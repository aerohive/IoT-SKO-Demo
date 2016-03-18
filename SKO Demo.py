#!/usr/bin/env python

### SKO DEMO
### This Application will poll presence APIs for a specific machine
### This Application uses the Python-Twitter, which must be installed for this functionality to work.
### https://github.com/bear/python-twitter
### You must generate an access token for your twitter account here: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
### Alternatively, you can remove all the Python-Twitter calls.

import requests #to fire off HTTP requests
import datetime #to get the current date, and format dates for the APIs
import csv      #to read & write CSV files
import sys      #to create the progress indicator and print directly to the console.
import time     #to let us sleep things for a timer
import twitter  #to let us make calls to the Twitter API

#---Variables you will need to setup for your application:
#See http://developer.aerohive.com and navigate to 'My Applications'
clientID = "19a087a8"
clientSecret = "daffa2ecd066ef09da98e4527749dee2"
redirectURL = "https://mysite.com"

#-----------------------------------------------------------------------
# create twitter API object
# The below Twitter credentials are hard-coded for the account @whats_up_home
# IT's OK if these are compromised since the account isn't important outside of these tests.
#-----------------------------------------------------------------------
api = twitter.Api(consumer_key="vkjY6dqeQYQMgh5Y7XXLH60y4", consumer_secret="Db7wyKaqY18tCSA97rA47PTl7VIJj1hnc8yE2EoFJ6ciF1Qg7o",
                      access_token_key="2309100307-gQS91nGvGquIEcdCWA3GialQnkYv7QqZ3jlOMgo", access_token_secret="Kb5zqoRxwgHbtf4puKefhZR4FBu8fuv0CsUWbsNpAV3Cj")
#-----------------------------------------------------------------------

#---MAKE API: https://ifttt.com/maker
makeClientSecret = "" #Set this value & uncomment the Make API posts at the bottom to enable IoT Action.
# For more, see the README file with this project!

#------Variables for NG interaction
VaUrl = "https://cloud-va.aerohive.com/xapi"
IrUrl = "https://cloud-ir.aerohive.com/xapi"
baseUrl = VaUrl



minuetsOfData = 5
# These are the headers we will use to interact with the APIs. We will need to set the Autorization Header 
# These are the headers we will use to interact with the APIs. Authorization will need to be updated with the access token.
headers= {'Authorization':'Bearer ', 'X-AH-API-CLIENT-ID':clientID, 'X-AH-API-CLIENT-SECRET':clientSecret, 'X-AH-API-CLIENT-REDIRECT-URI':redirectURL}
#locationFolder = 5433133630928 # 330
hostToTrack = 'xxxxxxxxx'
locationFolder = 123456789
#------------------------------------------------------------------


#------Begin Application
print "\n\nAerohive Monitoring API Demo - Presence"
print "Written by: Daniel O'Rorke (dororke@aerohive.com)"
print "(c) 2016 Aerohive Networks"
print "This application will poll the monitoring API for a client, and notify you when it comes online or offline.\n\n"

#---Prompt user for input:
print "We need your VHM ID and access token to fetch data from your Hive Manager instance."
print "For information on how to get yours, look here: https://developer.aerohive.com/docs/authentication\n\n\n"
print "VHM information can be obtained from NG's About section."
ownerID = raw_input('Please enter your VHM: ')
accessToken = raw_input('Please enter your Access Token: ')
headers["Authorization"] = "Bearer "+accessToken
#minutesToTrackLocationFor = int(raw_input('How many minutes should this run? '))
#secondsToWaitBetweenRequests = int(raw_input('Seconds to wait between updates: '))

print "\nI want to be able to send you a message on Twitter when something happens."
userTwitterName = raw_input("What is your Twitter handle? ")

print "Please make sure the device to track is connected to your network."
neverUsedVariable = raw_input('Press Enter when ready: ')
print "OK, great! Checking for clients that are connected..."

#---Query the Monitoring API for a list of clients.
# Build Client Monitoring API URL
#https://cloud-va.aerohive.com/xapi/v1/location/clients/?ownerId=1265
clientMonURL = "/v1/monitor/clients/"
queryParams = "?ownerId="+ownerID
url = baseUrl+clientMonURL+queryParams
print "Requesting: "+url
# Request data for all clients
response = requests.get(url, headers=headers)
print "Monitoring API response code: "+str(response.status_code)
JSON = response.json()
i = 1
for client in JSON["data"]:
    print str(i)+".\t"+client["hostName"]
    i+=1 #increment the counter
clientNumber = int(raw_input("Enter the client NUMBER to be notified on: ")) #convert the user's input to a number
clientIndex = clientNumber -1 # Remember, indexes start at 0. Our list starts at 1.

hostToTrack = JSON["data"][clientIndex]["hostName"] #Set the client we're looking for.







# Set the end of the time period to now
timeNow = datetime.datetime.now()
#queryParams = '?ownerId='+str(ownerID)
##clientPresenceAPI = '/v1/clientlocation/clientpresence'
##url = baseUrl + clientPresenceAPI + queryParams
monitoringAPI = '/v1/monitor/clients/'
#url = baseUrl + monitoringAPI + queryParams
#
##-----Print a list of current clients to the screen-----
#response = requests.get(url, headers=headers)
#JSON = response.json()
#print "Currently connected:"
#for client in JSON["data"]:
#    print client["clientMac"]+" : "+client["ip"]+"  "+client["hostName"]
#print "========================="


print ("Checking for "+hostToTrack+". The Time is: "+str(timeNow))
# set up a variable to track previous state
oldState = False

runCounter = 0
for i in range (0,1000): #do this 1000 times (~15m)
    now = datetime.datetime.now()
    timeNow = now
    timeBegin = now - datetime.timedelta(minutes=minuetsOfData)
    #queryParams = '?ownerId='+str(ownerID)+'&location='+str(locationFolder)+'&startTime='+timeBegin.isoformat()+UTCoffset+'&endTime='+timeNow.isoformat()+UTCoffset+'&timeunit=FiveMinutes'
    queryParams = '?ownerId='+str(ownerID)
    url = baseUrl + monitoringAPI + queryParams
    #print url
    response = requests.get(url, headers=headers)
    JSON = response.json()
    found = False
    for client in JSON["data"]:
        if client["hostName"] == hostToTrack:
            found = True
            if client["connected"] == True:
                #print str(timeNow)+": "+client["userName"]+" is here."
                if (client["connected"] != oldState and runCounter !=0):
                    print "State Changed. "+client["hostName"]+": Was "+str(oldState)+" Now "+str(client["connected"])
                    #print "Posting to MAKER API..."
                    #response = requests.get(makeURL+"Demo2On/with/key/"+makeClientSecret) #Post LightsOn to Make
                    #response = requests.get(makeURL+"HeaterOn/with/key/"+makeClientSecret) #Post LightsOff to Make
                    #print "MAKER API Response Code: "+str(response.status_code)
                    # Post to twitter =========================================================================
                    print "Posting to Twitter API"
                    stringToPost = "@"+userTwitterName+", "+client["hostName"]+" has entered the building! #LightsOn "+str(timeNow)
                    status = api.PostUpdate(stringToPost)
                    print "Twitter says: "+status.text
                    # End twitter post =========================================================================
                oldState = True
            else:
                #print str(timeNow)+": "+client["userName"]+" is here."
                if (client["connected"] != oldState and runCounter !=0):
                    print "State Changed. "+client["hostName"]+": Was "+str(oldState)+" Now "+str(client["connected"])
                    #response = requests.get(makeURL+"Demo2Off/with/key/"+makeClientSecret) #Post LightsOff to Make
                    #response = requests.get(makeURL+"HeaterOff/with/key/"+makeClientSecret) #Post LightsOff to Make
                    # Post to twitter =========================================================================
                    stringToPost = "@"+userTwitterName+", "+client["hostName"]+" has left the building! #LightsOn "+str(timeNow)
                    status = api.PostUpdate(stringToPost)
                    print status.text
                    # End twitter post =========================================================================
                oldState = False
    if found == False:    
        #print "No matches."
        if (oldState == True and runCounter!=0):
            print "State Changed. "+hostToTrack+": Was "+str(oldState)+" Now False"
            #print "Posting to MAKER API..."
            #response = requests.get(makeURL+"Demo2Off/with/key/"+makeClientSecret) #Post LightsOff to Make
            #response = requests.get(makeURL+"HeaterOff/with/key/"+makeClientSecret) #Post LightsOff to Make
            #print "MAKER API Response Code: "+str(response.status_code)
            # Post to twitter =========================================================================
            stringToPost = "@"+userTwitterName+", "+hostToTrack+" has left the building! #LightsOff "+str(timeNow)
            status = api.PostUpdate(stringToPost)
            print status.text
            # End twitter post =========================================================================
        oldState = False
    time.sleep(1)
    runCounter += 1