import httplib2
import json


#
# Return geo code location of a location, using the google maps api.
#
def get_geo_code_location(input_string):
    google_api_key = "<API key>"
    location_string = input_string.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/'
           'geocode/json?address=%s&key=%s' % (
           location_string, google_api_key))

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    return result
    # latitude = result['results'][0]['geometry']['location']['lat']
    # longitude = result['results'][0]['geometry']['location']['lng']

    # return (latitude, longitude)

print get_geo_code_location(raw_input())
