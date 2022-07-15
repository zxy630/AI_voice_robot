"""
查询疫情情况
    可查询疫情的相关知识
    各个省份的现存确诊人数和疑似人数
    北京各个区的今日新增确诊人数和现存确诊人数
"""
import requests
import json


# 获取城市疫情数据，返回json的data
def Down_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    data_res = json.loads(res['data'])
    return data_res


# 打印地区疫情数据
def get_bj_area_info(area_name):
    data = Down_data()['areaTree'][0]['children']
    path = '北京'
    for i in data:
        if path in i['name']:
            for item in i['children']:
                if area_name in item['name'] or item['name'] in area_name:
                    list_city = [
                        '地区: ' + str(item['name']) + '\n',
                        '新增确诊：' + str(item['today']['confirm']),
                        ' 现存确诊：' + str(item['total']['nowConfirm'])
                    ]
                    res_city = ''.join(list_city)
                    print(res_city)


# 获取url返回json格式数据
def get_ncov_info(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except:
        return None


# 获取标准城市名称，如用户输入北京，但是接口使用的是北京市，则返回北京市
def get_city_name():
    city_name = input("请输入你想要查询的省市名称：")
    url = 'https://lab.isaaclin.cn/nCoV/api/provinceName'
    try:
        response = requests.get(url)
        data = response.json()
    except:
        print('获取城市信息失败！')
    for i in data['results']:
        if city_name in i:
            return i
    return None


# 获取疫情小贴士
def get_covid_tips():
    url = 'https://lab.isaaclin.cn/nCoV/api/overall'
    data = get_ncov_info(url)
    if not data:
        print('未爬取到疫情小贴士')
    else:
        remark1 = data['results'][0]['remark1']
        remark2 = data['results'][0]['remark2']
        remark3 = data['results'][0]['remark3']
        note2 = data['results'][0]['note2']
        note3 = data['results'][0]['note3']
        print('1.' + remark1)
        print('2.' + remark2)
        print('3.' + remark3)
        print('4.' + note2)
        print('5.' + note3)


# 获取省市疫情信息
def get_city_info():
    city_name = get_city_name()
    if city_name:
        url = f'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province={city_name}'
        data = get_ncov_info(url)
        if not data:
            print("未爬取到数据")
        else:
            currentConfirmedCount = data['results'][0]['currentConfirmedCount']
            confirmedCount = data['results'][0]['confirmedCount']
            suspectedCount = data['results'][0]['suspectedCount']
            curedCount = data['results'][0]['curedCount']
            deadCount = data['results'][0]['deadCount']
            print(f'{city_name}现存确诊人数{currentConfirmedCount};'
                  f'疑似人数{suspectedCount};'
                  f'请注意防护！')
    else:
        print('未查找到该城市的疫情信息')


def main():
    print('进入疫情查询板块')
    print('1. 获取疫情科普小贴士')
    print('2. 获取省市疫情数量')
    print('3. 查询北京地区疫情情况')
    choice = int(input())
    if choice == 1:
        get_covid_tips()
    elif choice == 2:
        get_city_info()
    elif choice == 3:
        print('请输入您想要查询的地区：')
        area_name = input()
        get_bj_area_info(area_name)


if __name__ == '__main__':
    main()