###########################################################################################
# 'GeocodeTowns.py' Module
#
# Uses Google Maps API to calculate the latitude and longitude of each location listed in
# an input CSV file.
#
# Inputs:
#  -The "InputTownList" should be the file path of your input CSV file.  Your CSV file's 
#      first column should be a list of towns and the second column should be the towns 
#      corresponding state or country.
#  -The "APIKey" input is your unique Google API key. This key can be obtained for free 
#      from Google but as of May 2015 there is a limit of 2,500 requests per 24 hour period 
#      (1 request = 1 location from your input CSV file).  Instructions on how to obtain a 
#      key from google can be found at the following url:
#      https://developers.google.com/maps/documentation/geocoding/get-api-key#key
#
# Output:
#  -A csv file with corresponding lat/long values for each location
#
# Example usage:
# GeocodeTowns.geocodeTowns(InputTownList, APIKey)
#
# Author: Henry Whipps
# Last updated: 3/14/2017
###########################################################################################

from urllib.request import urlopen
import io
import csv

#Primary function:
def geocodeTowns(InputTownList, APIKey):
    #Tests the input path
    TestTownListPath = testInputLocation(InputTownList)
    
    if (TestTownListPath == "OK"):
        
        #Reads the input file and returns a formatted list of towns, regions, and URL text to be plugged into the Google geocoding API URL
        FormattedLocationList = geocodingFormat(InputTownList)
        
        #Returns and parses the XML data from the Google geocoding API
        FormattedXYAndCityData = getCoords(FormattedLocationList, APIKey)
    
        #Creates the output text file containing a list of towns, regions, and long/lat data
        createOutputDataFile(FormattedXYAndCityData)    

#######################################################
# "geocodingFormat" function
# Reads the input file and returns a formatted list 
# of towns to be plugged into the Google geocoding API
# URL.
#######################################################
def geocodingFormat(InputTownList):
    FormattedLocationList=[]
    
    with open(InputTownList, newline='') as csvfile:
        TownListCSV = csv.reader(csvfile, delimiter=',', quotechar="|")
    
        SuccessfulOutputCount=0 #To track the number of successfully formatted locations.
    
        for row in TownListCSV:
            PreliminaryFormat = (row[0])+",+"+(row[1])
            FormattedName = PreliminaryFormat.replace(" ", "+")
            ReadableTown = row[0]
            ReadableRegion = row[1]
            SubList = [FormattedName, ReadableTown, ReadableRegion]
            FormattedLocationList.append(SubList)
            SuccessfulOutputCount+=1

    print ((str(SuccessfulOutputCount))+" entries from your input CSV were successfully read...") #prints the number of lines successfully read.    
    return (FormattedLocationList)

#######################################################
# "getCoords" function:
# Gets lat/long data from Google API and formats data
# in a list.
#######################################################
def getCoords(FormattedLocationList, APIKey):
    try:
        SuccessfulOutputCount=0 #To track the number of successfully parsed locations.
        LatLongTownList = []
        for item in FormattedLocationList: #item[0] is formatted towns, item[1] is towns, item[2] is regions
            GeocodingURL=("https://maps.googleapis.com/maps/api/geocode/xml?address="+(item[0])+"&sensor=false&key="+APIKey)
            TheResponse = urlopen(GeocodingURL, data=None)
            txtFormat = io.TextIOWrapper(TheResponse, encoding='utf-8')
            TheData = txtFormat.read()
                
            #Searches for "<status>" to check if the geocoding was successful:
            StartStatusIndex=TheData.find("<status>")
            EndStatusIndex=TheData.find("</status>")
            GeocodingStatus=(str(TheData[StartStatusIndex+len("<status>"):EndStatusIndex]))
                
            if GeocodingStatus == ("OK"):
                StartIndexLat=TheData.find("<lat>")
                EndIndexLat=TheData.find("</lat>")
            
                StartIndexLng=TheData.find("<lng>")
                EndIndexLng=TheData.find("</lng>")
            
                Latitude=TheData[StartIndexLat+len("<lat>"):EndIndexLat]
                Longitude=TheData[StartIndexLng+len("<lng>"):EndIndexLng]
                City = item[1]
                Region = item[2]
                
                LocalList = [City, Region, str(Latitude), str(Longitude)] #adds city, region, latitude, and longitude to 'LocalList'
                LatLongTownList.append(LocalList)
                SuccessfulOutputCount+=1
            else:
                #prints an error message for any locations that could not be geocoded:
                print ("for entry "+"'"+(item[1])+", "+(item[2])+"'"+", the geocoding data returned from Google resulted in an error: "+"'"+GeocodingStatus+"'")
                
        print(str(SuccessfulOutputCount)+" Long/Lat values were successfully collected from Google geocoding API...")
        return (LatLongTownList)
    except:
        print("An error has occured in the 'getCoords' function")

#######################################################
# "createOutputDataFile" function:
# Creates the output csv file containing a list of 
# towns, regions, and lat/long data
#######################################################
def createOutputDataFile(FormattedXYAndCityData):
    try:
        with open('Output/OutputData.csv', 'w', newline='') as csvfile:
            OutputData = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            OutputData.writerow(['Town','Region','Latitude','Longitude']) #header
            
            SuccessfulOutputCount=0
            for item in FormattedXYAndCityData:
                OutputData.writerow(item)
                SuccessfulOutputCount+=1

        print ((str(SuccessfulOutputCount))+" entries were successfully written to the 'OutputData' file...\nScript complete.")
    except:
        print("An error has occured while opening/writing the 'OutputData' file")

#######################################################
# "testInputLocation" function:
# Tests the input CSV file location by opening the file
# to see if it exists.
#######################################################
def testInputLocation(InputTownList):
    try:
        TestOpen = open(InputTownList, "r")
        TestOpen.close
        Test="OK"
    except:
        Test="Error"
        print("Your town list could not be found. Please check the input file path.")
    return (Test)