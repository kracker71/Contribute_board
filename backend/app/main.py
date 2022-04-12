from fastapi import FastAPI
from .database.init_db import engine
from .models.user import User
from .models.comment import Comment
from .models.post import Post
from .api import post


User.metadata.create_all(bind=engine)
Comment.metadata.create_all(bind=engine)
Post.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)


@app.get("/hello")
def hello():
    return "hello world"



if __name__ == '__main__':
    pass

