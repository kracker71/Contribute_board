import time
import pandas as pd
from urllib.parse import urljoin
from urllib.error import HTTPError

from sqlalchemy.orm import Session

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

import os
from pathlib import Path
import sys


from .user import scrape_user_data,scrape_user_data_by_id
from .comment import comment_collecting

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
ROOT = FILE.parents[0].parents[0].parents[0]  # backend root directory

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from backend.app.crud.post import create_post,init_post_data_by_id,get_post_by_id
from backend.app.crud.user import get_user_by_name,get_user_by_id


NPOST_FEED = '?sorting_setting=CHRONOLOGICAL'
RECENT_FEED = '?sorting_setting=RECENT_ACTIVITY'

def get_post_link(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name):
    
    post_Prefix = group_url + '/posts'
    seed_url = group_url + NPOST_FEED
    
    driver.get(seed_url)
    time.sleep(4)
        
    print('\n',"Scrolling")
    
    # Scrolling page 
    count = 0
    cond = 0
    scroll_pause_time = 1 # set your own pause time. 
    
    while True:
        
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(scroll_pause_time)
        
        post_block = driver.find_elements(By.XPATH,"//div[@class='ll8tlv6m j83agx80 btwxx1t3 n851cfcs hv4rvrfc dati1w0a pybr56ya']")
        
        if not post_block:
            break
        
        # #Stop scrolling when found an old post
        # try:
        #     info = post_block[-1]
            
        #     #Update 13/8/2565
        #     link = info.find_element(By.XPATH,".//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")
            
        #     ActionChains(driver).move_to_element(link).perform()
        #     url = link.get_attribute('href')
        #     if post_Prefix not in url:
        #         continue
        #     if url in post_links:
        #         continue
        #     else:
        #         id = url.split("posts/")[1].split("/")[0]
        #         try:
        #             get_post_by_id(id,db)
        #             break
        #         except:
        #             pass

        # except:
        #     print("Can't find the element")
        
        # #for dev
        # if len(post_block) > 10:
        #     break
        
        # Break the loop when no more new post
        if  len(post_block) == count:
            cond+=1
            if cond == 5:
                break
        else: cond = 0
        count = len(post_block)
        
    print('\n',"Done Scrolling")
    print('\n',"This Group has",len(post_block),"posts",'\n')

    # Collecting Data 
    
    print("Collecting Data")
    
    #Return to the top of page avoid selenium error
    driver.execute_script("window.scrollTo(0, 0);")  
    
    pos = 0
    #Data array
    fail_post = []
    post_links = []
    
    #Log array
    updated_post = []
    created_post = []
    
    for info in post_block:
        # print(info.value_of_css_property('class'))
        # print(info.tag_name)
        # print(info.text)
        # ActionChains(driver).move_to_element(info).perform()
        
        data = []
        
        user = info.find_element(By.XPATH,".//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']")
        
        if user:
            user_name = user.text
            
            if not user_name:
                # print("Text didn't work")
                user_name = user.get_attribute("innerHTML").split('<span>')[1].split('</span>')[0]
                
            # print("username" , user_name)
            user_href = user.get_attribute('href')
            # print("href",user_href)
            if "user/" not in user_href:
                # user_id = user_href[25:].split("/")[0].split("?")[0]
                try:
                    tmp_user = get_user_by_name(user_name,db)
                    user_id = tmp_user.user_id
                    # print("Exist")
                except:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    scrape_user_data(driver,db_conn,db,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name,is_page_scrape=True)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                    
                    tmp_user = get_user_by_name(user_name,db)
                    user_id = tmp_user.user_id
                    
            else:
                user_id = user_href.split("user/")[1].split("/")[0]
        else:
            user_name = None
            user_id = None
            print("Can't find user element")
        
        #Update 13/8/2565
        link_section = info.find_element(By.XPATH,".//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")
        if not link_section:
            print("Can't Find Link")
        
        
        try:
            ActionChains(driver).move_to_element(link_section).perform()
            url = link_section.get_attribute('href')
            if post_Prefix not in url:
                continue
            if url in post_links:
                continue
            else:
                id = url.split("posts/")[1].split("/")[0]
                data.append(id)
                data.append(url)
                data.append(user_id)
                data.append(True)
                
                post_links.append(data)

        except OSError as e:
            print("Can't find the element")
            print(e)
        
        # Collecting data every 100 row
        if len(post_links) >= limit_row:
            df = pd.DataFrame(post_links,columns=["post_id","post_url","user_id","post_is_update"])
            print("exceed {} Rows... Saving to csv".format(limit_row))
            
            # Save To .csv
            if savecsv:
                path = ROOT_FILE
                name = "post_links{}.csv".format(pos+1)
                try:
                    df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False) 
                except:
                    os.makedirs(os.path.join(path,'result','post'))
                    df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False)
            
            
            ###### Post data to DB#########
            if savedb:
                for post_data in df.itertuples():
                    temp_dict = {"post_id":post_data.post_id,
                                 "post_url":post_data.post_url,
                                 "user_id":post_data.user_id,
                                 "post_is_update":post_data.post_is_update}
                    try:
                        get_post_by_id(post_data.post_id,db)
                        continue
                    except:
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(1)
                        scrape_user_data_by_id(driver,db_conn,db,domain,group_url,post_data.user_id,savedb,gcp_bucket_name)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                        
                        create_post(post_data,db)
                        created_post.append(post_data.post_id)
                
            ###############################
            
            post_links = []
        
        pos +=1
    ###########################################################################################
    
    df = pd.DataFrame(post_links,columns=["post_id","post_url","user_id","post_is_update"])
    
    # Save To .csv
    if savecsv:
        path = ROOT_FILE
        name = "post_links{}.csv".format(pos+1)
        try:
            df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False) 
        except:
            os.makedirs(os.path.join(path,'result','post'))
            df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False)


    ###### Post data to DB#########
    if savedb:
        for post_data in df.itertuples():
            temp_dict = {"post_id":post_data.post_id,
                        "post_url":post_data.post_url,
                        "user_id":post_data.user_id,
                        "post_is_update":post_data.post_is_update}
            # try:
            #     get_post_by_id(post_data.post_id,db)
            #     continue
            # except:
            #     try:
            #         create_post(post_data,db)
            #         created_post.append(post_data.post_id)
            #     except:
            #         try:
            #             try:
            #                 print("user:",get_user_by_id(post_data.user_id,db))
            #                 create_post(post_data,db)
            #                 created_post.append(post_data.post_id)
            #             except:
            #                 driver.execute_script("window.open('');")
            #                 driver.switch_to.window(driver.window_handles[1])
            #                 time.sleep(1)
            #                 try:
            #                     scrape_user_data_by_id(driver,db_conn,db,domain,group_url,post_data.user_id,savedb,gcp_bucket_name)
            #                 except HTTPError as e:
            #                     print(e)
            #                 driver.close()
            #                 driver.switch_to.window(driver.window_handles[0])
            #                 time.sleep(1)
                            
            #                 create_post(post_data,db)
            #                 created_post.append(post_data.post_id)
            #         except:
            #             print("Can't create new post :{}".format(post_data.post_id))
            #             fail_post.append(post_data.post_id)
            
            try:
                get_post_by_id(post_data.post_id,db)
                continue
            except:
                try:
                    get_user_by_id(post_data.user_id,db)
                    pass
                except:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    scrape_user_data_by_id(driver,db_conn,db,domain,group_url,post_data.user_id,savedb,gcp_bucket_name)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                    
                create_post(post_data,db)
                created_post.append(post_data.post_id)
                        
            
    ###############################
    
    print("Task Done")
    print("Created post :",created_post,"\nFail post :",fail_post)
    
    return df,len(post_block)

