#encoding=utf-8
import sys
sys.path.append("../")
import jieba
txt = open("F:/BaiduNetdiskDownload/NLP-Project/xinwen/wiki_xinwen_fengci.txt", encoding="utf-8").read()
# txt = open('wiki_xinwen_fenci.txt', encoding="utf-8").read()
#加载停用词表  
stopwords = [line.strip() for line in open(u'中文停用词表.txt', "r", encoding="utf-8").readlines()]  
words  = jieba.lcut(txt)  
counts = {}  
for word in words:  
    #不在停用词表中  
    if word not in stopwords:  
        #不统计字数为一的词  
        if len(word) == 1:  
            continue  
        else:  
            counts[word] = counts.get(word,0) + 1  
items = list(counts.items())  
items.sort(key=lambda x:x[1], reverse=True)
output = open("sorted_words.txt", "w")
for i in range(len(items)):
    word, count = items[i]  
    # print ("{:<10}{:>7}".format(word, count))
    output.write(word + str(count) + "\n")
output.close()