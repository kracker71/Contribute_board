import pickle
# import xgboost as xgb
from sklearn.feature_extraction.text import CountVectorizer
from pythainlp.corpus.common import thai_stopwords
from attacut import tokenize

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            from utils import splitter
            return splitter
        return super().find_class(module, name)

class TextScorrer:
    """
    Predict text class and give score to the given text
    """
    def __init__(
        self, 
        model_path="models/xgb_model.pkl", 
        cvec_path="models/cvec.pkl",
        ):           
        self.cvec = CustomUnpickler(open(cvec_path, 'rb')).load()
        # self.cvec = pickle.load(open(cvec_path, "rb"))
        self.model = pickle.load(open(model_path, "rb"))
        self.thai_stopwords = list(thai_stopwords())
        self.classes = {
            "0" : "general",
            "1" : "information",
            "2" : "question",
            "3" : "badbeat",
            "4" : "share",
            "5" : "showoff",
        }    
        self.classes_base_score = {
            "general" : 0.0,
            "information" : 0.5,
            "question" : 0.3,
            "badbeat" : 0.0,
            "share" : 0.0,
            "showoff" : 0.3,
        }
        self.bonus_words_score = {
            "gto" : 0.25,
            "solver" : 0.25,
        }
    
    def preprocess_text(self, text):
        final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"', "ๆ", "ฯ"))
        final = tokenize(final)
        final = " ".join(word for word in final if word.lower not in self.thai_stopwords)
        return final
    
    def get_score_and_class(self, sentence, is_comment=False):
        preprocessed_sentence = self.preprocess_text(sentence)
        num_word = self.get_num_word(preprocessed_sentence)
        class_word = self.get_class(preprocessed_sentence) if not is_comment else "general"
        bonus_word_score = self.get_bonus_word_score(preprocessed_sentence)

        score = self.classes_base_score[class_word]
        score += num_word * 0.1
        score += bonus_word_score

        return score, class_word

    def get_bonus_word_score(self, preprocessed_sentence):
        bonus_word_score = 0.0
        for word in preprocessed_sentence.split():
            if word.lower() in self.bonus_words_score:
                bonus_word_score += self.bonus_words_score[word.lower()]
        return bonus_word_score
    
    def get_num_word(self, preprocessed_sentence):
        return len(preprocessed_sentence.split())

    def get_class(self, preprocessed_sentence):
        text_vector = self.cvec.transform([preprocessed_sentence])
        pred = self.model.predict(text_vector)
        return self.classes[str(pred[0])]
