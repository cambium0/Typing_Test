words = []

with open('vocab.txt') as f:
    newline_words = f.readlines()

for word in newline_words:
    words.append(word.strip())


# don't care about words of length < 4 #

def get_start(my_list, start):
    start_index = 0
    for i in range(0, len(my_list)):
        if len(my_list[i]) == start:
            start_index = i
            break

    my_list = my_list[start_index:]
    return my_list


def get_len(w):
    return len(w)


def avg_length(my_list):
    sum = 0
    for word in my_list:
        sum += len(word)
    return int(sum / len(my_list))


def find_thirds(my_list):
    thirds = [0, 0]
    i = 0
    n = 0
    stop = False
    lengths_sum = 0
    check = 5
    for x in words:
        lengths_sum += len(my_list[i])
        try:
            if lengths_sum / (i+1) >= check:
                print(f"length of words[{i+1}] is {len(words[i+1])}")
                thirds[n] = 0 if i == 0 else i-1
                lengths_sum = 0
                check += 1
                n += 1
        except ZeroDivisionError:
            print("ZeroDivisionError")
            pass
        i += 1
    return tuple(thirds)

words.sort(key=get_len)


# start at first occurrence of a 4-letter word #

words = get_start(words, 4)

words_length = len(words)

print(f"words[] has {words_length} elements")

print(f"{words[0:10]}")

max_length = len(words[len(words)-1])

print(f"{words[words_length - 1]} is the longest word in words--it has {max_length} letters.")

print(f"{words[0]} is the shortest word")

avg_length = avg_length(words)

print(f"Average length of words in words[] is {avg_length}")

median_length = len(words[int(words_length/2)])

print(f"The median word length of words is the length of {words[int(words_length/2)]}, {median_length}.")

print(f"Thirds is {find_thirds(words)}")
