from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import random
from dotenv import load_dotenv

SCRAPER_ENDPOINT="host.docker.internal"
SCRAPER_PORT="9000"

SCORER_ENDPOINT="host.docker.internal"
SCORER_PORT="7000"

# SCRAPER_ENDPOINT=os.environ.get("SCRAPER_ENDPOINT")
# SCRAPER_PORT=os.environ.get("SCRAPER_PORT")

# SCORER_ENDPOINT=os.environ.get("SCORER_ENDPOINT")
# SCORER_PORT=os.environ.get("SCORER_PORT")

args = {
    "owner" : "cboard-airflow",
    "start_date" : datetime(2022, 7, 10)
}
    
def trigger_scraper():
    # url = f"http://{SCRAPER_ENDPOINT}:{SCRAPER_PORT}" + "/scrape-data" # end point path + "/"
    url = "http://host.docker.internal:9000" + "/scrape-data"
    req = requests.get(url)
    print(req.json())

def trigger_scorer():
    # url = f"http://{SCORER_ENDPOINT}:{SCORER_PORT}" + "/predict-and-insert" # end point path + "/"
    url = "http://host.docker.internal:7000" + "/scoring-and-insert"
    req = requests.get(url)
    print(req.json())

dag = DAG(dag_id="pipline_dag", 
          default_args=args, 
          schedule_interval= "@hourly", #"*/1 * * * *", # run every 1 minute for hourly, use "@hourly"
          description="Scrape and Scoring Pipeline for Poker Thailand", 
          catchup=False) 

with dag:
    scraping = PythonOperator(
        task_id = "scrape_data",
        python_callable = trigger_scraper,    
    )
    
    scoring = PythonOperator(
        task_id = "scoring_data",
        python_callable = trigger_scorer,
    )
    
    scraping >> scoring