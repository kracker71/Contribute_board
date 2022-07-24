import time

from fastapi import HTTPException, Depends
from pydantic import PastDate
from sqlalchemy.orm import Session
from sqlalchemy import String, DateTime, Float,Text,Integer

from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import pandas as pd
import os
import sys


from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0].parents[0].parents[0]
ROOT_FILE = FILE.parents[0].parents[0]
PAGE = '/posts'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from scraper.utils.post import get_post_info
from backend.app.crud.post import get_post
# from backend.app.models

def init_post_links(db_conn,db:Session):
    
    csv_post_type = {'post_id' : String(length=100),
                     'post_url' : String(length=2048),
                     }
    
    # user_datetime_col = ['user_update_score_date']
    
    df = pd.read_csv(os.path.join(ROOT_FILE,'result','post','post_links8.csv'),encoding='utf-8-sig',index_col=False)
    # df = pd.DataFrame(df)
    print(df)
    
    try:
        r = df.to_sql('post',con = db_conn,if_exists='append', index=False,dtype=csv_post_type)
        print(r)
        print("POST SUCCESS")
        # db.commit()
    except :
        print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    return df

def init_post_data(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row):
    
    csv_post_type = {'post_id' : String(length=100),
                     'post_url' : String(length=2048),
                     'post_date' : DateTime,
                     'post_username' : String(length=100),
                     'post_content' : Text,
                     'post_shared_content' : Text,'post_reaction_count' : Integer,'post_comment_count' : Integer,'post_shared_count' : Integer,
                     'post_score' : Float,
                     'post_scraped_date' : DateTime,
                     'post_class' : Integer,
                     'user_id' : String(length=100)
                     }
    # user_datetime_col = ['user_update_score_date']
    tmp_post = get_post(db,None,0)
    print(tmp_post)
    
    

def test_post_data(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row):
    
    df = pd.read_csv(os.path.join(ROOT_FILE,'result','post','post_links8.csv'),encoding='utf-8-sig',index_col=False)
    # df = pd.DataFrame(df)
    tmp_posts = zip(df['post_id'].tolist(),df['post_url'].tolist())
    
    get_post_info(driver,db_conn,db,domain,group_url,savecsv,savedb,limit_row,tmp_posts)
    
    # try:
    #     r = df.to_sql('post',con = db_conn,if_exists='append', index=False,dtype=csv_post_type)
    #     print(r)
    #     print("POST SUCCESS")
    #     # db.commit()
    # except :
    #     print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    return df

