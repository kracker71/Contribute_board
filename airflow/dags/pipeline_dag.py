from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import os
import requests
import random

SCRAPER_ENDPOINT=Variable.get("SCRAPER_ENDPOINT")
SCRAPER_PORT=Variable.get("SCRAPER_PORT")

AI_ENDPOINT=Variable.get("AI_ENDPOINT")
AI_PORT=Variable.get("AI_PORT")

BACKEND_ENDPOINT=Variable.get("BACKEND_ENDPOINT")   
BACKEND_PORT=Variable.get("BACKEND_PORT")

args = {
    "owner" : "cboard-airflow",
    "start_date" : datetime(2022, 8, 21)
}

def trigger_get_all_posts():
    url = f"http://{BACKEND_ENDPOINT}:{BACKEND_PORT}" + "/post/all"
    req = requests.get(url)
    print(req.json())

# def trigger_scraper():
#     print(foo)
#     # url = f"http://{SCRAPER_ENDPOINT}:{SCRAPER_PORT}" + "/scrape-data" # end point path + "/"
#     # url = "http://host.docker.internal:9000" + "/scrape-data"
#     # req = requests.get(url)
#     # print(req.json())

# def trigger_scorer():
#     # url = f"http://{SCORER_ENDPOINT}:{SCORER_PORT}" + "/predict-and-insert" # end point path + "/"
#     # url = "http://host.docker.internal:7000" + "/scoring-and-insert"
#     # req = requests.get(url)
#     # print(req.json())
#     print(foo)

dag = DAG(dag_id="pipline_dag", 
          default_args=args, 
          schedule_interval= "*/1 * * * *", # run every 1 minute for hourly, use "@hourly"
          description="Scrape and Scoring Pipeline for Poker Thailand", 
          catchup=False) 

with dag:
    all_post = PythonOperator(task_id="get_all_posts", python_callable=trigger_get_all_posts)
    # scraping = PythonOperator(
    #     task_id = "scrape_data",
    #     python_callable = trigger_scraper,    
    # )
    
    # scoring = PythonOperator(
    #     task_id = "scoring_data",
    #     python_callable = trigger_scorer,
    # )
    
    all_post
    # scraping >> scoring