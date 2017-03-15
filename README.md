# Geocode Towns
'GeocodeTowns.py' uses the Google Geocoding API to find the latitude and longitude of each location listed in an input CSV file.  The data is then output in a CSV file in the 'GeocodeTowns/Output' directory.  The output file can be easily used in ArcMap or another GIS as 'XY' data.

## Inputs
-The 'InputTownList' should be the file path of your input CSV file.  Your CSV file’s first column should be a list of towns and the second column should be the towns' corresponding state, state abbreviation, or country.

-The 'APIKey' input should be your Google API key.  This key can be obtained for free from Google but there is a limit of 2,500 requests per 24 hour period (1 request = 1 location from your input CSV file).  Instructions on how to obtain a key from google can be found at the following url:
https://developers.google.com/maps/documentation/geocoding/?hl=en_US#api_key

## Example Usage
*from GeocodeTowns import geocodeTowns*  
*InputTownList = "SampleInputList.csv"*  
*APIKey = "YOUR_API_KEY"*  
*geocodeTowns(InputTownList, APIKey)*  

### Sample input CSV file:  

![input](http://henrygeo.com/programming/images/SampleInput.png)

### Sample output CSV file:
![output](http://henrygeo.com/programming/images/SampleOut.png)
