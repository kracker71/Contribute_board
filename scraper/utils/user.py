import time
import pandas as pd
from urllib.parse import urljoin

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from selenium.webdriver.common.by import By

import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
PAGE = '/members'
    
def init_user_collecting(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row):
    
    seed_url = group_url + PAGE
        
    driver.get(seed_url)
    time.sleep(4)
    print('\n',"Scrolling")
    ##################################### Scrolling page #####################################
    count = 0
    cond = 0
    scroll_pause_time = 1

    while True:
        # Get only all user section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(scroll_pause_time)
        
        info_blocks = driver.find_elements(By.XPATH,"//div[@class = 'b20td4e0 muag1w35']")
        
        # Check if None
        if info_blocks:
            info_block = info_blocks[-1]
        else: break

        users = info_block.find_elements(By.XPATH,"div")
        
        #for dev
        if len(users) > 200:
            break
        
        # Break the loop when no more new post
        if  len(users) == count:
            cond+=1
            if cond == 5:
                break
        else: cond = 0
        count = len(users)
        time.sleep(0.5)
    
###########################################################################################
    print('\n',"Done Scrolling")
    print('\n',"This Group has",len(users),"users",'\n')
    
    group_info = ['users',len(users)]
        
    ##################################### Collecting Data #####################################
    
    # Initialize time
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    print("Collecting Data")
    all_users = []
    pos = 0
    
    for user in users:
        
        data = []
        
        profile_pic = user.find_element(By.XPATH,".//div[@class = 'j83agx80 cbu4d94t tvfksri0 aov4n071 bi6gxh9e l9j0dhe7 nqmvxvec']//*[name()='svg']/*[name() = 'g']/*[name() = 'image']")
        # print(profile_pic)
        if profile_pic:
            profile_pic = profile_pic.get_attribute('xlink:href')
            
            # Download Picture
            
            # Encode Picture
            
        else : profile_pic = None
        
        
        user_info = user.find_element(By.XPATH,".//div[@class = 'ow4ym5g4 auili1gw rq0escxv j83agx80 buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 hpfvmrgz qt6c0cv9 jb3vyjys l9j0dhe7 du4w35lb bp9cbjyn btwxx1t3 dflh9lhu scb9dxdr nnctdnn4']//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']")
        if user_info:
            name = user_info.text
            user_href = user_info.get_attribute('href')
            profile_link = urljoin(domain,user_href)
            if "user/" not in user_href:
                user_id = user_href[25:].split("/")[0].split("?")[0]
            else:
                user_id = user_href.split("user/")[1].split("/")[0]
        else:
            name = None
            user_id = None
            profile_link = None
            
        data.append(user_id)
        data.append(name)
        data.append(profile_link)
        data.append(profile_pic)
        data.append(0)
        data.append(datetime)
        
        all_users.append(data)
        
        
        # Collecting data every 100 row
        if len(all_users) >= limit_row:
            df = pd.DataFrame(all_users,columns=["user_id","user_name","user_profile_url","user_profile_picture_url","user_score","user_update_score_date"])
            print("exceed {} Rows of data... Saving data...".format(limit_row))
            
            # Save To .csv
            if savecsv:
                path = ROOT_FILE
                name = "user{}.csv".format(pos+1)
                try:
                    df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
                except:
                    os.makedirs(os.path.join(path,'result','user'))
                    df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
     
            ###### Post data to DB#########
            if savedb:
                try:
                    r = df.to_sql('user',con = db_conn,if_exists='append', index=False)
                    print('New Rows append =',r)
                    print("POST SUCCESS")
                    # db.commit()
                except :
                    print("UNABLE TO POST TO DB")
            ###############################
            
            #Clear users list
            all_users = []
            
        pos+=1
    ###########################################################################################
    
    df = pd.DataFrame(all_users,columns=["user_id","user_name","user_profile_url","user_profile_picture_url","user_score","user_update_score_date"])
    
    # Save To .csv
    if savecsv:
        path = ROOT_FILE
        name = "user{}.csv".format(pos+1)
        try:
            df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
        except:
            os.makedirs(os.path.join(path,'result','user'))
            df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
    
    ###### Post data to DB#########
    if savedb:
        try:
            r = df.to_sql('user',con = db_conn,if_exists='append', index=False)
            print('New Rows append =',r)
            print("POST SUCCESS")
            # db.commit()
        except :
            print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    return df
    # First block is a group user that already collect above
    # tag_name = info_blocks.find_element() 
    
