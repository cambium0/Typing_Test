import requests
from random import choice, randint
import os.path
from typing_gui import TypingTester as tt
import prepare_test_file as ptf
import json

data = ""
headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept":"text/html,application/xhtml+xml,applications/json/application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language":"en-US,en;q=0.5",
    "Accept-Encoding":"gzip, deflate, br",
    "Referer":"https://www.google.com/",
    "upgrade-insecure-requests":"1",
    "sec-fetch-dest":"document",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"cross-site",
    "te":"trailers",
    "x-forwarded-proto":"https",
    "x-https":"on"}                        #X-Forwarded-For:98.46.168.233


## if first run, write downloaded lists to local files ##

if (os.path.isfile('conjunctions.txt') and os.path.isfile('pronouns.txt') and
        os.path.isfile('prepositions.txt') and os.path.isfile('vocab.txt')):
    print("vocab files exist")  # ... write up the json from the local files then call json() on the string, I *think*
    raw_file = ptf.create_json()
    words = json.loads(raw_file)
else:
    response = requests.get('http://www.cambiumsoftware.com/wordlist_api/words.cgi', headers=headers)
    difficulty = ""  # set by gui

    if response.status_code != 200:
        print("error, status code " + str(response.text))
        print("Sorry, but the vocabulary files could not be downloaded and they are not stored on your computer.")
        print("You'll have to fix one or both of these issues before you can use the program. Thank you.")
        exit(1)
    else:
        words = response.json()
        with open('conjunctions.txt', encoding='utf-8', mode='w') as f:
            for word in words['data']['conjunctions']:
                f.write(word + "\n")

        with open('prepositions.txt', encoding='utf-8', mode='w') as f:
            for word in words['data']['prepositions']:
                f.write(word + "\n")

        with open('pronouns.txt', encoding='utf-8', mode='w') as f:
            for word in words['data']['pronouns']:
                f.write(word + "\n")

        with open('vocab.txt', encoding='utf-8', mode='w') as f:
            for word in words['data']['vocab']:
                f.write(word + "\n")


test_text = ptf.make_test_text(words, "moderate")
# ok going to make a gui object, just because

test_gui = tt(test_text, words)
test_gui.input.focus()

tt.window.mainloop()

