import requests
import re
from bs4 import BeautifulSoup
import sys
import MySQLdb

# from google.cloud import firestore

# db = firestore.Client()

conn = MySQLdb.connect(host='localhost', port=3306,
                       user='root', password='astuvastu')
cur = conn.cursor()

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
    if len(posList) > 0:
        return posList[0].get_text()
    else:
        return ''


# wordList_file = open('word_list.txt', 'r')
wordList_file = open(sys.argv[1], 'r')
wordList_not_done = open('wordList_NA.txt', 'a')
# wordList_Output = open('output/wordList_output.txt', 'a')


def word_details(index, word):
    wordList_not_done = open('wordList_NA.txt', 'a')
    print('We are processing--> ' + word)
    wordContent = requests.get(
        'https://en.oxforddictionaries.com/definition/'+word).content
    searchList = BeautifulSoup(wordContent, 'lxml').find_all(
        'h2', {'class': 'searchHeading'})

    if len(searchList) == 0:
        if getPhonetic(wordContent) == 0:
            # print('<-*-*-*-*-*-*-*-*-*-*->')
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
        if fPOS != 'abbreviation':
            # doc_ref = db.collection(u'word').document(word)
            # doc_ref.set({
            #     u'index': index,
            #     u'Phonetic': fPhonetic,
            #     u'Origin': fOrigin,
            #     u'POS': fPOS
            # })
            insert_statement = "INSERT INTO ashu.word_bank_a(word,phonetic,origin,part_of_speech) values(\"" + \
                word+"\",\""+fPhonetic+"\",\""+fOrigin+"\",\""+fPOS+"\")"
            print(insert_statement)
            cur.execute(insert_statement)
            conn.commit()
        else:
            wordList_not_done.write(word+'\n')
            wordList_not_done.close()

    else:
        wordList_not_done.write(word+'\n')
        wordList_not_done.close()


for row in wordList_file:
    word = re.sub('\n', '', row.split(',')[1])
    index = int(row.split(',')[0])
    word_details(index, word)
