import requests
import json
import random

def getFollowingWordWithSyllables(prompt_word, num_syllables):
    url_following = 'https://api.datamuse.com/words?rel_bga=' + str(prompt_word) + "&md=s"
    request_json = requests.get(url_following).json()

    if len(request_json) == 0:
        print("Failed to find a related word to " + str(prompt_word))
        return -1
    random_pos = random.randint(0, len(request_json) - 1)
    json_syllables = request_json[random_pos]['numSyllables']
    attempts = 0
    while json_syllables != num_syllables:
        random_pos = random.randint(0, len(request_json) - 1)
        json_syllables = request_json[random_pos]['numSyllables']
        attempts += 1
        if attempts >= 2 * len(request_json):
            # print("After " + str(attempts) + " attempts, found no word following " + str(prompt_word) + " with " + str(num_syllables) + " syllables.")
            return -1
    return request_json[random_pos]['word']

def getLineWithSyllables(prompt_word, prompt_word_syllables, total_syllables):
    prompt_word = str(prompt_word)
    words = [prompt_word.capitalize()]
    syllables = prompt_word_syllables

    while syllables < total_syllables:
        random_syllables = 100
        next_word = ""
        while next_word == "i" or next_word == "." or next_word == -1 or syllables + random_syllables > total_syllables:
            random_syllables = random.randint(0, 5)
            next_word = getFollowingWordWithSyllables(words[len(words) - 1], random_syllables)
        syllables += random_syllables
        words.append(next_word)
        print(words)

    return words

def syllables(word):
    url = 'https://api.datamuse.com/words?max=1&sp=' + str(word) + '&qe=sp&md=s'
    request_json = requests.get(url).json()
    syllables = request_json[0]['numSyllables']
    return syllables

def printLine(words):
    printed = ""
    for word in words:
        printed += word + " "
    print(printed)

def saveWordsIntoFile(words, file_name):
    poem_file = open(file_name, "a+")
    for word in words:
        poem_file.write(word + " ")
    poem_file.write("\n")
    poem_file.close()

seed = "Formal"

# first line begins with the seed
line1 = getLineWithSyllables(seed, syllables(seed), 5)
print("FIRST LINE DONE")

# second and third lines begin with a related word to the seed
url_rel = 'https://api.datamuse.com/words?ml=' + str(seed)
request_json_rel = requests.get(url_rel).json()

random_pos = random.randint(0, len(request_json_rel) - 1)
next_word = request_json_rel[random_pos]['word']
while next_word == 'I' or next_word == ".":
    random_pos = random.randint(0, len(request_json_rel) - 1)
    next_word = request_json_rel[random_pos]['word']


line2 = getLineWithSyllables(next_word, syllables(next_word), 7)
print("SECOND LINE DONE")

url_following = 'https://api.datamuse.com/words?rel_bga=' + str(line2[len(line2) - 1])
request_json = requests.get(url_following).json()

random_pos = random.randint(0, len(request_json) - 1)
next_word = request_json[random_pos]['word']
while next_word == 'I' or next_word == ".":
    random_pos = random.randint(0, len(request_json) - 1)
    next_word = request_json[random_pos]['word'] == 'I'

line3 = getLineWithSyllables(next_word, syllables(next_word), 5)
print("THIRD LINE DONE")

print()
printLine(line1)
printLine(line2)
printLine(line3)

print()
print("Poem finished!")
print()

file_name = seed + str(random.randint(0, 1000)) + ".txt"

saveWordsIntoFile(line1, file_name)
saveWordsIntoFile(line2, file_name)
saveWordsIntoFile(line3, file_name)
