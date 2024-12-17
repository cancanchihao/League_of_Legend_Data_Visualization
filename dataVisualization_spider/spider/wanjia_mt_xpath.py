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


def handleURL(driver,df,outputfile,matchid=0,ntry=1):
    url=f'https://www.wanplus.cn/schedule/{matchid}.html'
    try:    
        #文件写入
        datacsv_file = outputfile
        
        print(url+" in process:.................")
        print("get url.........")
        driver.get(url)
        #等待加载
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body")))
        time.sleep(ntry*0.5)

        #获取页面资源
        html_source = driver.page_source
        tree = etree.HTML(html_source)

        if ntry >=3:
            time.sleep(ntry*0.5)
            error_message=tree.xpath('//*[@id="info"]/div/div[2]/p')
            if error_message or (error_message[0]).text == "糟糕，页面未找到":
                error_csv_file = 'nothing_error_log.csv'
                df_error = pd.DataFrame([[matchid, "页面无内容"]], columns=['MatchID', 'Error'])
                if not os.path.exists(error_csv_file):
                    # 创建CSV文件并写入表头
                    df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
                else:
                    with nothing_error_log_lock:
                        # 追加错误信息到CSV文件
                        df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
                return 7
            
            gamekind=tree.xpath('/html/body/div/div[3]/div[1]/div/a[2]')
            if not gamekind or (gamekind[0]).text != "英雄联盟":
                error_csv_file = 'nothing_error_log.csv'
                df_error = pd.DataFrame([[matchid, "非英雄联盟"]], columns=['MatchID', 'Error'])
                if not os.path.exists(error_csv_file):
                    # 创建CSV文件并写入表头
                    df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
                else:
                    with nothing_error_log_lock:
                        # 追加错误信息到CSV文件
                        df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
                return 7


        #获取小局数
        gamesetButtons = tree.xpath('/html/body/div/div[3]/div[2]/div[1]/div/a')
        gamesets = len(gamesetButtons)

        for df_count in range(0,gamesets):
            #赛事类别
            df.at[df_count,'matchType']=(tree.xpath('/html/body/div/div[3]/div[2]/div[1]/h1/a')[0]).text
            #match id
            df.at[df_count,'MatchID'] = matchid
            #队伍、赛区
            for t_index in range(1,4,2):
                t_count=(t_index+1)//2
                #队伍
                df.at[df_count,f'Team{t_count}']=(tree.xpath(f'/html/body/div/div[3]/div[2]/div[1]/ul/li[{t_index}]/a/span')[0]).text
                #地区
                region_class=(tree.xpath( f'/html/body/div/div[3]/div[2]/div[1]/ul/li[{t_index}]/i')[0]).get('class')
                df.at[df_count,f'Team{t_count}_region'] = class2region(region_class)
                #对局日期
                alldata = (tree.xpath('/html/body/div/div[3]/div[2]/div[1]/ul/li[2]/span[2]')[0]).text
            df.at[df_count,'MatchDate']= all2date(alldata)
            
        
            #针对小局获取、写入
        for gameset in range(1,gamesets+1):
            df_count = gameset-1

            button_xpath=f'/html/body/div/div[3]/div[2]/div[1]/div/a[{gameset}]'
            button = driver.find_element(By.XPATH,button_xpath )

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button.click()
            time.sleep(0.5*ntry)

            html_source = driver.page_source
            tree = etree.HTML(html_source)
            #小局
            df.at[df_count,'gameset']=gameset

            #胜利
            team1_xpath = '//*[@id="player-stats"]/ul/li[1]/p'
            team2_xpath = '//*[@id="player-stats"]/ul/li[3]/p'
            win_xpath = ''
            if len(tree.xpath(f'{team1_xpath}/*')) > len(tree.xpath(f'{team2_xpath}/*')):
                win_xpath = team1_xpath
            else: 
                win_xpath = team2_xpath
            df.at[df_count,'win'] = ((tree.xpath(f'{win_xpath}/a'))[0]).text

            #持续时间   
            df.at[df_count,'Duration'] = tree.xpath('//*[@id="player-stats"]/div[1]/div/text()')[0]

            #推塔、大小龙、ban
            for t_index in range(1,3):                
                #大龙
                df.at[df_count,f'Team{t_index}_Baron'] = (tree.xpath( f'//*[@id="player-stats"]/div[1]/ul[{t_index}]/li[4]/p/span')[0]).text
                #小龙
                df.at[df_count,f'Team{t_index}_Dra'] = (tree.xpath(f'//*[@id="player-stats"]/div[1]/ul[{t_index}]/li[3]/p/span')[0]).text
                #推塔
                df.at[df_count,f'Team{t_index}_Turts'] = (tree.xpath(f'//*[@id="player-stats"]/div[1]/ul[{t_index}]/li[2]/p/span')[0]).text
                #ban
                five_ban = tree.xpath('//*[@id="player-stats"]/div[2]/ul/li[3]/a[5]/img')
                ban_range = 5
                if not five_ban:
                    ban_range = 3
                for i in range(1,ban_range+1):
                    ban_xpath = f'//*[@id="player-stats"]/div[2]/ul/li[{2*t_index-1}]/a[{i}]/img' if ban_range == 5 else f'//*[@id="player-stats"]/div[2]/ul/li[{2*t_index-1}]/a[{i}]/img'
                    ban_tree =tree.xpath(ban_xpath)
                    if ban_tree:
                        ban_tag = (ban_tree)[0]
                        src = ban_tag.get('src')
                        df.at[df_count,f'Team{t_index}_ban{i}']=src2name(src)
                    else:
                        df.at[df_count,f'Team{t_index}_ban{i}']='no_ban'

            #选手名和pick
            for p_index in range(1,6):
                for t_index in range(1,3):
                    t_count=2*t_index-1
                    #name
                    df.at[df_count,f'Team{t_index}_player{p_index}_name'] = (tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[{t_count}]/div[1]/p/a')[0]).text
                    #pick
                    pick_tag = tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[{2*t_index-1}]/div[2]/a/img')[0]
                    src = pick_tag.get('src')
                    df.at[df_count,f'Team{t_index}_player{p_index}_pick']=src2name(src)

                #个人数据
            for p_index in range(1,6):
                for t_index in range(1,3):
                    #KDA
                    KDA = (tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[2]/div[1]/span[{t_index}]')[0]).text
                    parts = KDA.split('/')
                    numbers = [int(part) for part in parts]
                    df.at[df_count,f'Team{t_index}_player{p_index}_K']=numbers[0]
                    df.at[df_count,f'Team{t_index}_player{p_index}_D']=numbers[1]
                    df.at[df_count,f'Team{t_index}_player{p_index}_A']=numbers[2]
                    #gold
                    gold=(tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[2]/div[2]/span[{t_index}]')[0]).text
                    df.at[df_count,f'Team{t_index}_player{p_index}_gold']=int(gold)
                    #CS
                    CS=(tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[2]/div[3]/span[{t_index}]')[0]).text
                    df.at[df_count,f'Team{t_index}_player{p_index}_CS']=int(CS)
                    #damage
                    d_tree=tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[2]/div[4]/span[{t_index}]')
                    df.at[df_count,f'Team{t_index}_player{p_index}_damage']=float((d_tree[0]).text) if d_tree else np.nan
                    #tanking
                    t_tree=tree.xpath(f'//*[@id="player-stats"]/div[3]/div[{p_index}]/ul/li[2]/div[5]/span[{t_index}]')
                    df.at[df_count,f'Team{t_index}_player{p_index}_tanking']=float((t_tree[0]).text) if t_tree else np.nan

        mode = 'a' if os.path.exists(datacsv_file) else 'w'  # 如果文件已存在，则追加；否则，写入
        df.to_csv(datacsv_file, mode=mode, index=False, header=not os.path.exists(datacsv_file), encoding='utf-8')

        return ntry
    
    except Exception as e:
        # 将出错的URL、Match ID、Gameset和错误描述记录到CSV文件
        print(f'exception happen in {url} for {ntry} times')
        if ntry >= max_try:
            error_csv_file = 'error_log.csv'
            df_error = pd.DataFrame([[matchid, str(e)]], columns=['MatchID', 'Error'])
            if not os.path.exists(error_csv_file):
                # 创建CSV文件并写入表头
                df_error.to_csv(error_csv_file, index=False, encoding='utf-8')
            else:
                with error_log_lock:
                    # 追加错误信息到CSV文件
                    df_error.to_csv(error_csv_file, mode='a', index=False, header=False, encoding='utf-8')
        return ntry+1
   

def spider_thread(matchids,outputfile):
    t_driver = setup_driver(True,matchids[1]//10+1)
    
    for matchid in matchids:
        t_df = set_dataframe()
        ntry = 1
        while ntry <= max_try:
            result = handleURL(t_driver,t_df,outputfile,matchid,ntry)
            if result == ntry :
                break
            ntry = result
    t_driver.quit()

def main():
    # 将0-100000的数字均匀分配到40个列表，每个列表的步长为10
    totalnum = 100000
    num_of_thread = 40
    base_lenth = 10
    matchid_lists =  [[] for _ in range(40)]
    

    cuts = totalnum//(num_of_thread*base_lenth) 
    for i in range(cuts):

        for j in range(num_of_thread):
            start = i*base_lenth*num_of_thread + base_lenth*j +1
            end = i*base_lenth*num_of_thread + base_lenth*(j+1) if i < (cuts - 1) or j <(num_of_thread - 1) else totalnum
            (matchid_lists[j]).extend((range(start, end + 1)))

    outputfile_prefix = 'output'
    # 创建线程池
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务
        futures = []
        n=1
        for l in range(num_of_thread):
            outputfile=f'{outputfile_prefix}_{n}.csv'
            
            futures.append(executor.submit(spider_thread, matchid_lists[l], outputfile))
            n+=1

        # 等待所有线程完成
        for future in as_completed(futures):
            future.result()

    # 合并所有输出的CSV文件
    merged_df = pd.DataFrame()
    for i in range(num_of_thread):
        filename = f'{outputfile_prefix}_{i+1}.csv'
        if os.path.exists(filename):
            temp_df = pd.read_csv(filename)
            merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
            os.remove(filename)  # 删除临时文件

    # 保存合并后的CSV文件
    merged_df.to_csv('merged_output.csv', index=False, encoding='utf-8')
if __name__ == "__main__":
    main()
