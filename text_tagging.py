#!/usr/bin/env python
import sys
import requests
import os
import json
calais_url = 'https://api.thomsonreuters.com/permid/calais'
access_token = '<Access token>'


def get_tags_util(input_string, headers):
    response = requests.post(calais_url, data=input_string, headers=headers, timeout=80)
    # print ('status code: %s' % response.status_code)
    content = json.loads(response.text)

    topics = []
    for key, value in content.items():
        if '_typeGroup' in value and value['_typeGroup'] == 'topics':
            topics.append(str(value['name']))

    if response.status_code == 200:
        return topics


#
# Take a text/paragraph as input from the user, and return the relevant topics, the text is related to.
#
# Input: Welcome to Bangalore!
# Output: ['Religion_Belief', 'Technology_Internet', 'Sports', 'Hospitality_Recreation', 'Business_Finance']
#
def get_tags(input_string):
    try:
        headers = {'X-AG-Access-Token': access_token, 'Content-Type': 'text/raw', 'outputformat': 'application/json'}
        tags = get_tags_util(input_string, headers)
        return tags

    except Exception, e:
        print 'Error in connect ', e

print get_tags(raw_input())
