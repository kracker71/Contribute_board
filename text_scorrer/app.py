from fastapi import FastAPI
from text_scorrer import TextScorrer
from utils import splitter

app = FastAPI()

# Deploy TextScorrer on FastAPI

print(__name__)
# Initialize TextScorrer
scorrer = TextScorrer()

# Get score and class of post
@app.get("/score-and-class/{post_content}")
def get_post_score_and_class(post_content: str):
    return scorrer.get_score_and_class(post_content, is_comment=False)

# Get score and class of comment
@app.get("/score-and-class/{comment_content}")
def get_comment_score_and_class(comment_content: str):
    return scorrer.get_score_and_class(comment_content, is_comment=True)

# Get sentence class
@app.get("/class/{sentence}")
def get_post_class(sentence: str):
    preprocessed_sentence = scorrer.preprocess_text(sentence)
    return scorrer.get_class(preprocessed_sentence)