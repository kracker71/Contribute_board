from msilib.schema import Error
import time
import pandas as pd
from urllib.parse import urljoin

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from selenium.webdriver.common.by import By

from .image import download_image
from .gcp import upload_blob_from_memory,upload_blob

import os
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
ROOT = ROOT_FILE.parents[0]
PAGE = '/members'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
    
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from backend.app.crud.user import create_user,get_user_by_id,get_user_by_name,update_user_profile_by_id
    

def image_upload(out_dir,img_url,file_name,local_save,
                 bucket_name,source_contents,destination_blob_name):
    
    #Download image from url
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
    
def scrape_user_data(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name,is_page_scrape):
    
    if is_page_scrape:
        seed_url = group_url + PAGE + '/pages'
    else:
        seed_url = group_url + PAGE
        
    driver.get(seed_url)
    time.sleep(4)
    print('\n',"Scrolling")
    
    # Scrolling page 
    count = 0 #count user numbers
    cond = 0 #condition for stop scrolling
    scroll_pause_time = 1

    while True:
        # Get only all group users section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(scroll_pause_time)
        
        info_blocks = driver.find_elements(By.XPATH,"//div[@class = 'b20td4e0 muag1w35']")
        
        # Check if None
        if info_blocks:
            info_block = info_blocks[-1]
        else: 
            print("No member in this group")
            break

        users = info_block.find_elements(By.XPATH,"div")
        
        # Break the loop when no more new user
        if  len(users) == count:
            cond+=1
            if cond == 5:
                break
        else: cond = 0
        count = len(users)
        time.sleep(1)
    
    print('\n',"Done Scrolling")
    print('\n',"This Group has",len(users),"users",'\n')
    group_info = ['users',len(users)]
        
    # Collecting Data 
    
    # Initialize localtime
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    print("Collecting Data")
    #Data array
    all_users = []
    
    #Log array
    fail_user = []
    updated_user = []
    created_user = []
    
    pos = 0
    
    for user in users:
        
        data = []
        
        #Update 3/8/2022
        user_info = user.find_element(By.XPATH,".//div[@class = 'goun2846 mk2mc5f4 ccm00jje s44p3ltw rt8b4zig sk4xxmp2 n8ej3o3l agehan2d rq0escxv j83agx80 buofh1pr g5gj957u i1fnvgqd kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x hpfvmrgz jb3vyjys qt6c0cv9 l9j0dhe7 du4w35lb bp9cbjyn btwxx1t3 dflh9lhu scb9dxdr nnctdnn4']//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']")
        if user_info:
            name = user_info.text
            
            if not name:
                # print("Text didn't work")
                name = user_info.get_attribute("innerHTML").split('<span>')[1].split('</span>')[0]
                
            user_href = user_info.get_attribute('href')
            profile_link = urljoin(domain,user_href)
            if "user/" not in user_href:
                # user_id = user_href[25:].split("/")[0].split("?")[0]
                try:
                    tmp_user = get_user_by_name(name,db)
                    user_id = tmp_user.user_id
                except:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(0.5)
                    scrape_user_data(driver,db_conn,db,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name,is_page_scrape=True)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(0.5)
                    
                    tmp_user = get_user_by_name(name,db)
                    user_id = tmp_user.user_id
            else:
                user_id = user_href.split("user/")[1].split("/")[0]
        else:
            name = None
            user_id = None
            profile_link = None
            
        #Scrape page id 
        # if is_name:
        #     if is_page_scrape:
        #         fail_user.append(user_id)
        #         print("Can't find {} id".format(user_id))
        #         is_name = False
        #         continue
        #     else:
        #         scrape_user_data(driver,db_conn,db,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name,is_page_scrape=True)
            
        profile_pic = user.find_element(By.XPATH,".//div[@class = 'j83agx80 cbu4d94t tvfksri0 aov4n071 bi6gxh9e l9j0dhe7 nqmvxvec']//*[name()='svg']/*[name() = 'g']/*[name() = 'image']")
        
        if profile_pic:
            profile_pic = profile_pic.get_attribute('xlink:href')
            
            # Download & Upload Picture to GCP
            image_out_dir = os.path.join(ROOT_FILE,'result','image')
            
            image_upload(image_out_dir,profile_pic,user_id,local_save=False,
                         bucket_name=gcp_bucket_name,
                         source_contents=os.path.join(image_out_dir,user_id+'.jpg'),
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
                for user_data in df.itertuples():
                    temp_dict = {"user_id":user_data.user_id,
                                "user_name":user_data.user_name,
                                "user_profile_url":user_data.user_profile_url,
                                "user_profile_picture_url":user_data.user_profile_picture_url,
                                "user_score":user_data.user_score,
                                "user_update_score_date":user_data.user_update_score_date}
                    
                    try:
                        get_user_by_id(user_data.user_id,db)
                        try:
                            update_user_profile_by_id(user_data.user_id,temp_dict,db)
                            updated_user.append(user_data.user_id)
                        except:
                            print("UNABLE TO PUT {} TO DB".format(user_data.user_id))
                            fail_user.append(user_data.user_id)
                    except:
                        try:
                            create_user(user_data,db)
                            created_user.append(user_data.user_id)
                        except:
                            fail_user.append(user_data.user_id)
                
            ###############################
            
            #Clear users list
            all_users = []
            
        pos+=1
        
    # Post & Put remaining data
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
        for user_data in df.itertuples():
            temp_dict = {"user_id":user_data.user_id,
                         "user_name":user_data.user_name,
                         "user_profile_url":user_data.user_profile_url,
                         "user_profile_picture_url":user_data.user_profile_picture_url,
                         "user_score":user_data.user_score,
                         "user_update_score_date":user_data.user_update_score_date}
            
            try:
                get_user_by_id(user_data.user_id,db)
                try:
                    update_user_profile_by_id(user_data.user_id,temp_dict,db)
                    updated_user.append(user_data.user_id)
                except:
                    print("UNABLE TO PUT {} TO DB".format(user_data.user_id))
                    fail_user.append(user_data.user_id)
            except:
                try:
                    create_user(user_data,db)
                    created_user.append(user_data.user_id)
                except:
                    print("Can't create new user :{}".format(user_data.user_id))
                    fail_user.append(user_data.user_id)
        
    ###############################
    
    print("Task Done...")
    print("Created user :",created_user,'\n',"Updated user :",updated_user,'\n',"Fail user :",fail_user,'\n')
    
    return df
    
def scrape_user_data_by_id(driver,db_conn,db:Session,domain,group_url,user_id:str,savedb,gcp_bucket_name):
    
    seed_url = domain+'/'+user_id
    driver.get(seed_url)
    time.sleep(4)
    
    # Collecting Data 
    
    # Initialize time
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    print("Collecting Data")
    tmp_user_data = []
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
    
    if profile_pic:
        profile_pic = profile_pic.get_attribute('xlink:href')
        
        # Download & Upload Picture to GCP
        image_out_dir = os.path.join(ROOT_FILE,'result','image')
        
        image_upload(image_out_dir,profile_pic,user_id,local_save=False,
                        bucket_name=gcp_bucket_name,
                        source_contents=os.path.join(image_out_dir,user_id+'.jpg'),
                        destination_blob_name=user_id)
        
    else : profile_pic = None
        
    data.append(user_id)
    data.append(name)
    data.append(profile_link)
    data.append(profile_pic)
    data.append(0)
    data.append(datetime)
    
    tmp_user_data.append(data)
        
    ###########################################################################################
    
    df = pd.DataFrame(tmp_user_data,columns=["user_id","user_name","user_profile_url","user_profile_picture_url","user_score","user_update_score_date"])
    
    ###### Post data to DB#########
    if savedb:
        for user_data in df.itertuples():

            temp_dict = {"user_id":user_data.user_id,
                         "user_name":user_data.user_name,
                         "user_profile_url":user_data.user_profile_url,
                         "user_profile_picture_url":user_data.user_profile_picture_url,
                         "user_score":user_data.user_score,
                         "user_update_score_date":user_data.user_update_score_date}
            
            try:
                get_user_by_id(user_data.user_id,db)
                try:
                    update_user_profile_by_id(user_data.user_id,temp_dict,db)
                    print("Updated :",user_data.user_id)
                except:
                    print("UNABLE TO PUT {} TO DB".format(user_data.user_id))
                    print(user_data.user_id)
            except:
                try:
                    create_user(user_data,db)
                    print("Created :",user_data.user_id)
                except:
                    print("Fail... user id:",user_data.user_id)
        
    ###############################
    
    return df