import urllib.request
import re
import json
import requests


def main(page):
    url='http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'+str(page)
    html=request_dandan(url)
    items=parse_result(html)        #信息过滤函数

    for item in items:
        write_item_to_file(item)
        # print(item)

def request_dandan(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(html):
    pattern=re.compile(
               r'<li>.*?list_num.*?(\d+).*?'       #得到排名
               r'img src=\"(.*?)\".*?'       #得到图片
               r'class=\"name\".*?title=\"(.*?)\">.*?'                   #得到书名
               r'class=\"tuijian\">(.*?)</span>.*?'   #推荐指数
               r'class=\"publisher_info\">.*?target="_blank">(.*?)</a>.*?' #作者
               r'biaosheng\">.*?<span>(.*?)</span></div>.*?'#五星评分次数
               r'<p><span\sclass=\"price_n\">&yen;(.*?).*?</li>'       #价钱
        # r'<li>.*?list_num.*?(\d+).</div>'
        # r'.*?<img src="(.*?)".*?'
        # r'class="name".*?title="(.*?)">.*?'
        # r'class="star">.*?class="tuijian">(.*?)</span>.*?'
        # r'class="publisher_info">.*?target="_blank">(.*?)</a>.*?'    title=\"([^ ]*)
        # r'class="biaosheng">.*?<span>(.*?)</span></div>.*?'
        # r'<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>'
              , re.S        )
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'rank':item[0],
            'image':item[1],
            'title':item[2],
            'recommend':item[3],
            'author':item[4],
            'times':item[5],
            'price':item[6]
        }

def write_item_to_file(item):
    with open('book.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    for i in range(1,26):
        main(i)
    # main(1)