def get_post_info(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name,post_info):
    
    # Initialize time
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    all_post_data = []
    pos = 0
    
    for x in post_info:
        
        link = x.post_url
        pid = x.post_id
        
        if not x.post_is_update:
            continue
        
        post = []
        driver.get(link)
        post.append(pid)
        
        time.sleep(1)
        data_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        #Date update 13/8/65
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")))
        
        date_section = driver.find_element(By.XPATH,"//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")

        date = date_section.text

        post.append(date)
        
        #user's data
        user = data_soup.find("a",{"class":'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p'})
        
        user_name = user.text
        
        if not user_name:
            # print("Text didn't work")
            user_name = user.get_attribute("innerHTML").split('<span>')[1].split('</span>')[0]
            
        if "user/" not in user['href']:
            # user_id = user['href'][25:].split("/")[0].split("?")[0]
            try:
                tmp_user = get_user_by_name(user_name,db)
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
            user_id = user['href'].split("user/")[1].split("/")[0]
        profile_link = urljoin(domain,user_id)
        post.append(user_name)
        post.append(profile_link)
        
        
        #Post content
        tmp_content = ['No_content','No_shared_content']
        contents = data_soup.find_all("div",{"class":"ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"})
        
        if contents:
            for content in contents:
                if 'id' in content.attrs:
                    tmp_content[0] = content.text
                else:
                    tmp_content[1] = content.text
                    
        post = post+tmp_content
        
        #Reaction
        react_count = data_soup.find("span",{"class":"pcp91wgn"})
        if react_count:
            post.append(react_count.text)
        else:
            post.append(0)
            
        #comment and share count
        tmp_info = [0,0]
        post_info = data_soup.find_all("div",{"class":"oajrlxb2 gs1a9yip mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o tgvbjcpo hpfvmrgz esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl dwo3fsh8 g5ia77u1 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv gmql0nx0 kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h du4w35lb gpro0wi8"})
        if post_info:
            for info in post_info:
                if 'id' in info.attrs:
                    if len(info.text.split(' ')) == 2:
                        tmp_info[0] = int(info.text.split(' ')[0])
                    else:
                        tmp_info[0] = int(info.text.split(' ')[1])
                    
                else:
                    if len(info.text.split(' ')) == 2:
                        tmp_info[1] = int(info.text.split(' ')[0])
                    else:
                        tmp_info[1] = int(info.text.split(' ')[1])
        post = post + tmp_info
        
        post.append(0)
        post.append(datetime)
        post.append(True)
        
        all_post_data.append(post)
        
        # Collecting data every 100 row
        if len(all_post_data) >= limit_row:
            df = pd.DataFrame(all_post_data,columns=["post_id","post_date","post_username","post_profile_url","post_content","post_shared_content","post_reaction_count","post_comment_count","post_shared_count","post_score","post_scraped_date","post_is_update"])
            print("exceed {} Rows... Saving to csv".format(limit_row))
            
            # Save To .csv
            if savecsv:
                path = ROOT_FILE
                name = "post_data{}.csv".format(pos+1)
                try:
                    df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False) 
                except:
                    os.makedirs(os.path.join(path,'result','post'))
                    df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False)
            
            
            ###### Post data to DB#########
            if savedb:
                for post_data in df.itertuples():
                    temp_dict = {"post_id":post_data.post_id,
                                "post_username":post_data.post_username,
                                "post_profile_url":post_data.post_profile_url,
                                "post_content":post_data.post_content,
                                "post_shared_content":post_data.post_shared_content,
                                "post_reaction_count":post_data.post_reaction_count,
                                "post_comment_count":post_data.post_comment_count,
                                "post_shared_count":post_data.post_shared_count,
                                "post_score":post_data.post_score,
                                "post_scraped_date":post_data.post_scraped_date,
                                "post_is_update":post_data.post_is_update}
                    
                    init_post_data_by_id(post_data.post_id,temp_dict,db)

            ###############################
            
            all_post_data = []
        
        pos +=1
        
    df = pd.DataFrame(all_post_data,columns=["post_id","post_date","post_username","post_profile_url","post_content","post_shared_content","post_reaction_count","post_comment_count","post_shared_count","post_score","post_scraped_date","post_is_update"])
    
    # Save To .csv
    if savecsv:
        path = ROOT_FILE
        name = "post_data{}.csv".format(pos+1)
        try:
            df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False) 
        except:
            os.makedirs(os.path.join(path,'result','post'))
            df.to_csv(os.path.join(path,'result','post',name),encoding='utf-8-sig',index=False)
    
    
    
    ###### Post data to DB#########
    if savedb:
        for post_data in df.itertuples():
            temp_dict = {"post_id":post_data.post_id,
                         "post_username":post_data.post_username,
                         "post_profile_url":post_data.post_profile_url,
                         "post_content":post_data.post_content,
                         "post_shared_content":post_data.post_shared_content,
                         "post_reaction_count":post_data.post_reaction_count,
                         "post_comment_count":post_data.post_comment_count,
                         "post_shared_count":post_data.post_shared_count,
                         "post_score":post_data.post_score,
                         "post_scraped_date":post_data.post_scraped_date,
                         "post_is_update":post_data.post_is_update}
            
            init_post_data_by_id(post_data.post_id,temp_dict,db)
    ###############################

    print("Task Done")
    
    return df