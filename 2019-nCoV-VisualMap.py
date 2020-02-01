import time
import json
import requests
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map


def catch_distribution():

    areaData = {}
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(
        time.time()*1000)
    data = json.loads(requests.get(url=url).json()['data'])
    # 获取更新时间
    lastUpdateTime = data['lastUpdateTime']
    # 找到中国信息
    for item in data['areaTree']:
        if item['name'] == '中国':
            chinaData = item['children']
            break
    # 获取各个省份确诊的人数
    for item in chinaData:
        areaData[item['name']] = item['total']['confirm']

    return areaData, lastUpdateTime


# 官网范例中的链式调用
def map_visualmap(time, pieces, data) -> Map:
    c = (
        Map()
        .add("确诊人数", data.items(), "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国各省份确诊人数分布\n截至: " + time),
            visualmap_opts=opts.VisualMapOpts(
                max_=5000, is_piecewise=True, pieces=pieces)
        )
    )
    return c


data, lastUpdateTime = catch_distribution()
pieces = [
    {"min": 1000},
    {"min": 100, "max": 1000},
    {"min": 10, "max": 100},
    {"max": 10}
]
map1 = map_visualmap(lastUpdateTime, pieces, data)
map1.render()
