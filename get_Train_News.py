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
    news = soup.select('a')
    # print(news)
    links = []
    for item in news:
        link ='http://wx.stcard.cn/app/wx/question/'+ item.get('href')
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
    news_detail['content'] = soup.find('body').text
    sel=['body']#使用数据清洗去掉换行，来源：https://blog.csdn.net/weixin_35649143/article/details/113366757
    data=[]
    for i in range(len(sel)):
        d = soup.select(sel[i])
    #x=[],若使用，在后续的转换中还有括号去不掉
    for item in d:
        s = str(item.get_text()).replace('\n', '').replace(' ','').replace('\r','').replace('\t','')#去掉换行符与空格
        # if s=="":#空数据过滤continue
        #        s+='\n'
        data.append(s)
    data1=''.join('%s' %id for id in data)#join可以把列表转换为字符串，但是里面含数字，不能直接转化成字符串，即遍历list的元素，把他转化成字符串
    news_detail['content']=data1

    # news_detail1 = soup.find('body').text
    # # news_detail = str(news_detail).replace(" ", "")
    # result = re.match('.*', news_detail1, re.S)
    # news_detail['content'] = result.group(0)
    return news_detail

def main():
    print('进入火车票学生优惠卡介绍板块')
    print('1. 关于铁路客票系统学生资质绑定')
    print('2. 如何查询自己绑定的资质信息')
    print('3. 没有先去车站绑定资质，12306未显示资质信息可以买学生票吗？')
    print('4. 哪些大中专学生可以购买学生票？')
    print('5. 如何申领火车票学生优惠卡')
    print('6. 什么时候可以买学生票')
    #print('7. 可以在网上购票吗？如何购买学生票？'),含图片
    print('7. 什么是优惠乘车区间、区间如何填写？')
    print('8. 如何更改优惠乘车区间？')
    print('9.当在优惠区间内乘车但没有直达列车或者需要换成高铁、动车时如何购票？')
    print('10.如何查询优惠卡内个人信息？')
    print('11.关于使用优惠卡时优惠次数限制的问题？')
    #print('12.在12306买学生票时无法正常购票的相关问题解答？')，含图片
    print('12.什么类型的火车票可以打折？打几折？')
    print('13.学生票退票后，优惠次数是否返还？')
    print('14.购买联程车票，会核销几次优惠次数呢？')
    print('15.公众号“个人中心”是不是每个学生都需要注册（是不是注册了就可以买学生票了）?')
    print('16.列车上查票时没有绑定优惠资质怎么办？')

    choice = int(input())
    # 获取院系通知标题集，共20个
    url = "http://wx.stcard.cn/app/wx/question/index.html"  # 列表页URL
    links = get_news_list(url)  # 从列表页中获取每一篇详情页链接
    news_list = []
    for link in links[:]:  # 跳过第一个首页的链接
        news_detail = get_news_detail(link)  # 获取该详情页的信息返回的是字典
        news_list.append(news_detail)  # 将字典追加到新闻的列表中
    if choice == 1:
        print(news_list[0]['content'])
    elif choice == 2:
        print(news_list[1]['content'])
    elif choice == 3:
        print(news_list[2]['content'])
    elif choice == 4:
        print(news_list[3]['content'])
    elif choice == 5:
        print(news_list[4]['content'])
    elif choice == 6:
        print(news_list[5]['content'])
    # elif choice == 7:
    #     print(news_list[6]['content'])
    elif choice == 7:
        print(news_list[7]['content'])
    elif choice == 8:
        print(news_list[8]['content'])
    elif choice == 9:
        print(news_list[9]['content'])
    elif choice == 10:
        print(news_list[10]['content'])
    elif choice == 11:
        print(news_list[11]['content'])
    # elif choice == 12:
    #     print(news_list[12]['content'])
    elif choice == 12:
        print(news_list[13]['content'])
    elif choice == 13:
        print(news_list[14]['content'])
    elif choice == 14:
        print(news_list[15]['content'])
    elif choice == 15:
        print(news_list[16]['content'])
    elif choice == 16:
        print(news_list[17]['content'])

if __name__ == "__main__":
    main()