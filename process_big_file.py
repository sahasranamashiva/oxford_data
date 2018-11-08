big_file = open('all_english_copy.txt', 'r')
i = 1
for f in big_file:
    big_in_file = open('all_english_words.txt', 'a')
    big_in_file.write(str(i)+','+f)
    i += 1
    print(f)
