from sqlalchemy.orm import Session
from sqlalchemy import String, DateTime, Float ,Integer, Text

import pandas as pd
import os
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]
ROOT = FILE.parents[0].parents[0].parents[0]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from scraper.utils.comment import comment_collecting
from scraper.utils.user import scrape_user_data_by_id
from backend.app.crud.user import get_user_by_id

def test_comment(driver,db_conn,db:Session,domain,savecsv,savedb,limit_row):
    
    post_info =[('https://www.facebook.com/groups/120212836680964/posts/419434260092152','419434260092152')]
    comment_number = 6

    comment_collecting(driver,db_conn,db,domain,savecsv,savedb,limit_row,post_info,comment_number)
    
def init_comment(driver,db_conn,db:Session,domain,group_url,savecsv,savedb,limit_row,gcp_bucket_name):
    csv_post_type = {'comment_id' : String(length=100),
                     'comment_content' : Text,
                     'comment_username' : String(length=100),
                     'comment_profile_url': String(length=2048),
                    #  'comment_date' : DateTime,
                     'comment_reaction_count': Integer,
                     'comment_score' : Float,
                     'comment_date_scraped' : DateTime,
                     'user_id' : String(length=100),
                     'post_id' : Integer
                     }
    
    # user_datetime_col = ['user_update_score_date']
    
    df = pd.read_csv(os.path.join(ROOT_FILE,'result','comment','comment7.csv'),encoding='utf-8-sig',index_col=False).drop(['comment_date'],1)
    # df = pd.DataFrame(df)
    print(df)
    
    for user_id in df['user_id']:
        print(user_id)
        try:
            get_user_by_id(user_id,db)
            print("Exist")
        except:
            scrape_user_data_by_id(driver,db_conn,db,domain,group_url,user_id,savedb = True,gcp_bucket_name=gcp_bucket_name)
    
    try:
        r = df.to_sql('comment',con = db_conn,if_exists='append', index=False,dtype=csv_post_type)
        print(r)
        print("POST SUCCESS")
        # db.commit()
    except :
        print("UNABLE TO POST TO DB")
    ###############################
    
    print("Task Done")
    return df