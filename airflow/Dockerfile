FROM puckel/docker-airflow:1.10.9

USER root

# Install dependencies
RUN apt-get update
RUN apt-get install -y cmake

WORKDIR /app

RUN pip install python-dotenv