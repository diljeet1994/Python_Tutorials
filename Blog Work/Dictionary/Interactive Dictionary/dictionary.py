# json library helps to load json data into python
import json
# difflib module provides classes and functions for comparing sequences.
# get_close_matches : Return a list of the best 'good enough' matches. word is a sequence for which close matches are desired
# (typically a string),and possibilities is a list of sequences against which to match word (typically a list of strings).
from difflib import get_close_matches

#loading data from json file into a dict words_data
words_data = json.load(open("words.json"))


def word_meaning(word):
    # translate the word in lowercase, since all the words in json file is in lower case.
    word = word.lower()
    # check if word exists in words_data dict, If yes than return the value of that word by using d[key] method of dictionary,
    if word in words_data:
        return words_data[word]
    # tile() is a string method which converts the First letter of every word in uppercase, since some words have first letter in uppercase
    # so we will be checking it in below mentioned way as well.
    elif word.title() in words_data:
        return words_data[word.title()]
    # some words are completely in uppercase, such as GIMP
    elif word.upper() in words_data:
        return words_data[word.upper()]
    # now lets say, you wanted to find meaning of word 'canopy' but somehow you misspelled it to 'canpy', then,
    # get_close_matches() function will find matching keys from words_data dict and we can use them to ask users if
    # they meant another word from the returned list of similar_words_list
    elif len(get_close_matches(word, words_data.keys())) >0:
        # getting similar list of words and converting them to string format
        similar_words_list = list(map(str, get_close_matches(word, words_data.keys())))
        # asking users if they mean any other word form the list of similar_words_list
        ans = input("Did you mean %s instead? Enter 'Y' If yes or 'N' if No " % similar_words_list)
        if ans.lower() == 'y':
            # asking user to select the word
            index = input("Enter the position number of word to select the word. Ex 1 or 2 or 3 : ")
            return word_meaning(get_close_matches(word, words_data.keys())[int(index)-1])
        elif ans.lower() == 'n':
            print("Word Doesnt exists. Please double check it!!!")
        else:
            print("Sorry, We don't understand you!!!!")
    else:
        print("Word Doesnt exists. Please double check it!!!")

# ask user for a word
word = input("Enter a word :")
# print the meaning of word returned by the function word_meaning
print(word_meaning(word))
