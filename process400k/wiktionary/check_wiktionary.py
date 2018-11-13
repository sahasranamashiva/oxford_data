import requests
import re
import json
import sys
import MySQLdb

conn = MySQLdb.connect(host='localhost', port=3306,
                       user='root', password='astuvastu')
cur = conn.cursor()

word_file = open(sys.argv[1], 'r')

# word_needs = open('word_needs.txt','a')
# word_na = open('word_na_1.txt', 'a')
for row in word_file:
    word_in = re.sub('\n','',row)
    url = 'https://en.wiktionary.org/w/api.php?action=query&titles=' + \
        word_in+'&format=json'
    # print(url)
    req = requests.get(url)
    req_content = req.content.decode("utf-8")
    d = json.loads(req_content)
    j = d["query"]["pages"].keys()
    if '-1' in j:
        word_avail = 'False'
        print(word_in+" : "+"False")
    else:
        word_avail = 'True'
        print(word_in+" : "+"True")
    
    insert_state = 'INSERT INTO  ashu.wiktionary_table VALUES(\''+word_in+'\',\''+word_avail+'\');'
    print(insert_state)
    cur.execute(insert_state)
    conn.commit()
