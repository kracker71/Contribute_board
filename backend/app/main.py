from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .database.init_db import engine
from .models.user import User
from .models.comment import Comment
from .models.post import Post
from .models.admin import Admin
from .api import user,post,comment,admin


User.metadata.create_all(bind=engine)
Comment.metadata.create_all(bind=engine)
Post.metadata.create_all(bind=engine)
Admin.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(admin.router)


@app.get("/hello")
def hello():
    return "hello world"

app.include_router(user.router)


if __name__ == '__main__':
    pass

