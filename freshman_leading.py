# 列表页与详情页
# 先获取详情页的URL，再向页面发送一个请求，再接收页面数据
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


# 获取指定url页面的HTML
def get_page(url):
    """
    获取页面内容
    :param url:URL链接
    :return:BeautifulSoup对象
    """
    ua = UserAgent()
    try:
        headers = {
            'User-Agent': ua.random,
            'X-Requested-With': 'XMLHttpRequest'  # 必须通过异步的方式加载数据
        }
        response = requests.get(url, headers=headers)
    except:
        raise Exception("请求失败")
    response.encoding = "utf-8"  # 解决中文编码出错问题
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


# 获取指定url页面中的详情
def get_news_detail(url):
    """
    获取详情页信息
    :param url:URL链接
    :return: 详情页内容，字典
    """
    soup = get_page(url)
    # print(soup)
    news_detail = {}
    # 获取通知第一段内容
    # p = soup.select('title')
    # print(p)
    description = soup.find(attrs={"name": "description"})['content']
    news_detail['basis'] = description
    # div = soup.find("div", class_="para")
    # for i in range(20,32):
    #     print(di
    #     v.contents[i])
    # div = soup.select('.para')
    # div = div.contents[0]
    # print(div)
    return news_detail


def main():
    print('进入新生指引板块')
    print('1. 学校基础介绍')
    print('2. 信工基础介绍')
    print('3. 自由问答')
    choice = int(input())
    if choice == 1:
        url = "https://baike.baidu.com/item/%E9%A6%96%E9%83%BD%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6/244249"  # 列表页URL
        data = get_news_detail(url)  # 从列表页中获取每一篇详情页链接
        print(data['basis'])
    elif choice == 2:
        url = "https://baike.baidu.com/item/%E9%A6%96%E9%83%BD%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E4%BF%A1%E6%81%AF%E5%B7%A5%E7%A8%8B%E5%AD%A6%E9%99%A2"
        data = get_news_detail(url)
        print(data['basis'])
    elif choice == 3:
        print("请问你有什么问题嘛？")
        question = input()
        if "学校一共有多少个校区" in question:
            print("首师大一共有6个校区")
        elif "信工是在哪个校区" in question:
            print("信工在北二区，但是大一新生在良乡哦！")
        elif "信工一共有多少个专业" in question:
            print("本科是有5个哦，分别是计科师范、计科、人工智能师范、人工智能、电子信息工程")
        else:
            print("对不起，这个问题我不会")


if __name__ == "__main__":
    main()
