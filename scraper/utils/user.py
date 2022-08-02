import time
import pandas as pd
from urllib.parse import urljoin

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from selenium.webdriver.common.by import By

import os
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
ROOT = FILE.parents[0].parents[0].parents[0]
PAGE = '/members'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
    
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
    
from scraper.utils.image import download_image
from scraper.utils.gcp import upload_blob_from_memory,upload_blob

def image_upload(out_dir,img_url,file_name,local_save,
                 bucket_name,source_contents,destination_blob_name):
    
    image_content = download_image(file_name=file_name,
                       img_url=img_url,
                       out_dir=out_dir,
                       local_save=local_save)
    if local_save:
        upload_blob(bucket_name=bucket_name,
                    source_file_name=source_contents,
                    destination_blob_name=destination_blob_name)
    else :
        upload_blob_from_memory(bucket_name=bucket_name,
                                contents=image_content,
                                destination_blob_name=destination_blob_name)
    
def init_user_collecting(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name):
    
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
        if len(users) > 10:
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
            
        profile_pic = user.find_element(By.XPATH,".//div[@class = 'j83agx80 cbu4d94t tvfksri0 aov4n071 bi6gxh9e l9j0dhe7 nqmvxvec']//*[name()='svg']/*[name() = 'g']/*[name() = 'image']")
        # print(profile_pic)
        if profile_pic:
            profile_pic = profile_pic.get_attribute('xlink:href')
            
            # Download & Upload Picture to GCP
            image_dir = os.path.join(ROOT_FILE,'result','image')
            
            image_upload(image_dir,profile_pic,user_id,local_save=False,
                         bucket_name=gcp_bucket_name,
                         source_contents=os.path.join(image_dir,user_id+'.jpg'),
                         destination_blob_name=user_id)
            
        else : profile_pic = None
            
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
    
def scrape_user_data_by_id(driver,db_conn,db:Session,domain,group_url,user_id:str,savedb,gcp_bucket_name):
    
    user_id = str(user_id)
    
    seed_url = domain+'/'+user_id
        
    driver.get(seed_url)
    time.sleep(4)
    
    ##################################### Collecting Data #####################################
    
    # Initialize time
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    print("Collecting Data")
    user_data = []
    pos = 0
        
    data = []
    
    #Member is a user    
    try:
        user_block = driver.find_element(By.XPATH,"//div[@class = 'bp9cbjyn j83agx80 psu0lv52 di70i8f1 s4qno8f7 py2vq5j3 owhy4gn4']")
    
    #Member is a Page_admin
    except:
        user_block = driver.find_element(By.XPATH,"//div[@class = 'rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw i1fnvgqd aovydwv3 lhclo0ds btwxx1t3 discj3wi dlv3wnog rl04r1d5 enqfppq2 muag1w35']")
        
    
    try:
        user_info = user_block.find_element(By.XPATH,".//div[@class = 'j83agx80 mpmpiqla ahl66waf tmq14sqq rux31ns4 sjcfkmk3 dti9y0u4 nyziof1z']//div[@class = 'bi6gxh9e aov4n071']")
    except:
        user_info = user_block.find_element(By.XPATH,".//div[@class = 'rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t d2edcug0 hpfvmrgz buofh1pr g5gj957u o8rfisnq ph5uu5jm b3onmgus ecm0bbzt on77hlbc ihqw7lf3']//div[@class = 'bi6gxh9e aov4n071']")
    
    if user_info:
        name = user_info.text.split('(')[0]
        profile_link = group_url + '/user/' + user_id
    else:
        name = None
        user_id = None
        profile_link = None
        
    profile_pic = user_block.find_element(By.XPATH,".//div[@class = 'q9uorilb l9j0dhe7 pzggbiyp du4w35lb']//*[name()='svg']/*[name() = 'g']/*[name() = 'image']")
    # print(profile_pic)
    if profile_pic:
        profile_pic = profile_pic.get_attribute('xlink:href')
        
        # Download & Upload Picture to GCP
        image_dir = os.path.join(ROOT_FILE,'result','image')
        
        image_upload(image_dir,profile_pic,user_id,local_save=False,
                        bucket_name=gcp_bucket_name,
                        source_contents=os.path.join(image_dir,user_id+'.jpg'),
                        destination_blob_name=user_id)
        
    else : profile_pic = None
        
    data.append(user_id)
    data.append(name)
    data.append(profile_link)
    data.append(profile_pic)
    data.append(0)
    data.append(datetime)
    
    user_data.append(data)
        
    ###########################################################################################
    
    df = pd.DataFrame(user_data,columns=["user_id","user_name","user_profile_url","user_profile_picture_url","user_score","user_update_score_date"])
    
    # print(df.to_string)
    
    ###### Post data to DB#########
    if savedb:
        try:
            r = df.to_sql('user',con = db_conn,if_exists='append', index=False)
            # print('New Rows append =',r)
            print("POST SUCCESS")
            # db.commit()
        except :
            print("UNABLE TO POST TO DB")
    ###############################
    
    # print("Task Done")s
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
                        os.makedirs(os.path.join(path,'result','user'))
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