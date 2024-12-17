from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from lxml import etree
import time
import csv

def setup_driver(headless=True):
    webdriver_path = "E:/edgeWebDriver/msedgedriver.exe"
    service = Service(webdriver_path)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.257"

    options = webdriver.edge.options.Options()
    if headless:
        options.add_argument("--headless")  # 无头模式
        options.add_argument(f'user-agent={user_agent}')
    else:
        options.add_argument("--disable-gpu")  # 禁用GPU硬件加速
        options.add_argument("--window-size=1920,1080")  # 设置窗口大小

    # 禁用图片和视频加载
    options.add_experimental_option('prefs', {
        'profile.managed_default_content_settings.plugins': 1,  # 禁用插件
    })

    driver = webdriver.Edge(service=service, options=options)
    return driver

# 定义CSV文件路径********************************************************************
csv_file_path = 'heroes.csv'

# 创建CSV文件并写入表头
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Cn_name', 'En_name'])


# 设置WebDriver
driver = setup_driver()
driver.get('https://101.qq.com/#/hero')

time.sleep(5)

html_source = driver.page_source
tree = etree.HTML(html_source)

# 遍历英雄信息并写入CSV文件
for i in range(1, 170):
    base_xpath = f'//*[@id="app"]/div/div[3]/div/div[2]/ul/li[{i}]/div'
    Cn_name = (tree.xpath(f'{base_xpath}/p')[0]).text

    En_name_el = (tree.xpath(f'{base_xpath}/div/img'))[0]
    En_name = En_name_el.get('alt')
    print(f'{Cn_name}-----------------{En_name}')

    # 将英雄信息写入CSV文件
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([Cn_name, En_name])

# 关闭WebDriver
driver.quit()