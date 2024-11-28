import os
import io
from PIL import Image
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def exist_in_list(item,your_list:list):
    """
    判断一个元素是否在list中
    :param your_list:
    :return: bool
    """
    for i in your_list:
        if i==item:
            return True
    return False

def list2set(your_list:list):
    """
    将list去重而不改变源list的元素顺序
    :param your_list:
    :return:
    """
    res=[]
    for i in your_list:
        if exist_in_list(i,res):continue
        res.append(i)
    return res
def create_dir(path:str):
    """
    若不存在传入的path，就创建目录
    """
    if not os.path.exists(path):
        os.makedirs(path)
def save_pictures(pic_list:list,file_path,pdf_name):
    """
    将传入的照片url的照片存入固定文件夹
    :param pic_list:
    :return:
    """
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    cnt = 1
    create_dir(file_path)
    img_list=[]
    for i,pic in enumerate(pic_list):
        binnary_data=requests.get('https:' + pic, headers=headers).content
        img_list.append(Image.open(io.BytesIO(binnary_data)).convert("RGB"))
    img_list[0].save(file_path+pdf_name+'.pdf', "PDF",resolution=100.0,save_all=True, append_images=img_list[1:])

def getdriver(url,timeout):
    """
    得到模拟浏览器
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver,WebDriverWait(driver, timeout)

def open_all_pages(driver,wait):
    """
    点开所有预览按钮
    :param driver:
    :param wait:
    :return:
    """
    count = 1
    while True:
        try:
            btn_remain = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[4]/div[3]/div/button')))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn_remain)
            print(f'点击第{count}次预览')
            count += 1
            # 强制点击
            driver.execute_script("arguments[0].click();", btn_remain)
            time.sleep(2)
            del btn_remain
        except Exception as e:
            print(e)
            break

def scroll_to_pages(driver):
    """
    让所有的图片开始加载
    :param driver:
    :return:
    """
    items = driver.find_elements(By.CLASS_NAME, "webpreview-item")
    for i, item in enumerate(items):
        print(f'翻到第{i}页')
        # 滚动到元素可见
        driver.execute_script("arguments[0].scrollIntoView(true);", item)
        time.sleep(2)
    time.sleep(1)

def main(url,file_path,pdf_name,timeout=10):
    """

    :param url:你想下载的url
    :param pdf_name: 不用加.pdf
    :param timeout: 等待的最大时常，默认为10s
    :return:
    """
    driver,wait=getdriver(url,timeout)
    open_all_pages(driver,wait)
    scroll_to_pages(driver)

    source = driver.page_source
    print(source)
    all_pictures=re.findall('src="(//view-cache.*?)"',source)
    all_pictures=list2set(all_pictures)
    print(len(all_pictures))
    save_pictures(all_pictures,file_path,pdf_name)

if __name__ == '__main__':
    # https: // max.book118.com / html / 2018 / 1026 / 5302042132001323.shtm
    url=input('输入你的url')
    # file_path=input('输入你想存入的位置：')
    # pdf_name=input('输入保存的pdf名字')
    # timeout=int(input('输入你的timeout'))
    # main(url,file_path,pdf_name,timeout)
    main(url,'./pic/','test',5)

