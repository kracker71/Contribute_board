import time
import pandas as pd
from urllib.parse import urljoin

from sqlalchemy.orm import Session

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

import os
from pathlib import Path
import sys

from .comment import comment_collecting

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
ROOT = FILE.parents[0].parents[0].parents[0]  # backend root directory
# print(FILE)
# print(ROOT)

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from backend.app.crud.post import init_post_data_by_id

NPOST_FEED = '?sorting_setting=CHRONOLOGICAL'
RECENT_FEED = '?sorting_setting=RECENT_ACTIVITY'

def get_post_link(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row):
    
    Post_Prefix = group_url + '/posts'
    # print(Post_Prefix,'\n')
    seed_url = group_url + NPOST_FEED
    
    driver.get(seed_url)
    time.sleep(4)
        
    print('\n',"Scrolling")
    ##################################### Scrolling page #####################################
    count = 0
    cond = 0
    scroll_pause_time = 1 # set your own pause time. 
    
    while True:
        
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(scroll_pause_time)
        
        user_blocks = driver.find_elements(By.XPATH,"//div[@class='ll8tlv6m j83agx80 btwxx1t3 n851cfcs hv4rvrfc dati1w0a pybr56ya']")
        
        if not user_blocks:
            break
        
        #for dev
        if len(user_blocks) > 5:
            break
        
        # Break the loop when no more new post
        if  len(user_blocks) == count:
            cond+=1
            if cond == 5:
                break
        else: cond = 0
        count = len(user_blocks)
    ###########################################################################################
    print('\n',"Done Scrolling")

    print('\n',"This Group has",len(user_blocks),"posts",'\n')
        

    ##################################### Collecting Data #####################################
    
    print("Collecting Data")
    pos = 0
    post_links = []
    
    for link in user_blocks:
        
        data = []
        
        user = link.find_element(By.XPATH,".//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p']")
        
        if user:
            user_name = user.text
            user_href = user.get_attribute('href')
            if "user/" not in user_href:
                user_id = user_href[25:].split("/")[0].split("?")[0]
            else:
                user_id = user_href.split("user/")[1].split("/")[0]
        else:
            user_name = None
            user_id = None
        
        link = link.find_element(By.XPATH,".//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 m9osqain']")
        
        
        try:
            ActionChains(driver).move_to_element(link).perform()
            url = link.get_attribute('href')
            if Post_Prefix not in url:
                continue
            if url in post_links:
                continue
            else:
                id = url.split("posts/")[1].split("/")[0]
                data.append(id)
                data.append(url)
                data.append(user_id)
                
                post_links.append(data)

        except:
            print("Can't find the element")
        
        # Collecting data every 100 row
        if len(post_links) >= limit_row:
            df = pd.DataFrame(post_links,columns=["post_id","post_url","user_id"])
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
                try:
                    r = df.to_sql('post',con = db_conn,if_exists='append', index=False)
                    print('New Rows append =',r)
                    print("POST SUCCESS")
                    # db.commit()
                except :
                    print("UNABLE TO POST TO DB")
            ###############################
            
            post_links = []
        
        pos +=1
    ###########################################################################################
    
    df = pd.DataFrame(post_links,columns=["post_id","post_url","user_id"])
    
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
        try:
            r = df.to_sql('post',con = db_conn,if_exists='append', index=False)
            print('New Rows append =',r)
            print("POST SUCCESS")
            # db.commit()
        except :
            print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    
    print(df)
    
    return df,len(user_blocks)

def get_post_info(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,post_info):
    
    now = time.localtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    all_post_data = []
    pos = 0
    
    for pid,link in post_info:
        # print(pid,link)
        post = []
        driver.get(link)
        post.append(pid)
        # post.append(link)
        time.sleep(1)
        data_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        #Date update 24/7/65
        date_section = driver.find_element(By.XPATH,"//a[@class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 m9osqain']")

        date = date_section.text

        post.append(date)
        
        #user's data
        user = data_soup.find("a",{"class":'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p'})
        
        user_name = user.text
        if "user/" not in user['href']:
            user_id = user['href'][25:].split("/")[0].split("?")[0]
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
                    if 'comment' in info.text:
                        tmp_info[0] = int(info.text.split('comment')[0])
                    else:
                        tmp_info[0] = int(info.text.split(' ')[1])
                    
                else:
                    if 'share' in info.text:
                        tmp_info[1] = int(info.text.split('share')[0])
                    else:
                        tmp_info[1] = int(info.text.split(' ')[1])
        post = post + tmp_info
        
        post.append(0)
        post.append(datetime)
        post.append(True)
        # post.append(user_id)
        
        
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
                try:
                    for post_data in df:
                        try:
                            init_post_data_by_id(post_data['post_id'],post_data.drop(['post_id'],axis = 1),db)
                        except:
                            print("UNABLE TO POST {} TO DB".format(post_data['post_id']))
                            
                    print("POST SUCCESS")
                    # db.commit()
                except :
                    print("UNABLE TO POST TO DB")
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
    
    #Get Comment data
    # comment_collecting(driver,domain,savecsv,limit_row,[link,pid],tmp_info[0])
    
    ###### Post data to DB#########
    if savedb:
        try:
            r = df.to_sql('post',con = db_conn,if_exists='append', index=False)
            print('New Rows append =',r)
            print("POST SUCCESS")
            # db.commit()
        except :
            print("UNABLE TO POST TO DB")
    ###############################
    
    # df = pd.DataFrame(all_post_data,columns=["Username","Profile_link","Date","content","shared_content","likes","shares"])
    # df.to_csv("post_data[test].csv",encoding='utf-8-sig')

    print("Task Done")
    
    return df