import requests
import re
from bs4 import BeautifulSoup
import sys

from google.cloud import firestore

db = firestore.Client()


def getPhonetic(wordContent):
    phoneticList = BeautifulSoup(wordContent, 'lxml').find_all(
        'span', {'class': 'phoneticspelling'})
    if len(phoneticList) > 0:
        return BeautifulSoup(wordContent, 'lxml').find_all('span', {'class': 'phoneticspelling'})[0].get_text()
    else:
        return 0


def getOrigin(wordContent):
    originList = BeautifulSoup(wordContent, 'lxml').find_all(
        'div', {'class': 'senseInnerWrapper'})
    if len(originList) > 0:
        return originList[-1].findChildren('p', recursive=True)[0].get_text()
    else:
        return 0


def getPartOfSpeech(wordContent):
    posList = BeautifulSoup(wordContent, 'lxml').find_all(
        'span', {'class': 'pos'})
    return posList[0].get_text()


# wordList_file = open('word_list.txt', 'r')
wordList_file = open(sys.argv[1], 'r')
# wordList_Output = open('output/wordList_output.txt', 'a')


def word_details(word):
    print('We are processing--> ' + word)
    wordContent = requests.get(
        'https://en.oxforddictionaries.com/definition/'+word).content
    searchList = BeautifulSoup(wordContent, 'lxml').find_all(
        'h2', {'class': 'searchHeading'})

    if len(searchList) >= 0:
        if getPhonetic(wordContent) == 0:
            fPhonetic = ''
        else:
            # print('This is phonetic--> '+getPhonetic(wordContent))
            fPhonetic = getPhonetic(wordContent)
            # wordList_Output.write(getPhonetic(wordContent))

        if getOrigin(wordContent) == 0:
            # print('<==                                             ==>')
            fOrigin = ''
        else:
            # print('=====>'+getOrigin(wordContent))
            fOrigin = getOrigin(wordContent)
            # wordList_Output.write(getOrigin(wordContent))

        # print('Part of Speech -->'+getPartOfSpeech(wordContent))
        fPOS = getPartOfSpeech(wordContent)
        # wordList_Output.write(getPartOfSpeech(wordContent))
        doc_ref = db.collection(u'word').document(word)
        doc_ref.set({
            u'Phonetic': fPhonetic,
            u'Origin': fOrigin,
            u'POS': fPOS
        })
    else:
        return ''


for row in wordList_file:
    word = re.sub('\n', '', row)
    word_details(word)
