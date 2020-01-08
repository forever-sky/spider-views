import requests
from bs4 import BeautifulSoup
import json
import re
import os


headers = {
    "Host" : "www.mafengwo.cn",
    "Connection" : "keep-alive",
    "Pragma" : "no-cache",
    "Cache-Control" : "no-cache",
    "Accept" : "*/*",
    "X-Requested-With" : "XMLHttpRequest",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Referer" : "http://www.mafengwo.cn/gonglve/ziyouxing/mdd_10065/",
    "Accept-Language" : "en,zh-CN;q=0.8,zh;q=0.6",
}

def getpage():
    file_path = os.getcwd() + '\\' + "mafengwo"
    if os.path.exists(file_path):
            print('当前文件已经存在，删除之后再进行插入')
            import shutil
            shutil.rmtree(r"C:\Users\pc\Desktop\wordcloud\mafengwo")
            print ('删除完毕，正在重新创建')
    os.mkdir('./mafengwo')
    base_url = 'http://www.mafengwo.cn/gonglve/ziyouxing/list/list_page?mddid=10065&page=1'
    response = requests.get(base_url,headers=headers)
    json_html = json.loads(response.text)
    html = json_html["html"]
    # print(html)
    html = BeautifulSoup(html,'lxml')
    max_page = html.select('span.count')[0].text
    #用正则把页数从字符串中抽取出来
    pattern = re.compile(r'\d+')
    res = pattern.search(max_page)
    max_number = res.group()
    for i in range(1,int(max_number)+1):
        base_url = 'http://www.mafengwo.cn/gonglve/ziyouxing/list/list_page?mddid=10065&page=%d'
        response = requests.get(base_url % i,headers=headers)
        print('正在抓取第%s页' % i)
        json_html = json.loads(response.text)
        html = json_html["html"]
        html = BeautifulSoup(html, 'lxml')
        list_link = html.select('a._j_item')
        for link in list_link:
            info = link.get('href')
            info_link = 'http://www.mafengwo.cn' + info
            # print(info_link)
            details_page(info_link)


def details_page(info_link):
    response = requests.get(info_link,headers=headers)
    html = BeautifulSoup(response.text,'lxml')
    title = html.select('div.l-topic h1')[0].text
    name = html.select('span.name')
    if name == []:
        name = '匿名'
    else:
        name = name[0].text.strip()
    brief = html.select('div.l-topic > p')
    if brief == []:
        brief = '无简介'
    else:
        brief = brief[0].text.strip()
    content_list = html.select('div.f-block')
    text = ['\n']
    #循环内容列表把左右空格去掉 再用换行拼接成字符串
    for i in content_list:
        centent = i.text.strip() 
        text.append(centent)
    content_text = '\n'.join(text)
    img_list = html.select('img._j_lazyload')
    img = ['\n']
    for n in img_list:
        src = n.get('data-rt-src') 
        img.append(src)
    img_src = '\n'.join(img)
    #去除名字中的非法字符
    res = r"[\/\\\:\*\?\"\<\>\|]"
    title = re.sub(res, "_", title)
    # print(title,name,brief,content_text,img_src)
    item = {
        'title': title,
        'name': name,
        'brief': '\n'+ brief,
        'content_text': content_text,
        'img_src': img_src,
    }
    storage(item)

def storage(item):

    # 以文章标题命名存成TXT
    with open('./mafengwo/' + item['title'] + '.txt','w',encoding = 'utf-8') as f:
        txt_list = []
        txt_list.append(''.join([item['title'], item['name'],item['brief'],item['content_text'],item['img_src']]))
        f.writelines(txt_list)


if __name__ == '__main__':
    getpage()