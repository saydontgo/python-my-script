# 豆瓣电影爬取要加反爬机制
from setupproxy import getip
from bs4 import BeautifulSoup
import requests
import xlwt

def main(page,sheet):
    url='https://movie.douban.com/top250?start='+str(page*25)
    html=request_douban(url)
    soup=BeautifulSoup(html,'lxml')
    list=soup.find(class_='grid_view').find_all('li')
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        item_intr='该电影无介绍词'
        if item.find(class_="inq")!=None:
            item_intr = item.find(class_="inq").string
        # print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | ' + item_intr)
    save_to_execl(list,sheet)
def request_douban(url):
   try:
       header = {
           # 假装自己是浏览器
           # 这里的header需要自己填哦
                  }
       response = requests.get(url,headers=header)
       if response.status_code == 200:
           return response.text
   except requests.RequestException:
        return None
n=1
def save_to_execl(list,sheet):
    global n
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        item_intr='该电影无介绍词'
        if item.find(class_="inq")!=None:
            item_intr = item.find(class_="inq").string
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)
        n+=1
    book.save(u'豆瓣最受欢迎的250部电影.xls')


book=xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')
for i in range(0,10):
    main(i,sheet)