import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from lxml import etree
import os
import time

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

def src2name(src):
    if src.startswith("//game.gtimg.cn/images/lol/act/img/champion/") and src.endswith(".png"):
        filename = src.split('/')[-1]
        hero_name = filename.split('.')[0]
        return hero_name
    else:
        return "not_a_champ"



url = 'https://lol.qq.com/guides/hero.shtml?ADTAG=cooperation.glzx.web'


driver = setup_driver()
driver.get(url)

time.sleep(5)

html_source = driver.page_source
tree = etree.HTML(html_source)


for i in range(1, 170):
    img_src = tree.xpath(f'//*[@id="content-hero-list"]/a[{i}]/span[1]/img/@src')[0]
    cham_name = src2name(img_src)

    print(f'{i}---{img_src}-----------------{cham_name}')
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(f'https:{img_src}', stream=True,headers=headers)

        print(response.status_code)
        if response.status_code == 200:
            imgpath=r'D:\MyCode\PYTHON\dataVisualization\hero_img'

            # 构建文件路径
            file_path = os.path.join(imgpath, f"{cham_name}.png")
            # 写入文件
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {cham_name} to {file_path}")
    except Exception as e:
        print(f"Failed to download {img_src}: {e}")

driver.quit()