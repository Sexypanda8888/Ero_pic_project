import os
from selenium import webdriver
import urllib
import requests
file_url="file:///C:/Users/Administrator/Desktop/Ero_pic_project/wechat_pc_api/docs/index_cn.html"
driver_url='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'

def get_redwhite_pic(top,buttom):

    url=file_url
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    c=webdriver.Chrome(chrome_options=option,
        executable_path=driver_url) #获取chrome浏览器的驱动，并启动Chrome浏览器
    c.get(url)
    top_input=c.find_element_by_xpath('//*[@id="textboxTop"]')
    save=c.find_element_by_xpath('/html/body/div[6]/button[1]')
    buttom_input=c.find_element_by_xpath('//*[@id="textboxBottom"]')
    top_input.send_keys(top)
    buttom_input.send_keys(buttom)
    save.click()
    url=c.find_element_by_xpath('/html/body/a')
    url=url.get_attribute("href")
    picname="./thumb/redwhite.png"

    urllib.request.urlretrieve(url,filename="./thumb/redwhite.png")
    picname=os.path.abspath(picname)
    c.close()
    return picname


if __name__=="__main__":
    url=file_url
    top='xixi'
    buttom='ahha'
    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    c=webdriver.Chrome(chrome_options=option,
        executable_path=driver_url) #获取chrome浏览器的驱动，并启动Chrome浏览器
    c.get(url)
    top_input=c.find_element_by_xpath('//*[@id="textboxTop"]')
    save=c.find_element_by_xpath('/html/body/div[6]/button[1]')
    buttom_input=c.find_element_by_xpath('//*[@id="textboxBottom"]')
    top_input.send_keys(top)
    buttom_input.send_keys(buttom)
    save.click()
    url=c.find_element_by_xpath('/html/body/a')
    url=url.get_attribute("href")
    picname="./thumb/redwhite.png"
    urllib.request.urlretrieve(url,filename="./thumb/redwhite.png")
    c.close()