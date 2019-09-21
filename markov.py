from dictogram import Dictogram
from rando_word import random_word
import sys
import os
import random
import re
import sample


"""
For small to medium sized corpuses, the MarkovChain will be built quickly,
however we may want to refactor to accomadate cached tokenization and token retrival.
The web app should quickly generate sentences.

"""


class MarkovChain:

    def __init__(self, filename):
        """Initializes MarkovChain and saves the filename that needs to be utilized """
        self.filename = filename

    def cleanup(self, filename):
        """ takes in a text file, opens it and cleans text using regex. outputs
        string of cleaned text """
        with open(filename, 'r') as file:
            # print(source_text.read())
            no_chapters = re.sub('[A-Z]{3,}', ' ', file.read())
            remove_periods = re.sub('(\s\.){4,}', '', no_chapters)
            cleaned_text = re.sub('\*', '', remove_periods)
        return cleaned_text



    def tokenize(self, text):
        """ takes in cleaned text as string and makes it into a list of tokens """
        return text.split()

    def build_markov(self):
        dict = {}
        with open('holmes-text.txt') as file:
            corpus = file.read().split()

        i=0
        while i+1 < len(corpus):
            word = corpus[i]
            if dict.get(word) == None:
                next_word = corpus[i+1]
                list = [next_word]
                histogram = Dictogram(list)
                dict[word] = histogram
            else:
                next_word = corpus[i+1]
                dict.get(word).add_count(next_word)
            i += 1

        return dict


    def nth_order_markov_chain(self, order, text_list):
        """ this function takes in a word and checks to see what words come after it
        to determine the word sequence for our generated markov chain"""
        markov_dict = dict()
        # for each word in list, key is word and value is dictogram
        for index in range(len(text_list) - order):
            # text_list[index] should be our word from list, and we're slicing based on the order of the markov chain
            window = tuple(text_list[index: index + order])
            # check if key is stored already
            if window in markov_dict:
                # if it is, then append it to the existing histogram
                # NOTE: Instead of going through the corpus repeatedly, lets save text_list[index + order] in scope
                markov_dict[window].add_count([text_list[index + order]])
            else:
                # if not, create new entry with window as key and dictogram as value
                markov_dict[window] = Dictogram([text_list[index + order]])
        # return dictionary
        return markov_dict


    def start_token(self, dictionary):
        """ Get words that can start a sentence; this method is O(n) worst case
        because one must check every word in the corpus"""
        start_tokens = []
        for key in dictionary:

            # TODO: Can refactor to small one liner function isStartOfSentence
            if key[0].islower() is False and key[0].endswith('.') is False:
                start_tokens.append(key)

        token = random.choice(start_tokens)
        return token

    def stop_token(self, dictionary):
        """ Get words that can end a sentence"""
        stop_tokens = []
        for key, value in dictionary.items():
            # the key number must be changed depending on order number
            if key[2].endswith('.') or key[2].endswith('?'):
                # print("word with .", key)
                stop_tokens.append(key)
        return stop_tokens

    def create_sentence(self, start_token, stop_tokens, dictionary):
        """ takes dictionary, start and end tokens and makes a sentence """
        # create sentence and add first word
        sentence = []
        # this is hard coded; must be changed to fit the order number; currently third
        (word1, word2, word3) = start_token
        sentence.append(word1)
        sentence.append(word2)
        sentence.append(word3)
        # print("There should be three words", sentence)

        current_token = start_token
        # print("This is my dictionary", dictionary)
        # stop when current_token is a stop token
        while current_token not in stop_tokens or len(sentence) <= 8:
            for key, value in dictionary.items():
                if key == current_token:

                    # sample from histogram of values
                    cumulative = sample.cumulative_distribution(value)
                    sample_word = sample.sample(cumulative)
                    # add new sample to sentence_list
                    sentence.append(sample_word)
                    # assign second word of key and value to current token
                    # this is hard coded; must be changed to fit the order number
                    # I am unpacking the current token
                    (current_token_one, current_token_two, current_token_three) = current_token
                    current_token = (current_token_two, current_token_three, sample_word)
                    # get out of for loop and start process over
                    break
        return sentence


def generate_lincoln_tweet(filename):
    """ Main function for generating the tweet text based on given filename """

    markov = MarkovChain(filename)
    cleaned_text = markov.cleanup(markov.filename)

    tokenized_text = markov.tokenize(cleaned_text)
    third_order_markov = markov.nth_order_markov_chain(3, tokenized_text)
    # print(second_order_markov)

    first_word = markov.start_token(third_order_markov)
    end_words = markov.stop_token(third_order_markov)
    markov_list = markov.create_sentence(first_word, end_words, third_order_markov)
    markov_sentence = " ".join(markov_list)
    print(markov_sentence)
    return markov_sentence



if __name__ == '__main__':

    """ For local testing purposes run the markov.py file to print sample tweet """
    # Use Qoutes or Think and Grow RICH
    # Think and Grow rich is in need of text cleaning
    # Perhaps research methods of text cleaning books

    # markov = MarkovChain('think-and-grow-rich.txt')
    # markov = MarkovChain('harry_potter_7.txt')
    markov = MarkovChain('harry_potter_7.txt')
    cleaned_text = markov.cleanup(markov.filename)

    tokenized_text = markov.tokenize(cleaned_text)
    third_order_markov = markov.nth_order_markov_chain(3, tokenized_text)
    # print(second_order_markov)

    first_word = markov.start_token(third_order_markov)
    end_words = markov.stop_token(third_order_markov)
    markov_list = markov.create_sentence(first_word, end_words, third_order_markov)
    markov_sentence = " ".join(markov_list)
    print(markov_sentence)

    # markov = MarkovChain()
    # dict = markov.build_markov()
    # markov.generate_sentence(dict)
