FROM python:3.7

RUN apt-get update
RUN apt-get install -y cmake

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app","--host", "0.0.0.0"]