def update_user(driver,domain,group_url,savecsv,limit_row,it_now,it_end):
    
    seed_url += PAGE
    
    # First call function
    if it_now == 0:
        driver.get(seed_url)
        time.sleep(4)
    # Initialize time
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    all_users = []

    ##################################### Scrolling page #####################################
    iter = it_now
    scroll_pause_time = 1
    isuserExist = False
    task_done = False
    pos = 0

    while True:
        # Get only all user section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(scroll_pause_time)
        
        info_blocks = driver.find_elements(By.XPATH,"//div[@class = 'b20td4e0 muag1w35']")
        
        # Check if None
        if info_blocks:
            info_block = info_blocks[-1]
        else: break

        users = info_block.find_elements(By.XPATH,"div")
        
        # Break the loop when no more new user
        for i in range(iter,len(users)):
            pos = i
            user = users[i]
            
            ##################################### Collecting Data #####################################

            print("Collecting Data")
                
            data = []
            
            profile_pic = user.find_element(By.XPATH,".//div[@class = 'j83agx80 cbu4d94t tvfksri0 aov4n071 bi6gxh9e l9j0dhe7 nqmvxvec']//*[name()='svg']/*[name() = 'g']/*[name() = 'image']")
            # print(profile_pic)
            if profile_pic:
                profile_pic = profile_pic.get_attribute('xlink:href')
                
                # Download Picture...
                
                # Encode Picture....
                
            else : profile_pic = None
            
            user_info = user.find_element(By.XPATH,".//div[@class = 'ow4ym5g4 auili1gw rq0escxv j83agx80 buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 hpfvmrgz qt6c0cv9 jb3vyjys l9j0dhe7 du4w35lb bp9cbjyn btwxx1t3 dflh9lhu scb9dxdr nnctdnn4']//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']")
            if user_info:
                name = user_info.text
                user_href = user_info.get_attribute('href')
                profile_link = urljoin(domain,user_href)
                if "user/" not in user_href:
                    user_id = user_href[25:].split("/")[0].split("?")[0]
                else:
                    user_id = user_href.split("user/")[1].split("/")[0]
                    
                ############ Check if user exist in db ############ 
                if user_id:
                    isuserExist = True
                    break
                ###################################################### 
                
            else:
                name = None
                user_id = None
                profile_link = None
                
            data.append(user_id)
            data.append(name)
            data.append(profile_link)
            data.append(0)
            data.append(datetime)
            data.append(profile_pic)
            all_users.append(data)
            
            # Collecting data every 100 row
            if len(all_users) >= limit_row:
                df = pd.DataFrame(all_users,columns=["UID","Name","Link","Profile_Picture","Score","ScrapeDate"])
                print("exceed {} Rows... Saving to csv".format(limit_row))
                
                # Save To .csv
                if savecsv:
                    path = ROOT_FILE
                    name = "user{}.csv".format(i+1)
                    try:
                        df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
                    except:
                        os.mkdirs(os.path.join(path,'result','user'))
                        df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
    
                    
                return (df,i+1,len(users),task_done)
            
            ###########################################################################################
        
        if isuserExist:
            task_done = True
            break
        
        iter = len(users)
        time.sleep(0.5)
        
    ###########################################################################################
    
    print("Task Done")
    if savecsv:
        path = ROOT_FILE
        name = "user{}.csv".format(i+1)
        try:
            df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
        except:
            os.makedirs(os.path.join(path,'result','user'))
            df.to_csv(os.path.join(path,'result','user',name),encoding='utf-8-sig',index=False) 
    
        
    return (df,pos+1,len(users),task_done)