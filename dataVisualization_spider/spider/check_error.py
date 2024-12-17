from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import pandas as pd
import os
import time
import re
import csv
import random
from lxml import etree
import numpy as np

error_counts = 0
max_try=5
error_log_lock = threading.Lock()
nothing_error_log_lock = threading.Lock()

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


#setup_driver用于创建一个driver实例
def setup_driver(headless=True,index=0):
    webdriver_path = "E:/edgeWebDriver/msedgedriver.exe"
    service = Service(webdriver_path)

    user_agent=user_agents[index%20]


    options = Options()
    if headless:
        options.add_argument("--headless")  # 无头模式
        options.add_argument(f'user-agent={user_agent}')
    else:
        options.add_argument("--disable-gpu")  # 禁用GPU硬件加速
        options.add_argument("--window-size=1920,1080")  # 设置窗口大小
   
    # 禁用图片和视频加载
    options.add_experimental_option('prefs', {
        'profile.managed_default_content_settings.images': 2,  # 禁用图片
        'profile.managed_default_content_settings.videos': 1,  # 禁用视频
        'profile.managed_default_content_settings.plugins': 1,  # 禁用插件
    })

    driver = webdriver.Edge(service=service, options=options)
    return driver

#set_dataframe用于初始化用于写入数据的df
def set_dataframe():
    columns = []
    columns.append('MatchID')
    columns.append('matchType')
    columns.append('gameset')
    columns.append('MatchDate')
    columns.append('Duration')
    columns.append('win')
    for team in ['Team1', 'Team2']:
        columns.append(f'{team}')
        columns.append(f'{team}_region')
        for event in ['Baron','Dra','Turts']:
            columns.append(f'{team}_{event}')
        for count in range(1,6):
            columns.append(f'{team}_ban{count}')

    for team in ['Team1', 'Team2']:
        for role in range(1,6):
            for stat in ['name','pick', 'K', 'D', 'A', 'CS', 'gold', 'damage', 'tanking']:
                columns.append(f'{team}_player{role}_{stat}')
    #创建空df
    return pd.DataFrame(columns=columns)

def all2date(alldate):
    # 使用正则表达式匹配日期格式，精确到日
    match = re.search(r'\d{4}-\d{2}-\d{2}', alldate)
    # 返回匹配的日期字符串
    return match.group()

def src2name(src):
    # 检查src是否符合英雄图片的格式
    if src.startswith("https://cdn.jishukong.com/data/lol/hero/square/") and src.endswith(".png"):
        # 提取文件名
        filename = src.split('/')[-1]
        # 提取英雄名称
        hero_name = filename.split('.')[0]
        return hero_name
    else:
        # 如果不符合英雄图片的格式，返回"not_a_champ"
        return "not_a_champ"

def class2region(class_name):
    parts = class_name.split()
    return parts[1]


def handleURL(driver,outputfile,matchid=0,ntry=1):
    url=f'https://www.wanplus.cn/schedule/{matchid}.html'
    try:    
        
        print(url+" in process:.................")
        print("get url.........")
        driver.get(url)
        #等待加载
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body")))
        time.sleep(ntry*1)

        #获取页面资源
        html_source = driver.page_source
        tree = etree.HTML(html_source)


        error_csv_file=outputfile
        error_message=tree.xpath('//*[@id="info"]/div/div[2]/p')
        if error_message or (error_message[0]).text == "糟糕，页面未找到":
            df_error = pd.DataFrame([[matchid, "页面无内容"]], columns=['MatchID', 'Error'])
            if not os.path.exists(error_csv_file):
                # 创建CSV文件并写入表头
                df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
            else:
                # 追加错误信息到CSV文件
                df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
            return 7
        
        gamekind=tree.xpath('/html/body/div/div[3]/div[1]/div/a[2]')
        if not gamekind or (gamekind[0]).text != "英雄联盟":
            df_error = pd.DataFrame([[matchid, "非英雄联盟"]], columns=['MatchID', 'Error'])
            if not os.path.exists(error_csv_file):
                # 创建CSV文件并写入表头
                df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
            else:
                # 追加错误信息到CSV文件
                df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
            return 7
        
        
        with nothing_error_log_lock():
            file = 'still_check.csv'
            mode = 'a' if os.path.exists(file) else 'w'  # 如果文件已存在，则追加；否则，写入
            df_corre = pd.DataFrame([[matchid]], columns=['MatchID'])
            df_corre.to_csv(file, mode=mode, index=False, header=not os.path.exists(), encoding='utf-8')
            
        return ntry
    
    except Exception as e:
        if ntry >= max_try:
            error_csv_file = 'other_error_log.csv'
            df_error = pd.DataFrame([[matchid, str(e)]], columns=['MatchID', 'Error'])
            if not os.path.exists(error_csv_file):
                # 创建CSV文件并写入表头
                df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
            else:
                with error_log_lock:
                    # 追加错误信息到CSV文件
                    df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
        return ntry+1
   

def spider_thread(matchids,thead_c,outputfile):
    print(f'this is thread {thead_c}.............{len(matchids)}')
    print(matchids)
    t_driver = setup_driver(True,thead_c)
    
    for matchid in matchids:
        ntry = 1
        while ntry <= max_try:
            result = handleURL(t_driver,outputfile,matchid,ntry)
            if result == ntry :
                break
            ntry = result
    t_driver.quit()

def main():
    # 读取noexist.csv文件中的MatchID
    noexist_df = pd.read_csv('noexist.csv')
    # 将'MatchID'列转换为列表
    matchid_list = noexist_df['MatchID'].to_list()

    total = len(matchid_list)
    num_of_thread = 20

    step = total//num_of_thread

    outputfile_prefix = 'noexist'
    # 创建线程池
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(num_of_thread):
            start = i*step+1
            end = (i+1)*step if i<num_of_thread-1 else total

            # 提交任务
            futures.append(executor.submit(spider_thread, matchid_list[start:end], i+1,f'{outputfile_prefix}_{i+1}.csv'))

        # 等待线程完成
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error occurred: {e}')

    # 合并所有输出的CSV文件
    merged_df = pd.DataFrame()
    for i in range(num_of_thread):
        filename = f'{outputfile_prefix}_{i+1}.csv'
        if os.path.exists(filename):
            temp_df = pd.read_csv(filename)
            merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
            os.remove(filename)  # 删除临时文件
    merged_df.to_csv('merged_noexist_output.csv', index=False, encoding='utf-8')
if __name__ == "__main__":
    main()
