# 列表页与详情页
# 先获取详情页的URL，再向页面发送一个请求，再接收页面数据
from bs4 import BeautifulSoup
import requests
import datetime
import lxml
import re


# 获取指定url页面的HTML
def get_page(url):
    """
    获取页面内容
    :param url:URL链接
    :return:BeautifulSoup对象
    """
    try:
        response = requests.get(url)
    except:
        raise Exception("请求失败")
    response.encoding = "utf-8"  # 解决中文编码出错问题
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


# 获取指定url页面中的新闻列表跳转链接
def get_news_list(url):
    """
    获取列表页内容
    :param url: URL链接
    :return: links列表
    """
    soup = get_page(url)
    # print(soup)
    news = soup.select('.pageList ul li a')
    # print(news)
    links = []
    for item in news:
        link = item.get('href')
        links.append(link)
    # print(links)
    return links


# 获取指定url页面中的详情
def get_news_detail(url):
    """
    获取详情页信息
    :param url:URL链接
    :return: 详情页内容，字典
    """
    soup = get_page(url)
    news_detail = {}
    # 获取通知标题
    title_content = soup.select('.articleTitle h2')[0].string
    news_detail['Title'] = title_content  # 通知题目
    news_date = soup.select('.articleAuthor')
    # 只想要日期，去掉其他字符（利用正则表达式匹配）
    if news_date:
        news_date = str(news_date).replace(" ", "")
        news_date = str(news_date).replace("\n", "")
        result = re.match('.*发布日期：(\d{4}-\d{2}-\d{2}).*', str(news_date).replace(" ", ""))
        news_detail['news_date'] = result.group(1)
    else:
        news_detail['news_date'] = "未知日期"
    # print(news_detail['news_date'])
    # 获取通知第一段内容
    p = soup.select('.article p')
    for item in p[0:1]:
        content = ""
        for i in item.select('span'):
            if i.string:
                content = content + i.string
    if content:
        news_detail['Content'] = content
    else:
        news_detail['Content'] = '这个网页有点复杂，我解析不了'
    return news_detail


def main():
    print('进入院系通知查询板块')
    print('1. 获取最新通知标题')
    print('2. 获取指定通知标题')
    print('3. 获取指定通知内容')
    choice = int(input())
    # 获取院系通知标题集，共20个
    url = "https://iec.cnu.edu.cn/ggml/tzgg1/index.htm"  # 列表页URL
    links = get_news_list(url)  # 从列表页中获取每一篇详情页链接
    news_list = []
    for link in links[1:]:  # 跳过第一个首页的链接
        news_detail = get_news_detail('https://iec.cnu.edu.cn/ggml/tzgg1/' + link)  # 获取该详情页的信息返回的是字典
        news_list.append(news_detail)  # 将字典追加到新闻的列表中
    if choice == 1:
        print(news_list[0]['news_date'][0:4] + '年' + news_list[0]['news_date'][5:7] + '月' + news_list[0]['news_date'][
                                                                                            8:10] + '日' + '发布' +
              news_list[0]['Title'])
    elif choice == 2:
        num = int(input("您想看第几条通知："))
        print(news_list[num - 1]['Title'])
    elif choice == 3:
        print('请输入您想要查询的通知关键字：')
        key_words = input()
        for item in news_list:
            if key_words in item['Title']:
                print(item['Content'])


if __name__ == "__main__":
    main()
