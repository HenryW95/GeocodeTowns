# GeocodingTowns.py example usage
# See ReadMe.txt for more details
#
# Instructions on how to obtain a free key from google can be found at the following url:
#  https://developers.google.com/maps/documentation/geocoding/get-api-key#key

from GeocodeTowns import geocodeTowns

# *** INPUT: ***
InputTownList = "SampleInputList.csv" #Must be a CSV file with the first column containing cities (i.e. Portland or Denver) and the second containing regions (i.e. Oregon or USA)
APIKey="API_KEY_GOES_HERE" #Google API key

geocodeTowns(InputTownList, APIKey)