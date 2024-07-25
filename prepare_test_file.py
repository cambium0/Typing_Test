from random import randint, choice


def create_json():
    conjunctions = []
    prepositions = []
    pronouns = []
    words = []
    return_words = ""
    conjunctions_string = ""
    prepositions_string = ""
    pronouns_string = ""
    words_string = ""
    json_string = ""

    with open('conjunctions.txt') as f:
        file_lines = f.read()

    conjunctions = file_lines.split('\n')
    conjunctions = conjunctions[:-1]
    # print(f"conjunctions[] is {conjunctions}")

    with open('prepositions.txt') as f:
        file_lines = f.read()

    prepositions = file_lines.split('\n')
    prepositions = prepositions[:-1]

    with open('pronouns.txt') as f:
        file_lines = f.read()

    pronouns = file_lines.split('\n')
    pronouns = pronouns[:-1]

    try:
        with open('vocab.txt') as f:
            words = f.read().splitlines()
    except:
        print("")

    json_string = '{"data":{"conjunctions":'

    conjunctions_string = '['

    for word in conjunctions:
        conjunctions_string += '"' + word + '", '

    conjunctions_string = conjunctions_string[:-2]

    conjunctions_string += '], '

    json_string += conjunctions_string

    prepositions_string = '"prepositions":['

    for word in prepositions:
        prepositions_string += '"' + word + '", '

    prepositions_string = prepositions_string[:-2]

    prepositions_string += '], '

    json_string += prepositions_string

    pronouns_string = '"pronouns":['

    for word in pronouns:
        pronouns_string += '"' + word + '", '

    pronouns_string = pronouns_string[:-2]

    pronouns_string += '],'

    json_string += pronouns_string

    words_string = '"vocab":['

    for word in words:
        words_string += '"' + word + '", '

    words_string = words_string[:-2]

    words_string += ']}}'

    json_string += words_string

    return json_string


vocab_words = []
thirds = []
test_text = ""
difficulty = "moderate"

# sort vocab by length ##


def get_length(w):
    return len(w)


def find_thirds(my_list, num_check):
    global thirds
    thirds = [0, 0]
    i = 0
    n = 0
    stop = False
    lengths_sum = 0

    for x in my_list:
        lengths_sum += len(my_list[i])
        try:
            if lengths_sum / (i + 1) >= num_check:
                thirds[n] = 0 if i == 0 else i - 1
                lengths_sum = 0
                num_check += 1
                n += 1
        except ZeroDivisionError:
            pass
        i += 1
    return tuple(thirds)


def get_start(my_list, start):
    start_index = 0
    for i in range(0, len(my_list)):
        if len(my_list[i]) == start:
            start_index = i
            break

    my_list = my_list[start_index:]
    return my_list


def get_words_word(indexes, diff_level):
    ret_word = ""
    if diff_level == "easy":
        (a, b, c) = 7, 8, 10
    elif diff_level == "moderate":
        (a, b, c) = 6, 8, 10
    elif diff_level == 'hard':
        (a, b, c) = 3, 7, 10
    result = randint(1, 10)
    if result < b:
        ret_word = choice(vocab_words[:thirds[0]])
    elif a < result < c:
        ret_word = choice(vocab_words[thirds[0]:thirds[1]])
    else:
        ret_word = choice(vocab_words[thirds[1]:])
    return ret_word


def make_test_text(words, diff):
    global vocab_words, thirds, test_text
    test_text = ""
    vocab = words['data']['vocab']

    vocab.sort(key=get_length)

    vocab_words = get_start(vocab, 4)

    thirds = find_thirds(vocab_words, 5)

    ## build 200-random-word list from the four lists in data ##

    check = "go"
    counter = 0

    while check != "stop":
        chooser = randint(3, 5)  # 4--preposition, 5--pronoun, 6--conjunction
        for i in range(0, chooser + 1):
            if i == chooser:
                if chooser == 3:
                    word = choice(words['data']['prepositions'])
                elif chooser == 4:
                    word = choice(words['data']['pronouns'])
                else:
                    word = get_words_word(thirds, diff)
            else:
                word = get_words_word(thirds, diff)
            counter += 1
            test_text += word + " "
            if counter == 199:
                check = "stop"
                break
    return test_text

