#encoding=utf-8
import sys
sys.path.append("../")
import jieba
import sys
import time
if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
#加载停用词表
stops = open(u'中文停用词表.txt', "r", encoding="utf-8").readlines()
stop = [line.strip() for line in stops]
# 读取文本

f = open(input, "r", encoding="utf-8")
output= open(output, "w", encoding="utf-8")
i = 0
while True:
    s = f.readline()
    i = i + 1
    if s == "":
        break
# s = f.read()
#s="朝鲜半岛西北部古元古代高温变质-深熔作用:宏观和微观岩石学以及锆石U-Pb年代学制约"
#分词
    segs = jieba.cut(s, cut_all=False)
    #print u"[精确模式]: ", "  ".join(segs)

    #分词并标注词性
    # segs = pseg.cut(s)
    final = ''
    for seg in segs:
        #去停用词
        if seg not in stop:
           #去数词和去字符串
           # if flag !='m' and flag !='x':
                #输出分词
                output.write(seg + " ")
                # final +=' '+ seg
                #输出分词带词性
                # final +=' '+ seg+'/'+flag
    output.write("\n")
    if i % 10000 == 0:
        print(i, time.localtime(time.time()))
output.close()