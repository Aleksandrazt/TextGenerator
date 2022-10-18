import random

from nltk import bigrams, trigrams
from collections import Counter
from random import choice, choices


ENDING = '!.?'


def file_reader(name):
    with open(name, "r", encoding="utf8") as f:
        text = ''
        for line in f:
            text += line
    return text


def tokenizer(text):
    words = text.split()
    print('Corpus statistics')
    print('All tokens:', len(words))
    print('Unique tokens:', len(set(words)))
    return words


def bigram_search(text):
    words = text.split()
    bigrams_list = list(bigrams(words))
    # print('Number of bigrams:', len(bigrams_list))
    return bigrams_list


def trigram_search(text):
    words = text.split()
    trigram_list = list(trigrams(words))
    # print('Number of trigram:', len(trigram_list))
    return trigram_list


def create_chain(b_list):
    chain = dict()
    for pairs in b_list:
        if pairs[0] not in chain.keys():
            chain[pairs[0]] = [pairs[1]]
        else:
            chain[pairs[0]].append(pairs[1])
    return chain


def create_chain_for_trigram(t_list):
    chain = dict()
    for triple in t_list:
        if triple[0][-1] not in ENDING:
            head = triple[0] + ' ' + triple[1]
            if head not in chain.keys():
                chain[head] = [triple[2]]
            else:
                chain[head].append(triple[2])
    return chain


def showing_chain(chain):
    index = input()
    while index != 'exit':
        print("Head:", index)
        tails = chain.setdefault(index, False)
        if tails:
            freq_dict = Counter(tails)
            for tail in freq_dict.keys():
                print(f"Tail: {tail}    Count: {freq_dict[tail]}")
        else:
            print("Key Error. The requested word is not in the model. Please input another word.")
        print()
        index = input()


def showing(words, kind='t'):
    index = input()
    while index != 'exit':
        try:
            index = int(index)
        except ValueError:
            print('Type Error. Please input an integer.')
        else:
            try:
                if kind == 't':
                    print(words[index])
                elif kind == 'b':
                    print(f'Head: {words[index][0]}     Tail: {words[index][1]}')
            except IndexError:
                print('Index Error. Please input an integer that is in the range of the corpus.')
        print()
        index = input()


def generate(words, chain):
    for _ in range(10):
        first_word = choice(words)
        freq_dict = Counter(chain[first_word])
        sentence = first_word
        for _ in range(9):
            next_word = random.choices(list(freq_dict.keys()), list(freq_dict.values()))
            sentence += ' ' + next_word[0]
            freq_dict = Counter(chain[next_word[0]])
        print(sentence)


def better_generate(chain):
    i = 0
    while i < 10:
        first_word = choice(list(chain.keys()))
        while first_word[0].islower() or first_word[-1] in ENDING or not first_word[0].isalpha():
            first_word = choice(list(chain.keys()))
        freq_dict = Counter(chain[first_word])
        sentence = first_word
        while True:
            circle = 0
            next_word = random.choices(list(freq_dict.keys()), list(freq_dict.values()))
            while len(sentence.split()) < 4 and next_word[0][-1] in ENDING and circle < 10000:
                next_word = random.choices(list(freq_dict.keys()), list(freq_dict.values()))
                circle += 1
            if circle == 10000:
                break
            sentence += ' ' + next_word[0]
            if next_word[0][-1] in ENDING:
                break
            next_word = sentence.split()[-2] + ' ' + sentence.split()[-1]
            freq_dict = Counter(chain[next_word])
        if circle < 10000:
            print(sentence)
            i += 1


my_text = file_reader(input())
my_triple = trigram_search(my_text)
marc_chain = create_chain_for_trigram(my_triple)
better_generate(marc_chain)
