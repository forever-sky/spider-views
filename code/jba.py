import numpy as np
import os
import glob
import jieba
import wordcloud
import imageio


def jba():
    mk = imageio.imread("chinamap.png")

    # 构建并配置词云对象w，注意要加stopwords集合参数，将不想展示在词云中的词放在stopwords集合里，这里去掉“曹操”和“孔明”两个词
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc',
                            mask=mk,
                            scale=3,
                            collocations=False,
                            stopwords={'jpeg', 'mafengwo', 'View2', '2F1360', 'M00', '2F2', 'net', '2Fw', '2Fq', 'p1', 's10', 's15', 'jpg', 's13', 'by', '2F90', 'E0', 'n1', 'png', 'imageView2', 's11', 'http', 'b1', 's14', '这里', '可以', '时间', '就是', '位于', '没有', '来自', '如果', '其中', '以及', '这个', '雪场', '开放', '自己', '之一', '其实', '八达岭长城', '我们', '一下', 's2', 'Tips', '作为', '地方', '非常', '我们', '还有', '一个', '看到', '一些', '一定', '一些', 's9', 's12', '时候', '除了'})

    # 对来自外部文件的文本进行中文分词，得到string
    path = r"C:\Users\YHUNDEROBOT\Desktop\信息安全\code\mafengwo"
    files = os.listdir(path)
    txts = []
    for file in files:
        position = path + '\\' + file
        print(position)
        with open(position, "r", encoding='utf-8') as f:
            data = f.read()
            txts.append(data)

    txts = ','.join(txts)
    txtlist = jieba.lcut(txts)
    #print (txtlist)
    # print(txts)
    str = []
    for each in txtlist:
        str.append(each)
    string = " ".join(str)
    w.generate(string)
    w.to_file('output8-threekingdoms.png')
