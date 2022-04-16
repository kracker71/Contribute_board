from sqlalchemy import Float


class Scorer:
    def __init__(self) -> None:
        self.text_class = ['information','question','general','badbeat','showoff','share']
    
    def calculate_score(text) -> Float:
        text_len = len(text)
        return text_len * 0.1

def test():
    scoring_model = Scorer()
    test_text = 'สวัสดีครับ'
    test_score = scoring_model.calculate_score(test_text)
    print(test_score)


if __name__ == '__main__':
    test()