import argparse
import analyse
import spider
import os
import sys
import time
import mafengwo
import jba


def main():
    print('''
    へ　　　　　／|
　　/＼7　　　 ∠＿/
　 /　│　　 ／　／
　│　Z ＿,＜　／　　 /`ヽ
　│　　　　　ヽ　　 /　　〉
　 Y　　　　　`　 /　　/
　ｲ●　､　●　　⊂⊃〈　　/
　()　 へ　　　　|　＼〈
　　>ｰ ､_　 ィ　 │ ／／
　 / へ　　 /　ﾉ＜| ＼＼
　 ヽ_ﾉ　　(_／　 │／／
　　7　　　　　　　|／
　　＞―r￣￣`ｰ―＿
  ''')


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-s", help="爬取国内热门城市的美食和景点", action="store_true")
    parse.add_argument("-f", help="爬取所选城市的美食和景点")
    parse.add_argument("-p1", help="绘制热门城市top景点热力图", action="store_true")
    parse.add_argument("-p2", help="绘制所选城市top美食饼图")
    parse.add_argument("-p3", help="绘制所选城市top景点饼图")
    parse.add_argument("-p4", help="绘制热门城市美食top柱状图", action="store_true")
    parse.add_argument("-p5", help="生成游记词云", action="store_true")

    args = parse.parse_args()
    main()
    if args.s:

        city_url = spider.get_city()
        city_url.remove("http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10439.html")
        city_url1 = city_url.copy()
        city_url2 = city_url.copy()
        spider.get_city_food_info(city_url1)
        spider.get_city_top_JD(city_url2)

    elif args.p1:
        if os.path.exists("all_jd_hot.xlsx"):

            analyse.analyse_all_top_jd()
        else:
            print("请先获取数据 可以尝试-s选项")
    elif args.p2:

        if os.path.exists(args.p2 + "_top_jd_hot.xlsx"):

            analyse.analyse_single_jd(args.p2)
        else:
            print("请先获取数据 可以尝试-f选项")
    elif args.p3:
        if os.path.exists(args.p3 + "_food_point.xlsx"):
            analyse.analyse_single_food(args.p3)
        else:
            print("请先获取数据 可以尝试-f选项")
    elif args.p5:
        mafengwo.getpage()
        jba.jba()

    elif args.p4:
        if os.path.exists("all_food_point.xlsx"):
            analyse.analyse_all_top_food()
        else:
            print("请先获取数据 可以尝试-s选项")
    elif args.f:
        if os.path.exists(args.f + "_top_jd_hot.xlsx"):
            print("已有该城市数据")
        else:
            spider.get_single_city_info(args.f)
    else:
        print("请添加-h查看使用")
        time.sleep(1)
        sys.exit()
