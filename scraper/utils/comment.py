import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os

def comment_collecting(driver,domain,savecsv,limit_row,post_info,comment_number):
    
    now = time.gmtime(time.time())
    datetime = time.strftime("%m/%d/%Y, %H:%M:%S", now)
    
    for link,pid in post_info:
        driver.get(link)
        time.sleep(1)
    
        #Change comment sorting
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//div[@class ='bp9cbjyn j83agx80 kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x h3fqq6jp']"))).click()
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,"//div[@class ='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz p7hjln8o esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql abiwlrkh p8dawk7l lzcic4wl dwo3fsh8 rq0escxv nhd2j8a9 j83agx80 btwxx1t3 pfnyh3mw opuu4ng7 kj2yoqh6 kvgmc6g5 oygrvhab pybr56ya dflh9lhu f10w8fjw scb9dxdr l9j0dhe7 i1ao9s8h du4w35lb bp9cbjyn' ]" )))
        all_comment = driver.find_elements(By.XPATH,"//div[@class ='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz p7hjln8o esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql abiwlrkh p8dawk7l lzcic4wl dwo3fsh8 rq0escxv nhd2j8a9 j83agx80 btwxx1t3 pfnyh3mw opuu4ng7 kj2yoqh6 kvgmc6g5 oygrvhab pybr56ya dflh9lhu f10w8fjw scb9dxdr l9j0dhe7 i1ao9s8h du4w35lb bp9cbjyn' ]" )
        all_comment[-1].click()
        time.sleep(2)
        
        ##################################### Scrolling page #####################################
        #Open all the comment's replies
        print("Opening all comment....")
        while True:
            
            #avoid endless replies
            comment_count = driver.find_elements(By.XPATH,"//div[@class = 'rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
            if len(comment_count) >= comment_number:
                break
            
            replies = driver.find_elements(By.XPATH,"//span[@class = 'j83agx80 fv0vnmcu hpfvmrgz']")
            
            #Click see more & more replies
            if replies:
                for reply in replies:
                    action=ActionChains(driver)
                    try:
                        action.move_to_element(reply).click().perform()
                    except:
                        try:
                            driver.execute_script("arguments[0].click();", reply)

                        except:
                            continue
                    time.sleep(1)
            else :
                break
        ###########################################################################################
        print("All comment opened")
        
        ##################################### Collecting Data #####################################
        print("Collecting data")
        
        comment_soup = BeautifulSoup(driver.page_source, "html.parser")
        comments = comment_soup.find_all("div",{"class":"tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"})
        comment_block = comment_soup.find_all("div",{"class":"rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc"})
        
        all_comment_data = []
        pos = 0
        
        if comments:
            for (comment,block) in zip(comments,comment_block):
                data = []
                user_comment = comment.findChildren("span" ,{"class":"nc684nl6"})[0]
                # print(user_comment)
                comment_content = comment.findChildren("div",{"class":"ecm0bbzt e5nlhep0 a8c37x1j"},recursive = False)
                if comment_content:
                    content = comment_content[0].text
                # print(comment_content)
                
                user_name = user_comment.text
                if "user/" not in user_comment.a['href']:
                    user_id = user_comment.a['href'][25:].split("/")[0].split("?")[0]
                else:
                    user_id = user_comment.a['href'].split("user/")[1].split("/")[0]
                profile_link = urljoin(domain,user_id)
                
                comment_id = user_comment.a['href'].split("comment_id=")[1].split("&__")[0]

                data.append(comment_id)
                data.append(content)
                data.append(user_id)
                data.append(user_name)
                data.append(profile_link)
                data.append(pid)
                
                # Comment date
                comment_date = block.findChildren("a",{"class":"oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 m9osqain knj5qynh"})
                if comment_date:
                    data.append(comment_date[0].text)
                else:
                    data.append(None)
                    
                # Reaction
                comment_reaction = block.findChildren("div",{"class":"du4w35lb pmk7jnqg lthxh50u ox23h4wi kr9hpln1"})
                if comment_reaction:
                    react_count = comment_reaction[0].findChildren("span",{"class":"g0qnabr5 hyh9befq qt6c0cv9 n8tt0mok jb3vyjys j5wam9gi knj5qynh e9vueds3 m9osqain"})
                    if react_count:
                        data.append(int(react_count[0].text))
                    else:
                        data.append(1)
                else:
                    data.append(0)
                data.append(0)
                data.append(datetime)
                
                all_comment_data.append(data)
                
                # Collecting data every 100 row
                if len(all_comment_data) >= limit_row:
                    df = pd.DataFrame(all_comment_data,columns=["CID","Content","UID","Name","Profile_Link","PID","Comment_Date","Reaction","Score","ScrapeDate"])
                    print("exceed {} Rows... Saving to csv".format(limit_row))
                    
                    # Save To .csv
                    if savecsv:
                        path = os.getcwd()
                        name = "all_comment_data{}.csv".format(pos+1)
                        try:
                            df.to_csv(os.path.join(path,'result','comment',name),encoding='utf-8-sig') 
                        except:
                            os.mkdirs(os.path.join(path,'result','comment'))
                            df.to_csv(os.path.join(path,'result','comment',name),encoding='utf-8-sig')
                    
                    
                    #POST TO DB

                    all_comment_data = []
                    
                pos +=1
    ###########################################################################################

    df = pd.DataFrame(all_comment_data,columns=["CID","Content","UID","Name","Profile_Link","PID","Comment_Date","Reaction","Score","ScrapeDate"])
    # df.to_csv("comment.csv",encoding='utf-8-sig')

    print("Task Done")
    
    return df