from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os
from goto import with_goto
import analyse
import argparse
import configparser

headers = {
    "Referer": "http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10156.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

root_dir = os.path.dirname(os.path.abspath('.'))
cf = configparser.ConfigParser()
cf.read(root_dir + "\\config.ini")
sec = cf.sections()
path = cf.get("chromedriver-path", "path")
if path is None:
    print("配置文件有误")
    sys.exit()
# chrome_driver = "C:\\Users\\YHUNDEROBOT\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
chrome_driver = path
opt = webdriver.ChromeOptions()


def get_proxy():  # 获取代理ip
    return requests.get("http://47.97.160.248:5010/get/").json()


def get_city():
    city_list = []
    city_url = []
    proxy = get_proxy().get("proxy")
    opt.add_argument(f"–proxy-server=http://{proxy}")
    driver = webdriver.Chrome(chrome_driver, chrome_options=opt)
    driver.get("http://www.mafengwo.cn/mdd/")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    city_list = soup.find(attrs={"class": "hot-list clearfix"}).find_all('dd')
    for i in range(0, len(city_list)):
        for j in range(0, len(city_list[i].find_all('a'))):
            city_url.append("http://www.mafengwo.cn" + city_list[i].find_all('a')[j].get('href'))

    city_list = soup.find(attrs={"class": "hot-list clearfix hide"}).find_all('dd')
    for i in range(0, len(city_list)):
        for j in range(0, len(city_list[i].find_all('a'))):
            city_url.append("http://www.mafengwo.cn" + city_list[i].find_all('a')[j].get('href'))

    return city_url


@with_goto
def get_city_food_info(city_url):  # 爬取热门城市的top10美食及分数,并保存数据到xlsx文件中
    city_food = {}
    city_url = list(set(city_url))
    label .begin

    proxy = get_proxy().get("proxy")
    opt.add_argument(f"–proxy-server=http://{proxy}")
    driver = webdriver.Chrome(chrome_driver, chrome_options=opt)
    if len(city_url) == 0:
        goto .end

    for i in city_url:

        s = re.compile(".*?([0-9]{0,}).html")
        try:

            url = "http://www.mafengwo.cn/cy/" + str(re.findall(s, i)[0]) + "/gonglve.html"
        except:
            continue
        print(url)
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        s = re.compile(r"\"tese.html\">(.*?)特色美食排行")
        try:

            name = soup.find(attrs={"class": "hd"}).find('a').text
            name = str(re.findall(s, html)[0])
        except Exception as e:
            city_url.remove(i)
            continue
        try:
            city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top1"}).find('a').get("title"): soup.find(attrs={"class": "rank-item top1"}).find('a').find(attrs={"class": "num-orange"}).text})
            city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top2"}).find('a').get("title"): soup.find(attrs={"class": "rank-item top2"}).find('a').find(attrs={"class": "num-orange"}).text})
        except Exception as e:
            city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top1"}).find('a').get("title"): 0})
            city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top2"}).find('a').get("title"): 0})

        for j in soup.find_all(attrs={"class": "rank-item top3"}):
            for m in j.find_all('a'):
                try:
                    city_food.update({name + "-" + m.get('title'): m.find(attrs={"class": "num-orange"}).text})
                except Exception as e:
                    city_food.update({name + "-" + m.get('title'): 0})

        time.sleep(3)
        city_url.remove(i)
        driver.close

    label .end

    food = []
    point = []
    for j in city_food:
        food.append(j)
        point.append(city_food[j])
    data_df = pd.DataFrame({"food": food, "point": point})
    writer = pd.ExcelWriter('all_food_point.xlsx')
    data_df.to_excel(writer, float_format='%.5f')
    writer.save()

    driver.quit
    return city_food


@with_goto
def get_city_top_JD(city_url):
    city_jd = []
    city_jd_dianping = []

    label .begin
    proxy = get_proxy().get("proxy")
    opt.add_argument(f"–proxy-server=http://{proxy}")
    driver = webdriver.Chrome(chrome_driver, chrome_options=opt)

    if len(city_url) == 0:
        goto .end
    try:
        for i in city_url:

            t = re.compile(".*?([0-9]{5,}).html")
            url = "http://www.mafengwo.cn/jd/" + str(re.findall(t, i)[0]) + "/gonglve.html"
            print("[+]" + url)

            driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            jd_location = ""

            for m in soup.find(attrs={"class": "crumb"}).find_all(attrs={"class": "item"})[1:-1]:

                jd_location = jd_location + m.find("span").find("a").text + "-"
            jd_location = jd_location.strip("-")

            for j in soup.find_all(attrs={"class": "item clearfix"}):

                city_jd.append(jd_location + "-" + j.find_all('a')[1].get("title"))
                city_jd_dianping.append(j.find_all('a')[1].find("em").text)

            time.sleep(3)
            city_url.remove(i)
            driver.close
    except Exception as e:
        goto .begin

    label .end
    data_df = pd.DataFrame({"city_jd": city_jd, "hot": city_jd_dianping})
    writer = pd.ExcelWriter('all_jd_hot.xlsx')
    data_df.to_excel(writer, float_format='%.5f')
    writer.save()
    return dict(zip(city_jd, city_jd_dianping))


def get_single_city_food_info(driver):

    city_food = {}
    url = driver.current_url
    s = re.compile(".*?([0-9]{5,}).html")
    url = "http://www.mafengwo.cn/cy/" + str(re.findall(s, url)[0]) + "/gonglve.html"

    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    s = re.compile(r"(.*?)美食")
    name = soup.find("title").text
    name = str(re.findall(s, name)[0])
    try:

        city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top1"}).find('a').get("title"): soup.find(attrs={"class": "rank-item top1"}).find('a').find(attrs={"class": "num-orange"}).text})
        city_food.update({name + "-" + soup.find(attrs={"class": "rank-item top2"}).find('a').get("title"): soup.find(attrs={"class": "rank-item top2"}).find('a').find(attrs={"class": "num-orange"}).text})
    except:
        pass

    for j in soup.find_all(attrs={"class": "rank-item top3"}):
        for m in j.find_all('a'):
            city_food.update({name + "-" + m.get('title'): m.find(attrs={"class": "num-orange"}).text})
    time.sleep(2)

    food = []
    point = []
    for j in city_food:
        food.append(j)
        point.append(city_food[j])
    data_df = pd.DataFrame({"food": food, "point": point})
    writer = pd.ExcelWriter(name + '_food_point.xlsx')
    data_df.to_excel(writer, float_format='%.5f')
    writer.save()

    return city_food


def get_single_city_top_JD(driver):
    city_jd = []
    city_jd_dianping = []
    url = driver.current_url

    url = url.replace("cy", "jd")

    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    jd_location = ""

    for m in soup.find(attrs={"class": "crumb"}).find_all(attrs={"class": "item"})[1:-1]:

        jd_location = jd_location + m.find("span").find("a").text + "-"
    jd_location = jd_location.strip("-")

    s = re.compile("(.*?)景点介绍")

    city_name = soup.find("title").text
    city_name = str(re.findall(s, city_name)[0])

    for j in soup.find_all(attrs={"class": "item clearfix"}):

        city_jd.append(jd_location + "-" + j.find_all('a')[1].get("title"))
        city_jd_dianping.append(j.find_all('a')[1].find("em").text)

    for i in soup.find_all(attrs={"class": "row row-hotScenic row-bg"}):

        for j in i.find_all("a"):

            try:
                city_jd.append(jd_location + "-" + "-" + j.get("title"))
                uri = "http://www.mafengwo.cn" + j.get("href")
                driver.get(uri)
                html = driver.page_source
                ss = re.compile(r"([0-9]*?)条")
                s = re.findall(ss, html)

                city_jd_dianping.append(s[0])
            except:

                city_jd.remove(jd_location + "-" + "-" + j.get("title"))
                continue

    if os.path.exists(city_name + "_top_jd_hot.xlsx"):
        os.remove(city_name + "_top_jd_hot.xlsx")
    data_df = pd.DataFrame({"city_jd": city_jd, "hot": city_jd_dianping})
    writer = pd.ExcelWriter(city_name + '_top_jd_hot.xlsx')
    data_df.to_excel(writer, float_format='%.5f')
    writer.save()


def get_single_city_info(city_name):

    proxy = get_proxy().get("proxy")
    opt.add_argument(f"–proxy-server=http://{proxy}")
    driver = webdriver.Chrome(chrome_driver, chrome_options=opt)
    url = "http://www.mafengwo.cn/search/q.php?q="
    proxies = {
        "http": proxy
    }
    print("[+]当前搜索城市关键词---->" + city_name)
    driver.get(url + city_name)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    url = soup.find(attrs={"class": "search-mdd-wrap"}).find_all("a")[0].get("href")
    driver.get(url)
    get_single_city_food_info(driver)
    get_single_city_top_JD(driver)
    print("[+]数据已抓取完毕")


if __name__ == "__main__":

    print("Please use -h")
    # city_url = get_city()
    # city_url.remove("http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10439.html")
    # city_url_1=city_url
    # get_city_food_info(city_url_1)
    # get_single_city_info("北京")
    # analyse.analyse_single_jd("北京")
