from wiktionaryparser import WiktionaryParser
import re

parser = WiktionaryParser()
word_file = open('all_english_mains.txt', 'r')

for row in word_file:
    word_in = re.sub('\n', '', row)
    print(word_in)
    word = parser.fetch(word_in)
    print(word)
    print('Len of data: '+str(len(word))+' partofspeech: ' +
          word[0]['definitions'][0]['partOfSpeech'])
