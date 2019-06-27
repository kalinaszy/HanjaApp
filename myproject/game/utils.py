import hashlib
import os
from random import randint

import requests
from bs4 import BeautifulSoup

from game.models import Guess

page = requests.get("http://hanzidb.org/character-list/by-frequency")
page
print(page.status_code)

class Word:
    def __init__(self, character, definition):
        self.character = character
        self.definition = definition
    def __str__(self):
        return self.character + self.definition
    def __repr__(self):
        return self.character + self.definition

def get_content(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def find_words(soup):
    words_list = []
    table_tr = soup.find_all("tr")
    for item in table_tr[1:]:
        a = item.find("a")
        character = a.get_text()
        definition = item.find("span", class_="smmr").get_text()
        word = Word(character=character, definition=definition)
        words_list.append(word)
    return words_list

def runt_this_thing_later():
    url = "http://hanzidb.org/character-list/by-frequency?page={}"
    list_of_all_characters = []
    for i in range(1, 5):
        soup = get_content(url.format(i))
        words_list = find_words(soup)
        for i in range(len(words_list)):
            word = str(words_list[i])
            char = word[0]
            rest_def = word[1:]
            if not rest_def: continue
            random_answer = str(words_list[randint(1, len(words_list)-1)])
            random_answer2 = str(words_list[randint(1, len(words_list)-1)])
            guessed_wrong1 = random_answer[1:]
            guessed_wrong2 = random_answer2[1:]
            list_of_all_characters.append((char, rest_def, guessed_wrong1, guessed_wrong2))
            from .models import Guess
            Guess.objects.create(
                char_character=char,
                guessed_right=rest_def,
                guessed_wrong1=guessed_wrong1,
                guessed_wrong2=guessed_wrong2,
            )
    return list_of_all_characters

# qs = Guess.objects.filter(char_character__isnull=True)
# qs.delete()