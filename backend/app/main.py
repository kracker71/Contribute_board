from fastapi import FastAPI
from .database.init_db import engine
from .models.user import User
from .models.comment import Comment
from .models.post import Post
from .api import post
from .api import user
from .api import comment


User.metadata.create_all(bind=engine)
Comment.metadata.create_all(bind=engine)
Post.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)


@app.get("/hello")
def hello():
    return "hello world"

app.include_router(user.router)


if __name__ == '__main__':
    pass

