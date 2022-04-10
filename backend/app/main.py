from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return "hello world"


if __name__ == '__main__':
    pass

