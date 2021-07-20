import os
from selenium import webdriver
from selenium.webdriver.common.by import By
driver_url='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'

def search_pic(pic_url,pic_save_url):
    option = webdriver.ChromeOptions()
    # 隐藏窗口
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    c=webdriver.Chrome(chrome_options=option,
        executable_path=driver_url) #获取chrome浏览器的驱动，并启动Chrome浏览器
    c.get('https://saucenao.com/')
    inputs=c.find_element_by_xpath("//*[@id='fileInput']")
    path=os.path.abspath(pic_url)
    inputs.send_keys(path)
    button_1=c.find_element_by_xpath("//*[@id='searchButton']")
    button_1.click()
    c.save_screenshot(pic_save_url+"temp.png")
    results=c.find_elements_by_class_name("result")
    results_hidden=c.find_elements_by_css_selector(".result.hidden")
    links=[]
    #绝了，在选择器这里卡了好久！久命
    for i in range(len(results)-1-len(results_hidden)):
        a=results[i].find_elements_by_class_name('resultcontentcolumn')
        a=a[0].find_elements_by_tag_name("a")
        if len(a)!=0:
            link=a[0]
            links.append(link.get_attribute('href'))
    print(links)
    c.quit()
    return [len(links),links]
if __name__=="__main__":
    option = webdriver.ChromeOptions()
    # 隐藏窗口
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    c=webdriver.Chrome(chrome_options=option,
        executable_path=driver_url) #获取chrome浏览器的驱动，并启动Chrome浏览器
    c.get('https://saucenao.com/')
    inputs=c.find_element_by_xpath("//*[@id='fileInput']")
    path=os.path.abspath("./a.jpg")
    inputs.send_keys(path)
    button_1=c.find_element_by_xpath("//*[@id='searchButton']")
    button_1.click()
    c.save_screenshot("test.png")
    results=c.find_elements_by_class_name("result")
    results_hidden=c.find_elements_by_css_selector(".result.hidden")
    links=[]
    #绝了，在选择器这里卡了好久！久命
    for i in range(len(results)-1-len(results_hidden)):
        a=results[i].find_elements_by_class_name('linkify')
        link=a[1]
        links.append(link.get_attribute('href'))
    print(links)
    c.quit()
