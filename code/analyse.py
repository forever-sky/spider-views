import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import time
import configparser
import os
import sys

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def analyse_single_food(city):
    df = pd.read_excel(city + "_food_point.xlsx")

    dic = dict(zip(df["food"].values, df["point"].values))
    data1 = pd.Series(dic)
    data1.name = ""
    data1.plot(kind="pie",
               autopct="%.1f%%",
               radius=1,
               startangle=180,
               counterclock=False,
               title=city + "的top美食",
               wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},
               textprops={'fontsize': 10, 'color': 'black'}

               )
    plt.show()


def analyse_single_jd(city):
    df = pd.read_excel(city + "_top_jd_hot.xlsx")

    dic = dict(zip(df["city_jd"].values, df["hot"].values))
    data1 = pd.Series(dic)
    data1.name = ""
    data1.plot(kind="pie",
               autopct="%.1f%%",
               radius=1,
               startangle=180,
               counterclock=False,
               title=city + "的top景点",
               wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},
               textprops={'fontsize': 10, 'color': 'black'}

               )
    plt.show()


def analyse_all_top_food():
    df = pd.read_excel("all_food_point.xlsx")
    dic = dict(zip(df["food"].values, df["point"].values))
    dic = sorted(dic.items(), key=lambda dic: dic[1])
    num = 15
    dit = {}
    dic = dic[-15:]
    for j in dic:
        dit.update({j[0]: j[1]})
    data1 = pd.Series(dit)
    data1.plot(kind='bar')

    plt.show()


def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '7UI8T08wRB33tqldtqCvwZcOCn0aLkDG'

    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = requests.get(uri)
    res = req.text

    temp = json.loads(res)  # 对json数据进行解析
    return temp


def analyse_all_top_jd():
    df = pd.read_excel("all_jd_hot.xlsx")

    point = df["hot"].values
    hot_map_path = "hot_map.html"
    hot_map_template_path = "hot_map_template_path.html"
    dic = dict(zip(df["city_jd"].values, df["hot"].values))
    jd = []
    dit = {}
    s = sorted(point)[-100:]

    for j in s:
        now = [k for (k, v) in dic.items() if v == j]

        jd = jd + now

    for i in range(0, len(jd) - 1):
        for j in range(i + 1, len(jd)):
            try:
                if jd[i].split("-")[-1] == jd[j].split("-")[-1]:

                    jd.remove(jd[j])
            except:
                pass
    jd = list(set(jd))

    for m in jd:
        dit.update({f"{m}": dic[m]})

    str_list = []
    print("[+]正在绘制热力图")
    '''
    获取城市经纬度坐标绘制热力图
    '''

    from tqdm import tqdm
    from tqdm._tqdm import trange

    for i, k in tqdm(dit.items()):
        city = i

        count = k
        try:
            lng = getlnglat(city)['result']['location']['lng']  # 获取经度

            lat = getlnglat(city)['result']['location']['lat']  # 获取纬度
            # time.sleep(1)

            str_temp = {"lng": float(lng), "lat": float(lat), "count": count * 1000}

            str_list.append(str_temp)

        except Exception as e:
            pass
    '''
    读取配置文件中的网站目录路径
    '''
    import time
    from tqdm import tqdm
    from tqdm._tqdm import trange

    for i in tqdm(range(100)):
        time.sleep(0.01)
    data = f'var points ={str(str_list)};'
    root_dir = os.path.dirname(os.path.abspath('.'))
    cf = configparser.ConfigParser()
    cf.read(root_dir + "\\config.ini")

    sec = cf.sections()
    path = cf.get("www-path", "path")
    if path is None:
        print("配置文件有误")
        sys.exit()
    with open(hot_map_template_path, "r", encoding="utf-8") as f1, open(path + hot_map_path, 'w', encoding="utf-8") as f2:
        s = f1.read()
        s2 = s.replace("%data%", data)
        f2.write(s2)
        f1.close()
        f2.close()
        print("[+]热力图绘制完毕请去网站根目录下访问")


if __name__ == "__main__":
    analyse_single_jd("北京")
