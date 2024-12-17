import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from lxml import etree
import os
import time
import pandas as pd


#提供可选的20个用户代理
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.149",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 OPR/74.0.3911.203",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.149",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 OPR/74.0.3911.203",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.257",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.257",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.133"
]


def setup_driver(headless=True,idx=0):
    webdriver_path = "E:/edgeWebDriver/msedgedriver.exe"
    service = Service(webdriver_path)

    user_agent = user_agent=user_agents[(idx+3)%20]

    print(user_agent)

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

def src2name(src):
    if src.startswith("//game.gtimg.cn/images/lol/act/img/champion/") and src.endswith(".png"):
        filename = src.split('/')[-1]
        hero_name = filename.split('.')[0]
        return hero_name
    else:
        return "not_a_champ"

#---------------------------------------------------------------------------------------

csv_file_path = r'D:\MyCode\PYTHON\dataVisualization\id2getIMG.csv'
df = pd.read_csv(csv_file_path)
# 遍历DataFrame中的每一行
for index, row in df.iterrows():
    if index%5==0:
        driver = setup_driver(True,index//5)

    match_id = row['FirstMatchID']
    url=f'https://www.wanplus.cn/schedule/{match_id}.html'

    driver.get(url)
    time.sleep(2)

    html_source = driver.page_source
    tree = etree.HTML(html_source)

    for i in [1,3]:
        img_src = tree.xpath(f'/html/body/div/div[3]/div[2]/div[1]/ul/li[{i}]/a/img/@src')[0]
        team_name= tree.xpath(f'/html/body/div/div[3]/div[2]/div[1]/ul/li[{i}]/a/img/@alt')[0]


        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(img_src, stream=True,headers=headers)

        if response.status_code == 200:
            imgpath=r'D:\MyCode\PYTHON\dataVisualization\team_img'

            # 构建文件路径
            file_path = os.path.join(imgpath, f"{team_name}.png")

            if not os.path.exists(file_path):
                # 写入文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {team_name} to {file_path}")



driver.quit()