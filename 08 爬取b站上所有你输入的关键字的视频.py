import requests
from bs4 import BeautifulSoup
import xlwt
import time

def write_to_excel(list):
    if len(list)==0:
        return False
    for item in list:
        item_title = item.find(class_='bili-video-card__info--tit').text
        item_link = item.find('a').get('href')
        item_author=item.find('span',class_='bili-video-card__info--author').text
        stats = item.find_all("span", class_="bili-video-card__stats--item")
        item_view=stats[0].find('span').text
        item_biubiu=stats[1].find('span').text
        item_date = item.find(class_='bili-video-card__info--date').text

        print('爬取：' + item_title)
        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n,2,item_author)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n = n + 1
    return True
n=1
def save_to_excel(soup):
    list = soup.find_all("div", class_=['to_hide_xs','col_3', 'col_xs_1_5', 'col_md_2', 'col_xl_1_7','mb_x40'])

    return write_to_excel(list)

def main(page,keywords):
    url='https://search.bilibili.com/all?vt=53655423&keyword='+keywords+'&page='+str(page)
    # 网址
    # 设置请求头，用于模拟浏览器发送请求
    headers = {
    'referer':'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'cookie':'buvid3=DE4CAAE9-C47B-BEF2-7742-9B1CAD735A1D77536infoc; _uuid=96E910C73-C5F5-6717-52AB-B76CC410B7BC677164infoc; buvid_fp=bfe120f5ac52b1a13a67d361b4febd8d; buvid4=84CCFE37-4220-7313-9394-5810964D4AD379217-024082902-EstQ3uIfQEbgiXDYFfOhNA%3D%3D; b_nut=100; is-2022-channel=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=16; header_theme_version=CLOSE; enable_web_push=DISABLE; home_feed_column=4; browser_resolution=851-931; b_lsid=399B6D109_19328D3CE1B'
    }
    response=requests.get(url=url,headers=headers,verify=False).text
    # print(response)
    soup=BeautifulSoup(response,'html.parser')
    return save_to_excel(soup)





if __name__ == '__main__':
    try:
        keywords = input("输入你想爬取的关键字：")
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)

        sheet = book.add_sheet('b站' + keywords + '的视频', cell_overwrite_ok=True)
        sheet.write(0, 0, '视频名称')
        sheet.write(0, 1, '视频链接')
        sheet.write(0,2,'视频作者')
        sheet.write(0, 3, '播放量')
        sheet.write(0, 4, '弹幕数')
        sheet.write(0, 5, '上传时间')
        m=1
        while True:
            res=main(m,keywords)
            book.save(u'b站'+keywords+'的视频.xls')
            time.sleep(3)
            print(res)
            if not res:
                break
            m+=1
    except requests.exceptions.ConnectTimeout  as e:
        print('时间超时,可能触发了网站反爬虫机制')
