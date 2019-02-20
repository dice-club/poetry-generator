# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install

import  requests
import json
import random

# Using the Oxford Dictionaries API
# app_id = '9bced530'
# app_key = '7131a452260273b5655c5e3e2ca2b1ec'
# language = 'en'
#
# word_id = 'Ace'
# url_oxford = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'  + language + '/'  + word_id.lower()
# #url Normalized frequency
# urlFR = 'https://od-api.oxforddictionaries.com:443/api/v1/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
#
# r = requests.get(url_oxford, headers = {'app_id' : app_id, 'app_key' : app_key})
#
# print("code {}\n".format(r.status_code))
# print("text \n" + r.text)
# print("json \n" + json.dumps(r.json()))

# Using the Datamuse api
cities = ["Fiery"]#
for city in cities:
    words = [city]

    while len(words) < 125:
        url_datamuse = 'https://api.datamuse.com/words?rel_bga=' + words[len(words)-1]
        request_json = requests.get(url_datamuse).json()

        if len(request_json) > 1:
            words.append(request_json[random.randint(0, len(request_json)-1)]['word'])
        else: # Add a random word instead, placeholder for now
            words.append(words[0])

    for word in words:
        print(word)

    file_index = str(random.randint(0, 10000000))
    poem_file = open(city + ".txt", "w")
    for word in words:
        poem_file.write(word + " ")
        if random.randint(0, 5) == 0:
            poem_file.write("\n")
    poem_file.close()
